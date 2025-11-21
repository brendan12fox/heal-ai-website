# Quick Deployment Guide

## 🚀 Fastest Way to Deploy (Railway - 5 minutes)

1. **Push to GitHub**:
   ```bash
   git init
   git add .
   git commit -m "Ready for deployment"
   git remote add origin https://github.com/yourusername/heal-ai-website.git
   git push -u origin main
   ```

2. **Go to Railway**: https://railway.app → Sign up with GitHub

3. **New Project** → **Deploy from GitHub repo** → Select your repo

4. **Add Environment Variable**:
   - Click on your service → **Variables**
   - Add: `OPENAI_API_KEY` = `your-actual-openai-key`

5. **Deploy!** Railway auto-detects everything. Your app will be live in ~2 minutes.

**Done!** Your app is live at: `https://your-app-name.railway.app`

---

## 🔄 Alternative: Render (Free tier available)

1. Go to: https://render.com
2. **New** → **Web Service** → Connect GitHub
3. Configure:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn fastapi_app:app --host 0.0.0.0 --port $PORT`
4. Add environment variable: `OPENAI_API_KEY`
5. Deploy!

---

## 📋 Pre-Deployment Checklist

- [ ] Code pushed to GitHub
- [ ] `.env` file NOT in git (check `.gitignore`)
- [ ] `OPENAI_API_KEY` ready to add as environment variable
- [ ] Tested locally: `./run_fastapi.sh`

---

## 🐳 Docker Deployment

If you want to use Docker:

```bash
# Build
docker build -t heal-ai-website .

# Test locally
docker run -p 8502:8502 -e OPENAI_API_KEY=your-key heal-ai-website

# Push to registry (example: Docker Hub)
docker tag heal-ai-website yourusername/heal-ai-website
docker login
docker push yourusername/heal-ai-website
```

Then deploy to any platform that supports Docker (Railway, Fly.io, Google Cloud Run, etc.)

---

## 📚 Full Deployment Guide

See `DEPLOYMENT.md` for detailed instructions on:
- Railway, Render, Fly.io, DigitalOcean, Google Cloud Run, Heroku
- Custom domain setup
- Monitoring and maintenance
- Troubleshooting

---

**Need help?** Check the logs in your platform's dashboard for errors.

