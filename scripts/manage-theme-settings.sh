#!/bin/bash

# =============================================================================
# THEME SETTINGS MANAGEMENT SCRIPT
# =============================================================================
# 
# This script helps manage Shopify theme settings to prevent them from being
# overwritten when running shopify theme dev or git operations
#
# Usage:
#   ./manage-theme-settings.sh backup    # Backup current settings
#   ./manage-theme-settings.sh restore   # Restore from backup
#   ./manage-theme-settings.sh commit    # Commit current settings
#   ./manage-theme-settings.sh diff      # Show differences
#   ./manage-theme-settings.sh watch     # Watch for changes
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
SETTINGS_FILE="config/settings_data.json"
BACKUP_DIR="backups/settings"
BACKUP_PREFIX="settings_data"
LOG_FILE="logs/theme-settings-$(date +%Y%m%d_%H%M%S).log"

# Create required directories
mkdir -p "$BACKUP_DIR" logs

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
    
    if [ ! -f "$SETTINGS_FILE" ]; then
        log "${RED}Error: Settings file not found: $SETTINGS_FILE${NC}"
        exit 1
    fi
}

# Create backup of current settings
backup_settings() {
    local timestamp=$(date +%Y%m%d_%H%M%S)
    local backup_file="$BACKUP_DIR/${BACKUP_PREFIX}_${timestamp}.json"
    
    log "${BLUE}Creating settings backup...${NC}"
    
    cp "$SETTINGS_FILE" "$backup_file"
    
    # Also create a human-readable backup with git info
    local info_file="$BACKUP_DIR/${BACKUP_PREFIX}_${timestamp}.info"
    {
        echo "=== Theme Settings Backup Info ==="
        echo "Date: $(date)"
        echo "Git Branch: $(git branch --show-current 2>/dev/null || echo 'unknown')"
        echo "Git Commit: $(git rev-parse HEAD 2>/dev/null || echo 'unknown')"
        echo "File Size: $(stat -f%z "$SETTINGS_FILE" 2>/dev/null || stat -c%s "$SETTINGS_FILE" 2>/dev/null || echo 'unknown')"
        echo "Settings Preview:"
        head -20 "$SETTINGS_FILE"
        echo "..."
    } > "$info_file"
    
    log "${GREEN}✓ Settings backed up to: $backup_file${NC}"
    log "${GREEN}✓ Info file created: $info_file${NC}"
}

