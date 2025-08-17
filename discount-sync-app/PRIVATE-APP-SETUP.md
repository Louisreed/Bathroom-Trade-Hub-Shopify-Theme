# 🔒 Private App Setup Guide

## 📋 Step 1: Create Private App in Shopify

1. **Go to your Shopify Admin**:

   ```
   https://ab97df-6.myshopify.com/admin/settings/apps
   ```

2. **Click "Develop apps"** (bottom of the page)

3. **Click "Create an app"**

   - **App name**: `Bathroom Trade Hub Discount Sync`
   - **App developer**: Your name/company

4. **Configure Admin API access**:

   - Click "Configure Admin API scopes"
   - **Enable these scopes**:
     - ✅ `read_discounts` - Read discount codes
     - ✅ `write_discounts` - Create/update discount codes
     - ✅ `read_products` - Read products and collections
     - ✅ `read_themes` - Read theme files
     - ✅ `write_themes` - Write theme files

5. **Install the app**:
   - Click "Install app"
   - **Copy the Admin API access token** (you'll need this!)

## 📋 Step 2: Configure Environment

1. **Create `.env` file**:

   ```bash
   cd discount-sync-app
   cp env.example .env
   ```

2. **Edit `.env` with your token**:

   ```env
   # Replace 'your_token_here' with your actual token
   SHOPIFY_STORE_URL=ab97df-6.myshopify.com
   SHOPIFY_ACCESS_TOKEN=shpat_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

   # These are not needed for private apps
   SHOPIFY_API_KEY=not_required_for_private_app
   SHOPIFY_API_SECRET=not_required_for_private_app
   SHOPIFY_APP_URL=http://localhost:3000

   PORT=3000
   NODE_ENV=development
   THEME_PATH=../
   ```

## 📋 Step 3: Test the App

1. **Start the app**:

   ```bash
   npm run dev
   ```

2. **Open dashboard**:

   ```
   http://localhost:3000
   ```

3. **Test API connection**:

   - Click "🔍 Test API Connection"
   - Should show your store info and sample discounts

4. **Test manual sync**:
   - Click "🔄 Trigger Manual Sync"
   - Check that templates are updated in `../snippets/`

## ✅ Expected Results

### Dashboard Should Show:

- ✅ **Store**: ab97df-6.myshopify.com
- ✅ **API Status**: API Connected ✅
- ✅ **Active Discounts**: [number]+
- ✅ **Sync Mode**: Private App

### After Manual Sync:

- ✅ Template files updated in theme
- ✅ Backup created in `../backups/`
- ✅ Success message with details

## 🔧 Troubleshooting

### "API Error ❌"

- Check your access token is correct
- Verify scopes are enabled
- Make sure app is installed

### "Sync Failed"

- Check file permissions in theme directory
- Verify theme path is correct (`../`)
- Look at console logs for details

### "No Discounts Found"

- Create some discount codes in Shopify Admin
- Make sure they're active
- Check discount titles match expected patterns

## 🚀 Next Steps

Once working:

1. **Set up webhooks** for real-time sync (Phase 2)
2. **Add template versioning** (Phase 3)
3. **Deploy to production** server

---

**🎯 Goal**: Replace manual `python3 sync_discounts.py` with automated sync!
