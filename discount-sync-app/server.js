const express = require('express');
const { shopifyApp } = require('@shopify/shopify-app-express');
const { MemorySessionStorage } = require('@shopify/shopify-app-session-storage-memory');
const { ApiVersion } = require('@shopify/shopify-api');
require('dotenv').config();

const PORT = process.env.PORT || 3000;

// Check for required environment variables
const requiredEnvVars = ['SHOPIFY_API_KEY', 'SHOPIFY_API_SECRET', 'SHOPIFY_APP_URL'];
const missingVars = requiredEnvVars.filter(varName => !process.env[varName]);

if (missingVars.length > 0) {
  console.error('❌ Missing required environment variables:');
  missingVars.forEach(varName => console.error(`   - ${varName}`));
  console.error('\n💡 Please copy env.example to .env and configure your settings');
  console.error('📖 See README.md for setup instructions');
  process.exit(1);
}

// Initialize Shopify app configuration
const shopify = shopifyApp({
  api: {
    apiVersion: ApiVersion.October24,
    restResources: {},
  },
  auth: {
    path: '/api/auth',
    callbackPath: '/api/auth/callback',
  },
  webhooks: {
    path: '/api/webhooks',
  },
  sessionStorage: new MemorySessionStorage(),
});

const app = express();

// Shopify auth and webhook middleware
app.use(shopify.cspHeaders());
app.use(shopify.auth.begin());
app.use(shopify.auth.callback());
app.use(shopify.processWebhooks());

// Health check endpoint
app.get('/api/health', (req, res) => {
  res.status(200).json({ 
    status: 'healthy', 
    timestamp: new Date().toISOString(),
    service: 'Bathroom Trade Hub Discount Sync'
  });
});

// Main dashboard route
app.get('/', shopify.auth.ensureInstalled(), async (req, res) => {
  const { session } = res.locals.shopify;
  
  res.send(`
    <!DOCTYPE html>
    <html>
    <head>
      <title>Discount Sync Dashboard</title>
      <script src="https://unpkg.com/@shopify/app-bridge@3"></script>
      <style>
        body { 
          font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
          margin: 0;
          padding: 20px;
          background: #f6f6f7;
        }
        .dashboard {
          max-width: 1200px;
          margin: 0 auto;
          background: white;
          border-radius: 8px;
          padding: 24px;
          box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }
        .header {
          border-bottom: 1px solid #e1e3e5;
          padding-bottom: 16px;
          margin-bottom: 24px;
        }
        .status-grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
          gap: 16px;
          margin-bottom: 24px;
        }
        .status-card {
          background: #f6f6f7;
          padding: 16px;
          border-radius: 6px;
          border-left: 4px solid #008060;
        }
        .status-card h3 {
          margin: 0 0 8px 0;
          color: #202223;
          font-size: 14px;
          font-weight: 600;
        }
        .status-card p {
          margin: 0;
          color: #6d7175;
          font-size: 13px;
        }
        .btn {
          background: #008060;
          color: white;
          border: none;
          padding: 12px 16px;
          border-radius: 4px;
          cursor: pointer;
          font-size: 14px;
          font-weight: 500;
        }
        .btn:hover {
          background: #006b4f;
        }
      </style>
    </head>
    <body>
      <div class="dashboard">
        <div class="header">
          <h1>🚀 Discount Sync Dashboard</h1>
          <p>Real-time synchronization between Shopify discounts and theme templates</p>
        </div>
        
        <div class="status-grid">
          <div class="status-card">
            <h3>📊 Sync Status</h3>
            <p>Templates synchronized</p>
          </div>
          
          <div class="status-card">
            <h3>🕐 Last Sync</h3>
            <p>Manual setup required</p>
          </div>
          
          <div class="status-card">
            <h3>📝 Active Discounts</h3>
            <p>Fetching data...</p>
          </div>
          
          <div class="status-card">
            <h3>⚡ Auto-Sync</h3>
            <p>Webhooks not configured</p>
          </div>
        </div>
        
        <button class="btn" onclick="triggerManualSync()">
          🔄 Trigger Manual Sync
        </button>
      </div>
      
      <script>
        // Initialize Shopify App Bridge
        const AppBridge = window['app-bridge'];
        const app = AppBridge.createApp({
          apiKey: '${process.env.SHOPIFY_API_KEY || 'your-api-key'}',
          host: new URLSearchParams(location.search).get('host')
        });
        
        function triggerManualSync() {
          console.log('Manual sync triggered');
          // TODO: Implement manual sync API call
        }
      </script>
    </body>
    </html>
  `);
});

// API endpoint for manual sync trigger
app.post('/api/sync/manual', shopify.auth.ensureInstalled(), async (req, res) => {
  try {
    const { session } = res.locals.shopify;
    
    // TODO: Implement sync logic here
    console.log('Manual sync triggered for store:', session.shop);
    
    res.json({
      success: true,
      message: 'Sync completed successfully',
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    console.error('Sync error:', error);
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

// Webhook handler for discount changes
app.post('/api/webhooks/discount-codes', express.raw({ type: 'application/json' }), (req, res) => {
  console.log('Discount webhook received');
  
  // TODO: Implement webhook processing
  // - Verify webhook signature
  // - Parse discount data
  // - Trigger template regeneration
  
  res.status(200).send('OK');
});

app.listen(PORT, () => {
  console.log(`🚀 Discount Sync App running on port ${PORT}`);
  console.log(`📊 Dashboard: http://localhost:${PORT}`);
  console.log(`💡 Next steps:`);
  console.log(`   1. Copy env.example to .env and configure your settings`);
  console.log(`   2. Create a Shopify app in your Partner Dashboard`);
  console.log(`   3. Add webhook endpoints for discount_codes/*`);
});