# Restore settings from backup
restore_settings() {
    log "${BLUE}Available backups:${NC}"
    
    local backups=($(ls -t "$BACKUP_DIR"/${BACKUP_PREFIX}_*.json 2>/dev/null || true))
    
    if [ ${#backups[@]} -eq 0 ]; then
        log "${RED}No backups found in $BACKUP_DIR${NC}"
        exit 1
    fi
    
    # List available backups
    for i in "${!backups[@]}"; do
        local backup_file="${backups[$i]}"
        local timestamp=$(basename "$backup_file" .json | sed "s/${BACKUP_PREFIX}_//")
        local readable_date=$(date -j -f "%Y%m%d_%H%M%S" "$timestamp" "+%Y-%m-%d %H:%M:%S" 2>/dev/null || echo "$timestamp")
        log "$((i+1)). $readable_date - $(basename "$backup_file")"
    done
    
    # Get user choice
    echo -n "Select backup to restore (1-${#backups[@]}, or 'q' to quit): "
    read -r choice
    
    if [ "$choice" = "q" ] || [ "$choice" = "Q" ]; then
        log "${YELLOW}Restore cancelled${NC}"
        return
    fi
    
    if ! [[ "$choice" =~ ^[0-9]+$ ]] || [ "$choice" -lt 1 ] || [ "$choice" -gt ${#backups[@]} ]; then
        log "${RED}Invalid choice${NC}"
        exit 1
    fi
    
    local selected_backup="${backups[$((choice-1))]}"
    
    # Create backup of current settings before restoring
    log "${YELLOW}Creating backup of current settings before restore...${NC}"
    backup_settings
    
    # Restore the selected backup
    cp "$selected_backup" "$SETTINGS_FILE"
    
    log "${GREEN}✓ Settings restored from: $(basename "$selected_backup")${NC}"
    log "${YELLOW}⚠️ Remember to commit these changes if you want to keep them${NC}"
}

# Commit current settings
commit_settings() {
    log "${BLUE}Committing current theme settings...${NC}"
    
    # Check if there are changes
    if git diff --quiet "$SETTINGS_FILE"; then
        log "${YELLOW}No changes to commit in $SETTINGS_FILE${NC}"
        return
    fi
    
    # Show the diff
    log "${BLUE}Changes to be committed:${NC}"
    git diff "$SETTINGS_FILE" || true
    
    echo -n "Commit these settings changes? (y/N): "
    read -r confirm
    
    if [[ $confirm =~ ^[Yy]$ ]]; then
        # Create backup before committing
        backup_settings
        
        # Add and commit
        git add "$SETTINGS_FILE"
        git commit -m "Update theme settings: $(date '+%Y-%m-%d %H:%M:%S')"
        
        log "${GREEN}✓ Settings committed successfully${NC}"
    else
        log "${YELLOW}Commit cancelled${NC}"
    fi
}

# Show differences between current and last backup
show_diff() {
    log "${BLUE}Showing differences...${NC}"
    
    local latest_backup=$(ls -t "$BACKUP_DIR"/${BACKUP_PREFIX}_*.json 2>/dev/null | head -1)
    
    if [ -z "$latest_backup" ]; then
        log "${YELLOW}No backups found to compare with${NC}"
        return
    fi
    
    log "${BLUE}Comparing with latest backup: $(basename "$latest_backup")${NC}"
    
    # Use jq for prettier diff if available, otherwise use regular diff
    if command -v jq >/dev/null 2>&1; then
        log "${BLUE}Current settings (formatted):${NC}"
        jq '.' "$SETTINGS_FILE" 2>/dev/null || cat "$SETTINGS_FILE"
        
        log "${BLUE}Latest backup (formatted):${NC}"
        jq '.' "$latest_backup" 2>/dev/null || cat "$latest_backup"
        
        echo ""
        log "${BLUE}Raw diff:${NC}"
    fi
    
    diff "$latest_backup" "$SETTINGS_FILE" || true
}

# Watch for changes to settings file
watch_settings() {
    log "${BLUE}Watching $SETTINGS_FILE for changes...${NC}"
    log "${YELLOW}Press Ctrl+C to stop${NC}"
    
    # Get initial file modification time
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        local last_modified=$(stat -f %m "$SETTINGS_FILE")
    else
        # Linux
        local last_modified=$(stat -c %Y "$SETTINGS_FILE")
    fi
    
    while true; do
        sleep 2
        
        # Get current file modification time
        if [[ "$OSTYPE" == "darwin"* ]]; then
            local current_modified=$(stat -f %m "$SETTINGS_FILE")
        else
            local current_modified=$(stat -c %Y "$SETTINGS_FILE")
        fi
        
        if [ "$current_modified" != "$last_modified" ]; then
            log "${GREEN}✓ Settings file changed at $(date)${NC}"
            
            # Automatically create backup
            backup_settings
            
            # Show brief info about the change
            local file_size=$(wc -c < "$SETTINGS_FILE")
            log "${BLUE}New file size: $file_size bytes${NC}"
            
            last_modified=$current_modified
            
            # Ask if user wants to commit
            echo -n "Commit these changes now? (y/N): "
            read -t 10 -r auto_commit || auto_commit=""
            
            if [[ $auto_commit =~ ^[Yy]$ ]]; then
                commit_settings
            fi
        fi
    done
}

# Setup development workflow
setup_dev_workflow() {
    log "${BLUE}Setting up development workflow...${NC}"
    
    # Create backup of current settings
    backup_settings
    
    # Add git hook to prevent accidental overwrites
    local pre_pull_hook=".git/hooks/pre-push"
    
    if [ ! -f "$pre_pull_hook" ]; then
        cat > "$pre_pull_hook" << 'EOF'
#!/bin/bash
# Pre-push hook to backup theme settings
echo "🔄 Auto-backing up theme settings before push..."
if [ -f "scripts/manage-theme-settings.sh" ]; then
    ./scripts/manage-theme-settings.sh backup
fi
EOF
        chmod +x "$pre_pull_hook"
        log "${GREEN}✓ Created pre-push git hook${NC}"
    fi
    
    # Create .gitignore entry for settings backups
    if ! grep -q "backups/settings" .gitignore 2>/dev/null; then
        echo "" >> .gitignore
        echo "# Theme settings backups" >> .gitignore
        echo "backups/settings/" >> .gitignore
        log "${GREEN}✓ Added settings backups to .gitignore${NC}"
    fi
    
    log "${GREEN}✓ Development workflow setup complete${NC}"
    log "${YELLOW}Recommended workflow:${NC}"
    log "1. Make changes in Shopify theme editor"
    log "2. Run: ./scripts/manage-theme-settings.sh backup"
    log "3. Run: ./scripts/manage-theme-settings.sh commit"
    log "4. Continue development with confidence"
}

# Clean old backups
clean_backups() {
    log "${BLUE}Cleaning old backups...${NC}"
    
    # Keep only last 10 backups
    local backups=($(ls -t "$BACKUP_DIR"/${BACKUP_PREFIX}_*.json 2>/dev/null || true))
    local keep_count=10
    
    if [ ${#backups[@]} -le $keep_count ]; then
        log "${YELLOW}Only ${#backups[@]} backups found, nothing to clean${NC}"
        return
    fi
    
    log "${BLUE}Found ${#backups[@]} backups, keeping newest $keep_count${NC}"
    
    # Remove old backups
    for ((i=$keep_count; i<${#backups[@]}; i++)); do
        local backup_file="${backups[$i]}"
        local info_file="${backup_file%.json}.info"
        
        rm -f "$backup_file"
        rm -f "$info_file"
        
        log "${GREEN}✓ Removed old backup: $(basename "$backup_file")${NC}"
    done
}

# Main execution
main() {
    check_directory
    
    log "${BLUE}=== Theme Settings Management Script ===${NC}"
    log "Started: $(date)"
    log ""
    
    case "${1:-}" in
        backup)
            backup_settings
            ;;
        restore)
            restore_settings
            ;;
        commit)
            commit_settings
            ;;
        diff)
            show_diff
            ;;
        watch)
            watch_settings
            ;;
        setup)
            setup_dev_workflow
            ;;
        clean)
            clean_backups
            ;;
        *)
            log "Usage: $0 {backup|restore|commit|diff|watch|setup|clean}"
            log ""
            log "Commands:"
            log "  backup   - Create backup of current settings"
            log "  restore  - Restore settings from backup"
            log "  commit   - Commit current settings to git"
            log "  diff     - Show differences with latest backup"
            log "  watch    - Watch for settings changes and auto-backup"
            log "  setup    - Setup development workflow with git hooks"
            log "  clean    - Remove old backups (keep latest 10)"
            log ""
            log "Examples:"
            log "  $0 backup           # Before making changes"
            log "  $0 commit           # After making changes in theme editor"
            log "  $0 watch            # Monitor changes during development"
            log "  $0 restore          # If changes were lost"
            exit 1
            ;;
    esac
    
    log ""
    log "Completed: $(date)"
    log "Log file: $LOG_FILE"
}

main "$@" 