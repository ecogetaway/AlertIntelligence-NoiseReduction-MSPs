# Next.js Frontend Deployment Guide - Netlify

**Target:** Deploy `frontend/` as a separate Netlify site  
**Features:** Incident grouping, AI triage drawer, filter presets, live simulator, bulk ops

---

## 🚀 Quick Deploy via Netlify Dashboard

### Step 1: Create New Site
1. Log in to https://app.netlify.com
2. Click **"Add new site"** → **"Import an existing project"**
3. Connect to your GitHub repository: `ecogetaway/AlertIntelligence-NoiseReduction-MSPs`
4. Select branch: `perf-benchmarks-evidence` (or your working branch)

### Step 2: Configure Build Settings
Set the following in the Netlify dashboard:

**Base directory:**
```
frontend
```

**Build command:**
```
npm ci && npm run build
```

**Publish directory:**
```
.next
```

**Environment variables:**
```
NODE_VERSION=20
NEXT_PUBLIC_API_BASE=http://localhost:8000
NEXT_TELEMETRY_DISABLED=1
```

> **Note:** Update `NEXT_PUBLIC_API_BASE` to your deployed backend URL once available (e.g., `https://msp-backend.onrender.com`)

### Step 3: Deploy
1. Click **"Deploy site"**
2. Wait for build to complete (~2-3 minutes)
3. Netlify will auto-detect Next.js and configure runtime

### Step 4: Verify Deployment
1. Open your site URL (e.g., `https://msp-nextjs-app.netlify.app`)
2. Check dashboard loads
3. Test grouping toggle
4. Test Live Simulator
5. Test filter presets
6. Test alert detail drawer
7. Test bulk operations

---

## 📝 Manual Deploy via Netlify CLI (Alternative)

### Install Netlify CLI
```bash
npm install -g netlify-cli
```

### Login
```bash
netlify login
```

### Deploy from frontend directory
```bash
cd frontend
netlify deploy --prod
```

Follow prompts:
- Create & configure new site? **Yes**
- Base directory: `.` (already in frontend/)
- Build command: `npm ci && npm run build`
- Publish directory: `.next`

---

## 🔧 Configuration Files

### `frontend/netlify.toml`
✅ Already created with:
- Build command: `npm ci && npm run build`
- Publish: `.next`
- Node version: 20
- Security headers
- Cache headers for static assets
- Next.js redirect rules

### `frontend/package.json`
Ensure these scripts exist:
```json
{
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint"
  }
}
```

---

## 🌐 Environment Variables

### Required
| Variable | Value | Purpose |
|----------|-------|---------|
| `NODE_VERSION` | `20` | Node.js runtime version |
| `NEXT_PUBLIC_API_BASE` | `http://localhost:8000` or `https://your-backend.com` | Backend API URL |

### Optional
| Variable | Value | Purpose |
|----------|-------|---------|
| `NEXT_TELEMETRY_DISABLED` | `1` | Disable Next.js telemetry |

**To set in Netlify:**
1. Site settings → Environment variables
2. Add variable → Key + Value
3. Save

---

## ✅ Post-Deployment Checklist

### Functionality
- [ ] Dashboard loads without errors
- [ ] Alert list displays
- [ ] Grouping toggle works (Grouped by Incident ↔ All Alerts)
- [ ] Click alert opens detail drawer
- [ ] Detail drawer shows AI triage data (if available)
- [ ] Filter presets apply correctly
- [ ] Save custom preset persists (localStorage)
- [ ] Live simulator injects alerts
- [ ] Bulk operations dialog opens
- [ ] Select all/deselect works
- [ ] Mobile responsive

### Integration
- [ ] API calls reach backend (check Network tab)
- [ ] CORS configured on backend for Netlify domain
- [ ] No console errors
- [ ] All assets load (check 404s)

### Performance
- [ ] Lighthouse score >90
- [ ] First Contentful Paint <2s
- [ ] Time to Interactive <3s

---

## 🐛 Troubleshooting

### Issue: 404 on navigation
**Solution:** Netlify's redirect rules should handle this. Verify `frontend/netlify.toml` has:
```toml
[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
```

### Issue: API calls fail (CORS)
**Solution:** Add Netlify domain to backend CORS allowed origins:
```python
# backend/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://msp-nextjs-app.netlify.app",
        "http://localhost:3000"
    ],
    ...
)
```

### Issue: Build fails with "Module not found"
**Solution:** Ensure all dependencies are in `frontend/package.json`, not root `package.json`. Run:
```bash
cd frontend
npm install
```

### Issue: Environment variables not working
**Solution:** 
- Prefix with `NEXT_PUBLIC_` for client-side access
- Redeploy after adding env vars
- Clear cache: Deploys → Trigger deploy → Clear cache and deploy site

### Issue: Slow build times
**Solution:**
- Enable Netlify Build Plugin for Next.js (auto-enabled)
- Check build logs for warnings
- Reduce dependencies if possible

---

## 🔄 Continuous Deployment

Netlify automatically rebuilds when you push to GitHub:

1. Push changes to your branch
2. Netlify detects commit
3. Triggers build automatically
4. Deploys if build succeeds

**To disable auto-deploy:**
- Site settings → Build & deploy → Build settings → Stop auto publishing

---

## 📊 Monitoring

### Netlify Analytics
- Site settings → Analytics
- Enable analytics to track:
  - Page views
  - Unique visitors
  - Top pages
  - Referrers

### Deploy Logs
- Deploys tab → Click deploy → View deploy log
- Check for build warnings/errors

### Function Logs (if using Netlify Functions)
- Functions tab → View logs

---

## 🎯 Multiple Deployments

You now have **two sites**:

| Site | Content | URL |
|------|---------|-----|
| **Static Demo** | `frontend-demo.html` (root) | https://msp-alert-intelligence.netlify.app |
| **Next.js App** | `frontend/` (Next.js) | https://msp-nextjs-app.netlify.app (your new site) |

Both can coexist. The Next.js app has the new features:
- ✅ Incident grouping
- ✅ AI triage drawer
- ✅ Filter presets
- ✅ Live simulator
- ✅ Polished bulk ops

---

## 🔗 Useful Links

- **Netlify Docs:** https://docs.netlify.com/
- **Next.js on Netlify:** https://docs.netlify.com/frameworks/next-js/overview/
- **Deploy Settings:** https://app.netlify.com → Your Site → Site settings
- **Environment Vars:** https://app.netlify.com → Your Site → Site settings → Environment variables

---

## 📝 Summary

**Deployment Steps:**
1. Create new Netlify site from Git
2. Set base directory: `frontend`
3. Set build command: `npm ci && npm run build`
4. Set publish directory: `.next`
5. Add environment variable: `NEXT_PUBLIC_API_BASE`
6. Deploy and test

**New Features Live:**
- Incident grouping with correlation badges
- Alert detail drawer with AI triage
- Filter presets (built-in + custom)
- Live data simulator
- Polished bulk operations with confirm/undo

**Status:** ✅ Ready to deploy to Netlify as separate site

---

**Next:** Deploy via dashboard or CLI, then update backend CORS to allow your new Netlify domain.

