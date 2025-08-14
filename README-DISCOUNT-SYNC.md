# 🔄 Shopify Discount Synchronization System

**Version 2.0** - Enhanced with robust Liquid syntax validation and error handling

Automatically synchronizes Shopify Admin discount codes with theme template files to ensure product page discount previews match actual cart/checkout discounts.

## 🎯 Problem Solved

**Issue**: Product pages can't show discount previews natively in Shopify, but customers expect to see member pricing before adding items to cart.

**Solution**: Fetch discount rules from Shopify Admin API and automatically generate synchronized template code that mirrors Shopify's discount application logic exactly.

## 🏗️ How It Works

```
┌─────────────────────┐    ┌──────────────────────┐    ┌─────────────────────┐
│   Shopify Admin     │    │   Sync Script        │    │   Theme Templates   │
│                     │    │                      │    │                     │
│ • Discount Codes    │───▶│ • Fetch via GraphQL  │───▶│ • hubpro-discount-  │
│ • Customer Tags     │    │ • Parse Rules        │    │   simple.liquid     │
│ • Collection Rules  │    │ • Generate Logic     │    │ • product-price.    │
│ • Percentages       │    │ • Update Files       │    │   liquid            │
└─────────────────────┘    └──────────────────────┘    └─────────────────────┘
```

### Key Benefits

✅ **Perfect Consistency**: Template previews match cart/checkout exactly  
✅ **Zero Manual Maintenance**: No more hardcoded percentage updates  
✅ **Automatic Collection Mapping**: Handles collection ID → handle mapping  
✅ **Customer Segment Logic**: Mirrors Shopify's tag-based targeting  
✅ **Error Prevention**: Eliminates sync mistakes and inconsistencies  
✅ **Robust Error Handling**: Advanced Liquid syntax validation and auto-correction  
✅ **Production Ready**: Comprehensive testing with end-to-end validation

## 🚀 Quick Start

### ⚡ Automated Setup (Recommended)

Run the interactive setup wizard:

```bash
python3 setup_discount_sync.py
```

The wizard will:

- Guide you through Shopify API setup
- Create configuration file
- Test your connection
- Run your first sync
- Show next steps

### 🔧 Manual Setup

### 1. Setup Shopify API Access

1. **Create Private App** in Shopify Admin:

   - Go to **Apps** → **App and sales channel settings**
   - Click **Develop apps for your store**
   - Create new app: "Discount Sync Tool"

2. **Configure API Permissions**:

   ```
   Admin API access scopes:
   ✅ read_discounts
   ✅ read_products (includes collections access)
   ```

3. **Get Access Token**:
   - Install the app to your store
   - Copy the **Admin API access token**

### 2. Configure the Script

Copy the config template:

```bash
cp shopify_config_template.json shopify_config.json
```

Edit `shopify_config.json`:

```json
{
  "store_url": "your-store.myshopify.com",
  "access_token": "shpat_your_actual_token_here"
}
```

### 3. Run Synchronization

```bash
# Using config file (recommended)
python3 sync_discounts.py --config shopify_config.json

# Or direct parameters
python3 sync_discounts.py --store your-store.myshopify.com --token shpat_your_token
```

### 4. Verify Results

The script will automatically:

- ✅ Fetch all discount codes from Shopify
- ✅ Update `snippets/hubpro-discount-simple.liquid`
- ✅ Update customer segmentation in `snippets/product-price.liquid`
- ✅ Validate the synchronization worked

## 📋 Command Options

### Basic Usage

```bash
python3 sync_discounts.py --config shopify_config.json
```

### Advanced Options

```bash
# Custom theme path
python3 sync_discounts.py --config config.json --theme-path /path/to/theme

# Validation only (no changes)
python3 sync_discounts.py --config config.json --validate-only

# Direct parameters
python3 sync_discounts.py --store store.myshopify.com --token shpat_token
```

## 🔧 Generated Template Logic

### hubpro-discount-simple.liquid

The script generates two types of discount lookup logic:

#### 1. Title-Based Lookup (Cart Badges)

```liquid
{%- if title contains 'HUBPRO' or title contains 'Kartell' -%}
  {%- assign percentage = 35 -%}
{%- elsif title contains 'Maxi' or title contains 'Panels' -%}
  {%- assign percentage = 50 -%}
{%- endif -%}
```

#### 2. Collection + Segment Lookup (Product Previews)

```liquid
{%- elsif segment == 'hubpro-free' -%}
  {%- if collection contains 'kartell' -%}
    {%- assign percentage = 35 -%}
  {%- elsif collection contains 'maxi-panels' -%}
    {%- assign percentage = 50 -%}
  {%- endif -%}
```

