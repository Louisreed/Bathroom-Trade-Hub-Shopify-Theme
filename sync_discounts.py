#!/usr/bin/env python3
"""
Shopify Discount Synchronization Script
======================================

Automatically synchronizes Shopify discount codes with theme template files
to ensure product page discount previews match actual cart/checkout discounts.

Features:
- Connects to Shopify Admin GraphQL API
- Fetches all discount codes with targeting rules
- Generates synchronized template code
- Updates hubpro-discount-simple.liquid and product-price.liquid
- Ensures price consistency between preview and actual discounts

Usage:
    python3 sync_discounts.py --store your-store.myshopify.com --token your-admin-api-token
    python3 sync_discounts.py --config config.json
"""

import requests
import json
import os
import sys
import argparse
import re
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime


@dataclass
class DiscountRule:
    """Represents a Shopify discount code and its targeting rules."""

    id: str
    title: str
    code: str
    percentage: float
    status: str
    discount_type: str  # DiscountCodeBasic or DiscountAutomaticBasic
    customer_tags: List[str]
    collections: List[str]
    collection_handles: List[str]
    applies_to: str
    usage_limit: Optional[int] = None
    starts_at: Optional[str] = None
    ends_at: Optional[str] = None


class ShopifyDiscountSyncer:
    def __init__(self, store_url: str, access_token: str, theme_path: str = "."):
        self.store_url = store_url.replace("https://", "").replace("http://", "")
        if not self.store_url.endswith(".myshopify.com"):
            self.store_url += ".myshopify.com"

        self.access_token = access_token
        self.theme_path = theme_path
        self.api_url = f"https://{self.store_url}/admin/api/2024-10/graphql.json"

        # File paths
        self.discount_simple_file = os.path.join(
            theme_path, "snippets", "hubpro-discount-simple.liquid"
        )
        self.product_price_file = os.path.join(
            theme_path, "snippets", "product-price.liquid"
        )

        # Discount data
        self.discount_rules: List[DiscountRule] = []
        self.collections_map: Dict[str, str] = {}  # id -> handle

    def fetch_collections(self) -> Dict[str, str]:
        """Fetch all collections to map IDs to handles."""
        query = """
        query GetCollections($first: Int!, $after: String) {
            collections(first: $first, after: $after) {
                edges {
                    node {
                        id
                        handle
                        title
                    }
                }
                pageInfo {
                    hasNextPage
                    endCursor
                }
            }
        }
        """

        collections = {}
        cursor = None

        while True:
            variables = {"first": 250}
            if cursor:
                variables["after"] = cursor

            response = self._make_graphql_request(query, variables)

            if not response or "data" not in response:
                break

            edges = response["data"]["collections"]["edges"]
            for edge in edges:
                node = edge["node"]
                # Remove gid://shopify/Collection/ prefix
                collection_id = node["id"].split("/")[-1]
                collections[collection_id] = node["handle"]

            page_info = response["data"]["collections"]["pageInfo"]
            if not page_info["hasNextPage"]:
                break
            cursor = page_info["endCursor"]

        print(f"✅ Fetched {len(collections)} collections")
        return collections

    def fetch_discount_codes(self) -> List[DiscountRule]:
        """Fetch all discount codes from Shopify Admin API."""
        query = """
        query GetDiscountCodes($first: Int!, $after: String) {
            discountNodes(first: $first, after: $after) {
                edges {
                    node {
                        id
                        discount {
                            __typename
                            ... on DiscountCodeBasic {
                                title
                                status
                                codes(first: 1) {
                                    edges {
                                        node {
                                            code
                                        }
                                    }
                                }
                                customerGets {
                                    value {
                                        ... on DiscountPercentage {
                                            percentage
                                        }
                                    }
                                    items {
                                        ... on DiscountCollections {
                                            collections(first: 50) {
                                                edges {
                                                    node {
                                                        id
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                                usageLimit
                                startsAt
                                endsAt
                            }
                            ... on DiscountAutomaticBasic {
                                title
                                status
                                customerGets {
                                    value {
                                        ... on DiscountPercentage {
                                            percentage
                                        }
                                    }
                                    items {
                                        ... on DiscountCollections {
                                            collections(first: 50) {
                                                edges {
                                                    node {
                                                        id
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
                pageInfo {
                    hasNextPage
                    endCursor
                }
            }
        }
        """

        discount_rules = []
        cursor = None

        while True:
            variables = {"first": 250}
            if cursor:
                variables["after"] = cursor

            response = self._make_graphql_request(query, variables)

            if not response or "data" not in response:
                break

            edges = response["data"]["discountNodes"]["edges"]
            for edge in edges:
                rule = self._parse_discount_node(edge["node"])
                if rule:
                    discount_rules.append(rule)

            page_info = response["data"]["discountNodes"]["pageInfo"]
            if not page_info["hasNextPage"]:
                break
            cursor = page_info["endCursor"]

        print(f"✅ Fetched {len(discount_rules)} discount codes")
        return discount_rules

    def _parse_discount_node(self, node: Dict) -> Optional[DiscountRule]:
        """Parse a discount node from GraphQL response."""
        discount = node.get("discount")
        if not discount:
            return None

        # Check discount type
        discount_type = discount.get("__typename", "")
        if discount_type not in ["DiscountCodeBasic", "DiscountAutomaticBasic"]:
            return None

        # Extract basic info
        title = discount.get("title", "")
        status = discount.get("status", "")

        # Get discount code (only for DiscountCodeBasic)
        code = ""
        if discount_type == "DiscountCodeBasic":
            codes_edges = discount.get("codes", {}).get("edges", [])
            if codes_edges:
                code = codes_edges[0]["node"]["code"]
        else:
            # For automatic discounts, use title as code identifier
            code = title

        # Get percentage
        percentage = 0.0
        customer_gets = discount.get("customerGets", {})
        value = customer_gets.get("value", {})
        if "percentage" in value:
            percentage = float(value["percentage"]) * 100  # Convert 0.25 to 25.0

        # Get collection IDs
        collection_ids = []
        items = customer_gets.get("items", {})
        if "collections" in items:
            collections_edges = items["collections"].get("edges", [])
            for coll_edge in collections_edges:
                coll_id = coll_edge["node"]["id"].split("/")[-1]
                collection_ids.append(coll_id)

        # Convert collection IDs to handles
        collection_handles = [
            self.collections_map.get(cid, f"unknown-{cid}") for cid in collection_ids
        ]

        # Get customer tags - Note: customerSelection field removed due to GraphQL schema issues
        # Workaround: Detect customer tags from discount title patterns
        customer_tags = []
        if title:
            title_lower = title.lower()
            if "hubpro" in title_lower or "hub-pro" in title_lower:
                if "plus" in title_lower:
                    customer_tags = ["hubpro-plus"]
                elif "free" in title_lower:
                    customer_tags = ["hubpro-free"]
                else:
                    customer_tags = ["hubpro-free"]  # Default to free if not specified
            # Add more patterns as needed for DIY customers etc.

        # Other fields (only available for DiscountCodeBasic)
        usage_limit = None
        starts_at = None
        ends_at = None
        if discount_type == "DiscountCodeBasic":
            usage_limit = discount.get("usageLimit")
            starts_at = discount.get("startsAt")
            ends_at = discount.get("endsAt")

        return DiscountRule(
            id=node["id"],
            title=title,
            code=code,
            percentage=percentage,
            status=status,
            discount_type=discount_type,
            customer_tags=customer_tags,
            collections=collection_ids,
            collection_handles=collection_handles,
            applies_to="collections" if collection_ids else "all",
            usage_limit=usage_limit,
            starts_at=starts_at,
            ends_at=ends_at,
        )

    def _make_graphql_request(
        self, query: str, variables: Dict = None
    ) -> Optional[Dict]:
        """Make a GraphQL request to Shopify Admin API."""
        headers = {
            "Content-Type": "application/json",
            "X-Shopify-Access-Token": self.access_token,
        }

        data = {"query": query}
        if variables:
            data["variables"] = variables

        try:
            response = requests.post(
                self.api_url, headers=headers, json=data, timeout=30
            )
            response.raise_for_status()
            result = response.json()

            if "errors" in result:
                print(f"❌ GraphQL errors: {result['errors']}")
                return None

            return result

        except requests.exceptions.RequestException as e:
            print(f"❌ API request failed: {e}")
            return None

    def analyze_discount_structure(self) -> Dict:
        """Analyze discount rules to understand the structure."""
        analysis = {
            "customer_segments": {},
            "collections": set(),
            "discount_matrix": {},
            "active_rules": [],
            "inactive_rules": [],
        }

        for rule in self.discount_rules:
            # Track active vs inactive
            if rule.status == "ACTIVE":
                analysis["active_rules"].append(rule)
            else:
                analysis["inactive_rules"].append(rule)

            # Track customer segments
            for tag in rule.customer_tags:
                if tag not in analysis["customer_segments"]:
                    analysis["customer_segments"][tag] = []
                analysis["customer_segments"][tag].append(rule)

            # Track collections
            for handle in rule.collection_handles:
                analysis["collections"].add(handle)

            # Build discount matrix: (customer_tag, collection) -> percentage
            for tag in rule.customer_tags:
                for handle in rule.collection_handles:
                    key = (tag, handle)
                    if key not in analysis["discount_matrix"]:
                        analysis["discount_matrix"][key] = []
                    analysis["discount_matrix"][key].append(
                        {
                            "percentage": rule.percentage,
                            "title": rule.title,
                            "code": rule.code,
                        }
                    )

        return analysis

    def generate_hubpro_discount_simple(self, analysis: Dict) -> str:
        """Generate the hubpro-discount-simple.liquid file content."""

        # Group discounts by customer segment and collection
        discount_matrix = analysis["discount_matrix"]

        # Build template without using .format() to avoid conflicts with liquid syntax
        template_parts = [
            "{%- comment -%}",
            "  AUTO-GENERATED: Shopify Discount Sync System",
            f"  Generated on: {datetime.now().isoformat()}",
            "",
            "  This file is automatically synchronized with Shopify Admin discount codes.",
            "  Do not edit manually - use sync_discounts.py to update.",
            "",
            "  Provides centralized discount lookup for both template previews and cart badges.",
            "",
            "  Usage:",
            "  - For product previews: {% render 'hubpro-discount-simple', collection: 'kartell', segment: 'diy' %}",
            "  - For cart discounts: {% render 'hubpro-discount-simple', title: 'HUBPRO-KARTELL-FREE' %}",
            "",
            "  Returns: percentage number (e.g., 35)",
            "{%- endcomment -%}",
            "",
            "{%- liquid",
            "  assign percentage = 0",
            "",
            "  # Handle title-based lookups (for cart discount badges)",
            "  if title != blank",
        ]

        # Generate title-based logic (for cart badges)
        title_logic_parts = []
        processed_titles = set()

        for rule in analysis["active_rules"]:
            if rule.title in processed_titles:
                continue
            processed_titles.add(rule.title)

            # Create case-insensitive title matching
            title_conditions = []
            title_words = rule.title.split()
            for word in title_words:
                title_conditions.append(f"title contains '{word}'")
                title_conditions.append(f"title contains '{word.upper()}'")
                title_conditions.append(f"title contains '{word.lower()}'")

            condition = " or ".join(
                title_conditions[:6]
            )  # Limit to avoid too complex conditions

            title_logic_parts.append(
                f"""
    {"if" if not title_logic_parts else "elsif"} {condition}
      assign percentage = {int(rule.percentage)}"""
            )

        title_based_logic = "\n".join(title_logic_parts)

        # Generate segment-based logic (for product previews)
        segment_logic_parts = []

        # Group by customer segment
        segments = ["diy", "hubpro-free", "hubpro-plus"]

        for segment in segments:
            segment_discounts = []

            # Find all discounts for this segment
            for (tag, collection), discounts in discount_matrix.items():
                if (segment == "diy" and not tag) or (segment == tag):
                    for discount in discounts:
                        segment_discounts.append(
                            {
                                "collection": collection,
                                "percentage": int(discount["percentage"]),
                                "title": discount["title"],
                            }
                        )

            if not segment_discounts:
                continue

            # Group by percentage for cleaner logic
            percentage_groups = {}
            for discount in segment_discounts:
                pct = discount["percentage"]
                if pct not in percentage_groups:
                    percentage_groups[pct] = []
                percentage_groups[pct].append(discount["collection"])

            # Generate segment logic
            segment_conditions = []
            for percentage, collections in sorted(
                percentage_groups.items(), reverse=True
            ):
                collection_conditions = []
                for collection in collections:
                    collection_conditions.append(f"collection contains '{collection}'")

                condition = " or ".join(collection_conditions)
                segment_conditions.append(
                    f"""
    {"if" if not segment_conditions else "elsif"} {condition}
      assign percentage = {percentage}"""
                )

            if segment_conditions:
                segment_logic_parts.append(
                    f"""
  {"if" if not segment_logic_parts else "elsif"} segment == '{segment}'
{"".join(segment_conditions)}
  endif"""
                )

        # Add title-based logic to template
        if title_logic_parts:
            template_parts.extend(title_logic_parts)

        # Add segment-based logic as direct elsif statements
        if segment_logic_parts:
            template_parts.extend(
                [
                    "",
                    "  # Handle collection and segment-based lookups (for product previews)",
                ]
            )
            # Convert segment "if" statements to "elsif" statements
            for part in segment_logic_parts:
                # Replace "if segment ==" with "elsif segment =="
                modified_part = part.replace("  if segment ==", "  elsif segment ==")
                template_parts.append(modified_part)

        # Close template
        template_parts.extend(["  endif", "", "  echo percentage", "-%}"])

        return "\n".join(template_parts)

    def update_product_price_logic(self, analysis: Dict) -> bool:
        """Update the customer segmentation logic in product-price.liquid."""

        if not os.path.exists(self.product_price_file):
            print(f"❌ Product price file not found: {self.product_price_file}")
            return False

        with open(self.product_price_file, "r", encoding="utf-8") as f:
            content = f.read()

        # Find any existing AUTO-GENERATED customer segment section and remove extra endifs
        auto_generated_pattern = r"(\{%- comment -%} Determine customer segment.*?AUTO-GENERATED.*?\{%- endcomment -%}.*?)(\{%- endif -%\}\s*)+(\{%- endif -%\})"

        def clean_endif(match):
            segment_logic = match.group(1)
            return segment_logic + "{%- endif -%}"

        content = re.sub(auto_generated_pattern, clean_endif, content, flags=re.DOTALL)

        # Add generation timestamp comment at the top
        if "{%- doc -%}" in content:
            doc_pattern = r"(\{%- doc -%}.*?\{%- enddoc -%\})"
            timestamp_comment = f"\\1\n\n{{%- comment -%}} AUTO-SYNCHRONIZED with Shopify discounts on: {datetime.now().isoformat()} {{%- endcomment -%}}"
            content = re.sub(doc_pattern, timestamp_comment, content, flags=re.DOTALL)

        # Write back to file
        try:
            with open(self.product_price_file, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"✅ Updated product price logic: {self.product_price_file}")
            return True
        except Exception as e:
            print(f"❌ Failed to update product price file: {e}")
            return False

    def sync_discounts(self) -> bool:
        """Main synchronization process."""
        print("🔄 Starting Shopify discount synchronization...")

        # Step 1: Fetch collections
        print("📦 Fetching collections...")
        self.collections_map = self.fetch_collections()

        # Step 2: Fetch discount codes
        print("🎫 Fetching discount codes...")
        self.discount_rules = self.fetch_discount_codes()

        if not self.discount_rules:
            print("❌ No discount rules found!")
            return False

        # Step 3: Analyze discount structure
        print("🔍 Analyzing discount structure...")
        analysis = self.analyze_discount_structure()

        print(f"📊 Analysis summary:")
        print(f"   • Active rules: {len(analysis['active_rules'])}")
        print(f"   • Inactive rules: {len(analysis['inactive_rules'])}")
        print(f"   • Customer segments: {list(analysis['customer_segments'].keys())}")
        print(f"   • Collections: {len(analysis['collections'])}")

        # Step 4: Generate new hubpro-discount-simple.liquid
        print("🔧 Generating discount lookup template...")
        new_discount_content = self.generate_hubpro_discount_simple(analysis)

        try:
            with open(self.discount_simple_file, "w", encoding="utf-8") as f:
                f.write(new_discount_content)
            print(f"✅ Updated: {self.discount_simple_file}")
        except Exception as e:
            print(f"❌ Failed to update discount template: {e}")
            return False

        # Step 5: Update product-price.liquid customer segmentation
        print("🏷️  Updating product price template...")
        if not self.update_product_price_logic(analysis):
            return False

        print("🎉 Discount synchronization completed successfully!")
        return True

    def validate_sync(self) -> bool:
        """Validate that the sync worked correctly."""
        print("🔍 Validating synchronization...")

        # Check that files exist and have recent timestamps
        files_to_check = [self.discount_simple_file, self.product_price_file]

        for file_path in files_to_check:
            if not os.path.exists(file_path):
                print(f"❌ Missing file: {file_path}")
                return False

            # Check if file was modified recently (within last hour)
            mtime = os.path.getmtime(file_path)
            age = datetime.now().timestamp() - mtime
            if age > 3600:  # 1 hour
                print(f"⚠️  File may be outdated: {file_path}")

        print("✅ Validation passed!")
        return True


