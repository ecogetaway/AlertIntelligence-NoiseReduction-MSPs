# Keep Integration Demo - Quick Reference

## 🎯 Demo Objective
Showcase MSP Alert Intelligence platform with Keep integration, highlighting both Keep's foundation and our MSP-specific enhancements.

## ⚡ Quick Demo (3-5 minutes)

### 1. Start Services
```bash
# Terminal 1: Backend
cd backend && python main.py

# Terminal 2: Frontend  
cd frontend && npm run dev

# Terminal 3: Demo Script
./scripts/demo-keep-integration.sh
```

### 2. Key Demo Points

#### A. Keep Webhook Integration (1 minute)
```bash
# Show working Keep webhook
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
- ✅ Automatic data mapping

#### B. MSP Noise Reduction (1 minute)
```bash
# Show noise reduction
curl http://localhost:8000/api/v1/alerts/filter-rules
```

**Demo Points:**
- ✅ 80% alert reduction
- ✅ Client-specific filtering
- ✅ SLA-based thresholds

#### C. AI Correlation (1 minute)
```bash
# Show AI agent status
curl http://localhost:8000/api/v1/agents/status
```

**Demo Points:**
- ✅ AWS Bedrock integration
- ✅ Alert correlation
- ✅ Incident grouping

#### D. Frontend Dashboard (1 minute)
Open: `http://localhost:3000/frontend-demo.html`

**Demo Points:**
- ✅ Multi-client selector
- ✅ Real-time updates
- ✅ SLA indicators
- ✅ Noise reduction metrics

### 3. Talking Points

#### Keep Integration Benefits:
1. **Proven Foundation** - Keep's battle-tested alert management
2. **Webhook Compatibility** - Standard Keep webhook format
3. **Database Schema** - PostgreSQL with Keep-compatible tables
4. **Workflow Format** - YAML-based automation
5. **Multi-tenancy** - Secure client isolation

#### MSP Value Add:
1. **80% Noise Reduction** - Intelligent filtering
2. **AI Correlation** - AWS Bedrock integration
3. **SLA Management** - Client-specific routing
4. **Multi-client Dashboard** - Unified view
5. **Cost Optimization** - Reduced alert fatigue

## 🎬 Demo Script

### Opening (30 seconds)
*"Today I'll demonstrate our MSP Alert Intelligence platform, built on Keep's open-source foundation with MSP-specific enhancements for 80% alert reduction and AI-powered correlation."*

### Keep Integration (2 minutes)
1. **Webhook Endpoint** - Show `/api/v1/ingest/keep`
2. **Database Schema** - PostgreSQL with Keep compatibility
3. **Workflow Format** - YAML-based automation
4. **Multi-tenancy** - Client isolation

### MSP Extensions (2 minutes)
1. **Noise Reduction** - 80% alert filtering
2. **AI Correlation** - Bedrock analysis
3. **SLA Management** - Client-specific routing
4. **Dashboard** - Multi-client view

### Live Demo (1 minute)
1. **Frontend** - Real-time dashboard
2. **API** - RESTful endpoints
3. **Metrics** - Performance data
4. **Health** - System status

## 📊 Key Metrics

### Keep Integration:
- ✅ Webhook endpoint working
- ✅ Database schema aligned
- ✅ YAML workflow format
- ✅ Multi-tenant isolation
- ⏳ Provider framework (planned)

### MSP Features:
- ✅ 80% noise reduction
- ✅ AI correlation active
- ✅ SLA management configured
- ✅ Multi-client dashboard
- ✅ Real-time updates

## 🔧 Technical Details

### Architecture:
```
Keep Foundation → MSP Extensions → Frontend Dashboard
├── Webhook Integration
├── Database Schema
├── Workflow Format
├── Multi-tenancy
└── Provider Framework (planned)
```

### Integration Points:
1. **Keep Webhook** - `/api/v1/ingest/keep`
2. **Database** - PostgreSQL with Keep schema
3. **Workflows** - YAML format compatibility
4. **Multi-tenancy** - Tenant isolation
5. **Providers** - 100+ integrations (planned)

## 🎯 Success Criteria

### Demo Must Show:
- ✅ Keep webhook integration working
- ✅ MSP noise reduction active
- ✅ AI correlation functional
- ✅ SLA management configured
- ✅ Frontend dashboard live
- ✅ Real-time processing

### Key Messages:
1. **Keep Foundation** - Proven alert management
2. **MSP Extensions** - 80% noise reduction
3. **AI Integration** - Bedrock correlation
4. **SLA Management** - Client-specific routing
5. **Technical Excellence** - Security, scalability

## 🚀 Demo Flow

1. **Start with Keep** - Show webhook endpoint
2. **Show MSP Extensions** - Noise reduction, AI
3. **Live Demo** - Frontend dashboard
4. **API Demo** - RESTful endpoints
5. **Architecture** - Integration points
6. **Q&A** - Technical questions

## 📝 Backup Plans

### If Backend Fails:
- Show frontend demo mode
- Explain Keep integration architecture
- Highlight MSP features
- Discuss planned integration

### If Frontend Fails:
- Show API endpoints
- Demonstrate webhook integration
- Explain database schema
- Highlight AI features

### If Demo Fails:
- Show code architecture
- Explain Keep compatibility
- Highlight MSP value
- Discuss integration benefits

## 🎬 Demo Checklist

### Before Demo:
- [ ] Backend running (`python main.py`)
- [ ] Frontend running (`npm run dev`)
- [ ] Demo script ready (`./scripts/demo-keep-integration.sh`)
- [ ] Browser open to frontend
- [ ] Terminal ready for API calls

### During Demo:
- [ ] Show Keep webhook endpoint
- [ ] Demonstrate noise reduction
- [ ] Highlight AI correlation
- [ ] Show frontend dashboard
- [ ] Explain integration benefits

### After Demo:
- [ ] Answer technical questions
- [ ] Explain planned integration
- [ ] Highlight MSP value
- [ ] Discuss next steps

## 📞 Support

### Quick Fixes:
- **Backend not starting**: Check Python version, dependencies
- **Frontend not loading**: Check Node.js version, npm install
- **API errors**: Check database connection, environment variables
- **Demo script fails**: Check curl, network connectivity

### Documentation:
- **Keep Integration**: `KEEP_INTEGRATION_DEMO.md`
- **Architecture**: `ARCHITECTURE.md`
- **Setup Guide**: `DEMO_SETUP_GUIDE.md`
- **Demo Script**: `scripts/demo-keep-integration.sh`

---

**Remember**: Be honest about current vs. planned integration while showcasing the working MSP features and Keep compatibility.
