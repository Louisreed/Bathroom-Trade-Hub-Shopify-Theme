# Bathroom Trade Hub - Shopify Theme

A comprehensive e-commerce Shopify theme designed specifically for **Bathroom Trade Hub**, a Dorset-based bathroom supplies company serving trade professionals and DIY enthusiasts.

## 🏪 About

**Bathroom Trade Hub** is a specialized e-commerce platform offering:

- Wall panels and cladding solutions
- Bathroom fixtures and fittings
- Shower enclosures and trays
- Brassware and accessories
- Heating solutions
- Trade-focused pricing and accounts

**Live Site**: [bathroomtradehub.co.uk](https://bathroomtradehub.co.uk/)

## 🎨 Theme Features

### Core Functionality

- **Multi-language support** (EN, DE, ES, FR, IT, VI)
- **Responsive design** optimized for all devices
- **Trade account integration** with custom pricing
- **Advanced product filtering** and search
- **Real-time inventory management**
- **Newsletter popup** and email marketing integration
- **Age verification** system
- **Cookie banner** for GDPR compliance

### Specialized Components

- **Product bundles** for bulk ordering
- **Volume pricing** displays
- **Pickup availability** for local customers
- **Recently viewed** products
- **Product recommendations** engine
- **Gift wrapping** options
- **Mobile dock** for enhanced mobile UX

### Page Templates

- **Homepage** with hero slideshow
- **Product pages** with detailed specifications
- **Collection pages** with advanced filtering
- **Blog** for industry insights
- **Contact forms** and store locator
- **Trade account** signup and management
- **Multiple page layouts** for different content types

## 🚀 Getting Started

### Prerequisites

- [Shopify CLI](https://shopify.dev/docs/themes/tools/cli) (v3.44.1+)
- [Node.js](https://nodejs.org/) (recommended)
- Git
- A Shopify store with theme development access

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/Louisreed/Bathroom-Trade-Hub-Shopify-Theme.git
   cd Bathroom-Trade-Hub-Shopify-Theme
   ```

2. **Authenticate with Shopify CLI**

   ```bash
   shopify auth login
   ```

3. **Connect to your store**

   ```bash
   shopify theme dev --store=your-store-name.myshopify.com
   ```

4. **Start development server**
   ```bash
   shopify theme dev --store=ab97df-6
   ```

### Development URLs

- **Local Preview**: http://127.0.0.1:9292
- **Theme Editor**: Access via Shopify admin
- **Live Preview**: Available via Shopify admin

## 📁 Project Structure

```
Bathroom-Trade-Hub-Shopify-Theme/
├── assets/                 # CSS, JS, and static assets
│   ├── theme.css          # Main stylesheet
│   ├── theme.js           # Main JavaScript
│   └── ...
├── config/                 # Theme configuration
│   ├── settings_data.json # Theme settings
│   └── settings_schema.json
├── layout/                 # Layout templates
│   └── theme.liquid       # Main layout
├── locales/               # Translation files
│   ├── en.default.json    # English (default)
│   └── ...
├── sections/              # Theme sections
│   ├── header.liquid      # Site header
│   ├── footer.liquid      # Site footer
│   └── ...
├── snippets/              # Reusable code snippets
│   ├── product-card.liquid
│   └── ...
└── templates/             # Page templates
    ├── index.json         # Homepage
    ├── product.json       # Product pages
    └── ...
```

## 🛠️ Development

### Available Commands

```bash
# Start development server
shopify theme dev --store=ab97df-6

# Pull theme from store
shopify theme pull --store=ab97df-6

# Push theme to store
shopify theme push --store=ab97df-6

# Check theme for issues
shopify theme check
```

### Key Files to Modify

- **`assets/theme.css`** - Main stylesheet
- **`assets/theme.js`** - Main JavaScript functionality
- **`sections/header.liquid`** - Site navigation and header
- **`sections/footer.liquid`** - Site footer
- **`templates/index.json`** - Homepage layout
- **`templates/product.json`** - Product page layout

### Custom Features

#### Trade Account Integration

- Custom pricing display logic
- Account verification system
- Bulk order functionality

#### Product Specifications

- Detailed product attributes
- Technical specifications display
- Installation guidance

#### Local Delivery System

- Dorset postcode detection
- Free delivery calculations
- Pickup availability

## 🔧 Configuration

### Theme Settings

Access theme settings via:

1. Shopify Admin → Online Store → Themes
2. Click "Customize" on your theme
3. Navigate to "Theme settings"

### Environment Variables

Configure in `config/settings_data.json`:

- Store contact information
- Social media links
- Payment gateway settings
- Shipping configurations

## 📱 Mobile Optimization

This theme includes:

- **Mobile-first design** approach
- **Touch-friendly** navigation
- **Optimized images** for mobile
- **Mobile dock** for quick access
- **Responsive product galleries**

## 🌐 Multi-language Support

Supported languages:

- English (default)
- German (DE)
- Spanish (ES)
- French (FR)
- Italian (IT)
- Vietnamese (VI)

Translation files located in `/locales/`

## 🚢 Deployment

### To Development Store

```bash
shopify theme push --store=ab97df-6 --development
```

### To Production

```bash
shopify theme push --store=ab97df-6 --live
```

### Best Practices

1. Always test in development first
2. Backup current theme before deploying
3. Use version control for all changes
4. Test on multiple devices and browsers

## 🔍 SEO Features

- **Schema markup** for products
- **Meta tags** optimization
- **Social media** integration
- **Sitemap** generation
- **Canonical URLs**
- **Image alt tags**

## 🎯 Performance

- **Lazy loading** for images
- **Minified CSS/JS**
- **Optimized fonts**
- **Efficient liquid templating**
- **CDN integration**

## 🛡️ Security

- **HTTPS** enforcement
- **GDPR compliance**
- **Cookie consent**
- **Age verification**
- **Secure checkout**

## 📊 Analytics

Integrated with:

- Google Analytics
- Shopify Analytics
- Facebook Pixel
- Custom event tracking

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

This theme is proprietary software developed for Bathroom Trade Hub.

## 📞 Support

For technical support or questions:

- **Email**: enquiries@bathroomtradehub.co.uk
- **Phone**: 01305 608599
- **Address**: Weymouth, Dorset

## 🔗 Links

- **Live Site**: [bathroomtradehub.co.uk](https://bathroomtradehub.co.uk/)
- **Shopify Admin**: [Access via Shopify Partners](https://admin.shopify.com/store/ab97df-6)
- **GitHub Repository**: [Bathroom-Trade-Hub-Shopify-Theme](https://github.com/Louisreed/Bathroom-Trade-Hub-Shopify-Theme)

---

**Built with ❤️ for the Dorset trade community**
