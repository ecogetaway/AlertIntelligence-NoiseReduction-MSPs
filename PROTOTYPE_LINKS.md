# 🚀 MSP Alert Intelligence Platform - Prototype Links

## ✅ PRIMARY DEMO (USE THIS!)

**Frontend Demo (Dark Theme):**
```bash
open -a "Google Chrome" /Users/sanjay/msp-alert-app/frontend-demo.html
```

**File:** `frontend-demo.html`  
**Status:** ✅ READY FOR DEMO  
**Theme:** Dark with gradient background  
**Backend Required:** NO - standalone demo

**Features:**
- Dark-themed MSP Alert Intelligence dashboard
- Real-time alert management UI
- AI Agent status indicators
- Interactive filtering and search
- Incident management
- Analytics visualization
- Fully functional without backend

---

## 🔧 Development Versions (Not for Demo)

### Next.js Frontend (Light Theme)
**URL:** http://localhost:3000  
**Status:** ⚠️ In Development  
**Start:**
```bash
cd frontend
npm run dev
```
**Note:** Light theme, requires backend running

### Backend API
**URL:** http://localhost:8000  
**API Docs:** http://localhost:8000/docs  
**Status:** ⚠️ Python 3.13 compatibility issues  
**Start:**
```bash
cd backend
pip3 install -r requirements.txt
python3 main.py
```

---

## 📊 Demo Data

The `frontend-demo.html` includes:
- ✅ Sample alerts (Critical, High, Medium severity)
- ✅ Mock incidents
- ✅ AI processing metrics
- ✅ Correlation examples
- ✅ Deduplication showcase

---

## 🎯 FOR HACKATHON JUDGES

**Show This:**
```bash
open -a "Google Chrome" /Users/sanjay/msp-alert-app/frontend-demo.html
```

**Key Features to Highlight:**
1. **AI-Powered Noise Reduction** - 78% reduction shown
2. **Smart Alert Correlation** - Related alerts grouped
3. **Bedrock + Strands Agents** - Dual AI integration
4. **Real-time Deduplication** - Automatic duplicate detection
5. **MSP-Focused** - Built for managed service providers

---

## 🚀 Deployment Plan (Post-Hackathon)

### Frontend → Netlify
- Migrate dark theme to Next.js
- Build command: `npm run build`
- Publish directory: `.next`

### Backend → Render
- Fix Python 3.13 compatibility
- Deploy FastAPI service
- PostgreSQL database
- Redis cache

---

## 📁 Project Structure

```
msp-alert-app/
├── frontend-demo.html          ← ✅ USE THIS FOR DEMO
├── frontend/                   ← Next.js (future production)
├── backend/                    ← FastAPI API
├── workflows/                  ← AI workflows
└── benchmarks/                 ← Performance data
```

---

## ⚡ Quick Commands

### Demo Mode (Recommended)
```bash
open -a "Google Chrome" /Users/sanjay/msp-alert-app/frontend-demo.html
```

### Development Mode (Full Stack)
```bash
# Terminal 1 - Backend
cd backend && python3 main.py

# Terminal 2 - Frontend
cd frontend && npm run dev

# Open: http://localhost:3000
```

---

## 🎬 Demo Script

1. **Open** `frontend-demo.html` in Chrome
2. **Point out** dark theme and modern UI
3. **Show** AI Agents Active indicator
4. **Navigate** through Alerts, Incidents, Analytics tabs
5. **Demonstrate** filtering by severity/status
6. **Highlight** AI enrichment badges on alerts
7. **Show** correlation groups
8. **Display** analytics with 78% noise reduction
9. **Explain** AWS Bedrock + Strands integration

---

**Current Status:** Demo ready with frontend-demo.html ✅  
**Next Steps:** Review demo, prepare pitch, then discuss deployment  
**DO NOT DEPLOY** until you give the go-ahead
