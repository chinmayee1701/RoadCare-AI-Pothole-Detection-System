# Vercel Deployment Guide

This guide walks you through deploying the RoadCare application to Vercel.

## Architecture Overview

The application consists of two deployments:
- **Frontend**: React app hosted on Vercel (primary deployment)
- **Backend**: FastAPI app hosted separately (can use Vercel, Railway, Render, or another service)

## Frontend Deployment (Vercel)

### Prerequisites
- Vercel account
- GitHub repository (recommended for automatic deployments)

### Steps

1. **Connect Repository**
   - Go to [vercel.com](https://vercel.com)
   - Click "New Project"
   - Import your GitHub repository

2. **Configure Build Settings**
   - Framework Preset: Other (Vite)
   - Build Command: `cd frontend1 && npm run build`
   - Output Directory: `frontend1/dist`
   - Install Command: `npm install`

3. **Set Environment Variables**
   In Vercel Project Settings → Environment Variables, add:
   ```
   VITE_API_BASE_URL=https://your-backend-api-url.com
   ```

4. **Deploy**
   - Vercel will automatically deploy on every push to main branch

### Root-Level Deployment (Alternative)

If you want to deploy from the root directory:
1. In Project Settings, set Root Directory to `./frontend1`
2. Build Command: `npm run build`
3. Output Directory: `dist`

## Backend Deployment

### Option 1: Vercel (Python)

1. **Create Separate Repository (Recommended)**
   - Push backend code to its own repository
   - Or use monorepo approach with separate deployment

2. **Deploy Backend**
   ```bash
   # From backend directory
   vercel deploy
   ```

3. **Configure Environment Variables**
   Add to Vercel Backend Project Settings:
   ```
   MONGODB_URI=mongodb+srv://user:password@cluster.mongodb.net
   MONGODB_DB_NAME=roadcare_prod
   JWT_SECRET=your-secret-key-here
   TELEGRAM_BOT_TOKEN=your-telegram-bot-token
   ENVIRONMENT=production
   ```

### Option 2: Other Services

**Railway.app** (Recommended for Python):
```bash
# Install Railway CLI
npm i -g @railway/cli

# Deploy
railway init
railway link
railway up
```

**Render.com**:
- Connect GitHub repo
- Select Python as runtime
- Add environment variables
- Deploy

## Environment Variables

### Frontend (.env files)
```
VITE_API_BASE_URL=https://your-api.vercel.app
```

### Backend (.env)
```
MONGODB_URI=mongodb+srv://user:password@cluster.mongodb.net
MONGODB_DB_NAME=roadcare_prod
JWT_SECRET=your-super-secret-key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
TELEGRAM_BOT_TOKEN=your-bot-token
ENVIRONMENT=production
```

## Configuration Files

### vercel.json (Root)
Configures frontend deployment with:
- Build settings
- Routes and redirects
- Security headers
- CORS configuration

### backend/vercel.json
Configures backend Python deployment with:
- Python runtime settings
- Environment variables
- Lambda function size limits

### .vercelignore
Specifies files to exclude from deployment (reduces build size)

## Important Notes

### CORS Configuration
The backend CORS middleware allows all origins in production. For production:

```python
# In app/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://your-frontend.vercel.app",
        "https://yourdomain.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Database
- Ensure MongoDB connection string includes network access from Vercel IPs
- Or use MongoDB Atlas with IP allowlist: `0.0.0.0/0` (production: use specific IPs)

### File Uploads
- Vercel has limited ephemeral storage
- Use external storage: AWS S3, Azure Blob, or Cloudinary for uploaded images
- Update `image_service.py` to use cloud storage

### Large Dependencies
- TensorFlow/PyTorch in backend may exceed Vercel limits
- Consider using lightweight alternatives or serverless ML services
- For AI models: use Hugging Face Inference API or similar

## Troubleshooting

### Build Fails
- Check `vercel logs` command
- Verify all dependencies in requirements.txt
- Ensure correct Python version (3.11+)

### Frontend Can't Reach Backend
- Verify `VITE_API_BASE_URL` is set correctly
- Check backend CORS settings
- Ensure backend is deployed and running

### Environment Variables Not Working
- Redeploy after adding variables
- Use `vercel env ls` to verify
- Check that variables are set in correct environment

## Deployment Checklist

- [ ] Set up environment variables (both frontend and backend)
- [ ] Configure MongoDB connection string
- [ ] Update JWT_SECRET with secure random value
- [ ] Set Telegram bot token
- [ ] Configure storage for file uploads
- [ ] Update CORS origins in backend
- [ ] Test authentication flow
- [ ] Test file upload and image processing
- [ ] Verify API endpoints
- [ ] Set up monitoring/logging

## Useful Commands

```bash
# Check Vercel status
vercel status

# View deployment logs
vercel logs

# View function logs (backend)
vercel logs --follow

# List environment variables
vercel env ls

# Pull environment variables locally
vercel env pull

# Redeploy
vercel --prod
```

## Further Resources

- [Vercel Documentation](https://vercel.com/docs)
- [Vercel Python Support](https://vercel.com/docs/functions/runtimes/python)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
