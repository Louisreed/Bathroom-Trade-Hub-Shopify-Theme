#!/usr/bin/env python3
"""
Test Shopify Discount Sync Setup
================================

Validates your Shopify API connection and discount sync environment.
Run this before using sync_discounts.py to ensure everything is configured correctly.

Usage:
    python3 test_sync_setup.py --config shopify_config.json
    python3 test_sync_setup.py --store your-store.myshopify.com --token your_token
"""

import requests
import json
import os
import sys
import argparse
from typing import Dict, Optional


class SyncSetupTester:
    def __init__(self, store_url: str, access_token: str, theme_path: str = "."):
        self.store_url = store_url.replace("https://", "").replace("http://", "")
        if not self.store_url.endswith(".myshopify.com"):
            self.store_url += ".myshopify.com"

        self.access_token = access_token
        self.theme_path = theme_path
        self.api_url = f"https://{self.store_url}/admin/api/2024-10/graphql.json"

        self.tests_passed = 0
        self.tests_total = 0

    def run_test(self, test_name: str, test_func) -> bool:
        """Run a single test and track results."""
        self.tests_total += 1
        print(f"\n🧪 Testing: {test_name}")

        try:
            result = test_func()
            if result:
                print(f"✅ PASS: {test_name}")
                self.tests_passed += 1
                return True
            else:
                print(f"❌ FAIL: {test_name}")
                return False
        except Exception as e:
            print(f"❌ ERROR: {test_name} - {e}")
            return False

    def test_api_connection(self) -> bool:
        """Test basic API connectivity."""
        query = "{ shop { name } }"

        headers = {
            "Content-Type": "application/json",
            "X-Shopify-Access-Token": self.access_token,
        }

        try:
            response = requests.post(
                self.api_url, headers=headers, json={"query": query}, timeout=10
            )

            if response.status_code != 200:
                print(f"   HTTP {response.status_code}: {response.text}")
                return False

            data = response.json()

            if "errors" in data:
                print(f"   GraphQL errors: {data['errors']}")
                return False

            shop_name = data.get("data", {}).get("shop", {}).get("name", "Unknown")
            print(f"   Connected to shop: {shop_name}")
            return True

        except requests.exceptions.RequestException as e:
            print(f"   Connection error: {e}")
            return False

    def test_discount_permissions(self) -> bool:
        """Test discount read permissions."""
        query = """
        {
            discountNodes(first: 1) {
                edges {
                    node {
                        id
                    }
                }
            }
        }
        """

        headers = {
            "Content-Type": "application/json",
            "X-Shopify-Access-Token": self.access_token,
        }

        try:
            response = requests.post(
                self.api_url, headers=headers, json={"query": query}, timeout=10
            )
            data = response.json()

            if "errors" in data:
                errors = data["errors"]
                for error in errors:
                    if "discountNodes" in error.get("message", ""):
                        print(f"   Permission error: {error['message']}")
                        print("   💡 Add 'read_discounts' scope to your app")
                        return False
                return False

            discount_count = len(
                data.get("data", {}).get("discountNodes", {}).get("edges", [])
            )
            print(
                f"   Can access discount data (found {discount_count} discounts in first query)"
            )
            return True

        except Exception as e:
            print(f"   Error testing permissions: {e}")
            return False

    def test_collections_permissions(self) -> bool:
        """Test collections read permissions."""
        query = """
        {
            collections(first: 1) {
                edges {
                    node {
                        id
                        handle
                    }
                }
            }
        }
        """

        headers = {
            "Content-Type": "application/json",
            "X-Shopify-Access-Token": self.access_token,
        }

        try:
            response = requests.post(
                self.api_url, headers=headers, json={"query": query}, timeout=10
            )
            data = response.json()

            if "errors" in data:
                print(f"   Permission error: {data['errors']}")
                print(
                    "   💡 Add 'read_products' scope to your app (includes collections access)"
                )
                return False

            collections_count = len(
                data.get("data", {}).get("collections", {}).get("edges", [])
            )
            print(
                f"   Can access collections data (found {collections_count} collections in first query)"
            )
            return True

        except Exception as e:
            print(f"   Error testing permissions: {e}")
            return False

    def test_theme_files(self) -> bool:
        """Test theme file accessibility."""
        required_files = [
            "snippets/hubpro-discount-simple.liquid",
            "snippets/product-price.liquid",
        ]

        all_exist = True

        for file_path in required_files:
            full_path = os.path.join(self.theme_path, file_path)
            if os.path.exists(full_path):
                print(f"   ✅ Found: {file_path}")
            else:
                print(f"   ❌ Missing: {file_path}")
                all_exist = False

        if not all_exist:
            print("   💡 Make sure you're running from the theme root directory")

        return all_exist

    def test_file_permissions(self) -> bool:
        """Test that we can write to theme files."""
        test_files = [
            "snippets/hubpro-discount-simple.liquid",
            "snippets/product-price.liquid",
        ]

        for file_path in test_files:
            full_path = os.path.join(self.theme_path, file_path)

            if not os.path.exists(full_path):
                continue

            try:
                # Test write permission by appending and removing a comment
                with open(full_path, "a", encoding="utf-8") as f:
                    f.write(
                        "\n{%- comment -%} Test write permission {%- endcomment -%}"
                    )

                # Read the file and remove the test comment
                with open(full_path, "r", encoding="utf-8") as f:
                    content = f.read()

                content = content.replace(
                    "\n{%- comment -%} Test write permission {%- endcomment -%}", ""
                )

                with open(full_path, "w", encoding="utf-8") as f:
                    f.write(content)

                print(f"   ✅ Can write to: {file_path}")

            except Exception as e:
                print(f"   ❌ Cannot write to: {file_path} - {e}")
                return False

        return True

    def test_sample_discount_fetch(self) -> bool:
        """Fetch a sample of discount data to validate structure."""
        query = """
        {
            discountNodes(first: 3) {
                edges {
                    node {
                        id
                        discount {
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
                                }
                            }
                        }
                    }
                }
            }
        }
        """

        headers = {
            "Content-Type": "application/json",
            "X-Shopify-Access-Token": self.access_token,
        }

        try:
            response = requests.post(
                self.api_url, headers=headers, json={"query": query}, timeout=10
            )
            data = response.json()

            if "errors" in data:
                print(f"   Query errors: {data['errors']}")
                return False

            edges = data.get("data", {}).get("discountNodes", {}).get("edges", [])

            if not edges:
                print("   ⚠️  No discount codes found in your store")
                print("   💡 Create some discount codes in Shopify Admin first")
                return True  # Not a failure, just empty

            print(f"   Found {len(edges)} discount codes:")

            for edge in edges:
                discount = edge["node"]["discount"]
                title = discount.get("title", "Unknown")
                status = discount.get("status", "Unknown")

                # Get percentage
                percentage = 0
                customer_gets = discount.get("customerGets", {})
                value = customer_gets.get("value", {})
                if "percentage" in value:
                    percentage = float(value["percentage"]) * 100

                print(f"     • {title}: {percentage:.0f}% ({status})")

            return True

        except Exception as e:
            print(f"   Error fetching sample data: {e}")
            return False

    def run_all_tests(self):
        """Run all validation tests."""
        print("🔍 Shopify Discount Sync Setup Validation")
        print("=" * 50)

        # Test basic connectivity
        self.run_test("API Connection", self.test_api_connection)

        # Test permissions
        self.run_test("Discount Permissions", self.test_discount_permissions)
        self.run_test("Collections Permissions", self.test_collections_permissions)

        # Test theme files
        self.run_test("Theme Files Exist", self.test_theme_files)
        self.run_test("File Write Permissions", self.test_file_permissions)

        # Test sample data
        self.run_test("Sample Discount Fetch", self.test_sample_discount_fetch)

        # Summary
        print(f"\n📊 Test Results: {self.tests_passed}/{self.tests_total} passed")

        if self.tests_passed == self.tests_total:
            print("🎉 All tests passed! You're ready to run sync_discounts.py")
            return True
        else:
            print(
                "❌ Some tests failed. Please fix the issues above before running sync."
            )
            return False


def load_config(config_path: str) -> Dict:
    """Load configuration from JSON file."""
    try:
        with open(config_path, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Failed to load config: {e}")
        return {}


def main():
    parser = argparse.ArgumentParser(description="Test Shopify discount sync setup")
    parser.add_argument("--store", help="Shopify store URL")
    parser.add_argument("--token", help="Shopify Admin API access token")
    parser.add_argument("--config", help="JSON config file")
    parser.add_argument("--theme-path", default=".", help="Path to theme directory")

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
            "  python3 test_sync_setup.py --store your-store.myshopify.com --token your_token"
        )
        print("  python3 test_sync_setup.py --config shopify_config.json")
        return 1

    # Run tests
    tester = SyncSetupTester(store_url, access_token, args.theme_path)
    success = tester.run_all_tests()

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
