# MSP Alert Intelligence – Live Mode Demo Script (Updated)

Purpose: A tight 3–5 minute flow showcasing the zero‑backend, "looks live" demo in `frontend-demo.html` with the latest polish.

## Demo URLs (Live)

### Primary Deployments
- **Vercel**: https://msp-alert-app.vercel.app
- **Netlify**: https://msp-alert-intelligence.netlify.app

### Backup Options
- **GitHub**: https://github.com/ecogetaway/AlertIntelligence-NoiseReduction-MSPs
- **Local**: http://localhost:3000/frontend-demo.html

### For Judges
Use either Vercel or Netlify URL - both are identical. If one is slow, try the other.

## Setup
- Open live URL above in Chrome (or localhost for development).
- Ensure hard refresh (Cmd+Shift+R) before starting.

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
- “New alerts fade/slide in, existing alerts mutate, some resolve. Mix is 60% add / 30% mutate / 10% resolve, capped to last 20 alerts to keep it snappy.”
- Use filters:
  - Set Severity to “Critical” (or any) and Status to “Active”.
  - Toggle “Only Active” quick filter; show count text updates.
- Select a few alerts and show bulk actions (acknowledge/resolve) to demonstrate UX (no backend calls).

## Incidents (30–45s)
- Switch to Incidents.
- “Correlated incidents summarize related alerts and AI notes. In production, these derive from Keep or our API; here we show the flow.”

## Export (15–20s)
- Back on Alerts, click Export → choose CSV or JSON. “Quick export of the filtered view for handoff.”

## Wrap (15–20s)
- “This is a polished, judge‑friendly demo: zero servers, realistic live behavior, clear UX. Post‑hackathon, we’ll wire the frontend to Keep or our FastAPI and deploy backend to Render.”

## Troubleshooting Notes
- If animations stop: toggle Live Off/On.
- If events don’t highlight: wait for next tick (~8s) and click the newest event.
- Hard refresh if styles seem stale.

## Talking Points (Quick Reference)
- Live cadence: 8s; 60/30/10 add/mutate/resolve; cap 20 alerts.
- Live polish: pulsing Live badge, fade/slide‑in alerts, severity dots.
- Analytics: wider, believable drift ranges; auto‑switch on Live.
- Events: severity dots, click‑to‑highlight, pause on hover.
- Filters: auto‑reset on tab switch; “Only Active” quick toggle.

