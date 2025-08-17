# 🔗 Phase 2: Real-time Webhooks Setup

## 🎯 **What This Enables**

Transform your discount sync from **manual** → **fully automatic**:

- ✅ **Create discount in Shopify** → Templates update instantly
- ✅ **Update discount percentage** → Templates sync automatically
- ✅ **Delete discount** → Templates clean up instantly
- ✅ **Zero manual work** → Set it and forget it!

## 📋 **Setup Requirements**

### 1. **Public URL for Webhooks**

Your app needs to be accessible from the internet for Shopify to send webhooks.

**Option A: ngrok (Recommended for testing)**

```bash
# Install ngrok: https://ngrok.com/download
brew install ngrok

# Start tunnel (in a separate terminal)
ngrok http 3000

# Copy the https URL (e.g., https://abc123.ngrok.io)
```

**Option B: Deploy to cloud service**

- Heroku, Railway, DigitalOcean, etc.
- Must have HTTPS (required by Shopify)

### 2. **Webhook Secret (Optional but Recommended)**

```bash
# Add to your .env file for security
echo "SHOPIFY_WEBHOOK_SECRET=your_random_secret_here" >> .env
```

## 🚀 **Setup Steps**

### Step 1: Start Your App

```bash
cd discount-sync-app
npm run dev
```

### Step 2: Make App Publicly Accessible

```bash
# In another terminal
ngrok http 3000
# Copy the HTTPS URL shown (e.g., https://abc123.ngrok.io)
```

### Step 3: Register Webhooks

1. **Open dashboard**: http://localhost:3000
2. **Click**: "🔗 Setup Real-time Webhooks"
3. **Enter your public URL**: `https://abc123.ngrok.io`
4. **Confirm registration**

### Step 4: Test Real-time Sync

1. **Go to Shopify Admin**: https://ab97df-6.myshopify.com/admin/discounts
2. **Create a new discount** (any type)
3. **Watch your app logs** - you should see:
   ```
   🔔 Received discount_codes/create webhook for discount: TEST_DISCOUNT
   🔄 Auto-sync triggered by create event...
   ✅ Auto-sync completed
   ```
4. **Check your theme files** - templates should be updated!

## 🔧 **Webhook Endpoints**

Your app will register these webhook URLs:

- `POST /api/webhooks/discount-create` - New discounts
- `POST /api/webhooks/discount-update` - Modified discounts
- `POST /api/webhooks/discount-delete` - Removed discounts

## 📊 **Monitoring**

### View Webhook Status

- **Dashboard button**: "📋 List Active Webhooks"
- **API endpoint**: `GET /api/webhooks/list`

### Debug Webhook Events

Watch your app console for real-time webhook events:

```bash
# In your app terminal
npm run dev

# You'll see webhook events like:
🔔 Received discount_codes/create webhook for discount: SUMMER20
✨ New discount created - triggering sync...
🔄 Auto-sync triggered by create event...
✅ Auto-sync completed: { templatesUpdated: 2, backupPath: './backups/...' }
```

## 🛡️ **Security Features**

- **HMAC Verification**: Validates webhooks are from Shopify
- **Error Handling**: Graceful failures with detailed logging
- **Backup Creation**: Automatic backups before each sync
- **Rate Limiting**: Built-in delays to prevent API overload

## 🎯 **Success Criteria**

You'll know it's working when:

1. ✅ **Webhook registration succeeds** (3 webhooks registered)
2. ✅ **Create discount in Shopify** → App logs show webhook received
3. ✅ **Templates update automatically** → No manual sync needed
4. ✅ **Update/delete discounts** → Templates sync instantly

## 🚨 **Troubleshooting**

### Webhook Not Received

- ✅ Check ngrok is running and URL is correct
- ✅ Verify app is accessible: `curl https://your-ngrok-url.ngrok.io/api/health`
- ✅ Check Shopify webhook logs in admin

### Sync Fails

- ✅ Check app logs for error details
- ✅ Verify API permissions in Shopify private app
- ✅ Test manual sync first to isolate issue

### HMAC Verification Fails

- ✅ Set `SHOPIFY_WEBHOOK_SECRET` in environment
- ✅ Or remove secret for testing (less secure)

## 🎉 **Phase 2 Complete!**

Once webhooks are working, your discount sync is **fully automated**:

**Before**: Manual Python script every time discounts change
**After**: Real-time automatic sync on every discount change

**Next**: Phase 3 could add advanced features like:

- Visual diff previews
- Rollback capabilities
- Bulk operations
- Admin notifications
- Performance monitoring