### product-price.liquid Updates

Updates customer segmentation logic:

```liquid
{%- if customer.tags contains 'hubpro-plus' -%}
  {%- assign customer_segment = 'hubpro-plus' -%}
{%- elsif customer.tags contains 'hubpro-free' -%}
  {%- assign customer_segment = 'hubpro-free' -%}
{%- else -%}
  {%- assign customer_segment = 'diy' -%}
{%- endif -%}
```

## 📊 Discount Structure Analysis

The script analyzes your discount structure and shows:

```
📊 Analysis summary:
   • Active rules: 12
   • Inactive rules: 3
   • Customer segments: ['hubpro-free', 'hubpro-plus']
   • Collections: 8
```

## 🔒 Security & Best Practices

### API Token Security

- **Never commit tokens** to version control
- Use **config file** with restricted permissions: `chmod 600 shopify_config.json`
- **Rotate tokens** regularly
- Use **minimum required scopes**

### Theme Safety

- Script creates **backups** before making changes
- **Test on development theme** first
- **Review generated code** before deploying
- Keep **git history** of template changes

## 🐛 Troubleshooting

### Common Issues

#### ❌ "No discount rules found"

**Cause**: API permissions or authentication issue  
**Fix**: Verify your access token has `read_discounts` scope

#### ❌ "Collection handle not found"

**Cause**: Collection was deleted but discount still references it  
**Fix**: Update or disable the discount in Shopify Admin

#### ❌ "Template file not found"

**Cause**: Wrong theme path or file moved  
**Fix**: Check `--theme-path` parameter points to correct directory

#### ❌ "Liquid syntax error: 'if' tag was never closed"

**Cause**: Template generation created malformed Liquid structure  
**Symptoms**:

- `shopify theme dev` shows syntax errors
- Error mentions unclosed if/endif tags in generated templates

**Fix**: Re-run the sync script - it now includes enhanced error handling:

```bash
python3 sync_discounts.py --config shopify_config.json
```

**Technical Details**: The sync script now includes:

- Robust regex patterns for customer block endif detection
- Automatic Liquid structure validation
- Dual-pattern matching with fallback logic
- Enhanced template generation with proper if/elsif/endif balancing

#### ❌ "Failed to upload file to remote theme"

**Cause**: Generated templates contain Liquid syntax errors  
**Fix**:

1. Check the specific line mentioned in the error
2. Re-run sync script (includes automatic fixes)
3. Test with `shopify theme dev` before uploading

### Validation Checks

```bash
# Test API connection and validate sync
python3 sync_discounts.py --config shopify_config.json --validate-only

# Run complete sync and test templates
python3 sync_discounts.py --config shopify_config.json

# Test Liquid syntax with Shopify theme dev
shopify theme dev --store your-store

# Check generated template structure
shopify theme check snippets/hubpro-discount-simple.liquid snippets/product-price.liquid

# Check file permissions
ls -la snippets/hubpro-discount-simple.liquid snippets/product-price.liquid

# Verify GraphQL API access
curl -X POST https://your-store.myshopify.com/admin/api/2024-10/graphql.json \
  -H "X-Shopify-Access-Token: your_token" \
  -d '{"query": "{ shop { name } }"}'
```

#### End-to-End Testing

**Recommended testing sequence:**

1. **Sync**: `python3 sync_discounts.py --config shopify_config.json`
2. **Validate**: Check console output for "✅ Validation passed!"
3. **Test**: `shopify theme dev` - should start without syntax errors
4. **Verify**: Check product pages show correct discount previews

## 📈 Monitoring & Maintenance

### Regular Sync Schedule

Set up automated synchronization:

```bash
# Crontab: Sync daily at 6 AM
0 6 * * * cd /path/to/theme && python3 sync_discounts.py --config shopify_config.json
```

### Change Detection

The script adds timestamps to generated files:

```liquid
{%- comment -%}
  AUTO-GENERATED: Shopify Discount Sync System
  Generated on: 2024-01-15T10:30:45
{%- endcomment -%}
```

### Monitoring Checklist

- [ ] **Weekly**: Review discount structure in Shopify Admin
- [ ] **Monthly**: Run sync manually to check for issues
- [ ] **Before major sales**: Sync to ensure new discounts are included
- [ ] **After collection changes**: Re-sync to update mappings

## 🔗 Integration with Existing System

### Backward Compatibility

The new system maintains compatibility with:

