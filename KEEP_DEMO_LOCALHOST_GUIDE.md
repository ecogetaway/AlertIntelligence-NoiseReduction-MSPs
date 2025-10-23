# Keep Integration Demo - Localhost Links Guide

## 🚀 Quick Start

### Start the Demo Server
```bash
# Make the script executable (if not already done)
chmod +x start-keep-demo.sh

# Start the demo server
./start-keep-demo.sh
```

The server will start on `http://localhost:3000` and serve all demo files.

## 🔗 Localhost Demo Links

### Primary Demo Links
- **Keep Integration Demo**: http://localhost:3000/keep-integration-demo.html
- **Main Dashboard**: http://localhost:3000/frontend-demo.html  
<!-- Static demo removed -->
- **Landing Page**: http://localhost:3000/index.html

### Alternative Access Methods
If you prefer to start the server manually:
```bash
# Start HTTP server on port 3000
python3 -m http.server 3000

# Or on a different port (e.g., 8080)
python3 -m http.server 8080
```

## 🎯 Demo Features by Link

### 1. Keep Integration Demo (`/keep-integration-demo.html`)
**Primary demo showcasing Keep integration**
- ✅ Keep Foundation features
- ✅ MSP-specific enhancements  
- ✅ AI-powered correlation
- ✅ 80% noise reduction
- ✅ Webhook integration testing
- ✅ Integration flow visualization

### 2. Main Dashboard (`/frontend-demo.html`)
**Full-featured React dashboard**
- ✅ Interactive alert management
- ✅ Real-time updates
- ✅ Live mode simulation
- ✅ Advanced filtering
- ✅ Bulk operations
- ✅ Analytics dashboard
- ✅ AI agent status

<!-- Static demo removed -->
**Simple static HTML demo**
- ✅ Basic alert display
- ✅ Static data visualization
- ✅ Simple interactions
- ✅ No JavaScript dependencies

### 4. Landing Page (`/index.html`)
**Entry point with redirect**
- ✅ Automatic redirect to main demo
- ✅ Project overview

## 🛠️ Development Setup

### Prerequisites
- Python 3.x (for HTTP server)
- Modern web browser
- No additional dependencies required

### File Structure
```
msp-alert-app/
├── keep-integration-demo.html    # Keep integration showcase
├── frontend-demo.html            # Main React dashboard
<!-- Static demo removed -->
├── index.html                    # Landing page
├── start-keep-demo.sh           # Demo startup script
└── KEEP_DEMO_LOCALHOST_GUIDE.md  # This guide
```

## 🎮 Demo Scenarios

### Scenario 1: Keep Integration Testing
1. Open http://localhost:3000/keep-integration-demo.html
2. Click "Test Integration" button
3. Observe webhook simulation
4. View integration flow

### Scenario 2: Full Dashboard Experience
1. Open http://localhost:3000/frontend-demo.html
2. Enable "Live Mode" for real-time simulation
3. Use filters and bulk operations
4. Explore analytics tab

### Scenario 3: Static Demo
<!-- Static demo removed -->
2. View basic alert display
3. Test simple interactions

## 🔧 Troubleshooting

### Port Already in Use
If port 3000 is busy:
```bash
# Use a different port
python3 -m http.server 8080
# Then access: http://localhost:8080/keep-integration-demo.html
```

### File Not Found Errors
Ensure you're in the project root directory:
```bash
# Check current directory
pwd
# Should show: /path/to/msp-alert-app

# List demo files
ls -la *.html
```

### Browser Compatibility
- Chrome/Chromium (recommended)
- Firefox
- Safari
- Edge

## 📊 Demo Data

The demos use mock data including:
- **Alerts**: Various severities and statuses
- **Incidents**: AI-correlated alerts
- **Agents**: Processing statistics
- **Metrics**: Noise reduction, deduplication, correlation

## 🚀 Next Steps

After testing locally, you can:
1. Deploy to Netlify for public access
2. Set up backend integration
3. Configure Keep webhook endpoints
4. Customize for your MSP needs

## 📞 Support

For issues with the demo:
1. Check browser console for errors
2. Verify all HTML files are present
3. Ensure Python HTTP server is running
4. Try a different browser

---

**Ready to demo!** 🎉
Start the server and open http://localhost:3000/keep-integration-demo.html
