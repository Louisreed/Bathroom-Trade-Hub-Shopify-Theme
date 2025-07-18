# Testing Deprecated Liquid Patterns

## 🎯 Quick Start

**Before making ANY changes to deprecated `{% include %}` statements, run these tests to ensure you don't break functionality.**

```bash
# 1. Run the test setup
./scripts/convert-deprecated-includes.sh test

# 2. Create backups (critical!)
./scripts/convert-deprecated-includes.sh backup

# 3. Visit the test page in Shopify to see current behavior
# (Create a page with "Pre-conversion test" template)
```

## 📁 Files Created

This testing suite creates the following files for you:

```
tests/
├── deprecated-liquid-patterns-test.liquid      # Comprehensive test suite
├── pre-conversion-validation.liquid            # Focused validation test
docs/
├── deprecated-includes-conversion-guide.md     # Complete conversion guide
scripts/
├── convert-deprecated-includes.sh              # Automated conversion script
templates/
├── page.pre-conversion-test.liquid             # Test page template (created by script)
backups/
├── deprecated-includes-YYYYMMDD_HHMMSS/        # Backup files (created by script)
logs/
├── conversion-YYYYMMDD_HHMMSS.log              # Conversion logs (created by script)
```

## 🚨 Critical Warning

**This theme uses WCP (Wholesale Club Pricing) integration that will BREAK if you simply convert `{% include %}` to `{% render %}`.**

The WCP integration relies on shared variable scope, which `{% render %}` doesn't provide. Converting without proper refactoring will break:

- Wholesale pricing calculations
- Volume discount tables
- Cart pricing functionality
- Customer group pricing

## 🔍 What These Tests Do

### 1. Pre-Conversion Validation (`tests/pre-conversion-validation.liquid`)

**Purpose**: Captures exact current behavior before any changes

**Tests**:

- ✅ WCP integration functionality
- ✅ WLM (Wholesale Lockdown Manager) integration
- ✅ WPD (Wholesale Pricing Discount) integration
- ✅ Variable scope and assignments
- ✅ Error handling and recovery
- ✅ Price calculations and formatting

**Usage**:

```bash
# Creates the test page template
./scripts/convert-deprecated-includes.sh test

# Then create a page in Shopify admin using the template
```

### 2. Comprehensive Test Suite (`tests/deprecated-liquid-patterns-test.liquid`)

**Purpose**: Detailed analysis of all deprecated patterns and conversion strategy

**Features**:

- 🔍 Side-by-side comparison of `{% include %}` vs `{% render %}`
- ⚠️ Identifies critical breaking changes
- 📋 Lists all files requiring updates
- 🔄 Provides conversion strategy
- 📊 Risk assessment for each component

### 3. Automated Conversion Script (`scripts/convert-deprecated-includes.sh`)

**Purpose**: Safely manage the conversion process with backups and rollback capability

**Commands**:

```bash
./scripts/convert-deprecated-includes.sh test      # Setup test environment
./scripts/convert-deprecated-includes.sh backup    # Create file backups
./scripts/convert-deprecated-includes.sh convert   # Convert files (DANGEROUS)
./scripts/convert-deprecated-includes.sh rollback  # Restore from backup
./scripts/convert-deprecated-includes.sh validate  # Check conversion results
./scripts/convert-deprecated-includes.sh legacy    # Remove legacy files
```

## 📋 Testing Workflow

### Step 1: Pre-Conversion Testing

1. **Run baseline tests**:

   ```bash
   ./scripts/convert-deprecated-includes.sh test
   ```

2. **Create test page in Shopify**:

   - Go to Admin → Pages → Add page
   - Title: "Pre-Conversion Test"
   - Select template: "Pre-conversion test"
   - Save and visit the page

3. **Document results**:
   - Take screenshots of all test output
   - Note all variable values
   - Save HTML source of the page
   - Test with different customer types (wholesale vs retail)

### Step 2: Analysis

1. **Review test results**:

   - Check if WCP variables are being set correctly
   - Verify wholesale pricing is working
   - Confirm volume discount tables display
   - Test cart calculations

2. **Identify critical dependencies**:
   - Note which templates depend on WCP variables
   - Document the data flow from includes to parent templates
   - Map all integration points

### Step 3: Backup and Safety

1. **Create comprehensive backups**:

   ```bash
   ./scripts/convert-deprecated-includes.sh backup
   ```

2. **Test rollback procedure**:

   ```bash
   ./scripts/convert-deprecated-includes.sh rollback
   ```

3. **Verify backup integrity**:
   - Check that all files are backed up
   - Test that rollback restores functionality

### Step 4: Conversion (If Proceeding)

⚠️ **Only proceed if you understand the risks and have a recovery plan**

1. **Attempt conversion**:

   ```bash
   ./scripts/convert-deprecated-includes.sh convert
   ```

