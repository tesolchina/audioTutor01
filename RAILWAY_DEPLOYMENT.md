# 🚂 Railway Deployment Guide for audioTutor01

## Step-by-Step Railway Deployment

### 1. Prerequisites
- GitHub account with audioTutor01 repository
- Railway account (free tier available)
- Google Cloud credentials JSON file
- HKBU GenAI API key

### 2. Prepare Your Repository

Ensure your repository contains these files:
- `requirements.txt` ✅
- `main.py` ✅ 
- `Procfile` ✅
- `railway.json` ✅
- `.env.example` ✅

### 3. Deploy to Railway

#### Option A: GitHub Integration (Recommended)

1. **Visit Railway**
   - Go to [railway.app](https://railway.app)
   - Sign up/Login with GitHub

2. **Create New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose `tesolchina/audioTutor01`

3. **Configure Environment Variables**
   ```
   GOOGLE_APPLICATION_CREDENTIALS=/app/google-credentials.json
   HKBU_API_KEY=your_actual_hkbu_api_key
   PORT=5000
   FLASK_ENV=production
   ```

4. **Upload Google Credentials**
   - In Railway dashboard, go to "Files"
   - Upload your Google Cloud credentials JSON file
   - Name it `google-credentials.json`
   - Place it in `/app/` directory

#### Option B: Railway CLI

1. **Install Railway CLI**
   ```bash
   npm install -g @railway/cli
   ```

2. **Login to Railway**
   ```bash
   railway login
   ```

3. **Initialize Project**
   ```bash
   cd audioTutor01
   railway init
   ```

4. **Set Environment Variables**
   ```bash
   railway variables set GOOGLE_APPLICATION_CREDENTIALS=/app/google-credentials.json
   railway variables set HKBU_API_KEY=your_actual_hkbu_api_key
   railway variables set PORT=5000
   railway variables set FLASK_ENV=production
   ```

5. **Deploy**
   ```bash
   railway up
   ```

### 4. Configure API Credentials

#### Google Cloud Speech API
1. **Create Google Cloud Project**
   - Visit [Google Cloud Console](https://console.cloud.google.com)
   - Create new project or select existing

2. **Enable APIs**
   ```
   - Cloud Speech-to-Text API
   - Cloud Text-to-Speech API
   ```

3. **Create Service Account**
   - Go to IAM & Admin > Service Accounts
   - Create new service account
   - Download JSON key file

4. **Upload to Railway**
   - In Railway dashboard: Files > Upload
   - Upload the JSON file as `google-credentials.json`

#### HKBU GenAI API
1. **Get API Key**
   - Register at HKBU GenAI platform
   - Generate API key

2. **Set in Railway**
   ```
   HKBU_API_KEY=your_actual_api_key_here
   ```

### 5. Domain Configuration

Railway provides automatic domains:
```
https://audiotutor01-production.up.railway.app
```

#### Custom Domain (Optional)
1. Go to Railway dashboard
2. Click "Settings" > "Domains"
3. Add your custom domain
4. Update DNS records as instructed

### 6. Deployment Verification

#### Check Application Health
1. **Visit your Railway URL**
2. **Test main interface**: `https://your-app.railway.app/`
3. **Test voice assistant**: `https://your-app.railway.app/avatar`

#### Test API Endpoints
```bash
# Test chatbot API
curl -X POST https://your-app.railway.app/api/chatbot/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, test message"}'

# Test streaming avatar API
curl -X GET https://your-app.railway.app/api/streaming-avatar/a
```

#### Test Voice Functionality
1. Open `/avatar` page
2. Click "🎤 Start Talking"
3. Grant microphone permissions
4. Speak a test phrase
5. Verify AI response audio

### 7. Monitoring & Logs

#### View Logs
- Railway Dashboard > "Logs" tab
- Real-time application logs
- Error tracking and debugging

#### Monitor Performance
- Railway Dashboard > "Metrics" tab
- CPU, memory, and network usage
- Request/response analytics

### 8. Environment-Specific Configuration

#### Production Optimizations
```bash
# In Railway environment variables
FLASK_ENV=production
FLASK_DEBUG=false
WEB_CONCURRENCY=2
MAX_WORKERS=4
```

#### Audio Processing Settings
```bash
# Optional: Optimize for Railway resources
AUDIO_QUALITY=medium
MAX_AUDIO_LENGTH=60
TIMEOUT_SECONDS=30
```

### 9. Troubleshooting

#### Common Deployment Issues

**Build Failures**
```bash
# Check requirements.txt compatibility
pip install -r requirements.txt --dry-run

# Verify Python version
python --version  # Should be 3.8+
```

**Audio Processing Errors**
```bash
# Ensure ffmpeg is available (Railway includes it)
# Check Google credentials path
# Verify API keys are set correctly
```

**WebSocket Connection Issues**
```bash
# Check Railway logs for Socket.IO errors
# Verify CORS settings in production
# Test with Railway's provided domain first
```

#### Debug Mode
Set temporarily for debugging:
```bash
FLASK_DEBUG=true
FLASK_ENV=development
```

### 10. Scaling & Performance

#### Horizontal Scaling
- Railway automatically handles traffic scaling
- Monitor usage in dashboard
- Upgrade plan if needed

#### Database (Future Enhancement)
```bash
# Add PostgreSQL for user sessions
railway add postgresql

# Environment variable automatically added:
DATABASE_URL=postgresql://...
```

### 11. Continuous Deployment

Railway automatically deploys on git push:

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Update audioTutor features"
   git push origin main
   ```

2. **Automatic Deployment**
   - Railway detects changes
   - Builds and deploys automatically
   - Zero-downtime deployment

### 12. Cost Optimization

#### Free Tier Limits
- 500 hours/month execution time
- $5 credit included
- Automatic sleep after inactivity

#### Pro Plan Benefits
- No execution time limits
- Priority support
- Advanced metrics
- Custom domains included

---

## 🎯 Your audioTutor01 is now live on Railway!

Access your deployed application at:
`https://your-app-name.railway.app`

For support: [Railway Documentation](https://docs.railway.app)
