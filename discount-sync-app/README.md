# 🚀 Bathroom Trade Hub - Discount Sync App

Real-time synchronization between Shopify discount codes and theme template pricing displays.

## 📋 Current Status: Phase 1 Complete ✅

- ✅ **App Structure**: Node.js/Express server with Shopify App framework
- ✅ **Core Logic**: Python sync logic ported to Node.js
- ✅ **Basic Dashboard**: Admin interface ready for customization
- ⏳ **Next**: Authentication setup and webhook integration

## 🛠️ Setup Instructions

### 1. **Environment Configuration**

```bash
# Copy the environment template
cp env.example .env

# Edit .env with your settings
nano .env
```

### 2. **Required Environment Variables**

```env
# Get these from your Shopify Partner Dashboard
SHOPIFY_API_KEY=your_api_key_here
SHOPIFY_API_SECRET=your_api_secret_here
SHOPIFY_APP_URL=https://your-app-url.ngrok.io

# Your store details
SHOPIFY_STORE_URL=bathroomtradehub.myshopify.com
SHOPIFY_ACCESS_TOKEN=your_private_app_token

# App configuration
PORT=3000
NODE_ENV=development
```

### 3. **Install Dependencies & Start**

```bash
# Install packages
npm install

# Start development server
npm run dev
```

### 4. **Create Shopify App (Required)**

1. **Go to [Shopify Partner Dashboard](https://partners.shopify.com/)**
2. **Create new app** → Custom app
3. **App name**: "Bathroom Trade Hub Discount Sync"
4. **App URL**: `https://your-ngrok-url.ngrok.io`
5. **Allowed redirection URLs**: `https://your-ngrok-url.ngrok.io/api/auth/callback`

### 5. **Required Scopes**

```
read_discounts
write_discounts
read_products
read_themes
write_themes
```

### 6. **Webhook Endpoints (Phase 2)**

```
https://your-ngrok-url.ngrok.io/api/webhooks/discount-codes
```

## 🏗️ Architecture

```
├── server.js              # Main Express server
├── lib/
│   └── syncEngine.js      # Core sync logic (ported from Python)
├── env.example            # Environment template
└── README.md             # This file
```

## 📊 Features

### ✅ **Phase 1 - Complete**

- Basic Shopify app structure
- Admin dashboard interface
- Core sync engine (Python → Node.js)
- Manual sync trigger endpoint

### ⏳ **Phase 2 - Next**

- Webhook integration for real-time sync
- Authentication flow
- Enhanced dashboard with real data

### 🔮 **Phase 3 - Future**

- Template versioning & rollback
- Visual diff system
- Advanced error handling

## 🔧 API Endpoints

| Endpoint                       | Method | Description         |
| ------------------------------ | ------ | ------------------- |
| `/`                            | GET    | Main dashboard      |
| `/api/health`                  | GET    | Health check        |
| `/api/sync/manual`             | POST   | Trigger manual sync |
| `/api/webhooks/discount-codes` | POST   | Webhook handler     |

## 🚀 Quick Start

```bash
# 1. Start the app
npm run dev

# 2. Open dashboard
open http://localhost:3000

# 3. Install in your Shopify store
# (Follow authentication flow)
```

## 📝 Next Steps

1. **Get your Shopify Partner credentials**
2. **Set up ngrok for local development**
3. **Configure environment variables**
4. **Test the dashboard**
5. **Set up webhooks for real-time sync**

## 🆘 Need Help?

- **Shopify App Setup**: [Shopify App Development Docs](https://shopify.dev/docs/apps)
- **ngrok Setup**: [ngrok Getting Started](https://ngrok.com/docs/getting-started)
- **Partner Dashboard**: [partners.shopify.com](https://partners.shopify.com/)

---

**🎯 Goal**: Eliminate manual `python3 sync_discounts.py` runs with real-time automation!
