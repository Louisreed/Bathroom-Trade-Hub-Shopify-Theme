#!/usr/bin/env python3
"""
Shopify Discount Sync Setup Wizard
==================================

Interactive setup wizard for the Shopify discount synchronization system.
Walks you through configuration, testing, and first sync.

Usage:
    python3 setup_discount_sync.py
"""

import json
import os
import sys
import subprocess
from typing import Dict


def print_banner():
    """Print welcome banner."""
    print(
        """
🔄 Shopify Discount Synchronization Setup
==========================================

This wizard will help you set up automated discount synchronization
between your Shopify store and theme templates.

What this does:
✅ Fetches discount rules from Shopify Admin API  
✅ Generates synchronized template code
✅ Ensures product previews match cart/checkout exactly
✅ Eliminates manual discount maintenance

Let's get started!
"""
    )


def get_user_input(prompt: str, default: str = None, required: bool = True) -> str:
    """Get user input with optional default."""
    if default:
        full_prompt = f"{prompt} [{default}]: "
    else:
        full_prompt = f"{prompt}: "

    while True:
        value = input(full_prompt).strip()

        if not value and default:
            return default
        elif value or not required:
            return value
        else:
            print("❌ This field is required. Please enter a value.")


def create_config_file() -> Dict:
    """Interactive configuration creation."""
    print("\n📝 Step 1: Shopify API Configuration")
    print("-" * 40)

    print(
        """
First, you'll need to create a private app in Shopify Admin:

1. Go to your Shopify Admin → Apps → App and sales channel settings
2. Click "Develop apps for your store"
3. Create new app: "Discount Sync Tool"
4. Configure Admin API access with these scopes:
   ✅ read_discounts
   ✅ read_products (includes collections access)
5. Install the app and copy the Admin API access token

More details: https://shopify.dev/docs/apps/getting-started
"""
    )

    input("Press Enter when you have your API token ready...")

    # Get store URL
    store_url = get_user_input(
        "Enter your Shopify store URL (e.g., your-store.myshopify.com)"
    )

    # Clean up store URL
    store_url = store_url.replace("https://", "").replace("http://", "")
    if not store_url.endswith(".myshopify.com"):
        if "." not in store_url:
            store_url += ".myshopify.com"

    # Get API token
    access_token = get_user_input(
        "Enter your Admin API access token (starts with 'shpat_')"
    )

    if not access_token.startswith("shpat_"):
        print(
            "⚠️  Token doesn't look right (should start with 'shpat_'), but continuing..."
        )

    config = {
        "store_url": store_url,
        "access_token": access_token,
        "api_version": "2024-10",
        "sync_settings": {
            "backup_before_sync": True,
            "validate_after_sync": True,
            "dry_run": False,
        },
        "theme_settings": {
            "theme_path": ".",
            "target_files": [
                "snippets/hubpro-discount-simple.liquid",
                "snippets/product-price.liquid",
            ],
        },
    }

    return config


def save_config(config: Dict, config_path: str = "shopify_config.json") -> bool:
    """Save configuration to file."""
    try:
        with open(config_path, "w") as f:
            json.dump(config, f, indent=2)

        # Set restrictive permissions
        os.chmod(config_path, 0o600)

        print(f"✅ Configuration saved to: {config_path}")
        print(f"🔒 File permissions set to 600 (owner read/write only)")
        return True
    except Exception as e:
        print(f"❌ Failed to save config: {e}")
        return False


def check_dependencies() -> bool:
    """Check if required dependencies are installed."""
    print("\n🔧 Step 2: Checking Dependencies")
    print("-" * 40)

    try:
        import requests

        print("✅ requests library is available")
        return True
    except ImportError:
        print("❌ requests library is missing")
        print("\nTo install dependencies:")
        print("  pip install -r requirements-sync.txt")
        print("  # or")
        print("  pip install requests")
        return False


def run_connection_test(config_path: str) -> bool:
    """Run the setup test script."""
    print("\n🧪 Step 3: Testing API Connection")
    print("-" * 40)

    try:
        result = subprocess.run(
            [sys.executable, "test_sync_setup.py", "--config", config_path],
            capture_output=True,
            text=True,
            timeout=30,
        )

        print(result.stdout)
        if result.stderr:
            print(f"Errors: {result.stderr}")

        return result.returncode == 0
    except subprocess.TimeoutExpired:
        print("❌ Test timed out (check your network connection)")
        return False
    except Exception as e:
        print(f"❌ Failed to run test: {e}")
        return False


def run_first_sync(config_path: str) -> bool:
    """Run the first synchronization."""
    print("\n🔄 Step 4: First Synchronization")
    print("-" * 40)

    confirm = input(
        "Ready to run your first sync? This will update your theme files. (y/N): "
    )

    if confirm.lower() not in ["y", "yes"]:
        print("⏸️  Sync cancelled. You can run it later with:")
        print(f"   python3 sync_discounts.py --config {config_path}")
        return False

    try:
        result = subprocess.run(
            [sys.executable, "sync_discounts.py", "--config", config_path], timeout=60
        )

        return result.returncode == 0
    except subprocess.TimeoutExpired:
        print("❌ Sync timed out")
        return False
    except Exception as e:
        print(f"❌ Failed to run sync: {e}")
        return False


def show_next_steps():
    """Show next steps after successful setup."""
    print(
        """
🎉 Setup Complete!

Your discount synchronization system is now configured and ready to use.

📋 Next Steps:
1. Test the system:
   • Check product pages for discount previews
   • Add items to cart and verify discounts apply
   • Compare percentages between preview and cart

2. Set up regular syncing:
   • Run manually after discount changes
   • Consider automated daily sync via cron
   • Monitor for API changes or errors

3. Regular maintenance:
   • Review discount structure monthly
   • Update API tokens before expiry
   • Keep theme files backed up

📚 Documentation:
• README-DISCOUNT-SYNC.md - Complete guide
• sync_discounts.py --help - Command options
• test_sync_setup.py - Validation tool

🔄 Manual Sync Commands:
   python3 sync_discounts.py --config shopify_config.json
   python3 test_sync_setup.py --config shopify_config.json

💡 Pro Tip: Set up automated syncing with cron:
   0 6 * * * cd /path/to/theme && python3 sync_discounts.py --config shopify_config.json

Happy syncing! 🚀
"""
    )


def main():
    print_banner()

    # Check if files exist
    required_files = ["sync_discounts.py", "test_sync_setup.py"]
    for file in required_files:
        if not os.path.exists(file):
            print(f"❌ Missing required file: {file}")
            print("Make sure you're running this from the theme root directory.")
            return 1

    # Step 1: Create configuration
    config = create_config_file()
    config_path = "shopify_config.json"

    if not save_config(config, config_path):
        return 1

    # Step 2: Check dependencies
    if not check_dependencies():
        return 1

    # Step 3: Test connection
    if not run_connection_test(config_path):
        print(
            "\n❌ Connection test failed. Please check your configuration and try again."
        )
        return 1

    # Step 4: Run first sync
    sync_success = run_first_sync(config_path)

    # Show completion message
    if sync_success:
        show_next_steps()
        return 0
    else:
        print(
            """
⚠️  Setup completed but first sync failed.

You can try running the sync manually:
  python3 sync_discounts.py --config shopify_config.json

Or re-run the connection test:
  python3 test_sync_setup.py --config shopify_config.json
"""
        )
        return 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n❌ Setup cancelled by user.")
        sys.exit(1)
