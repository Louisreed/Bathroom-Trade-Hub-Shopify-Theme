const express = require('express');
const { createAdminApiClient } = require('@shopify/admin-api-client');
const { DiscountSyncEngine } = require('./lib/syncEngine');
const { WebhookHandler } = require('./lib/webhookHandler');
require('dotenv').config();

const PORT = process.env.PORT || 3000;
const STORE_URL = process.env.SHOPIFY_STORE_URL || 'ab97df-6.myshopify.com';

// Initialize Express app
const app = express();
app.use(express.json());

// Initialize Shopify Admin API client for private app
let shopifyClient = null;

if (process.env.SHOPIFY_ACCESS_TOKEN) {
  shopifyClient = createAdminApiClient({
    storeDomain: STORE_URL,
    accessToken: process.env.SHOPIFY_ACCESS_TOKEN,
    apiVersion: '2024-10',
  });
  console.log('✅ Shopify API client initialized');
} else {
  console.warn('⚠️  SHOPIFY_ACCESS_TOKEN not set - sync functionality disabled');
}

// Initialize sync engine
const syncEngine = new DiscountSyncEngine({
  themePath: process.env.THEME_PATH || '../',
  templateFiles: (process.env.TEMPLATE_FILES || '').split(',').filter(Boolean)
});

// Initialize webhook handler
const webhookHandler = shopifyClient ? new WebhookHandler({
  themePath: process.env.THEME_PATH || '../',
  templateFiles: (process.env.TEMPLATE_FILES || '').split(',').filter(Boolean),
  webhookSecret: process.env.SHOPIFY_WEBHOOK_SECRET
}, shopifyClient) : null;

// Health check endpoint
app.get('/api/health', (req, res) => {
  res.status(200).json({ 
    status: 'healthy', 
    timestamp: new Date().toISOString(),
    service: 'Bathroom Trade Hub Discount Sync (Private App)',
    store: STORE_URL,
    apiConnected: !!shopifyClient
  });
});

