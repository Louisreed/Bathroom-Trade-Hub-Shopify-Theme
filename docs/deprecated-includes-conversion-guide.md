# Deprecated Liquid Includes Conversion Guide

## 🚨 Critical Warning

**DO NOT perform a simple find-and-replace conversion from `{% include %}` to `{% render %}`**

This theme uses third-party app integrations (WCP, WLM, WPD) that rely on `{% include %}` sharing variable scope with parent templates. Converting to `{% render %}` without proper refactoring **WILL BREAK** wholesale pricing functionality.

## 📋 Overview

This guide provides a systematic approach to converting deprecated `{% include %}` statements to modern `{% render %}` statements while preserving functionality.

### Affected Integrations

- **WCP** (Wholesale Club Pricing) - Critical business functionality
- **WLM** (Wholesale Lockdown Manager) - Customer access control
- **WPD** (Wholesale Pricing Discount) - Volume pricing
- **LimeSpot** - Product recommendations

## 🔍 Pre-Conversion Testing

### Step 1: Run Baseline Tests

1. **Create the test files** (already provided):

   - `tests/deprecated-liquid-patterns-test.liquid`
   - `tests/pre-conversion-validation.liquid`

2. **Run the test script**:

   ```bash
   chmod +x scripts/convert-deprecated-includes.sh
   ./scripts/convert-deprecated-includes.sh test
   ```

3. **Create test page in Shopify**:

   - Go to Shopify Admin → Pages → Add page
   - Title: "Pre-Conversion Test"
   - Assign template: "Pre-conversion test"
   - Save and visit the page

4. **Document the results**:
   - Take screenshots of test output
   - Note all variable values
   - Save HTML output to file for comparison

### Step 2: Verify Critical Variables

Ensure these variables are being set correctly:

```liquid
wcp_price_min          # Minimum wholesale price
wcp_price_max          # Maximum wholesale price
wcp_v_price            # Variant wholesale price
wcp_v_compare_at_price # Variant compare price
wcp_vd_HTML_table      # Volume discount table HTML
```

## 📁 Files Requiring Conversion

### High Priority Templates (Business Critical)

```
templates/collection.wpd_collection_data.liquid     (7 includes)
templates/cart.wpd_cart_data.liquid                (1 include)
templates/product.wpd_product_data.liquid          (7 includes)
templates/search.wpd_search_data.liquid            (6 includes)
templates/search.wcp_discount_api.liquid           (2 includes)
templates/search.wcp_cart.liquid                   (3 includes)
templates/search.wpd_cart_refresh.liquid           (3 includes)
```

### Medium Priority Snippets

```
snippets/wcp_i_vdtable.liquid                      (4 includes)
snippets/wlm-head.liquid                           (6 includes)
snippets/wlm-body.liquid                           (1 include)
snippets/wcp_cart.liquid                           (4 includes)
```

### Legacy Files (Should be Removed)

```
layout/theme-bak-wlm.liquid                        (2 includes)
layout/theme-bak-WPD.liquid                        (1 include)
```

## 🔄 Conversion Strategy

### Phase 1: Preparation (1-2 days)

1. **Create comprehensive backups**:

   ```bash
   ./scripts/convert-deprecated-includes.sh backup
   ```

2. **Document current behavior**:

   - Run all tests and save outputs
   - Test with different customer types (wholesale vs retail)
   - Test with different product types
   - Document all variable dependencies

3. **Coordinate with stakeholders**:
   - Inform business stakeholders of planned changes
   - Coordinate with app developers (WCP, WLM) if possible
   - Plan for extended testing period

### Phase 2: WCP Integration Analysis (2-3 days)

This is the most critical phase as WCP handles wholesale pricing.

1. **Analyze WCP snippets**:

   ```bash
   # Examine these critical snippets
   snippets/wcp_discount.liquid
   snippets/wcp_variant.liquid
   snippets/wcp_vd_product.liquid
   snippets/wcp_vd_discount.liquid
   ```

2. **Identify variable dependencies**:

   - Map which templates depend on WCP-set variables
   - Document the data flow from includes to parent templates
   - Identify all points where WCP variables are used

3. **Plan refactoring approach**:
   - Option A: Modify WCP snippets to return data objects
   - Option B: Use assign statements with render outputs
   - Option C: Coordinate with WCP developers for updated integration

### Phase 3: Safe Conversion (Non-WCP Files First)

1. **Start with WLM files** (lower risk):

   ```bash
   # Convert WLM includes first
   templates/search.wlm-api.liquid
   snippets/wlm-head.liquid
   snippets/wlm-body.liquid
   ```

2. **Test WLM functionality**:
   - Test with locked/unlocked customers
   - Verify access control still works
   - Check for any display issues

### Phase 4: WCP Conversion (High Risk)

⚠️ **This phase will likely break wholesale pricing functionality**

1. **Attempt conversion with warnings**:

   ```bash
   ./scripts/convert-deprecated-includes.sh convert
   ```

2. **Immediate testing required**:
   - Test wholesale pricing on product pages
   - Test cart calculations
   - Test volume discount tables
   - Test API endpoints

### Phase 5: Recovery Plan

If conversion breaks functionality:

1. **Immediate rollback**:

   ```bash
   ./scripts/convert-deprecated-includes.sh rollback
   ```

