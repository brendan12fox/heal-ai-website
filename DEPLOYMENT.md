# HEAL-AI Deployment Guide

This guide covers multiple deployment options for the HEAL-AI FastAPI application.

## 🚨 Security Note

**Never commit your `.env` file or API keys to version control!** Use environment variables provided by your hosting platform.

## Prerequisites

1. **OpenAI API Key**: Required for the application to work
   - Get one at: https://platform.openai.com/api-keys
   - Set it as an environment variable: `OPENAI_API_KEY`

2. **GitHub Account**: For version control and some deployment platforms

## Deployment Options

### Option 1: Railway (Recommended - Easiest) ⭐

**Best for**: Quick deployment with minimal configuration  
**Pricing**: Free tier available, then pay-as-you-go (~$5-20/month)  
**Pros**: Very easy, auto-deploy from GitHub, free SSL, custom domains  
**Cons**: Can be more expensive at scale

#### Steps:

1. **Push code to GitHub**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/yourusername/heal-ai-website.git
   git push -u origin main
   ```

2. **Create Railway account**: https://railway.app

3. **New Project** → **Deploy from GitHub repo**

4. **Add environment variable**:
   - In Railway dashboard: Variables tab
   - Add: `OPENAI_API_KEY` = `your-key-here`

5. **Configure port** (if needed):
   - Add variable: `PORT` = `8502`
   - Railway will auto-detect FastAPI

6. **Deploy!** Railway will:
   - Auto-detect Python/Docker
   - Install dependencies
   - Run the app
   - Provide a public URL

**Your app will be live at**: `https://your-app-name.railway.app`

---

### Option 2: Render

**Best for**: Free tier with good features  
**Pricing**: Free tier available (with limitations), then $7+/month  
**Pros**: Free tier, easy setup, auto-deploy from GitHub  
**Cons**: Free tier sleeps after inactivity (slow first request)

#### Steps:

1. **Push code to GitHub** (same as Railway)

2. **Create Render account**: https://render.com

3. **New** → **Web Service** → **Connect GitHub**

4. **Configure service**:
   - **Name**: `heal-ai-website`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn fastapi_app:app --host 0.0.0.0 --port $PORT`
   - **Plan**: Free (or paid)

5. **Add environment variable**:
   - `OPENAI_API_KEY` = `your-key-here`

6. **Deploy!**

**Free tier URL format**: `https://heal-ai-website.onrender.com`

---

### Option 3: Fly.io

**Best for**: Full control, global edge deployment  
**Pricing**: Free tier (3 shared VMs), then pay-per-use  
**Pros**: Global edge network, Docker support, great performance  
**Cons**: Requires `flyctl` CLI setup

#### Steps:

1. **Install Fly CLI**:
   ```bash
   curl -L https://fly.io/install.sh | sh
   # Or: brew install flyctl (macOS)
   ```

2. **Login**:
   ```bash
   fly auth login
   ```

3. **Initialize Fly app**:
   ```bash
   fly launch
   ```
   - Choose app name
   - Choose region
   - Select Dockerfile

4. **Set secrets**:
   ```bash
   fly secrets set OPENAI_API_KEY=your-key-here
   ```

5. **Deploy**:
   ```bash
   fly deploy
   ```

6. **View logs**:
   ```bash
   fly logs
   ```

**Your app will be live at**: `https://your-app-name.fly.dev`

---

### Option 4: DigitalOcean App Platform

**Best for**: Managed platform with good scaling  
**Pricing**: $5+/month  
**Pros**: Easy scaling, managed databases available, good docs  
**Cons**: More expensive than alternatives

#### Steps:

1. **Create DigitalOcean account**: https://www.digitalocean.com

2. **App Platform** → **Create App** → **GitHub**

3. **Configure**:
   - Select repository
   - Auto-detect settings
   - Add environment variable: `OPENAI_API_KEY`
   - Choose plan ($5/month basic)

4. **Deploy!**

---

### Option 5: Docker + Any Cloud Provider

**Best for**: Maximum control and flexibility  
**Pricing**: Varies by provider  
**Pros**: Works anywhere, full control  
**Cons**: More setup required

#### Build Docker image:

```bash
# Build
docker build -t heal-ai-website .

# Run locally (test)
docker run -p 8502:8502 -e OPENAI_API_KEY=your-key heal-ai-website

# Push to registry (Docker Hub example)
docker tag heal-ai-website yourusername/heal-ai-website
docker push yourusername/heal-ai-website
```

