# Frontend Options - REFERENCE GUIDE

## ✅ PRIMARY DEMO (Dark Theme - The One You Want!)

**File:** `frontend-demo.html`

**How to Run:**
```bash
# Option 1: Open directly in Chrome
open -a "Google Chrome" /Users/sanjay/msp-alert-app/frontend-demo.html

# Option 2: Serve with Python
cd /Users/sanjay/msp-alert-app
python3 -m http.server 3000
# Then open: http://localhost:3000/frontend-demo.html
```

**Features:**
- ✅ Dark theme with gradient background
- ✅ Complete MSP Alert Intelligence UI
- ✅ Interactive demo data
- ✅ AI Agent status indicators
- ✅ Alert cards with filtering
- ✅ Incident management
- ✅ Analytics dashboard
- ✅ **This is your main demo for presentations!**

**Status:** Fully functional, standalone HTML file, no backend required

---

## ⚠️ SECONDARY OPTIONS (Do Not Use for Demo)

### 1. Next.js Frontend (`frontend/` directory)
**Status:** In development, light theme, requires backend
**URL:** http://localhost:3000 (when running `npm run dev`)
**Use Case:** Future development, production deployment
**Why Not Demo:** Light theme, incomplete integration

### 2. Simple Frontend (`frontend-simple.html`)
**Status:** Basic version
**Use Case:** Testing only

---

## 🎯 DEMO CHECKLIST

Before presenting, always verify:
- [ ] Using `frontend-demo.html` ✅
- [ ] Dark theme is visible ✅
- [ ] AI Agents showing as "Active" ✅
- [ ] Sample alerts are displaying ✅
- [ ] Filters and tabs work ✅

---

## 🚀 QUICK START FOR DEMO

```bash
# The ONLY command you need for demo:
open -a "Google Chrome" /Users/sanjay/msp-alert-app/frontend-demo.html
```

**That's it!** No backend, no npm install, no docker-compose needed for the demo.

---

## 📋 Future Development Plan

1. **For Hackathon Demo:** Use `frontend-demo.html` (dark theme)
2. **Post-Hackathon:** 
   - Migrate dark theme to Next.js (`frontend/`)
   - Connect to backend API
   - Deploy Next.js to Netlify
   - Deploy backend to Render

---

## ⚠️ IMPORTANT REMINDER

**DO NOT USE:**
- ❌ http://localhost:3000 (Next.js - light theme)
- ❌ `frontend-simple.html`

**ALWAYS USE:**
- ✅ `frontend-demo.html` opened in Chrome
- ✅ Dark theme with full features

---

**Last Updated:** October 14, 2025
**Demo Ready:** YES ✅
**Deployment Ready:** Use demo HTML for now, Next.js for production later

