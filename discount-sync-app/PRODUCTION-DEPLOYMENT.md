# 🚀 Production Deployment Guide

## 🎯 **Deployment Options**

### Option 1: Railway (Recommended - Easiest)

**✅ Free tier available, automatic HTTPS, simple setup**

### Option 2: Heroku

**✅ Popular, reliable, good documentation**

### Option 3: DigitalOcean App Platform

**✅ Cost-effective, good performance**

### Option 4: Your Own Server (VPS)

**✅ Full control, potentially cheaper for long-term**

---

## 🚂 **Option 1: Railway (Recommended)**

### Step 1: Prepare Your App

```bash
# Create production package.json script
echo '  "start": "node server-quick.js",' >> package.json
```

### Step 2: Deploy to Railway

1. **Sign up**: https://railway.app
2. **Connect GitHub**: Link your GitHub account
3. **Create new project**: "Deploy from GitHub repo"
4. **Select your repo**: Choose your theme repository
5. **Set root directory**: `discount-sync-app`

### Step 3: Configure Environment Variables

In Railway dashboard, add these variables:

```
SHOPIFY_ACCESS_TOKEN=your_shopify_access_token_here
SHOPIFY_STORE_URL=ab97df-6.myshopify.com
THEME_PATH=../
TEMPLATE_FILES=snippets/hubpro-discount-simple.liquid,snippets/product-price.liquid
PORT=3000
```

### Step 4: Deploy

- Railway will automatically build and deploy
- You'll get a URL like: `https://your-app-name.up.railway.app`

---

## 🟣 **Option 2: Heroku**

### Step 1: Install Heroku CLI

```bash
# macOS
brew install heroku/brew/heroku

# Login
heroku login
```

### Step 2: Prepare Your App

```bash
# Create Procfile
echo "web: node server-quick.js" > Procfile

# Create .gitignore if needed
echo "node_modules/" > .gitignore
echo ".env" >> .gitignore
```

### Step 3: Deploy

```bash
# Initialize git (if not already)
git init
git add .
git commit -m "Initial commit"

# Create Heroku app
heroku create your-discount-sync-app

# Set environment variables
heroku config:set SHOPIFY_ACCESS_TOKEN=your_shopify_access_token_here
heroku config:set SHOPIFY_STORE_URL=ab97df-6.myshopify.com
heroku config:set THEME_PATH=../
heroku config:set TEMPLATE_FILES=snippets/hubpro-discount-simple.liquid,snippets/product-price.liquid

# Deploy
git push heroku main
```

---

## 🌊 **Option 3: DigitalOcean App Platform**

### Step 1: Create App

1. **Sign up**: https://cloud.digitalocean.com
2. **Create App**: Choose "GitHub" as source
3. **Select repository**: Your theme repo
4. **Set source directory**: `discount-sync-app`

### Step 2: Configure Build

```yaml
# app.yaml (DigitalOcean will detect automatically)
name: discount-sync-app
services:
  - name: web
    source_dir: discount-sync-app
    github:
      repo: your-username/your-repo-name
      branch: main
    run_command: node server-quick.js
    environment_slug: node-js
    instance_count: 1
    instance_size_slug: basic-xxs
    envs:
      - key: SHOPIFY_ACCESS_TOKEN
        value: your_shopify_access_token_here
      - key: SHOPIFY_STORE_URL
        value: ab97df-6.myshopify.com
      - key: THEME_PATH
        value: ../
      - key: TEMPLATE_FILES
        value: snippets/hubpro-discount-simple.liquid,snippets/product-price.liquid
```

---

## 🖥️ **Option 4: Your Own Server (VPS)**

### Requirements

- Ubuntu/CentOS server with SSH access
- Domain name (optional, can use IP)
- Basic server administration knowledge

### Step 1: Server Setup

```bash
# Install Node.js
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Install PM2 (process manager)
sudo npm install -g pm2

# Install Nginx (reverse proxy)
sudo apt install nginx
```

### Step 2: Deploy App

```bash
# Clone your repo
git clone https://github.com/your-username/your-repo.git
cd your-repo/discount-sync-app

# Install dependencies
npm install

# Create production .env
cat > .env << EOF
SHOPIFY_ACCESS_TOKEN=your_shopify_access_token_here
SHOPIFY_STORE_URL=ab97df-6.myshopify.com
THEME_PATH=../
TEMPLATE_FILES=snippets/hubpro-discount-simple.liquid,snippets/product-price.liquid
PORT=3000
EOF

# Start with PM2
pm2 start server-quick.js --name discount-sync
pm2 startup
pm2 save
```

### Step 3: Configure Nginx

```nginx
# /etc/nginx/sites-available/discount-sync
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/discount-sync /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

## 🔒 **Security & Production Considerations**

### Environment Variables

- **Never commit** `.env` files to git
- **Use platform environment variables** for production
- **Rotate access tokens** periodically

### SSL/HTTPS

- **Required for webhooks** (Shopify requirement)
- **Railway/Heroku**: Automatic HTTPS
- **DigitalOcean**: Automatic HTTPS
- **Own server**: Use Let's Encrypt (certbot)

### Monitoring

```bash
# Add to package.json
"scripts": {
  "start": "node server-quick.js",
  "dev": "nodemon server-quick.js",
  "logs": "pm2 logs discount-sync"
}
```

### Health Checks

Most platforms will automatically check `/api/health` endpoint.

---

## 🎯 **Recommended Setup for You**

**For Bathroom Trade Hub, I recommend Railway because:**

1. **✅ Easiest setup** - Just connect GitHub and deploy
2. **✅ Free tier** - Good for testing, $5/month for production
3. **✅ Automatic HTTPS** - Required for webhooks
4. **✅ GitHub integration** - Auto-deploy on code changes
5. **✅ Built-in monitoring** - Logs, metrics, health checks

### Quick Railway Setup:

1. **Sign up**: https://railway.app
2. **New Project** → **Deploy from GitHub**
3. **Add environment variables** (listed above)
4. **Deploy** → Get your production URL
5. **Test** → Visit `https://your-app.up.railway.app`

---

## 🔄 **After Deployment**

### Test Your Production App

1. **Visit your app URL**
2. **Test manual sync** - Should work exactly like local
3. **Check Shopify templates** - Verify they're updated
4. **Set up webhooks** (optional) - For real-time sync

### Update Your Workflow

- **Replace Python script** with production app URL
- **Bookmark dashboard** for easy access
- **Set up monitoring** alerts if needed

### Webhook Setup (Optional)

Once deployed, you can set up real-time webhooks:

1. **Visit your production dashboard**
2. **Click "Setup Webhooks"**
3. **Enter your production URL** (e.g., `https://your-app.up.railway.app`)
4. **Test by creating/updating discounts in Shopify**

---

## 💡 **Need Help?**

- **Railway issues**: Check their docs or Discord
- **Heroku issues**: Extensive documentation available
- **Server setup**: Consider managed hosting first
- **App bugs**: Check logs via platform dashboard

**Your app is production-ready!** 🚀
