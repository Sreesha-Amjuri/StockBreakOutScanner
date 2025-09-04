# StockBreak Pro - Railway Deployment Guide

## 🚀 Quick Deployment to Railway

### Prerequisites
1. Railway account (https://railway.app)
2. GitHub repository with your code
3. Environment variables ready

### Step 1: Create Railway Project

1. **Visit Railway**: Go to https://railway.app
2. **Create New Project**: Click "New Project"
3. **Choose "Deploy from GitHub repo"**
4. **Select your repository** containing StockBreak Pro

### Step 2: Configure Services

Railway will auto-detect the configuration from `nixpacks.toml` and `railway.json`.

### Step 3: Add Environment Variables

In Railway dashboard, add these environment variables:

#### Backend Environment Variables:
```
MONGO_URL=<MongoDB connection string from Railway MongoDB service>
DB_NAME=stockbreak-pro-production
EMERGENT_LLM_KEY=sk-emergent-0003d045d6b9f4eAb4
ENVIRONMENT=production
DEBUG=false
CORS_ORIGINS=<Your frontend URL when deployed>
```

#### Frontend Environment Variables:
```
REACT_APP_BACKEND_URL=<Your backend URL from Railway>
GENERATE_SOURCEMAP=false
NODE_ENV=production
```

### Step 4: Add MongoDB Service

1. In Railway dashboard, click **"Add Service"**
2. Select **"Database" → "MongoDB"**
3. Copy the connection string to `MONGO_URL` environment variable

### Step 5: Deploy

1. Railway will automatically deploy when you push to GitHub
2. Monitor the build process in Railway dashboard
3. Once deployed, you'll get URLs for your services

### Step 6: Configure Domain (Optional)

1. Go to your service in Railway dashboard
2. Click **"Settings" → "Domains"**
3. Add a custom domain or use the Railway-provided domain

## 🔧 Manual Deployment Commands

If you prefer manual deployment:

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login to Railway
railway login

# Initialize project
railway init

# Deploy
railway up
```

## 📋 Post-Deployment Checklist

- [ ] Backend API is accessible
- [ ] Frontend loads correctly
- [ ] MongoDB connection is working
- [ ] AI Chat functionality works
- [ ] Stock scanning works with 100 stocks
- [ ] Dark/Light theme toggle works
- [ ] All environment variables are set correctly

## 🔍 Troubleshooting

### Common Issues:

1. **Build Failures**: Check `nixpacks.toml` configuration
2. **Environment Variables**: Ensure all required variables are set
3. **Database Connection**: Verify MongoDB URL is correct
4. **CORS Issues**: Update `CORS_ORIGINS` with your frontend URL
5. **API Endpoints**: Ensure backend routes are accessible

### Monitoring:

- Use Railway dashboard logs to monitor application health
- Check both frontend and backend service logs
- Monitor MongoDB connection status

## 🎯 Production URLs

After deployment, you'll have:
- **Frontend**: `https://your-app-name.up.railway.app`
- **Backend API**: `https://your-backend.up.railway.app/api`
- **API Documentation**: `https://your-backend.up.railway.app/docs`

## 🔐 Security Notes

1. Never commit `.env` files with real keys
2. Use Railway's environment variable system
3. Enable HTTPS (Railway provides this by default)
4. Consider rate limiting for production use
5. Monitor API usage and costs

## 📈 Scaling

Railway auto-scales based on traffic. For high-traffic scenarios:
1. Monitor resource usage in Railway dashboard
2. Consider upgrading to Railway Pro for better performance
3. Implement caching strategies for stock data
4. Consider CDN for frontend assets

## 💰 Cost Estimation

Railway pricing (as of 2025):
- **Hobby Plan**: Free tier with limitations
- **Pro Plan**: $5/month per user with better resources
- **Usage-based**: Additional costs for high resource usage

Your StockBreak Pro app should run comfortably on the Pro plan.