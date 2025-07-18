#!/bin/bash

# =============================================================================
# DEPRECATED LIQUID INCLUDES CONVERSION SCRIPT
# =============================================================================
# 
# This script helps manage the conversion from {% include %} to {% render %}
# It provides testing, backup, and conversion functionality
#
# Usage:
#   ./convert-deprecated-includes.sh test     # Run tests only
#   ./convert-deprecated-includes.sh backup   # Create backups
#   ./convert-deprecated-includes.sh convert  # Convert files
#   ./convert-deprecated-includes.sh rollback # Rollback changes
#
# =============================================================================

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
BACKUP_DIR="backups/deprecated-includes-$(date +%Y%m%d_%H%M%S)"
TEST_FILE="tests/pre-conversion-validation.liquid"
LOG_FILE="logs/conversion-$(date +%Y%m%d_%H%M%S).log"

# Files with deprecated includes (from our analysis)
DEPRECATED_FILES=(
    "templates/collection.wpd_collection_data.liquid"
    "templates/cart.wpd_cart_data.liquid"
    "templates/product.wpd_product_data.liquid"
    "templates/search.wpd_search_data.liquid"
    "templates/search.wcp_discount_api.liquid"
    "templates/search.wlm-api.liquid"
    "templates/search.wcp_cart.liquid"
    "templates/search.wpd_cart_refresh.liquid"
    "snippets/wcp_i_vdtable.liquid"
    "snippets/wlm-head.liquid"
    "snippets/wlm-body.liquid"
    "snippets/wcp_cart.liquid"
)

# Legacy files to be removed
LEGACY_FILES=(
    "layout/theme-bak-wlm.liquid"
    "layout/theme-bak-WPD.liquid"
)

# Create required directories
mkdir -p backups logs tests scripts

# Logging function
log() {
    echo -e "${1}" | tee -a "$LOG_FILE"
}

# Check if we're in the right directory
check_directory() {
    if [ ! -f "layout/theme.liquid" ]; then
        log "${RED}Error: Not in Shopify theme directory${NC}"
        log "Please run this script from the root of your Shopify theme"
        exit 1
    fi
}

# Create backup of files
create_backup() {
    log "${BLUE}Creating backup in ${BACKUP_DIR}${NC}"
    mkdir -p "$BACKUP_DIR"
    
    for file in "${DEPRECATED_FILES[@]}"; do
        if [ -f "$file" ]; then
            cp "$file" "$BACKUP_DIR/"
            log "${GREEN}✓ Backed up: $file${NC}"
        else
            log "${YELLOW}⚠ File not found: $file${NC}"
        fi
    done
    
    # Also backup legacy files
    for file in "${LEGACY_FILES[@]}"; do
        if [ -f "$file" ]; then
            cp "$file" "$BACKUP_DIR/"
            log "${GREEN}✓ Backed up legacy file: $file${NC}"
        fi
    done
    
    log "${GREEN}Backup completed: $BACKUP_DIR${NC}"
}

# Test current functionality
run_tests() {
    log "${BLUE}Running pre-conversion tests...${NC}"
    
    if [ ! -f "$TEST_FILE" ]; then
        log "${RED}Error: Test file not found: $TEST_FILE${NC}"
        log "Please ensure the test file exists before running tests"
        exit 1
    fi
    
    # Create a test page template
    cp "$TEST_FILE" "templates/page.pre-conversion-test.liquid"
    
    log "${GREEN}✓ Test template created: templates/page.pre-conversion-test.liquid${NC}"
    log "${YELLOW}Manual Action Required:${NC}"
    log "1. Create a new page in Shopify admin"
    log "2. Assign the 'Pre-conversion test' template"
    log "3. Visit the page to see test results"
    log "4. Save the test output for comparison"
}

# Convert files from include to render
convert_files() {
    log "${BLUE}Starting conversion process...${NC}"
    
    # First, create backup
    create_backup
    
    local converted_count=0
    local error_count=0
    
    for file in "${DEPRECATED_FILES[@]}"; do
        if [ -f "$file" ]; then
            log "${BLUE}Converting: $file${NC}"
            
            # Create temporary file for conversion
            temp_file="${file}.tmp"
            
            # Convert include to render (but with warnings for WCP files)
            if [[ "$file" == *"wcp"* ]] || [[ "$file" == *"wpd"* ]]; then
                log "${YELLOW}⚠ WARNING: $file contains WCP/WPD integration${NC}"
                log "${YELLOW}  This conversion may break wholesale pricing functionality${NC}"
                log "${YELLOW}  Manual review and testing required${NC}"
                
                # Add warning comment to file
                {
                    echo "{%- comment -%}"
                    echo "  WARNING: This file was converted from {% include %} to {% render %}"
                    echo "  Date: $(date)"
                    echo "  Original backed up to: $BACKUP_DIR"
                    echo "  CRITICAL: WCP/WPD integration may be broken - test thoroughly"
                    echo "{%- endcomment -%}"
                    echo ""
                } > "$temp_file"
                
                # Convert includes to renders with caution
                sed 's/{% include \x27\([^'\'']*\)\x27 with \([^%]*\)%}/{% render \x27\1\x27, \2%}/g' "$file" >> "$temp_file"
                sed -i 's/{% include \x27\([^'\'']*\)\x27 %}/{% render \x27\1\x27 %}/g' "$temp_file"
                
            else
                # Standard conversion for non-WCP files
                sed 's/{% include \x27\([^'\'']*\)\x27 with \([^%]*\)%}/{% render \x27\1\x27, \2%}/g' "$file" > "$temp_file"
                sed -i 's/{% include \x27\([^'\'']*\)\x27 %}/{% render \x27\1\x27 %}/g' "$temp_file"
            fi
            
            # Check if conversion was successful
            if [ -f "$temp_file" ]; then
                mv "$temp_file" "$file"
                log "${GREEN}✓ Converted: $file${NC}"
                ((converted_count++))
            else
                log "${RED}✗ Failed to convert: $file${NC}"
                ((error_count++))
            fi
        else
            log "${YELLOW}⚠ File not found: $file${NC}"
        fi
    done
    
    log "${GREEN}Conversion Summary:${NC}"
    log "  Converted: $converted_count files"
    log "  Errors: $error_count files"
    log "  Backup location: $BACKUP_DIR"
}

