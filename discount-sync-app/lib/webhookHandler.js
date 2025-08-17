const crypto = require('crypto');
const { DiscountSyncEngine } = require('./syncEngine');

class WebhookHandler {
  constructor(config, shopifyClient) {
    this.config = config;
    this.shopifyClient = shopifyClient;
    this.syncEngine = new DiscountSyncEngine(config);
    this.webhookSecret = config.webhookSecret || process.env.SHOPIFY_WEBHOOK_SECRET;
  }

  /**
   * Verify webhook authenticity using HMAC
   */
  verifyWebhook(body, signature) {
    if (!this.webhookSecret) {
      console.warn('⚠️  SHOPIFY_WEBHOOK_SECRET not set - webhook verification disabled');
      return true; // Allow in development
    }

    const expectedSignature = crypto
      .createHmac('sha256', this.webhookSecret)
      .update(body, 'utf8')
      .digest('base64');

    return crypto.timingSafeEqual(
      Buffer.from(signature),
      Buffer.from(expectedSignature)
    );
  }

  /**
   * Handle discount code webhook events
   */
  async handleDiscountWebhook(eventType, payload, headers) {
    try {
      console.log(`🔔 Received ${eventType} webhook for discount: ${payload.title || payload.id}`);
      
      // Verify webhook authenticity
      const signature = headers['x-shopify-hmac-sha256'];
      if (!this.verifyWebhook(JSON.stringify(payload), signature)) {
        throw new Error('Webhook verification failed');
      }

      // Log the event
      const logData = {
        timestamp: new Date().toISOString(),
        eventType,
        discountId: payload.id,
        discountTitle: payload.title,
        status: payload.status || 'unknown'
      };
      
      console.log('📊 Webhook Event:', logData);

      // Trigger automatic sync based on event type
      switch (eventType) {
        case 'discount_codes/create':
          console.log('✨ New discount created - triggering sync...');
          await this.triggerAutoSync('create', payload);
          break;
          
        case 'discount_codes/update':
          console.log('📝 Discount updated - triggering sync...');
          await this.triggerAutoSync('update', payload);
          break;
          
        case 'discount_codes/delete':
          console.log('🗑️  Discount deleted - triggering sync...');
          await this.triggerAutoSync('delete', payload);
          break;
          
        default:
          console.log(`ℹ️  Unhandled webhook type: ${eventType}`);
      }

      return {
        success: true,
        message: `Successfully processed ${eventType} webhook`,
        syncTriggered: true,
        timestamp: new Date().toISOString()
      };

    } catch (error) {
      console.error('❌ Webhook processing failed:', error.message);
      return {
        success: false,
        error: error.message,
        timestamp: new Date().toISOString()
      };
    }
  }

  /**
   * Trigger automatic sync after webhook event
   */
  async triggerAutoSync(eventType, discountData) {
    try {
      console.log(`🔄 Auto-sync triggered by ${eventType} event...`);
      
      // Add a small delay to ensure Shopify's data is consistent
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      // Perform the sync
      const syncResult = await this.syncEngine.syncDiscounts(this.shopifyClient);
      
      console.log('✅ Auto-sync completed:', {
        eventType,
        discountId: discountData.id,
        templatesUpdated: syncResult.templatesUpdated,
        backupPath: syncResult.backupPath
      });

      return syncResult;
      
    } catch (error) {
      console.error('❌ Auto-sync failed:', error.message);
      throw error;
    }
  }

  /**
   * Register webhooks with Shopify
   */
  async registerWebhooks(appUrl) {
    try {
      console.log('🔗 Registering webhooks with Shopify...');
      
      const webhooks = [
        {
          topic: 'discount_codes/create',
          address: `${appUrl}/api/webhooks/discount-create`,
          format: 'json'
        },
        {
          topic: 'discount_codes/update', 
          address: `${appUrl}/api/webhooks/discount-update`,
          format: 'json'
        },
        {
          topic: 'discount_codes/delete',
          address: `${appUrl}/api/webhooks/discount-delete`, 
          format: 'json'
        }
      ];

      const registeredWebhooks = [];
      
      for (const webhook of webhooks) {
        try {
          const mutation = `
            mutation webhookSubscriptionCreate($topic: WebhookSubscriptionTopic!, $webhookSubscription: WebhookSubscriptionInput!) {
              webhookSubscriptionCreate(topic: $topic, webhookSubscription: $webhookSubscription) {
                webhookSubscription {
                  id
                  callbackUrl
                  topic
                  format
                  createdAt
                }
                userErrors {
                  field
                  message
                }
              }
            }
          `;

          const response = await this.shopifyClient.request(mutation, {
            variables: {
              topic: webhook.topic.toUpperCase().replace('/', '_'),
              webhookSubscription: {
                callbackUrl: webhook.address,
                format: webhook.format.toUpperCase()
              }
            }
          });

          if (response.data.webhookSubscriptionCreate.userErrors.length > 0) {
            console.warn(`⚠️  Webhook registration warning for ${webhook.topic}:`, 
              response.data.webhookSubscriptionCreate.userErrors);
          } else {
            registeredWebhooks.push(response.data.webhookSubscriptionCreate.webhookSubscription);
            console.log(`✅ Registered webhook: ${webhook.topic}`);
          }
          
        } catch (error) {
          console.error(`❌ Failed to register ${webhook.topic}:`, error.message);
        }
      }

      console.log(`🎉 Webhook registration complete. Registered ${registeredWebhooks.length} webhooks.`);
      return registeredWebhooks;
      
    } catch (error) {
      console.error('❌ Webhook registration failed:', error.message);
      throw error;
    }
  }

  /**
   * List existing webhooks
   */
  async listWebhooks() {
    try {
      const query = `
        query webhookSubscriptions($first: Int!) {
          webhookSubscriptions(first: $first) {
            edges {
              node {
                id
                callbackUrl
                topic
                format
                createdAt
                updatedAt
              }
            }
          }
        }
      `;

      const response = await this.shopifyClient.request(query, {
        variables: { first: 50 }
      });

      return response.data.webhookSubscriptions.edges.map(edge => edge.node);
      
    } catch (error) {
      console.error('❌ Failed to list webhooks:', error.message);
      throw error;
    }
  }
}

module.exports = { WebhookHandler };