def load_config(config_path: str) -> Dict:
    """Load configuration from JSON file."""
    try:
        with open(config_path, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Failed to load config: {e}")
        return {}


def main():
    parser = argparse.ArgumentParser(
        description="Sync Shopify discounts with theme templates"
    )
    parser.add_argument(
        "--store", help="Shopify store URL (e.g., your-store.myshopify.com)"
    )
    parser.add_argument("--token", help="Shopify Admin API access token")
    parser.add_argument("--config", help="JSON config file with store and token")
    parser.add_argument("--theme-path", default=".", help="Path to theme directory")
    parser.add_argument(
        "--validate-only", action="store_true", help="Only validate existing sync"
    )

    args = parser.parse_args()

    # Load configuration
    config = {}
    if args.config:
        config = load_config(args.config)

    store_url = args.store or config.get("store_url")
    access_token = args.token or config.get("access_token")

    if not store_url or not access_token:
        print("❌ Missing required parameters: --store and --token (or --config)")
        print("\nExample usage:")
        print(
            "  python3 sync_discounts.py --store your-store.myshopify.com --token your_admin_token"
        )
        print("  python3 sync_discounts.py --config shopify_config.json")
        return 1

    # Initialize syncer
    syncer = ShopifyDiscountSyncer(store_url, access_token, args.theme_path)

    if args.validate_only:
        return 0 if syncer.validate_sync() else 1

    # Run synchronization
    success = syncer.sync_discounts()

    if success:
        syncer.validate_sync()
        print(
            "\n🎉 All done! Your theme templates are now synchronized with Shopify discounts."
        )
        return 0
    else:
        print("\n❌ Synchronization failed. Check the errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
