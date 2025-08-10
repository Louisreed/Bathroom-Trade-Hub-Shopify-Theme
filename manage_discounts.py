#!/usr/bin/env python3
"""
HubPRO Discount Manager
=====================

A Python script to view and edit hardcoded discount percentages in the Shopify theme.
This script manages the discounts defined in snippets/hubpro-discount-simple.liquid.

Usage:
    python manage_discounts.py              # Show current discounts
    python manage_discounts.py --edit       # Interactive edit mode
    python manage_discounts.py --set "HubPRO Kartell" 30  # Set specific discount
"""

import re
import sys
import os
from typing import Dict, Optional


class HubPRODiscountManager:
    def __init__(self, theme_path: str = "."):
        self.theme_path = theme_path
        self.discount_file = os.path.join(
            theme_path, "snippets", "hubpro-discount-simple.liquid"
        )
        self.discounts = {}

    def load_discounts(self) -> Dict[str, int]:
        """Load current discount percentages from the Liquid file."""
        if not os.path.exists(self.discount_file):
            print(f"❌ Error: {self.discount_file} not found!")
            return {}

        with open(self.discount_file, "r", encoding="utf-8") as f:
            content = f.read()

        # Parse discount conditions from Liquid
        discounts = {}

        # Look for patterns like: if title contains 'Kartell' assign percentage = 25
        kartell_match = re.search(
            r"if title contains ['\"]Kartell['\"].*?assign percentage = (\d+)",
            content,
            re.DOTALL,
        )
        if kartell_match:
            discounts["HubPRO Kartell"] = int(kartell_match.group(1))

        # Look for patterns like: elsif title contains 'Maxi Panels' assign percentage = 45
        maxi_match = re.search(
            r"elsif title contains ['\"]Maxi Panels['\"].*?assign percentage = (\d+)",
            content,
            re.DOTALL,
        )
        if maxi_match:
            discounts["HubPRO Maxi Panels"] = int(maxi_match.group(1))

        self.discounts = discounts
        return discounts

    def save_discounts(self, discounts: Dict[str, int]) -> bool:
        """Save updated discount percentages to the Liquid file."""
        if not os.path.exists(self.discount_file):
            print(f"❌ Error: {self.discount_file} not found!")
            return False

        with open(self.discount_file, "r", encoding="utf-8") as f:
            content = f.read()

        # Update Kartell discount
        if "HubPRO Kartell" in discounts:
            content = re.sub(
                r"(if title contains ['\"]Kartell['\"].*?assign percentage = )\d+",
                f"\\g<1>{discounts['HubPRO Kartell']}",
                content,
                flags=re.DOTALL,
            )

        # Update Maxi Panels discount
        if "HubPRO Maxi Panels" in discounts:
            content = re.sub(
                r"(elsif title contains ['\"]Maxi Panels['\"].*?assign percentage = )\d+",
                f"\\g<1>{discounts['HubPRO Maxi Panels']}",
                content,
                flags=re.DOTALL,
            )

        # Write back to file
        try:
            with open(self.discount_file, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"✅ Discounts saved to {self.discount_file}")
            return True
        except Exception as e:
            print(f"❌ Error saving file: {e}")
            return False

    def show_discounts(self):
        """Display current discount percentages."""
        discounts = self.load_discounts()

        if not discounts:
            print("❌ No discounts found!")
            return

        print("\n🎯 Current HubPRO Discount Percentages:")
        print("=" * 50)

        for discount_name, percentage in discounts.items():
            status = "🟢 Active" if percentage > 0 else "🔴 Disabled"
            print(f"{discount_name:<20} : {percentage:>3}% {status}")

        print("=" * 50)
        print(f"📁 Source file: {self.discount_file}")
        print()

    def edit_discount(self, discount_name: str, new_percentage: int) -> bool:
        """Edit a specific discount percentage."""
        discounts = self.load_discounts()

        if discount_name not in discounts:
            print(f"❌ Discount '{discount_name}' not found!")
            print(f"Available discounts: {', '.join(discounts.keys())}")
            return False

        old_percentage = discounts[discount_name]
        discounts[discount_name] = new_percentage

        if self.save_discounts(discounts):
            print(
                f"✅ Updated '{discount_name}': {old_percentage}% → {new_percentage}%"
            )
            return True
        return False

    def interactive_edit(self):
        """Interactive mode to edit discounts."""
        discounts = self.load_discounts()

        if not discounts:
            print("❌ No discounts found!")
            return

        print("\n🔧 Interactive Discount Editor")
        print("=" * 40)
        print("Enter new percentages (0 to disable, Enter to skip)")
        print()

        updated_discounts = discounts.copy()
        changes_made = False

        for discount_name, current_percentage in discounts.items():
            while True:
                try:
                    user_input = input(
                        f"{discount_name} (currently {current_percentage}%): "
                    ).strip()

                    if user_input == "":
                        # Skip this discount
                        break

                    new_percentage = int(user_input)
                    if 0 <= new_percentage <= 100:
                        if new_percentage != current_percentage:
                            updated_discounts[discount_name] = new_percentage
                            changes_made = True
                            print(f"  → Will change to {new_percentage}%")
                        break
                    else:
                        print("  ❌ Please enter a percentage between 0-100")

                except ValueError:
                    print("  ❌ Please enter a valid number")
                except KeyboardInterrupt:
                    print("\n\n❌ Cancelled by user")
                    return

        if changes_made:
            print(f"\n📋 Summary of changes:")
            for name, new_val in updated_discounts.items():
                old_val = discounts[name]
                if new_val != old_val:
                    print(f"  {name}: {old_val}% → {new_val}%")

            confirm = input("\n💾 Save changes? (y/N): ").strip().lower()
            if confirm in ["y", "yes"]:
                if self.save_discounts(updated_discounts):
                    print("✅ All changes saved successfully!")
                else:
                    print("❌ Failed to save changes")
            else:
                print("❌ Changes discarded")
        else:
            print("\n📝 No changes made")


def main():
    manager = HubPRODiscountManager()

    if len(sys.argv) == 1:
        # Show current discounts
        manager.show_discounts()

    elif len(sys.argv) == 2 and sys.argv[1] == "--edit":
        # Interactive edit mode
        manager.interactive_edit()

    elif len(sys.argv) == 4 and sys.argv[1] == "--set":
        # Set specific discount: python script.py --set "HubPRO Kartell" 30
        discount_name = sys.argv[2]
        try:
            percentage = int(sys.argv[3])
            if 0 <= percentage <= 100:
                manager.edit_discount(discount_name, percentage)
            else:
                print("❌ Percentage must be between 0-100")
        except ValueError:
            print("❌ Invalid percentage value")

    elif len(sys.argv) == 2 and sys.argv[1] in ["--help", "-h"]:
        # Show help
        print(__doc__)

    else:
        print("❌ Invalid arguments")
        print(__doc__)


if __name__ == "__main__":
    main()
