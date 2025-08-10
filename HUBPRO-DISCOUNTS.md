# HubPRO Discount System

This document explains how to set up and manage the HubPRO membership discount system for Bathroom Trade Hub.

## Overview

The HubPRO discount system provides collection-based percentage discounts for members with different tiers:

- **HubPRO Free**: Lower discount percentages
- **HubPRO Plus**: Higher discount percentages

**💡 DESIGN**: This system combines **Shopify discount codes** (for actual cart discounts) with **template enhancements** (for visual display of discount badges and labels).

## System Architecture

### Shopify Discount Codes (Backend)

- **Real discounts**: Actually reduces prices in cart/checkout
- **Tag-filtered**: Each discount restricted to specific customer tags
- **Dual setup**: Two discount codes per collection (Free + Plus tiers)
- **Automatic application**: Applied based on customer tags

### Template Enhancements (Frontend)

- **Visual badges**: Shows "HubPRO Kartell -25%" style labels
- **Before/after pricing**: Displays original vs discounted prices
- **Collection detection**: Identifies which discounts apply
- **Membership awareness**: Detects customer tier for appropriate display

## Shopify Admin Setup

### 1. Customer Tags Setup

#### Create Customer Tags

In Shopify Admin → Customers, create and assign these tags:

- `hubpro-free` - For basic HubPRO members
- `hubpro-plus` - For premium HubPRO members

#### Assign Tags to Customers

1. Go to **Customers** in Shopify Admin
2. Select a customer
3. In the **Tags** field, add either:
   - `hubpro-free` for basic members
   - `hubpro-plus` for premium members
4. Save the customer

### 2. Shopify Discount Codes Setup

#### Create Discount Codes for Each Collection + Tier

⚠️ **IMPORTANT**: You need **2 discount codes per collection** (one for each membership tier)

**Step-by-step for each collection:**

1. Go to **Shopify Admin** → **Discounts**
2. Click **Create discount** → **Percentage**

#### Kartell Collection Discounts

**HUBPRO-KARTELL-FREE**

- **Discount code**: `HUBPRO-KARTELL-FREE`
- **Type**: Percentage
- **Value**: 25%
- **Applies to**: Specific collections → Select "Kartell" collection
- **Customer eligibility**: Specific customer tags → `hubpro-free`
- **Usage limits**: Leave unlimited (for automatic application)
- **Active dates**: Set as needed

**HUBPRO-KARTELL-PLUS**

- **Discount code**: `HUBPRO-KARTELL-PLUS`
- **Type**: Percentage
- **Value**: 35%
- **Applies to**: Specific collections → Select "Kartell" collection
- **Customer eligibility**: Specific customer tags → `hubpro-plus`
- **Usage limits**: Leave unlimited
- **Active dates**: Set as needed

#### Maxi Panels Collection Discounts

**HUBPRO-MAXI-FREE**

- **Discount code**: `HUBPRO-MAXI-FREE`
- **Value**: 10%
- **Collections**: Maxi Panels
- **Customer tags**: `hubpro-free`

**HUBPRO-MAXI-PLUS**

- **Discount code**: `HUBPRO-MAXI-PLUS`
- **Value**: 25%
- **Collections**: Maxi Panels
- **Customer tags**: `hubpro-plus`

#### Cladworks Collection Discounts

**HUBPRO-CLADWORKS-FREE**

- **Discount code**: `HUBPRO-CLADWORKS-FREE`
- **Value**: 10%
- **Collections**: Cladworks
- **Customer tags**: `hubpro-free`

**HUBPRO-CLADWORKS-PLUS**

- **Discount code**: `HUBPRO-CLADWORKS-PLUS`
- **Value**: 25%
- **Collections**: Cladworks
- **Customer tags**: `hubpro-plus`

### 3. Collection Setup

#### Create Product Collections

Set up collections that match your discount codes:

1. **Kartell Collection** - Handle: `kartell`
2. **Maxi Panels Collection** - Handle: `maxi-panels`
3. **Cladworks Collection** - Handle: `cladworks`

#### Add Products to Collections

1. Go to **Products** → **Collections**
2. Select the appropriate collection
3. Add products that should receive the discount
4. Ensure collection handles match the template code

### 4. Testing the System

#### Test Customer Experience

1. Create test customers with different tags (`hubpro-free`, `hubpro-plus`)
2. Log in as test customers
3. Add products from discount collections to cart
4. Verify **automatic discount application** in cart
5. Check that **correct discount** applies based on customer tag
6. Confirm **visual badges** display on product pages

#### Expected Results

- **Cart**: Automatic discount application based on customer tags
- **Product pages**: Visual badges showing "HubPRO Kartell -35%" etc.
- **Pricing**: Before/after prices displayed correctly
- **No conflicts**: Only one discount per collection applies per customer

## Template Implementation

### Core Files

The template enhancements are implemented in:

#### `snippets/product-price.liquid`

Visual discount badges and pricing display:

```liquid
{%- comment -%} HubPRO discount configuration {%- endcomment -%}
{%- assign current_discount_percent = 0 -%}
{%- assign current_display_name = '' -%}
{%- assign is_hubpro_member = false -%}
{%- assign membership_tier = '' -%}

{%- comment -%} Check if customer is HubPRO member {%- endcomment -%}
{%- if customer and customer.tags -%}
  {%- if customer.tags contains 'hubpro-plus' -%}
    {%- assign is_hubpro_member = true -%}
    {%- assign membership_tier = 'plus' -%}
  {%- elsif customer.tags contains 'hubpro-free' -%}
    {%- assign is_hubpro_member = true -%}
    {%- assign membership_tier = 'free' -%}
  {%- endif -%}
{%- endif -%}
```