// Main dashboard route
app.get('/', async (req, res) => {
  let discountCount = 'Unknown';
  let lastSyncStatus = 'Not configured';
  
  // Try to fetch discount count if API is available
  if (shopifyClient) {
    try {
      const response = await shopifyClient.request(`
        query {
          codeDiscountNodes(first: 5) {
            edges {
              node {
                codeDiscount {
                  ... on DiscountCodeBasic {
                    title
                    status
                  }
                }
              }
            }
          }
        }
      `);
      
      discountCount = response.data.codeDiscountNodes.edges.length + '+';
      lastSyncStatus = 'API Connected ✅';
    } catch (error) {
      console.error('API test failed:', error.message);
      lastSyncStatus = 'API Error ❌';
    }
  }
  
  res.send(`
    <!DOCTYPE html>
    <html>
    <head>
      <title>Discount Sync Dashboard - Private App</title>
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
          margin-right: 12px;
        }
        .btn:hover {
          background: #006b4f;
        }
        .btn-secondary {
          background: #6d7175;
        }
        .btn-secondary:hover {
          background: #5c5f62;
        }
        .btn-webhook {
          background: #1f4788;
        }
        .btn-webhook:hover {
          background: #1a3a6b;
        }
        .setup-notice {
          background: #fff9c4;
          border: 1px solid #f0d000;
          border-radius: 6px;
          padding: 16px;
          margin-bottom: 24px;
        }
        .setup-notice h3 {
          margin: 0 0 8px 0;
          color: #9c6500;
        }
        .setup-notice p {
          margin: 0;
          color: #9c6500;
          font-size: 14px;
        }
      </style>
    </head>
    <body>
      <div class="dashboard">
        <div class="header">
          <h1>🔒 Private App Dashboard</h1>
          <p>Real-time discount synchronization for <strong>${STORE_URL}</strong></p>
        </div>
        
        ${!shopifyClient ? `
        <div class="setup-notice">
          <h3>⚠️ Setup Required</h3>
          <p>Please create a private app in your Shopify admin and add the access token to your environment.</p>
        </div>
        ` : ''}
        
        <div class="status-grid">
          <div class="status-card">
            <h3>🏪 Store</h3>
            <p>${STORE_URL}</p>
          </div>
          
          <div class="status-card">
            <h3>📊 API Status</h3>
            <p>${lastSyncStatus}</p>
          </div>
          
          <div class="status-card">
            <h3>📝 Active Discounts</h3>
            <p>${discountCount}</p>
          </div>
          
          <div class="status-card">
            <h3>⚡ Sync Mode</h3>
            <p>Private App</p>
          </div>
        </div>
        
        <button class="btn" onclick="triggerManualSync()" ${!shopifyClient ? 'disabled' : ''}>
          🔄 Trigger Manual Sync
        </button>
        
        <button class="btn btn-secondary" onclick="testConnection()">
          🔍 Test API Connection
        </button>
        
        <button class="btn btn-webhook" onclick="registerWebhooks()" ${!shopifyClient ? 'disabled' : ''}>
          🔗 Setup Real-time Webhooks
        </button>
        
        <button class="btn btn-secondary" onclick="listWebhooks()" ${!shopifyClient ? 'disabled' : ''}>
          📋 List Active Webhooks
        </button>
      </div>
      
      <script>
        async function triggerManualSync() {
          const btn = event.target;
          btn.disabled = true;
          btn.textContent = '🔄 Syncing...';
          
          try {
            const response = await fetch('/api/sync/manual', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' }
            });
            
            const result = await response.json();
            
            if (result.success) {
              alert('✅ Sync completed successfully!\\n\\nTemplates updated: ' + result.templatesUpdated);
            } else {
              alert('❌ Sync failed: ' + result.error);
            }
          } catch (error) {
            alert('❌ Sync failed: ' + error.message);
          } finally {
            btn.disabled = false;
            btn.textContent = '🔄 Trigger Manual Sync';
          }
        }
        
        async function testConnection() {
          try {
            const response = await fetch('/api/test-connection');
            const result = await response.json();
            
            alert('API Test Result:\\n\\n' + JSON.stringify(result, null, 2));
          } catch (error) {
            alert('❌ Connection test failed: ' + error.message);
          }
        }
        
        async function registerWebhooks() {
          const btn = event.target;
          btn.disabled = true;
          btn.textContent = '🔗 Registering...';
          
          try {
            // Prompt for app URL (for webhook endpoints)
            const appUrl = prompt('Enter your app URL (e.g., https://abc123.ngrok.io):', 'https://your-app-url.ngrok.io');
            
            if (!appUrl) {
              btn.disabled = false;
              btn.textContent = '🔗 Setup Real-time Webhooks';
              return;
            }
            
            const response = await fetch('/api/webhooks/register', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({ appUrl })
            });
            
            const result = await response.json();
            
            if (result.success) {
              alert('✅ Webhooks registered successfully!\\n\\n' + result.message + '\\n\\nYour discount sync is now REAL-TIME! 🚀');
            } else {
              alert('❌ Webhook registration failed: ' + result.error);
            }
          } catch (error) {
            alert('❌ Webhook registration failed: ' + error.message);
          } finally {
            btn.disabled = false;
            btn.textContent = '🔗 Setup Real-time Webhooks';
          }
        }
        
        async function listWebhooks() {
          try {
            const response = await fetch('/api/webhooks/list');
            const result = await response.json();
            
            if (result.webhooks && result.webhooks.length > 0) {
              const webhookList = result.webhooks.map(w => 
                `• ${w.topic}: ${w.callbackUrl}\\n  Status: ${w.format} (${w.createdAt})`
              ).join('\\n\\n');
              
              alert('📋 Active Webhooks:\\n\\n' + webhookList);
            } else {
              alert('📋 No active webhooks found.\\n\\nClick "Setup Real-time Webhooks" to enable automatic sync.');
            }
          } catch (error) {
            alert('❌ Failed to list webhooks: ' + error.message);
          }
        }
      </script>
    </body>
    </html>
  `);
});

