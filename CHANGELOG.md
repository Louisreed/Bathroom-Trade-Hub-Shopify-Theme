# Changelog

All notable changes to the Bathroom Trade Hub Shopify Theme are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Overview

This changelog is organized into two main categories:

- **🚀 Development Changes**: Features, improvements, and fixes implemented by the development team
- **📦 Shopify Theme Updates**: Automated updates and synchronizations from Shopify

---

## 🚀 Development Changes

### [Latest] - 2025-07-20

#### Added

- **Dynamic Menu Item Tags**: Enhanced header section with dynamic menu item tagging functionality
- **VAT Switcher Enhancements**:
  - Added mobile VAT switcher row with responsive display control
  - Improved desktop VAT switcher positioning in header icons
  - Enhanced comments for better understanding of VAT switcher behavior
- **Text Transformation Utilities**: Added text transformation utility classes and margin settings to main-page section

#### Enhanced

- **Header Structure**: Major refactoring of header section for improved responsiveness and functionality
- **T-selector App Integration**:
  - Added T-selector app block to header section configuration
  - Implemented proper CSS positioning for T-selector app blocks
  - Fixed positioning by integrating with header icons
  - Resolved Shopify schema validation errors with duplicate link_list settings

### [2025-07-19]

#### Added

- **Page Color Customization**:
  - Introduced new color settings for text, background, and gradient background in main-page.liquid
  - Added section variables rendering for enhanced customization
  - Users can now customize page appearance directly from the Shopify theme editor

#### Enhanced

- **Theme Structure**: Major refactoring of theme.liquid and header.liquid for improved readability and maintainability

### [2025-07-18] - Major Feature Releases

#### Added

- **🎯 Comprehensive Test Suite for Deprecated Liquid Patterns**
  - Complete testing and conversion management system
  - **Files Created**:
    - `tests/deprecated-liquid-patterns-test.liquid` - Comprehensive test suite with side-by-side comparison and analysis
    - `tests/pre-conversion-validation.liquid` - Focused validation test to capture exact current behavior
    - `scripts/convert-deprecated-includes.sh` - Automated conversion script with backup/rollback functionality
    - `docs/deprecated-includes-conversion-guide.md` - Complete conversion guide with risk assessment
    - `README-TESTING-DEPRECATED-PATTERNS.md` - Quick start guide and workflow documentation
  - 1,727 lines of testing and documentation added

#### Enhanced

- **Product Handling Logic**: Major updates to support trade-focused functionality
  - High-variant product support for complex bathroom fixtures
  - Bulk ordering features for trade professionals
  - Enhanced trade account verification workflows
  - Improved user experience for trade customers

#### Added

- **Comprehensive Documentation**:
  - Added detailed README.md with project documentation (293 lines)
  - Setup instructions and development guide
  - Architecture and best practices documentation

#### Improved

- **Code Structure & Maintainability**:
  - Refactored and cleaned up various CSS and JavaScript files
  - Removed unused product-reviews assets
  - Updated Liquid templates and snippets for improved structure
  - Enhanced maintainability across the codebase

#### Localization

- **Multi-language Enhancements**:
  - Added translations for typography and font size in multiple languages
  - Updated footer Liquid templates for improved structure and styling
  - Enhanced localization files with proper URL escaping
  - Improved HTML escaping for text elements in index and page templates

### [Initial Release] - 2025-07-18

#### Added

- **Initial Theme Structure**: Complete Shopify theme foundation for Bathroom Trade Hub
  - Multi-language support (EN, DE, ES, FR, IT, VI, AR, CS, DA, and more)
  - Responsive design optimized for trade professionals and DIY enthusiasts
  - UK market-specific features (GBP currency, UK VAT, local pickup)
  - Trade account integration with wholesale pricing
  - Advanced product filtering and search capabilities
  - Real-time inventory management
  - Newsletter popup and email marketing integration
  - Age verification system
  - GDPR-compliant cookie banner

---

## 📦 Shopify Theme Updates

### Recent Automated Updates (2025-07-19 to 2025-07-20)

The following commits represent automated synchronizations from Shopify:

