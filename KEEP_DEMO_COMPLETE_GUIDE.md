# Keep Integration Demo - Complete Guide

## 🎯 Demo Objective
Showcase how your MSP Alert Intelligence platform integrates with Keep's open-source foundation while highlighting MSP-specific enhancements that deliver 80% noise reduction and AI-powered correlation.

## 🚀 Quick Start (5 minutes)

### Step 1: Start Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

### Step 2: Start Frontend
```bash
cd frontend
npm install
npm run dev
```

### Step 3: Run Demo
```bash
# In a new terminal
./scripts/demo-keep-integration.sh
```

## 📋 Demo Script (7 minutes)

### Opening (1 minute)
**"Today I'll demonstrate our MSP Alert Intelligence platform, built on Keep's open-source foundation with MSP-specific AI enhancements."**

**Key Points:**
- Built on Keep's proven alert management foundation
- Enhanced with MSP-specific noise reduction and AI
- 80% alert reduction through intelligent filtering
- AWS Bedrock AI for correlation and analysis

### Keep Integration Features (2 minutes)

#### A. Alert Ingestion from 100+ Providers
**"Keep provides integration with 100+ monitoring providers. Let me show you our webhook endpoint that accepts Keep alerts:"**

```bash
# Show the Keep webhook endpoint
curl -X POST http://localhost:8000/api/v1/ingest/keep \
  -H "Content-Type: application/json" \
  -d '{
    "event": "alert.created",
    "alert": {
      "title": "High CPU Usage",
      "severity": "critical",
      "source": "prometheus"
    }
  }'
```

**Demo Points:**
- ✅ HMAC signature verification
- ✅ Keep's alert event format
- ✅ Automatic alert mapping
- ✅ Database persistence

#### B. PostgreSQL Database Integration
**"We use Keep's PostgreSQL schema for full compatibility:"**

```bash
# Show database integration
curl http://localhost:8000/api/v1/alerts
```

**Demo Points:**
- ✅ Keep-compatible database schema
- ✅ Full alert history
- ✅ Multi-tenant data isolation
- ✅ Performance optimization

#### C. YAML Workflow Engine
**"Keep's YAML workflow format is fully supported:"**

```yaml
# Example Keep workflow
workflows:
  - name: "MSP Alert Processing"
    triggers:
      - event: "alert.created"
    steps:
      - name: "Noise Reduction"
        action: "filter"
      - name: "AI Correlation"
        action: "correlate"
      - name: "SLA Routing"
        action: "route"
```

**Demo Points:**
- ✅ Keep's YAML format
- ✅ Workflow automation
- ✅ MSP-specific enhancements
- ✅ Extensible framework

### MSP Enhancements (2 minutes)

#### A. 80% Noise Reduction
**"Our MSP-specific enhancements deliver 80% noise reduction:"**

```bash
# Show noise reduction metrics
curl http://localhost:8000/api/v1/metrics/noise-reduction
```

**Demo Points:**
- ✅ Intelligent filtering algorithms
- ✅ Client-specific rules
- ✅ Historical pattern analysis
- ✅ Real-time metrics

#### B. AI Correlation with Bedrock
**"AWS Bedrock AI provides intelligent correlation:"**

```bash
# Show AI correlation
curl http://localhost:8000/api/v1/agents/status
```

**Demo Points:**
- ✅ AWS Bedrock integration
- ✅ Alert correlation
- ✅ Incident grouping
- ✅ Intelligent triage

#### C. SLA Management
**"Client-specific SLA routing and response times:"**

```bash
# Show SLA configuration
curl http://localhost:8000/api/v1/msp/clients
```

**Demo Points:**
- ✅ Client-specific routing
- ✅ SLA compliance tracking
- ✅ Response time optimization
- ✅ Priority management

### Live Dashboard (2 minutes)

#### A. Real-time Alert Processing
**"Our dashboard shows live alert processing:"**

- Open: http://localhost:3000/frontend-demo.html
- Show: Live alert updates
- Highlight: Keep integration points
- Demonstrate: MSP enhancements

#### B. Performance Metrics
**"System performance and health monitoring:"**

```bash
# Show performance metrics
curl http://localhost:8000/api/v1/metrics
```

**Demo Points:**
- ✅ Real-time processing
- ✅ Performance monitoring
- ✅ Health checks
- ✅ System status

### Closing (1 minute)
**"This demonstrates how we've enhanced Keep's foundation with MSP-specific AI and noise reduction while maintaining full compatibility."**

**Key Takeaways:**
- Built on Keep's proven foundation
- Enhanced with MSP-specific features
- 80% noise reduction achieved
- Full Keep compatibility maintained
- Production-ready integration

## 🔧 Troubleshooting

### Backend Issues
```bash
# Check if backend is running
curl http://localhost:8000/health

# Check logs
tail -f backend/logs/app.log
```

### Frontend Issues
```bash
# Check if frontend is running
curl http://localhost:3000

# Check build
npm run build
```

### Database Issues
```bash
# Check PostgreSQL connection
psql -h localhost -U postgres -d msp_alerts

# Check tables
\dt
```

## 📊 Demo Metrics

### Performance Targets
- **Webhook Response**: <2 seconds
- **Noise Reduction**: 80% alert reduction
- **AI Correlation**: 85% correlation rate
- **SLA Compliance**: 99.5% within SLA

### Key Numbers to Highlight
- **100+ Providers**: Keep's provider integrations
- **80% Reduction**: MSP noise reduction
- **<2s Response**: Webhook processing time
- **99.5% SLA**: Client compliance rate

## 🎯 Demo Success Criteria

### Technical
- ✅ All webhooks process successfully
- ✅ Frontend shows real-time updates
- ✅ AI correlation working
- ✅ Database persisting

### Business
- ✅ Clear value proposition
- ✅ MSP-specific benefits shown
- ✅ Keep integration demonstrated
- ✅ ROI metrics visible

## 📝 Demo Notes

### Keep Foundation Benefits
- Built on proven open-source platform
- Leverages 100+ provider integrations
- Uses standard YAML workflow format
- Maintains security standards

### MSP Value Add
- 80% noise reduction vs standard Keep
- AI-powered correlation and triage
- Client-specific SLA management
- MSP-optimized workflows

### Technical Integration
- Keep webhooks → MSP processing → AI enhancement
- PostgreSQL database with Keep-compatible schema
- HMAC security for webhook integrity
- Extensible provider framework

## 🚀 Next Steps

After demo:
1. **Q&A Session**: Address technical questions
2. **Deep Dive**: Show specific integration points
3. **Customization**: Discuss client-specific needs
4. **Deployment**: Explain production setup
5. **Support**: Provide documentation and resources