#### Deploy to:
- **AWS ECS/Fargate**
- **Google Cloud Run** (recommended - easy)
- **Azure Container Instances**
- **Heroku** (using Docker)
- **Any VPS** (DigitalOcean, Linode, etc.) with Docker installed

---

### Option 6: Google Cloud Run (Recommended for Docker) ⭐

**Best for**: Serverless containers, pay-per-use  
**Pricing**: Free tier (2M requests/month), then pay-per-use  
**Pros**: Auto-scaling, pay only for use, global  
**Cons**: Cold starts on free tier

#### Steps:

1. **Install Google Cloud SDK**: https://cloud.google.com/sdk

2. **Enable Cloud Run API**:
   ```bash
   gcloud services enable run.googleapis.com
   ```

3. **Build and push**:
   ```bash
   # Set project
   gcloud config set project YOUR_PROJECT_ID
   
   # Build and push
   gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/heal-ai
   ```

4. **Deploy**:
   ```bash
   gcloud run deploy heal-ai \
     --image gcr.io/YOUR_PROJECT_ID/heal-ai \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated \
     --set-env-vars OPENAI_API_KEY=your-key-here \
     --port 8502
   ```

---

### Option 7: Heroku

**Best for**: Traditional PaaS, familiar platform  
**Pricing**: Free tier removed, now $5+/month  
**Pros**: Well-known, easy setup  
**Cons**: More expensive, limited free tier

#### Steps:

1. **Install Heroku CLI**: https://devcenter.heroku.com/articles/heroku-cli

2. **Create `Procfile`**:
   ```
   web: uvicorn fastapi_app:app --host 0.0.0.0 --port $PORT
   ```

3. **Login and create app**:
   ```bash
   heroku login
   heroku create your-app-name
   ```

4. **Set config**:
   ```bash
   heroku config:set OPENAI_API_KEY=your-key-here
   ```

5. **Deploy**:
   ```bash
   git push heroku main
   ```

---

## Quick Comparison

| Platform | Ease | Free Tier | Cost | Best For |
|----------|------|-----------|------|----------|
| **Railway** | ⭐⭐⭐⭐⭐ | Limited | $5-20/mo | Quickest setup |
| **Render** | ⭐⭐⭐⭐ | Yes | $7+/mo | Free tier users |
| **Fly.io** | ⭐⭐⭐ | Yes | Pay-per-use | Global edge |
| **Cloud Run** | ⭐⭐⭐ | Yes | Pay-per-use | Serverless |
| **DigitalOcean** | ⭐⭐⭐⭐ | No | $5+/mo | Scaling needs |
| **Heroku** | ⭐⭐⭐⭐ | No | $5+/mo | Traditional PaaS |

## Post-Deployment Checklist

- [ ] Test all endpoints work (`/`, `/resource-finder`, `/perioperative`)
- [ ] Test API calls (generate instructions, find resources)
- [ ] Test PDF generation
- [ ] Set up custom domain (optional)
- [ ] Enable HTTPS/SSL (usually automatic)
- [ ] Set up monitoring/logging (optional)
- [ ] Configure rate limiting (if needed)
- [ ] Set up backups (if using databases)

## Custom Domain Setup

Most platforms support custom domains:

1. **Add domain in platform dashboard**
2. **Update DNS records** (usually A record or CNAME)
3. **Enable SSL** (automatic with Let's Encrypt)

## Monitoring & Maintenance

- **Health checks**: Most platforms auto-detect FastAPI health
- **Logs**: Check platform dashboard for logs
- **Errors**: Monitor for OpenAI API errors, rate limits
- **Updates**: Push to GitHub to auto-deploy (if configured)

## Troubleshooting

### App won't start
- Check `OPENAI_API_KEY` is set correctly
- Check logs in platform dashboard
- Verify port is correct (8502 or $PORT)

### API errors
- Verify OpenAI API key is valid
- Check OpenAI API quotas/limits
- Review error logs

### PDF generation fails
- Ensure all dependencies installed (reportlab)
- Check file permissions in Docker container

## Security Best Practices

1. ✅ Never commit `.env` files
2. ✅ Use environment variables for secrets
3. ✅ Enable HTTPS (usually automatic)
4. ✅ Set up rate limiting (consider using middleware)
5. ✅ Monitor for suspicious activity
6. ✅ Keep dependencies updated

## Support

For issues:
- Check platform documentation
- Review application logs
- Test locally first: `./run_fastapi.sh`

---

**Recommended for most users**: Start with **Railway** or **Render** for easiest deployment.

