# 🚀 Keep Integration Demo - Localhost Links

## Quick Start

### 1. Start the Demo Server
```bash
# Make the script executable
chmod +x start-keep-demo.sh

# Start the demo server
./start-keep-demo.sh
```

### 2. Access Demo Links
The server will start on `http://localhost:3000` and serve all demo files.

## 🔗 Localhost Demo Links

### Primary Demo Links
| Demo | URL | Description |
|------|-----|-------------|
| **Demo Hub** | http://localhost:3000/index.html | Main navigation hub with all demo links |
| **Keep Integration** | http://localhost:3000/keep-integration-demo.html | Primary Keep integration showcase |
| **Main Dashboard** | http://localhost:3000/frontend-demo.html | Full-featured React dashboard |
| **Static Demo** | http://localhost:3000/frontend-simple.html | Simple static HTML demo |

### Alternative Ports
If port 3000 is busy, you can use any other port:
```bash
# Use port 8080
python3 -m http.server 8080
# Access: http://localhost:8080/index.html
```

## 🎯 Demo Features

### Keep Integration Demo (`/keep-integration-demo.html`)
**Primary demo showcasing Keep Foundation integration**
- ✅ Keep Foundation features (100+ providers, PostgreSQL, YAML workflows)
- ✅ MSP-specific enhancements (80% noise reduction, AI correlation)
- ✅ Webhook integration testing (`/api/v1/ingest/keep`)
- ✅ Integration flow visualization
- ✅ HMAC security demonstration
- ✅ Real-time dashboard preview

### Main Dashboard (`/frontend-demo.html`)
**Full-featured React dashboard with advanced capabilities**
- ✅ Interactive alert management
- ✅ Real-time updates with Live Mode
- ✅ Advanced filtering and search
- ✅ Bulk operations (acknowledge, suppress, resolve)
- ✅ Analytics dashboard with charts
- ✅ AI agent status monitoring
- ✅ Live simulator for testing
- ✅ Export functionality (CSV/JSON)
- ✅ Alert grouping and correlation

### Static Demo (`/frontend-simple.html`)
**Simple static HTML demo**
- ✅ Basic alert display
- ✅ Static data visualization
- ✅ Simple interactions
- ✅ No JavaScript dependencies
- ✅ Lightweight and fast

### Demo Hub (`/index.html`)
**Navigation hub with all demo links**
- ✅ Easy navigation to all demos
- ✅ Feature descriptions
- ✅ Quick start instructions
- ✅ Demo overview and capabilities

## 🛠️ Development Setup

### Prerequisites
- Python 3.x (for HTTP server)
- Modern web browser (Chrome, Firefox, Safari, Edge)
- No additional dependencies required

### File Structure
```
msp-alert-app/
├── index.html                    # Demo hub (navigation)
├── keep-integration-demo.html    # Keep integration showcase
├── frontend-demo.html            # Main React dashboard
├── frontend-simple.html          # Static HTML demo
├── start-keep-demo.sh           # Demo startup script
├── KEEP_DEMO_LOCALHOST_GUIDE.md # Detailed guide
└── LOCALHOST_DEMO_LINKS.md      # This file
```

## 🎮 Demo Scenarios

### Scenario 1: Keep Integration Testing
1. **Start**: Open http://localhost:3000/index.html
2. **Navigate**: Click "Keep Integration Demo"
3. **Test**: Click "Test Integration" button
4. **Observe**: Webhook simulation and integration flow
5. **Explore**: View Keep Foundation features and MSP enhancements

### Scenario 2: Full Dashboard Experience
1. **Start**: Open http://localhost:3000/frontend-demo.html
2. **Enable**: Turn on "Live Mode" for real-time simulation
3. **Filter**: Use severity and status filters
4. **Bulk**: Select multiple alerts and perform bulk operations
5. **Analytics**: Switch to Analytics tab to view metrics

### Scenario 3: Static Demo
1. **Start**: Open http://localhost:3000/frontend-simple.html
2. **View**: Basic alert display with static data
3. **Interact**: Test simple checkbox interactions
4. **Compare**: See the difference from the full dashboard

## 🔧 Troubleshooting

### Port Already in Use
```bash
# Check what's using port 3000
lsof -i :3000

# Use a different port
python3 -m http.server 8080
# Then access: http://localhost:8080/index.html
```

### File Not Found Errors
```bash
# Check current directory
pwd
# Should show: /path/to/msp-alert-app

# List demo files
ls -la *.html

# Check if server is running
curl http://localhost:3000/index.html
```

### Browser Compatibility Issues
- **Chrome/Chromium**: Recommended for best experience
- **Firefox**: Full support
- **Safari**: Full support
- **Edge**: Full support

### JavaScript Errors
- Check browser console (F12)
- Ensure all CDN resources are loading
- Try refreshing the page
- Clear browser cache

## 📊 Demo Data

The demos use realistic mock data including:

### Alerts
- Various severities: critical, high, medium, low, info
- Different statuses: active, acknowledged, resolved
- Multiple sources: prometheus, datadog, newrelic, nagios
- Realistic timestamps and descriptions

### Incidents
- AI-correlated alerts
- Priority levels (P1, P2, P3)
- AI-generated summaries
- Related alert counts

### Metrics
- Noise reduction: 80%
- Deduplication rate: 65%
- Correlation accuracy: 92%
- Processing statistics

## 🚀 Next Steps

After testing locally:

1. **Deploy to Netlify**: Get public URLs for sharing
2. **Backend Integration**: Connect to real Keep instance
3. **Customization**: Adapt for your MSP needs
4. **Production**: Scale for enterprise use

## 📞 Support

For issues with the demo:
1. Check browser console for errors
2. Verify all HTML files are present
3. Ensure Python HTTP server is running
4. Try a different browser or port
5. Check the detailed guide: `KEEP_DEMO_LOCALHOST_GUIDE.md`

---

## 🎉 Ready to Demo!

**Start the server and open: http://localhost:3000/index.html**

This will give you access to all demo links and a comprehensive overview of the MSP Alert Intelligence platform with Keep integration.
