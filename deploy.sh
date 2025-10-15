#!/bin/bash

# MSP Alert Intelligence - Deployment Script
# Deploys to both Vercel and Netlify for maximum reliability

echo "🚀 MSP Alert Intelligence - Deployment Script"
echo "=============================================="
echo ""

# Check if we're in the right directory
if [ ! -f "frontend-demo.html" ]; then
    echo "❌ Error: frontend-demo.html not found. Run this script from the project root."
    exit 1
fi

echo "✅ Found frontend-demo.html"
echo ""

# Test locally first
echo "🧪 Testing locally..."
echo "Starting local server on port 3000..."
echo "Visit: http://localhost:3000/frontend-demo.html"
echo "Press Ctrl+C to stop local server and continue with deployment"
echo ""

# Start local server in background
python3 -m http.server 3000 &
LOCAL_PID=$!

# Wait for user to test
echo "⏳ Test the demo locally, then press Enter to continue with deployment..."
read -r

# Stop local server
kill $LOCAL_PID 2>/dev/null

echo ""
echo "🌐 Deploying to Vercel and Netlify..."
echo ""

# Deploy to Vercel
echo "📦 Deploying to Vercel..."
if command -v vercel &> /dev/null; then
    vercel --prod
    echo "✅ Vercel deployment initiated"
else
    echo "⚠️  Vercel CLI not found. Install with: npm i -g vercel"
fi

echo ""

# Deploy to Netlify
echo "📦 Deploying to Netlify..."
if command -v netlify &> /dev/null; then
    netlify deploy --prod
    echo "✅ Netlify deployment initiated"
else
    echo "⚠️  Netlify CLI not found. Install with: npm i -g netlify-cli"
fi

echo ""
echo "🎉 Deployment complete!"
echo ""
echo "📋 Next steps:"
echo "1. Check your Vercel dashboard for the live URL"
echo "2. Check your Netlify dashboard for the live URL"
echo "3. Test both URLs to ensure they work"
echo "4. Update demo script with actual URLs"
echo "5. Share URLs with judges"
echo ""
echo "🔗 Expected URLs:"
echo "- Vercel: https://msp-alert-app.vercel.app"
echo "- Netlify: https://msp-alert-intelligence.netlify.app"
echo ""
echo "📚 For detailed instructions, see DEPLOYMENT.md"
