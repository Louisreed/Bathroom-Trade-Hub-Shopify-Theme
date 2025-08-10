# HubPRO Discount Manager 🎯

A Python script to easily view and edit hardcoded discount percentages in the Shopify theme without manually editing Liquid code.

## 🚀 Quick Start

### View Current Discounts

```bash
python3 manage_discounts.py
```

### Interactive Edit Mode

```bash
python3 manage_discounts.py --edit
```

### Set Specific Discount

```bash
python3 manage_discounts.py --set "HubPRO Kartell" 30
python3 manage_discounts.py --set "HubPRO Maxi Panels" 50
```

## 📋 Features

- ✅ **View current discounts** - See all active discount percentages
- ✅ **Interactive editing** - Step-by-step discount updates
- ✅ **Direct updates** - Set specific discounts via command line
- ✅ **Safe editing** - Validates percentages (0-100%)
- ✅ **Automatic backup** - Preserves Liquid file structure
- ✅ **Status indicators** - Shows active/disabled discounts

## 🎯 Example Output

```
🎯 Current HubPRO Discount Percentages:
==================================================
HubPRO Kartell       :  25% 🟢 Active
HubPRO Maxi Panels   :  45% 🟢 Active
==================================================
📁 Source file: ./snippets/hubpro-discount-simple.liquid
```

## 🔧 Interactive Mode Example

```
🔧 Interactive Discount Editor
========================================
Enter new percentages (0 to disable, Enter to skip)

HubPRO Kartell (currently 25%): 30
  → Will change to 30%
HubPRO Maxi Panels (currently 45%): [Enter]

📋 Summary of changes:
  HubPRO Kartell: 25% → 30%

💾 Save changes? (y/N): y
✅ All changes saved successfully!
```

## ⚙️ How It Works

1. **Reads** `snippets/hubpro-discount-simple.liquid`
2. **Parses** discount percentages from Liquid code
3. **Updates** percentages while preserving file structure
4. **Validates** all changes before saving

## 🛡️ Safety Features

- Validates percentage ranges (0-100%)
- Preserves all Liquid code structure
- Shows preview before saving changes
- Requires confirmation for changes

## 📁 Files Modified

- `snippets/hubpro-discount-simple.liquid` - The centralized discount logic

## 🚨 Important Notes

- **0%** = Discount disabled
- **1-100%** = Active discount percentage
- Changes apply immediately to product pages and cart
- Always test changes on development environment first

## 🔗 Integration

This script manages the hardcoded discounts that show:

- **Product page previews** (visual discount display)
- **Cart discount badges** (percentage instead of money)
- **Consistent percentages** across all templates

The actual cart discounts still come from Shopify Admin discount codes, but this script manages the visual display percentages.