2. **Immediate testing**:

   - Run the same tests as Step 1
   - Compare results exactly
   - Test wholesale pricing functionality
   - Verify cart calculations

3. **Rollback if needed**:
   ```bash
   ./scripts/convert-deprecated-includes.sh rollback
   ```

## 🧪 Test Scenarios

### Critical Test Cases

1. **Wholesale Customer Pricing**:

   - Login as wholesale customer
   - View product pages
   - Add to cart
   - Check cart totals
   - Compare with retail pricing

2. **Volume Discount Tables**:

   - View products with volume pricing
   - Check discount table display
   - Verify discount calculations
   - Test different quantity tiers

3. **Customer Access Control**:

   - Test locked/unlocked customers
   - Verify WLM access restrictions
   - Check product visibility
   - Test page access controls

4. **API Endpoints**:
   - Test collection data APIs
   - Verify cart data endpoints
   - Check search functionality
   - Test product data APIs

### Error Scenarios

1. **Missing WCP App**:

   - What happens if WCP app is disabled?
   - How do includes handle missing snippets?
   - Are there fallback mechanisms?

2. **Invalid Product Data**:

   - Test with products missing pricing
   - Test with products without variants
   - Test with products missing in collections

3. **Customer Group Issues**:
   - Test with customers in wrong groups
   - Test with customers missing permissions
   - Test with unassigned customers

## 📊 Expected Results

### When WCP is Working Correctly

```
✅ WCP Integration: Working
✅ Variables Set:
   - wcp_price_min: $X.XX
   - wcp_price_max: $X.XX
   - wcp_v_price: $X.XX
   - wcp_v_compare_at_price: $X.XX
   - wcp_vd_HTML_table: [HTML content]
```

### When WCP is Not Working

```
❌ WCP Integration: Not Working
❌ Variables Set:
   - wcp_price_min: NOT SET
   - wcp_price_max: NOT SET
   - wcp_v_price: NOT SET
   - wcp_v_compare_at_price: NOT SET
   - wcp_vd_HTML_table: NOT SET
```

## 🔧 Troubleshooting

### Common Issues

1. **Test page not working**:

   - Ensure test template is created in correct location
   - Check Shopify page template assignment
   - Verify theme file upload

2. **WCP variables not set**:

   - Check if WCP app is installed and active
   - Verify WCP snippets exist in theme
   - Test with wholesale customer account

3. **Script permissions**:

   ```bash
   chmod +x scripts/convert-deprecated-includes.sh
   ```

4. **Backup issues**:
   - Check disk space
   - Verify file permissions
   - Ensure backup directory exists

### Debug Commands

```bash
# Check for remaining deprecated includes
grep -r "{% include" templates/ snippets/ layout/

# Validate liquid syntax
shopify theme check

# Check for specific WCP variables
grep -r "wcp_" templates/ snippets/

# View recent logs
tail -f logs/conversion-*.log
```

## 📝 Documentation

- **Complete Guide**: `docs/deprecated-includes-conversion-guide.md`
- **Risk Assessment**: See conversion guide for detailed risk analysis
- **Recovery Procedures**: Emergency rollback procedures in guide
- **Technical Details**: Variable scope differences and refactoring approach

## 🚀 Recommendations

### Conservative Approach (Recommended)

1. **Run tests and document current behavior**
2. **Convert only non-WCP files initially**
3. **Keep WCP integration using `{% include %}` until app is updated**
4. **Remove legacy files to clean up codebase**

### Full Conversion (High Risk)

1. **Extensive testing in development environment**
2. **Coordinate with WCP app developers**
3. **Plan for 1-2 weeks of testing and refinement**
4. **Have rollback plan tested and ready**

### Alternative Solutions

1. **Wait for WCP app update with `{% render %}` support**
2. **Engage professional Shopify developers**
3. **Consider switching to different wholesale pricing app**

## 📞 Support

If you encounter issues:

1. **Check the logs**: `logs/conversion-*.log`
2. **Review the guide**: `docs/deprecated-includes-conversion-guide.md`
3. **Test rollback**: `./scripts/convert-deprecated-includes.sh rollback`
4. **Contact WCP support**: For app-specific issues

---

**Remember**: The goal is to maintain business functionality while modernizing the codebase. If wholesale pricing breaks, the conversion has failed regardless of technical success.

## 🏁 Quick Commands Reference

```bash
# Setup and test
./scripts/convert-deprecated-includes.sh test
./scripts/convert-deprecated-includes.sh backup

# If you decide to convert (HIGH RISK)
./scripts/convert-deprecated-includes.sh convert

# If something breaks (RECOVERY)
./scripts/convert-deprecated-includes.sh rollback

# Check results
./scripts/convert-deprecated-includes.sh validate
```

**Next Steps**: Read the complete guide in `docs/deprecated-includes-conversion-guide.md` before proceeding with any conversion.
