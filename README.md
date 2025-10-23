# MSP Alert Intelligence & Noise Reduction Platform

[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![AWS Bedrock](https://img.shields.io/badge/AWS-Bedrock-orange?logo=amazon-aws)](https://aws.amazon.com/bedrock/)

🚀 Enhanced prototype showcasing AI-powered alert intelligence for MSPs with **Keep**, **Amazon Bedrock**, and **Strands Agents** integration.

## 🎯 Integration Status: ✅ COMPLETE

**Latest Update (Oct 20, 2025):** Successfully integrated with:
- ✅ **Keep Platform** - Webhook ingestion, HMAC verification, alert mapping
- ✅ **Amazon Bedrock** - Claude 3 Sonnet for AI triage and summarization  
- ✅ **Strands Agents** - Multi-agent correlation and incident grouping
- ✅ **Full Backend API** - RESTful endpoints for alert management
- ✅ **Live Frontend** - Deployed to Netlify with Live Mode demo

**Quick Links:**
- 🌐 **[Live Demo (Netlify)](https://msp-alert-intelligence.netlify.app)** - Frontend with Live Mode
- 📖 **[Integration Guide](KEEP_INTEGRATION_GUIDE.md)** - Setup and configuration
- 📊 **[Prototype Status](PROTOTYPE_STATUS.md)** - Current deployment status
- 🔧 **[Integration Complete](INTEGRATION_COMPLETE.md)** - Technical details

## Features

### 💎 Keep Integration (Current & Planned)
- 🔍 **Keep Webhook Integration** - ✅ Working webhook endpoint (`/api/v1/ingest/keep`)
- 📊 **Database Schema Alignment** - ✅ PostgreSQL with Keep-compatible schema
- 🔗 **YAML Workflow Format** - ✅ Keep-compatible workflow definitions
- 🎨 **Provider Framework** - ⏳ Planned integration with Keep's 100+ providers
- 🔐 **Multi-tenancy** - ✅ Tenant isolation with MSP client management

### 🎯 Our MSP Extensions
- 🎛️ **MSP Noise Reduction** - 80% alert reduction through intelligent filtering
- 🤖 **AWS Bedrock AI** - Advanced alert correlation and analysis
- 📈 **Client SLA Management** - SLA-aware alert prioritization
- 🔄 **MSP Workflows** - Pre-built workflows for MSP operations
- 👥 **Multi-client Dashboard** - Unified view across all managed clients

## Architecture

### Architecture Overview
This platform provides MSP-specific components and can optionally integrate with Keep in production:

```
┌─────────────────────────────────────────┐
│        MSP Alert Intelligence           │
├─────────────────────────────────────────┤
│  🎯 MSP Extensions (Our Code)          │
│  ├── Noise Reduction Layer             │
│  ├── AWS Bedrock AI Agents             │
│  ├── SLA Management                    │
│  └── MSP-specific Workflows            │
├─────────────────────────────────────────┤
│  💎 Foundation (Planned Integration)   │
│  ├── Alert Management (Keep optional)  │
│  ├── Workflow Engine (Keep optional)   │
│  ├── Provider Integrations (Keep opt.) │
│  └── Database Models                   │
└─────────────────────────────────────────┘
```

### Backend
- **FastAPI** - MSP routes and services
- **Alert Models** - With MSP enrichments
- **AWS Bedrock AgentCore** - Dynamic agent orchestration
- **Strands Agents** - Autonomous AI agents for processing
- **PostgreSQL** - Alert and incident storage
- **Redis** - Caching and session management

### Frontend
- **React 19** - Modern UI framework
- **Next.js 15** - Full-stack React framework
- **Tailwind CSS** - Utility-first styling
- **Shadcn/ui** - Component library
- **Recharts** - Data visualization

### AI Integration
- **Amazon Bedrock** - Foundation models
- **AgentCore Runtime** - Secure agent deployment
- **Strands Agents SDK** - Model-driven AI agents
- **OpenAI/Anthropic** - Additional AI backends

## Quick Start

### Demo Version (No AWS Credentials Required)

For a quick demo with simulated AI agents:

```bash
# Clone and setup demo
git clone https://github.com/ecogetaway/AlertIntelligence-NoiseReduction-MSPs.git
cd AlertIntelligence-NoiseReduction-MSPs

# Setup demo environment
./scripts/demo-setup.sh

# Start all services
docker-compose up -d

# Access application
open http://localhost
```

### Production Setup

### Prerequisites
- Node.js 18+
- Python 3.11+
- AWS CLI configured
- Docker and Docker Compose

### Installation

1. **Clone and setup**
```bash
git clone https://github.com/ecogetaway/AlertIntelligence-NoiseReduction-MSPs.git
cd AlertIntelligence-NoiseReduction-MSPs
```

2. **Backend setup**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. **Frontend setup**
```bash
cd frontend
npm install
```

4. **Environment configuration**
```bash
cp .env.example .env
# Configure your AWS credentials and other settings
```

5. **Start the application**
```bash
# Start backend
cd backend
python main.py

# Start frontend (in another terminal)
cd frontend
npm run dev
```

## Development

### Project Structure
```
msp-alert-app/
├── backend/                 # Python FastAPI backend
│   ├── agents/             # AWS AgentCore and Strands agents
│   ├── api/                # API routes and controllers
│   ├── core/               # Core business logic
│   ├── models/             # Data models
│   ├── providers/           # Alert providers (Prometheus, Datadog, etc.)
│   ├── workflows/          # YAML workflow definitions
│   └── main.py            # Application entry point
├── frontend/               # React Next.js frontend
│   ├── app/                # Next.js app directory
│   ├── components/         # Reusable UI components
│   ├── features/          # Feature-specific components
│   ├── lib/               # Utilities and configurations
│   └── public/             # Static assets
├── workflows/              # YAML workflow definitions
├── tests/                  # Test files
└── docs/                   # Documentation
```

### Key Components

#### Alert Processing Pipeline
1. **Ingestion** - Receive alerts from various sources
2. **Deduplication** - Remove duplicate alerts using fingerprinting
3. **Enrichment** - Add context using AI agents
4. **Correlation** - Group related alerts
5. **Filtering** - Apply noise reduction rules
6. **Routing** - Send to appropriate workflows

#### AI Agent Integration
- **Alert Correlation Agent** - Groups related alerts
- **Enrichment Agent** - Adds context and metadata
- **Decision Agent** - Makes routing and escalation decisions
- **Summary Agent** - Creates incident summaries

## Workflows (Optional)

The platform supports YAML-based workflows and can align with Keep workflows in production. Example:

```yaml
workflow:
  id: msp-alert-correlation
  name: MSP Alert Correlation
  description: Correlate related alerts using AI agents
  triggers:
    - type: alert
      conditions:
        - severity: high
  actions:
    - name: correlate-alerts
      provider:
        type: bedrock-agent
        with:
          agent: correlation-agent
          model: claude-3-sonnet
    - name: create-incident
      provider:
        type: strands-agent
        with:
          agent: incident-creation-agent
```

## Testing

### E2E Testing with Playwright
```bash
npm run test:e2e
```

### Unit Testing
```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

## Deployment

### AWS Deployment
```bash
# Deploy to AWS using CDK
cd infrastructure
npm install
cdk deploy
```

### Docker Deployment
```bash
docker-compose up -d
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Acknowledgments & Attribution

### Built on Keep Foundation

This project integrates with [Keep](https://github.com/keephq/keep), an open-source alert management platform.

**Keep Repository:** https://github.com/keephq/keep  
**Keep License:** Apache 2.0 / Elastic License 2.0 (EE features)  
**Keep Version:** 0.47.10  
**Keep Documentation:** https://docs.keephq.dev

#### What We Use From Keep:
- ✅ **Webhook Integration** - Keep's alert webhook format
- ✅ **Database Schema** - PostgreSQL with Keep-compatible tables
- ✅ **Workflow Format** - YAML-based workflow definitions
- ✅ **Multi-tenancy** - Tenant isolation and management
- ⏳ **Provider Framework** - 100+ monitoring integrations (planned)

#### Our MSP-Specific Contributions:
- 🎯 **Multi-client Noise Reduction** - 80% alert reduction algorithms
- 🤖 **AWS Bedrock AI Integration** - Advanced correlation and analysis
- 📈 **SLA-aware Alert Routing** - Client-specific prioritization
- 🔄 **MSP Workflow Templates** - Pre-built automation
- 👥 **Multi-client Dashboard** - Unified management view

### Other Technologies
- **AWS Bedrock** - Foundation models and AI agents
- **React & Next.js** - Frontend framework
- **Tailwind CSS** - UI styling
- **PostgreSQL** - Database (Keep's choice)

---

## License

**MSP Demo:** MIT License

See [ATTRIBUTION.md](ATTRIBUTION.md) for third‑party license information and planned production integrations.

---

## 🚀 Live Demo

Experience the MSP Alert Intelligence platform live:

- **Vercel Deployment**: https://msp-alert-app.vercel.app
- **Netlify Deployment**: https://msp-alert-intelligence.netlify.app

**Features:**
- ✅ Zero backend - runs entirely in browser
- ✅ Live mode simulation with realistic data
- ✅ 8-second update cadence
- ✅ Interactive filters and bulk operations
- ✅ Analytics and incident correlation

## Links

- **Live Demo:** https://msp-alert-app.vercel.app (Vercel) or https://msp-alert-intelligence.netlify.app (Netlify)
- **Local Development:** `http://localhost:3000/frontend-demo.html`
- **GitHub Repository:** `https://github.com/ecogetaway/AlertIntelligence-NoiseReduction-MSPs`
- **Demo Script:** [DEMO_SCRIPT_LIVE_MODE.md](./DEMO_SCRIPT_LIVE_MODE.md) - 3-4 minute demo guide
- **Setup Guide:** [DEMO_SETUP_GUIDE.md](./DEMO_SETUP_GUIDE.md) - Quick start instructions
- **Keep Project (for production consideration):** https://github.com/keephq/keep
- **Keep Documentation:** https://docs.keephq.dev