- `fc081f8` - Update from Shopify (2025-07-20)
- `6c4a209` - Update from Shopify (2025-07-20)
- `6223690` - Update from Shopify (2025-07-20)
- `1c3a247` - Update from Shopify (2025-07-20)
- `1674103` - Update from Shopify (2025-07-20)
- `00fde2d` - Update from Shopify (2025-07-20)
- `90b0cde` - Update from Shopify (2025-07-20)
- `bdc2ea7` - Update from Shopify (2025-07-20)
- `e8a40ff` - Update from Shopify (2025-07-20)
- `b03cf66` - Update from Shopify (2025-07-20)
- `da26a73` - Update from Shopify (2025-07-20)
- `28fada1` - Update from Shopify (2025-07-19)
- `620d241` - Update from Shopify (2025-07-19)
- `7190367` - Update from Shopify (2025-07-19)
- `9e266c1` - Update from Shopify (2025-07-19)
- `4aaf26a` - Update from Shopify (2025-07-19)
- `96d01f9` - Update from Shopify (2025-07-19)

### Previous Automated Updates (2025-07-18 to 2025-07-19)

- `05bb9fa` - Update from Shopify (2025-07-18)
- `c3ff4ee` - Update from Shopify (2025-07-18)
- `a2f8966` - Update from Shopify (2025-07-18)
- `57b9747` - Update from Shopify (2025-07-18)
- `c8ba082` - Update from Shopify (2025-07-18)
- `a036aac` - Update from Shopify (2025-07-18)
- `0d83978` - Update from Shopify (2025-07-18)
- `528794b` - Update from Shopify (2025-07-18)

### Historical Automated Updates

- `aba3e2f` - Update from Shopify
- `32490bf` - Update from Shopify
- `d606173` - Update from Shopify
- `c4ef73c` - Update from Shopify
- `aa654b1` - Update from Shopify
- `dbc1a2e` - Update from Shopify
- `b16c4a7` - Update from Shopify
- `3df9d03` - Update from Shopify
- `44f39a7` - Update from Shopify
- `4a5abf5` - Update from Shopify
- `e71c8e9` - Update from Shopify
- `e8aa60d` - Update from Shopify
- `ecb938f` - Update from Shopify
- `e6d1b6b` - Update from Shopify
- `a1c618d` - Update from Shopify
- `312894f` - Update from Shopify
- `3820381` - Update from Shopify
- `68c2917` - Update from Shopify
- `33e9ce9` - Update from Shopify (Theme sync)
- `5926853` - Update from Shopify (Theme sync)

---

## 🔧 Development Workflow Improvements

### Merge Conflict Resolutions

- `308ad5e` - Resolved conflicts in templates/index.json
- `da2f789` - Resolved URL escaping conflicts
- `74b2956` - Merged remote changes and resolved URL escaping conflicts
- `f1df08a` - Merged remote theme updates
- `4aaf26a` - Merged branch 'master' with remote updates

### Code Recovery & Maintenance

- `f9e0677` - Recovered test files lost during Shopify CLI pull
- `50dcdcf` - Restored comprehensive test suite content
- `8a91041` - Restored and fixed test suite and theme settings management
- `a53c597` - Resolved merge conflict and removed theme settings script

---

## 🎯 Key Features Summary

### Trade-Focused Functionality

- **Wholesale Pricing**: Custom pricing for trade accounts
- **Bulk Ordering**: Enhanced ordering interface for large quantities
- **Account Verification**: Streamlined trade account setup
- **UK Market Focus**: GBP currency, UK VAT, local Dorset pickup

### Technical Excellence

- **Performance Optimized**: Lazy loading, CDN optimization, minified assets
- **Accessibility**: WCAG 2.1 AA compliance
- **Multi-language**: Support for 20+ languages
- **Mobile-First**: Responsive design with mobile dock

### Developer Tools

- **Testing Suite**: Comprehensive liquid pattern testing
- **Documentation**: Detailed setup and development guides
- **Conversion Scripts**: Automated deprecated pattern conversion
- **Version Control**: Proper git workflow with clear commit history

---

## 🚀 What's Next

### Planned Features

- Enhanced trade account dashboard
- Advanced inventory management
- Extended payment gateway integrations
- Performance optimization phase 2

### Theme Maintenance

- Regular Shopify compatibility updates
- Continued code refactoring for maintainability
- Translation updates and new language support
- Security and performance monitoring

---

**Live Site**: [bathroomtradehub.co.uk](https://bathroomtradehub.co.uk/)  
**Repository**: Private Development Repository  
**Theme Version**: 4.3.0+ (Latest Shopify Standards)