### Adding New Collections

To add a new collection discount:

1. **Create Shopify discount codes** (2 codes - Free + Plus tiers):

   ```
   HUBPRO-NEWCOLLECTION-FREE (e.g., 15% discount)
   HUBPRO-NEWCOLLECTION-PLUS (e.g., 30% discount)
   ```

2. **Update template code** in `snippets/product-price.liquid`:

   ```liquid
   {%- comment -%} NEW COLLECTION DISCOUNTS {%- endcomment -%}
   {%- elsif c.handle contains 'your-collection-handle' -%}
     {%- assign current_display_name = 'Your Collection Name' -%}
     {%- if membership_tier == 'plus' -%}
       {%- assign current_discount_percent = 30 -%}
     {%- else -%}
       {%- assign current_discount_percent = 15 -%}
     {%- endif -%}
     {%- break -%}
   ```

3. **Create the collection** in Shopify Admin with matching handle

4. **Add products** to the new collection

### Customizing Discount Percentages

To modify discount percentages:

1. **Update Shopify discount codes** in Admin → Discounts
2. **Update template percentages** in `snippets/product-price.liquid` to match

**⚠️ CRITICAL**: Template percentages must match Shopify discount code values for accurate visual display.

### Display Customization

#### Discount Badges

Badges are automatically generated based on:

- **Product pages**: Shows collection name (e.g., "HubPRO Kartell")
- **Other pages**: Shows generic "HubPRO"

#### Price Display

The system shows:

- **Original price**: Struck through with reduced opacity
- **Discounted price**: Prominent display (calculated for visual purposes)
- **Discount badge**: Collection name and percentage

## Usage Examples

### Render Product Price with Discounts

```liquid
{%- render 'product-price',
  product: product,
  use_variant: true,
  class: 'flex flex-wrap items-baseline gap-2'
-%}
```

### Check if Customer is HubPRO Member

```liquid
{%- assign is_hubpro = false -%}
{%- if customer and customer.tags -%}
  {%- if customer.tags contains 'hubpro-plus' or customer.tags contains 'hubpro-free' -%}
    {%- assign is_hubpro = true -%}
  {%- endif -%}
{%- endif -%}

{%- if is_hubpro -%}
  <!-- Show member-only content -->
{%- endif -%}
```

## Troubleshooting

### Common Issues

#### Discounts Not Applying in Cart

1. **Check customer tags**: Ensure customer has correct tag (`hubpro-free` or `hubpro-plus`)
2. **Verify discount codes**: Confirm codes are active and properly configured
3. **Collection assignment**: Product must be in the correct collection
4. **Tag restrictions**: Discount code must be restricted to correct customer tags

#### Wrong Discount Amount

1. **Check membership tier**: Verify customer has correct tag
2. **Review discount codes**: Ensure correct percentage is set in Shopify Admin
3. **Multiple discounts**: Only one HubPRO discount should apply per collection

#### Badges Not Displaying

1. **Template integration**: Ensure `product-price.liquid` is properly rendered
2. **Collection handles**: Verify collection handles match template code
3. **Customer login**: Customer must be logged in to see member pricing

#### Multiple Discounts Conflicting

1. **Shopify discount stacking**: Check if other discounts are interfering
2. **Code priority**: HubPRO discounts should have appropriate priority settings
3. **Collection overlap**: Ensure products aren't in multiple discount collections

### Testing Checklist

- [ ] Customer tags are correctly assigned (`hubpro-free`, `hubpro-plus`)
- [ ] Discount codes are created for each collection + tier combination
- [ ] Collections have proper handles matching template code
- [ ] Products are assigned to correct collections
- [ ] Discount codes are restricted to correct customer tags
- [ ] Template percentages match Shopify discount code values
- [ ] Automatic discount application works in cart
- [ ] Visual badges display correctly on product pages
- [ ] No discount conflicts or stacking issues

## Maintenance

### Regular Tasks

1. **Monitor customer tags**: Ensure new members get proper tags
2. **Update discount codes**: Modify percentages as needed in Shopify Admin
3. **Sync template code**: Update template percentages to match discount codes
4. **Test functionality**: Regular testing with different customer scenarios

### Adding New Collections

1. **Create 2 discount codes** (Free + Plus tiers)
2. **Update template code** with new collection logic
3. **Create collection** with matching handle
4. **Add products** to collection
5. **Test thoroughly** with both membership tiers

### Seasonal Updates

When running promotions or changing discount structures:

1. **Update Shopify discount codes**: Modify percentages in Admin
2. **Update template percentages**: Keep visual display in sync
3. **Test all combinations**: Verify Free + Plus tiers work correctly
4. **Communicate changes**: Inform customers of updated benefits

## Technical Notes

### Performance Considerations

- **Shopify native**: Uses built-in discount system for optimal performance
- **Automatic application**: No manual code entry required
- **Template enhancements**: Minimal impact on page load times

### Browser Compatibility

- **Universal support**: Works with all browsers (Shopify native functionality)
- **Progressive enhancement**: Visual badges enhance but don't break experience
- **No JavaScript dependencies**: Pure Liquid template implementation

### Security

- **Customer tags**: Secure access control via Shopify's customer system
- **Automatic application**: No discount codes exposed to customers
- **Admin control**: Full control over discount activation/deactivation

## Support

For technical issues or questions about the HubPRO discount system:

1. **Check discount codes**: Verify all codes are active in Shopify Admin
2. **Review customer tags**: Ensure customers have correct membership tags
3. **Test cart functionality**: Confirm automatic discount application
4. **Verify template sync**: Check that visual percentages match actual discounts

---

_Last updated: [Current Date]_
_Version: 2.0 - Dual Discount Code System_
