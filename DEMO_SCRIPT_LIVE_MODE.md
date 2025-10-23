# MSP Alert Intelligence – Live Mode Demo Script (Enhanced v2.0)

Purpose: A comprehensive 5–7 minute flow showcasing the zero‑backend, "looks live" demo in `frontend-demo.html` with **5 new advanced features** plus the latest polish.

## Demo URLs (Live)

### Primary Deployments (Enhanced v2.0)
- **Keep + AWS Integration**: https://msp-alert-intelligence.netlify.app/ ⭐ **RECOMMENDED**
- **Dashboard**: https://msp-alert-intelligence.netlify.app/prototype ⭐ **LIVE MODE**
- **Vercel**: https://msp-alert-app.vercel.app

### Local Testing (Latest Features)
- **Local**: http://localhost:8080/frontend-demo.html ⭐ **NEW FEATURES**

### Backup Options
- **GitHub**: https://github.com/ecogetaway/AlertIntelligence-NoiseReduction-MSPs

### For Judges
Use Netlify URLs for the most stable experience:
- **Keep Integration**: https://msp-alert-intelligence.netlify.app/ (AWS badges, webhook testing)
- **Dashboard**: https://msp-alert-intelligence.netlify.app/prototype (Live Mode, advanced UI)

## 🆕 NEW FEATURES (Enhanced v2.0)

### 5 Major Enhancements Added:
1. **🎮 Live Simulator** - Real-time alert injection with controls
2. **🎚️ Filter Presets** - Quick filters + custom saved views  
3. **📊 Incident Grouping** - Smart correlation display
4. **📝 Alert Detail Drawer** - Rich right-side panel with AI triage
5. **⚡ Enhanced Bulk Ops** - Professional dialog with confirmation

## Setup
- Open live URL above in Chrome (or localhost for development).
- Ensure hard refresh (Cmd+Shift+R) before starting.
- **For new features**: Use `http://localhost:8080/frontend-demo.html`

## Narrative Hook (15–20s)
- “This is our MSP Alert Intelligence prototype. It’s a zero‑backend demo that simulates live operations, perfect for hackathon judging, with a production path to Keep or our FastAPI later.”

## Header + Live Badge (10s)
- Point to the title: “Notice the Live badge with pulsing dot when live is on. I’ll toggle Live now.”
- Click “Live Mode: Off” to turn it On – mention the auto‑switch to Analytics.

## Analytics First (45–60s)
- “We jump to Analytics on Live. Metrics drift realistically in tight ranges:”
  - Noise Reduction: 75–92%
  - Deduplication Rate: 60–80%
  - Correlation Accuracy: 88–98%
- Show the progress bars updating every ~8s.
- Mention agents list and overall trends chart.

## Live Events (45–60s)
- Scroll to “Live Events”.
- “Events stream in with severity dots. Hover pauses auto‑scroll; moving off resumes.”
- Click a recent event: “Clicking highlights and scrolls to the referenced alert card.”

## Alerts (60–75s)
- Switch to Alerts tab.
- "New alerts fade/slide in, existing alerts mutate, some resolve. Mix is 60% add / 30% mutate / 10% resolve, capped to last 20 alerts to keep it snappy."

### 🆕 NEW: Live Simulator (30s)
- Point to yellow banner: "This is our Live Simulator - real-time alert injection."
- Enable simulator, change interval to 2000ms, enable Burst mode.
- "Watch alerts flow in with 🎮 tags - perfect for demos!"

### 🆕 NEW: Filter Presets (20s)  
- Show preset bar: "Quick filters for common scenarios."
- Click "Critical Only", then "Save view" → name it "Demo Filter".
- "Custom presets persist in localStorage."

### 🆕 NEW: Incident Grouping (15s)
- Toggle "Grouped by Incident" button.
- "Smart correlation groups related alerts together."

### Enhanced Filters & Bulk Ops
- Use filters: Set Severity to "Critical" and Status to "Active".
- Toggle "Only Active" quick filter; show count text updates.
- **🆕 NEW**: Click "Bulk Actions" → show professional dialog with confirmation.
- Select a few alerts and demonstrate the enhanced bulk operations.

## 🆕 NEW: Alert Detail Drawer (30s)
- Click on any alert card to open the detail drawer.
- "Rich alert details with AI triage, metadata, and remediation steps."
- Show AI triage section for simulator alerts: "🤖 AI classification and recommendations."
- Close drawer and click another alert to show different details.

## Incidents (30–45s)
- Switch to Incidents.
- "Correlated incidents summarize related alerts and AI notes. In production, these derive from Keep or our API; here we show the flow."

## Export (15–20s)
- Back on Alerts, click Export → choose CSV or JSON. “Quick export of the filtered view for handoff.”

## Wrap (15–20s)
- "This is a polished, judge‑friendly demo: zero servers, realistic live behavior, clear UX, plus 5 new advanced features for professional alert management. Post‑hackathon, we'll wire the frontend to Keep or our FastAPI and deploy backend to Render."

## Troubleshooting Notes
- If animations stop: toggle Live Off/On.
- If events don’t highlight: wait for next tick (~8s) and click the newest event.
- Hard refresh if styles seem stale.

## Talking Points (Quick Reference)
- **Original Features**: Live cadence: 8s; 60/30/10 add/mutate/resolve; cap 20 alerts.
- **Original Features**: Live polish: pulsing Live badge, fade/slide‑in alerts, severity dots.
- **Original Features**: Analytics: wider, believable drift ranges; auto‑switch on Live.
- **Original Features**: Events: severity dots, click‑to‑highlight, pause on hover.
- **Original Features**: Filters: auto‑reset on tab switch; "Only Active" quick toggle.
- **🆕 NEW**: Live Simulator: Real-time injection, burst mode, severity controls.
- **🆕 NEW**: Filter Presets: Quick filters + localStorage persistence.
- **🆕 NEW**: Incident Grouping: Smart correlation display.
- **🆕 NEW**: Alert Detail Drawer: Rich details + AI triage.
- **🆕 NEW**: Enhanced Bulk Ops: Professional dialog with confirmation.