- ✅ Existing `manage_discounts.py` script (for manual overrides)
- ✅ Current template structure and styling
- ✅ Customer tag logic (`hubpro-free`, `hubpro-plus`, `diy`)
- ✅ Collection-based discount logic

### Migration Path

1. **Current**: Manual percentage updates in templates
2. **Transition**: Run sync script to generate automated templates
3. **Future**: Fully automated via API synchronization

## 🔧 Recent System Improvements

### Enhanced Reliability (Latest Version)

The discount synchronization system has been significantly improved with:

#### **Liquid Syntax Validation**

- **Automatic if/endif balancing**: Ensures all Liquid blocks are properly closed
- **Dual-pattern regex matching**: Primary patterns with fallback logic for edge cases
- **Template structure validation**: Prevents malformed Liquid code generation
- **Real-time syntax checking**: Validates templates before file writes

#### **Robust Error Handling**

- **Customer block closure detection**: Automatically fixes unclosed customer segmentation logic
- **Enhanced regex patterns**: Comprehensive pattern matching for complex template structures
- **Fallback mechanisms**: Multiple validation layers to prevent template corruption
- **End-to-end testing**: Automatic validation with `shopify theme dev` compatibility

#### **Production Hardening**

- **Comprehensive test suite**: Full validation cycle with syntax checking
- **Backup and recovery**: Safe template updates with rollback capabilities
- **Change tracking**: Detailed timestamps and generation metadata
- **Error reporting**: Clear diagnostics for troubleshooting

### System Architecture

```
🔄 Sync Process Flow:
┌─────────────┐   ┌───────────────┐   ┌──────────────┐   ┌─────────────┐
│ Fetch Data  │──▶│ Validate API  │──▶│ Generate     │──▶│ Test &      │
│ • Discounts │   │ • Collections │   │ Templates    │   │ Validate    │
│ • Rules     │   │ • Permissions │   │ • Syntax     │   │ • Upload    │
└─────────────┘   └───────────────┘   └──────────────┘   └─────────────┘

🛡️ Error Handling:
┌─────────────┐   ┌──────────────┐   ┌─────────────┐
│ Regex       │──▶│ Validation   │──▶│ Fallback    │
│ Detection   │   │ Checks       │   │ Logic       │
└─────────────┘   └──────────────┘   └─────────────┘
```

## 📚 Technical Reference

### GraphQL Queries Used

#### Discount Codes Query

```graphql
query GetDiscountCodes($first: Int!, $after: String) {
  discountNodes(first: $first, after: $after) {
    edges {
      node {
        discount {
          ... on DiscountCodeBasic {
            title
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
                  collections {
                    edges {
                      node {
                        id
                      }
                    }
                  }
                }
              }
            }
            customerSelection {
              ... on DiscountCustomerTags {
                tags
              }
            }
          }
        }
      }
    }
  }
}
```

#### Collections Query

```graphql
query GetCollections($first: Int!, $after: String) {
  collections(first: $first, after: $after) {
    edges {
      node {
        id
        handle
        title
      }
    }
  }
}
```

### File Structure

```
theme/
├── setup_discount_sync.py      # Interactive setup wizard
├── sync_discounts.py           # Main sync script
├── test_sync_setup.py          # Connection/setup validation
├── requirements-sync.txt       # Python dependencies
├── shopify_config.json         # API configuration (created)
├── shopify_config_template.json # Config template
├── snippets/
│   ├── hubpro-discount-simple.liquid  # Generated lookup logic
│   └── product-price.liquid           # Updated segmentation
└── README-DISCOUNT-SYNC.md     # This documentation
```

## 🆘 Support

### Getting Help

1. **Check logs**: Script provides detailed output of each step
2. **Validate setup**: Use `--validate-only` flag to test configuration
3. **Review generated code**: Check template files for syntax errors
4. **API documentation**: [Shopify Admin API Docs](https://shopify.dev/docs/admin-api)

### Common Questions

**Q: How often should I run the sync?**  
A: After any changes to discount codes, collections, or customer tags. Consider daily automated runs.

**Q: What happens if Shopify API is down?**  
A: Script will fail gracefully with error messages. Templates keep working with last synced values.

**Q: Can I customize the generated logic?**  
A: Yes, but changes will be overwritten on next sync. Consider extending the script instead.

**Q: Does this work with all discount types?**  
A: Currently supports percentage discounts with customer tag targeting. Fixed amount and other types planned.

---

**🎉 Result**: Perfect price consistency between product previews and cart/checkout, with zero manual maintenance!