// API endpoint for manual sync trigger
app.post('/api/sync/manual', async (req, res) => {
  if (!shopifyClient) {
    return res.status(400).json({
      success: false,
      error: 'Shopify API client not configured. Please set SHOPIFY_ACCESS_TOKEN.'
    });
  }

  try {
    console.log('🔄 Manual sync triggered...');
    
    // Create backup before sync
    const backupPath = await syncEngine.createBackup();
    console.log('📦 Backup created:', backupPath);
    
    // Perform sync
    const result = await syncEngine.syncDiscounts(shopifyClient);
    
    res.json({
      success: true,
      message: 'Sync completed successfully',
      ...result,
      backupPath
    });
    
  } catch (error) {
    console.error('❌ Sync failed:', error);
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

// API connection test endpoint
app.get('/api/test-connection', async (req, res) => {
  if (!shopifyClient) {
    return res.status(400).json({
      success: false,
      error: 'API client not configured'
    });
  }

  try {
    const response = await shopifyClient.request(`
      query {
        shop {
          name
          myshopifyDomain
          plan {
            displayName
          }
        }
        codeDiscountNodes(first: 3) {
          edges {
            node {
              codeDiscount {
                ... on DiscountCodeBasic {
                  title
                  status
                  codes(first: 1) {
                    edges {
                      node {
                        code
                      }
                    }
                  }
                }
              }
            }
          }
        }
      }
    `);

    res.json({
      success: true,
      shop: response.data.shop,
      sampleDiscounts: response.data.codeDiscountNodes.edges.map(edge => ({
        title: edge.node.codeDiscount.title,
        status: edge.node.codeDiscount.status,
        code: edge.node.codeDiscount.codes.edges[0]?.node.code
      }))
    });

  } catch (error) {
    console.error('Connection test failed:', error);
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

// Webhook endpoints for real-time sync
app.post('/api/webhooks/discount-create', express.raw({type: 'application/json'}), async (req, res) => {
  if (!webhookHandler) {
    return res.status(400).json({ error: 'Webhook handler not configured' });
  }

  try {
    const result = await webhookHandler.handleDiscountWebhook(
      'discount_codes/create', 
      JSON.parse(req.body), 
      req.headers
    );
    res.json(result);
  } catch (error) {
    console.error('Webhook error:', error);
    res.status(500).json({ error: error.message });
  }
});

app.post('/api/webhooks/discount-update', express.raw({type: 'application/json'}), async (req, res) => {
  if (!webhookHandler) {
    return res.status(400).json({ error: 'Webhook handler not configured' });
  }

  try {
    const result = await webhookHandler.handleDiscountWebhook(
      'discount_codes/update', 
      JSON.parse(req.body), 
      req.headers
    );
    res.json(result);
  } catch (error) {
    console.error('Webhook error:', error);
    res.status(500).json({ error: error.message });
  }
});

app.post('/api/webhooks/discount-delete', express.raw({type: 'application/json'}), async (req, res) => {
  if (!webhookHandler) {
    return res.status(400).json({ error: 'Webhook handler not configured' });
  }

  try {
    const result = await webhookHandler.handleDiscountWebhook(
      'discount_codes/delete', 
      JSON.parse(req.body), 
      req.headers
    );
    res.json(result);
  } catch (error) {
    console.error('Webhook error:', error);
    res.status(500).json({ error: error.message });
  }
});

// Webhook management endpoints
app.post('/api/webhooks/register', async (req, res) => {
  if (!webhookHandler) {
    return res.status(400).json({ error: 'Webhook handler not configured' });
  }

  try {
    const appUrl = req.body.appUrl || process.env.SHOPIFY_APP_URL || 'https://your-app-url.ngrok.io';
    const webhooks = await webhookHandler.registerWebhooks(appUrl);
    
    res.json({
      success: true,
      message: `Registered ${webhooks.length} webhooks`,
      webhooks
    });
  } catch (error) {
    console.error('Webhook registration error:', error);
    res.status(500).json({ error: error.message });
  }
});

app.get('/api/webhooks/list', async (req, res) => {
  if (!webhookHandler) {
    return res.status(400).json({ error: 'Webhook handler not configured' });
  }

  try {
    const webhooks = await webhookHandler.listWebhooks();
    res.json({ webhooks });
  } catch (error) {
    console.error('Webhook list error:', error);
    res.status(500).json({ error: error.message });
  }
});

app.listen(PORT, () => {
  console.log(`🚀 Private App Dashboard running on port ${PORT}`);
  console.log(`📊 Dashboard: http://localhost:${PORT}`);
  console.log(`🏪 Store: ${STORE_URL}`);
  
  if (!process.env.SHOPIFY_ACCESS_TOKEN) {
    console.log(`\n⚠️  SETUP REQUIRED:`);
    console.log(`   1. Go to ${STORE_URL}/admin/settings/apps`);
    console.log(`   2. Create a private app with these scopes:`);
    console.log(`      - read_discounts, write_discounts`);
    console.log(`      - read_products, read_themes, write_themes`);
    console.log(`   3. Copy the Admin API access token`);
    console.log(`   4. Set SHOPIFY_ACCESS_TOKEN in your environment`);
  } else {
    console.log(`\n✅ Ready to sync! Visit the dashboard to test.`);
  }
});