# Remove legacy files
remove_legacy_files() {
    log "${BLUE}Removing legacy files...${NC}"
    
    for file in "${LEGACY_FILES[@]}"; do
        if [ -f "$file" ]; then
            rm "$file"
            log "${GREEN}✓ Removed legacy file: $file${NC}"
        else
            log "${YELLOW}⚠ Legacy file not found: $file${NC}"
        fi
    done
}

# Rollback changes
rollback_changes() {
    log "${BLUE}Rolling back changes...${NC}"
    
    # Find most recent backup
    latest_backup=$(ls -t backups/deprecated-includes-* 2>/dev/null | head -1)
    
    if [ -z "$latest_backup" ]; then
        log "${RED}Error: No backup found${NC}"
        exit 1
    fi
    
    log "${BLUE}Using backup: $latest_backup${NC}"
    
    # Restore files
    for file in "$latest_backup"/*; do
        if [ -f "$file" ]; then
            filename=$(basename "$file")
            # Determine original location
            if [[ "$filename" == *"template"* ]]; then
                cp "$file" "templates/$filename"
            elif [[ "$filename" == *"snippet"* ]]; then
                cp "$file" "snippets/$filename"
            elif [[ "$filename" == *"layout"* ]]; then
                cp "$file" "layout/$filename"
            fi
            log "${GREEN}✓ Restored: $filename${NC}"
        fi
    done
    
    log "${GREEN}Rollback completed${NC}"
}

# Validate conversion
validate_conversion() {
    log "${BLUE}Validating conversion...${NC}"
    
    # Check for remaining deprecated includes
    remaining_includes=$(grep -r "{% include" templates/ snippets/ layout/ 2>/dev/null | wc -l)
    
    if [ "$remaining_includes" -eq 0 ]; then
        log "${GREEN}✓ No deprecated includes found${NC}"
    else
        log "${YELLOW}⚠ Found $remaining_includes remaining deprecated includes:${NC}"
        grep -r "{% include" templates/ snippets/ layout/ 2>/dev/null | head -10
    fi
    
    # Check for syntax errors
    log "${BLUE}Checking for obvious syntax errors...${NC}"
    
    error_count=0
    for file in "${DEPRECATED_FILES[@]}"; do
        if [ -f "$file" ]; then
            # Check for common syntax issues
            if grep -q "{% render.*with.*," "$file"; then
                log "${RED}✗ Syntax error in $file: 'with' keyword used with render${NC}"
                ((error_count++))
            fi
        fi
    done
    
    if [ "$error_count" -eq 0 ]; then
        log "${GREEN}✓ No obvious syntax errors found${NC}"
    else
        log "${RED}✗ Found $error_count syntax errors${NC}"
    fi
}

# Main execution
main() {
    check_directory
    
    log "${BLUE}=== Deprecated Liquid Includes Conversion Script ===${NC}"
    log "Started: $(date)"
    log ""
    
    case "${1:-}" in
        test)
            run_tests
            ;;
        backup)
            create_backup
            ;;
        convert)
            log "${YELLOW}⚠ CRITICAL WARNING ⚠${NC}"
            log "This conversion will likely break WCP/WPD wholesale pricing functionality"
            log "Ensure you have:"
            log "1. Created and tested backups"
            log "2. Coordinated with WCP/WPD app developers"
            log "3. Planned for extensive testing after conversion"
            log ""
            read -p "Continue with conversion? (y/N): " -n 1 -r
            echo
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                convert_files
                validate_conversion
            else
                log "${YELLOW}Conversion cancelled${NC}"
            fi
            ;;
        rollback)
            rollback_changes
            ;;
        validate)
            validate_conversion
            ;;
        legacy)
            remove_legacy_files
            ;;
        *)
            log "Usage: $0 {test|backup|convert|rollback|validate|legacy}"
            log ""
            log "Commands:"
            log "  test      - Run pre-conversion tests"
            log "  backup    - Create backup of files"
            log "  convert   - Convert includes to renders (DANGEROUS)"
            log "  rollback  - Restore from backup"
            log "  validate  - Check conversion results"
            log "  legacy    - Remove legacy backup files"
            log ""
            log "Recommended workflow:"
            log "1. ./convert-deprecated-includes.sh test"
            log "2. ./convert-deprecated-includes.sh backup"
            log "3. ./convert-deprecated-includes.sh convert"
            log "4. Test thoroughly"
            log "5. ./convert-deprecated-includes.sh validate"
            exit 1
            ;;
    esac
    
    log ""
    log "Completed: $(date)"
    log "Log file: $LOG_FILE"
}

main "$@" 