2. **Alternative approaches**:
   - Keep critical WCP files using `{% include %}`
   - Gradually migrate non-critical files only
   - Wait for WCP app update with `{% render %}` support

## 🧪 Testing Checklist

### Pre-Conversion Tests

- [ ] Baseline functionality documented
- [ ] All variable values recorded
- [ ] Screenshots of test outputs saved
- [ ] Different customer types tested
- [ ] Various product types tested

### Post-Conversion Tests

- [ ] All pre-conversion tests repeated
- [ ] Variable values match exactly
- [ ] Wholesale pricing calculations correct
- [ ] Volume discount tables display properly
- [ ] Cart calculations accurate
- [ ] API endpoints return correct data
- [ ] No JavaScript errors in console
- [ ] No Liquid errors in theme inspector

### Business Function Tests

- [ ] Wholesale customer pricing
- [ ] Retail customer pricing
- [ ] Volume discount calculations
- [ ] Cart total calculations
- [ ] Product bundle pricing
- [ ] Customer group restrictions
- [ ] API data accuracy

## 🔧 Technical Details

### Variable Scope Differences

#### With `{% include %}`

```liquid
{% assign test_var = 'not set' %}
{% include 'set-variable' %}
{{ test_var }} <!-- Shows value set in snippet -->
```

#### With `{% render %}`

```liquid
{% assign test_var = 'not set' %}
{% render 'set-variable' %}
{{ test_var }} <!-- Still shows 'not set' -->
```

### Required WCP Snippet Modifications

If WCP snippets need modification, they should be changed to:

```liquid
{%- comment -%}
  WCP Discount Snippet - Modified for {% render %} compatibility
{%- endcomment -%}

{%- liquid
  # Calculate wholesale pricing
  assign wcp_data = product | wcp_calculate_pricing

  # Return data object instead of setting global variables
  echo wcp_data | json
-%}
```

### Parent Template Updates

Templates would need to capture returned data:

```liquid
{%- liquid
  # Instead of:
  # include 'wcp_discount' with product

  # Use:
  assign wcp_result = 'wcp_discount' | render: product
  assign wcp_data = wcp_result | parse_json
  assign wcp_v_price = wcp_data.variant_price
-%}
```

## 📊 Risk Assessment

| Component            | Risk Level   | Impact           | Mitigation                         |
| -------------------- | ------------ | ---------------- | ---------------------------------- |
| WCP Integration      | **CRITICAL** | Business Revenue | Extensive testing, rollback plan   |
| WLM Integration      | **HIGH**     | Customer Access  | Test with different customer types |
| WPD Integration      | **HIGH**     | Pricing Display  | Verify all discount calculations   |
| LimeSpot Integration | **MEDIUM**   | Recommendations  | Visual testing required            |
| Template Performance | **LOW**      | Page Speed       | Monitor after conversion           |

## 🚀 Success Criteria

The conversion is successful when:

1. ✅ All pre-conversion tests pass with identical results
2. ✅ Wholesale pricing calculations are accurate
3. ✅ Volume discount tables display correctly
4. ✅ Customer access controls work properly
5. ✅ No Liquid errors in theme inspector
6. ✅ No JavaScript console errors
7. ✅ API endpoints return correct data
8. ✅ Performance is maintained or improved

## 🆘 Emergency Procedures

### If Conversion Breaks the Site

1. **Immediate Actions** (< 5 minutes):

   ```bash
   ./scripts/convert-deprecated-includes.sh rollback
   ```

2. **Verify Rollback** (< 10 minutes):

   - Test critical wholesale pricing
   - Verify cart functionality
   - Check customer access controls

3. **Communication** (< 15 minutes):
   - Notify stakeholders
   - Update status page if needed
   - Document what went wrong

### If Partial Functionality is Broken

1. **Selective Rollback**:

   - Identify specific broken files
   - Restore only those files from backup
   - Test incrementally

2. **Hybrid Approach**:
   - Keep critical WCP files using `{% include %}`
   - Convert only non-critical files to `{% render %}`
   - Plan future migration strategy

## 📝 Final Recommendations

### Recommended Approach

1. **Conservative Strategy**:

   - Convert only non-WCP files initially
   - Keep WCP integration using `{% include %}` until app is updated
   - Remove legacy files to clean up codebase

2. **Full Conversion Requirements**:

   - Dedicated development environment
   - Extensive testing period (1-2 weeks minimum)
   - Business stakeholder approval
   - Rollback plan tested and ready

3. **Alternative Solutions**:
   - Wait for WCP app update with `{% render %}` support
   - Engage professional Shopify developers
   - Consider switching to different wholesale pricing app

### Timeline Estimate

- **Conservative approach**: 3-5 days
- **Full conversion with testing**: 2-3 weeks
- **Recovery if issues occur**: 1-5 days

Remember: The goal is to maintain business functionality while modernizing the codebase. If wholesale pricing breaks, the conversion has failed regardless of technical success.

## 📞 Support Resources

- **Shopify Liquid Documentation**: https://shopify.dev/docs/api/liquid
- **Theme Inspector**: Use for debugging Liquid errors
- **WCP Support**: Contact app developers for guidance
- **Backup Strategy**: Always maintain multiple backup points

---

**⚠️ Final Warning**: This conversion affects critical business functionality. Proceed with extreme caution and thorough testing.
