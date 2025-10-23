# UI Features Visual Guide

## Layout Overview

```
┌─────────────────────────────────────────────────────────────────┐
│ MSP Alert Intelligence Dashboard                       [BADGES] │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  [Alerts] [Incidents] [Agents] [Analytics]                     │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │ 🟡 Live Simulator ON                                     │  │
│  │ [✓ Enable] [Interval: 3000ms] [✓ Burst] [Critical ▼]   │  │
│  └─────────────────────────────────────────────────────────┘  │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │ 🎚️ Presets: [Critical Only] [Active] [⭐ My View]       │  │
│  │                                  [Save view] [Delete]    │  │
│  └─────────────────────────────────────────────────────────┘  │
│                                                                 │
│  [📊 Grouped by Incident]                                      │
│                                                                 │
│  [Advanced Filters ▼] [Export ▼]              [☐ Select All]  │
│                                                                 │
│  [All Severities ▼] [All Status ▼]                            │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │ High CPU Usage • Server-01            [3 alerts] [HIGH]  │  │
│  │ Sources: prometheus, datadog                             │  │ ← Click to
│  └─────────────────────────────────────────────────────────┘  │   open drawer
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │ Memory Leak Detected             [2 alerts] [CRITICAL]   │  │
│  │ Sources: datadog, simulator            🤖 AI              │  │
│  └─────────────────────────────────────────────────────────┘  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────┐
│ ☑️ 3 alerts selected        │ ← Floating bulk actions bar
│ [⚡ Bulk Actions]            │
└─────────────────────────────┘
```

---

## Feature 1: Live Simulator

```
╔═══════════════════════════════════════════════════════════╗
║ 🟡 Live Simulator ON                                      ║
╠═══════════════════════════════════════════════════════════╣
║                                                           ║
║  [✓] Enable    Interval [3000] ms    [✓] Burst           ║
║                                                           ║
║  Severity Mix: [Balanced ▼]                               ║
║                 ├─ Balanced (info→high)                   ║
║                 ├─ High (medium→high)                     ║
║                 └─ Critical (high→critical)               ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝

Key:
- Yellow background = active simulator
- Enable = start/stop
- Interval = ms between alerts
- Burst = 3 alerts at once vs 1
- Severity = which severities to generate
```

---

## Feature 2: Filter Presets Bar

```
┌───────────────────────────────────────────────────────────┐
│ 🎚️ Presets:                                              │
│                                                           │
│ [Critical Only] [Active Incidents] [Noisy Sources]       │
│                                                           │
│ [⭐ My Custom View] [⭐ Weekend Filter]                   │
│                                                           │
│                    [Save view] [Delete preset]            │
└───────────────────────────────────────────────────────────┘

Built-in presets (gray):
• Critical Only → severity=critical, status=all
• Active Incidents → severity=all, status=active
• Noisy Sources → severity=all, status=all

Custom presets (blue with ⭐):
• Saved to localStorage
• Click "Save view" to create
• Click "Delete preset" to remove
```

---

## Feature 3: Incident Grouping Toggle

```
Toggle State 1: GROUPED VIEW
┌──────────────────────────┐
│ [📋 Grouped by Incident] │
└──────────────────────────┘

Shows:
┌─────────────────────────────────────────────────────┐
│ High CPU Usage • Server-01          [3 alerts] 🔴   │
│ Sources: prometheus, datadog, simulator      🤖 AI  │
└─────────────────────────────────────────────────────┘
        ↑                        ↑           ↑
    Group title            Alert count   AI badge
                                         (if any from simulator)

---

Toggle State 2: LIST VIEW
┌──────────────────────┐
│ [📊 All Alerts]      │
└──────────────────────┘

Shows:
┌──────────────────────────────────────────────────┐
│ ☐ High CPU Usage                         🔴 HIGH │
│   CPU usage has exceeded 90%...                  │
│   Source: prometheus • Jan 15, 11:00 AM          │
└──────────────────────────────────────────────────┘
 ↑
Checkbox for bulk selection
```

---

## Feature 4: Alert Detail Drawer

```
                                    ┌───────────────────────────┐
                                    │ Alert Details          [✕]│
                                    ├───────────────────────────┤
                                    │                           │
                                    │ High CPU Usage • Server-01│
                                    │ [HIGH] [ACTIVE]           │
                                    │                           │
                                    │ ┌────────────────────┐   │
                                    │ │ Description        │   │
                                    │ │ CPU usage exceeded │   │
                                    │ │ 90% threshold...   │   │
                                    │ └────────────────────┘   │
                                    │                           │
                                    │ ┌────────────────────┐   │
                                    │ │ 🤖 AI Triage       │   │← Purple theme
                                    │ │ Severity: HIGH     │   │
                                    │ │ Summary: ...       │   │
                                    │ │ Actions:           │   │
                                    │ │ • Check logs       │   │
                                    │ │ • Scale resources  │   │
                                    │ └────────────────────┘   │
                                    │                           │
                                    │ ┌────────────────────┐   │
                                    │ │ Labels & Tags      │   │
                                    │ │ [perf] [server-01] │   │
                                    │ └────────────────────┘   │
                                    │                           │
                                    │ ┌────────────────────┐   │
                                    │ │ Metadata           │   │
                                    │ │ Source: prometheus │   │
                                    │ │ Created: 11:00 AM  │   │
                                    │ │ ID: alert-12345... │   │
                                    │ └────────────────────┘   │
                                    │                           │
                                    └───────────────────────────┘
                                            ↑
                                    Slides in from right
                                    Full height, scrollable
```

---

## Feature 5: Enhanced Bulk Operations

```
Step 1: Select alerts (list view)
┌──────────────────────────────┐
│ ☑ Alert 1           [HIGH]  │ ← Checked
│ ☑ Alert 2           [MED]   │ ← Checked
│ ☐ Alert 3           [LOW]   │
└──────────────────────────────┘

Step 2: Floating bar appears
    ┌─────────────────────────────┐
    │ ☑️ 2 alerts selected  [Clear]│
    │ [⚡ Bulk Actions]             │
    └─────────────────────────────┘

Step 3: Modal dialog opens
        ┌───────────────────────────┐
        │ Bulk Action            [✕]│
        ├───────────────────────────┤
        │                           │
        │ 2 alerts selected         │
        │                           │
        │ Action:                   │
        │ [Acknowledge ▼]           │
        │  ├─ Acknowledge           │
        │  ├─ Suppress              │
        │  └─ Resolve               │
        │                           │
        │ Reason (optional):        │
        │ ┌──────────────────────┐  │
        │ │ False positive from  │  │
        │ │ maintenance window   │  │
        │ └──────────────────────┘  │
        │                           │
        │     [Cancel] [Confirm]    │
        └───────────────────────────┘

Step 4: Action executes
→ Alerts updated
→ Event stream logs action
→ Modal closes
→ Selection cleared
```

---

## Color Palette Reference

```
Background Colors:
├─ #181824  Main background (darkest navy)
├─ #252538  Cards, panels (medium navy)
├─ #3a3a4a  Hover states, inputs (light navy)
└─ #4a4a5a  Borders (lightest navy)

Text Colors:
├─ white     Headings, important text
├─ #e5e7eb   Body text (gray-300)
├─ #9ca3af   Secondary text (gray-400)
└─ #6b7280   Tertiary text (gray-500)

Accent Colors:
├─ 🔵 Blue    #2563eb  Primary actions, custom presets
├─ 🟡 Yellow  #eab308  Simulator, warnings
├─ 🟣 Purple  #9333ea  AI features, enrichment
├─ 🟢 Green   #16a34a  Success, resolved
├─ 🔴 Red     #dc2626  Critical, errors
└─ 🟠 Orange  #ea580c  High severity, suppress
```

---

## Interaction States

### Buttons
```
Default:  bg-[#3a3a4a] text-gray-300
Hover:    bg-[#4a4a5a] text-white
Active:   bg-blue-600 text-white
Disabled: opacity-50 cursor-not-allowed
```

### Cards
```
Default:  border-[#3a3a4a]
Hover:    border-[#4a4a5a] shadow-xl
Selected: ring-2 ring-blue-500
```

### Modals/Drawers
```
Backdrop:  bg-black/60
Panel:     bg-[#252538] border-[#4a4a5a]
Animation: slide-in-right (drawer)
           fade-in-scale (modal)
```

---

## Responsive Breakpoints

```
Mobile (< 640px):
- Stack controls vertically
- Full-width cards
- Drawer takes full screen

Tablet (640px - 1024px):
- 2-column preset bar
- Side-by-side filters
- Drawer 80% width

Desktop (> 1024px):
- Full horizontal layout
- Drawer max-w-2xl
- Multi-column advanced filters
```

---

## Animation Timings

```
Fast (150ms):   Hover effects
Medium (200ms): Button clicks, toggles
Slow (300ms):   Modal open/close, drawer slide
Custom (700ms): New alert fade-in-up
```

---

## Keyboard Shortcuts (Potential)

```
Spacebar:   Toggle selected alert
Escape:     Close drawer/modal
Arrow Up:   Previous alert
Arrow Down: Next alert
Enter:      Open alert detail
Ctrl+A:     Select all
Ctrl+E:     Export alerts
```

---

## Accessibility Features

```
✓ ARIA labels on all interactive elements
✓ Keyboard navigation support
✓ Focus indicators on buttons/inputs
✓ Screen reader friendly text
✓ Color contrast meets WCAG AA
✓ Semantic HTML structure
✓ Alt text for icons/emojis
```

---

**Pro Tip for Demo:**
1. Open browser DevTools (F12)
2. Go to Console
3. Type: `localStorage.clear()` to reset custom presets
4. Or: `localStorage.getItem('msp-presets')` to view saved presets

**Live URL:**
http://localhost:8080/frontend-demo.html

