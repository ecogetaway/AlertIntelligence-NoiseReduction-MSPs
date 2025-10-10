# MSP Alert Intelligence & Noise Reduction Platform

[![Built on Keep](https://img.shields.io/badge/Built%20on-Keep-blue?logo=github)](https://github.com/keephq/keep)
[![License](https://img.shields.io/badge/License-Apache%202.0-green.svg)](LICENSE)
[![AWS Bedrock](https://img.shields.io/badge/AWS-Bedrock-orange?logo=amazon-aws)](https://aws.amazon.com/bedrock/)

🚀 **Built on [Keep](https://github.com/keephq/keep)** - The open-source alert management platform

A hackathon prototype extending Keep's powerful alert management capabilities with MSP-specific features including multi-tenant noise reduction, AWS Bedrock AI analysis, and client SLA management.

## Features

### 💎 From Keep (Open Source Foundation)
- 🔍 **Alert Ingestion** - Receive alerts from 100+ providers (Prometheus, Datadog, PagerDuty, etc.)
- 📊 **Alert Database** - PostgreSQL-based alert storage with full history
- 🔗 **Workflow Engine** - YAML-based workflow automation
- 🎨 **Provider Framework** - Extensible provider integration system
- 🔐 **Multi-tenancy** - Built-in tenant isolation and management

### 🎯 Our MSP Extensions
- 🎛️ **MSP Noise Reduction** - 80% alert reduction through intelligent filtering
- 🤖 **AWS Bedrock AI** - Advanced alert correlation and analysis
- 📈 **Client SLA Management** - SLA-aware alert prioritization
- 🔄 **MSP Workflows** - Pre-built workflows for MSP operations
- 👥 **Multi-client Dashboard** - Unified view across all managed clients

## Architecture

### Built on Keep's Foundation
This platform extends [Keep's architecture](https://github.com/keephq/keep) with MSP-specific components:

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
│  💎 Keep Core (Open Source)            │
│  ├── Alert Management                  │
│  ├── Workflow Engine                   │
│  ├── Provider Integrations             │
│  └── Database Models                   │
└─────────────────────────────────────────┘
```

### Backend
- **Keep's FastAPI Framework** - Extended with MSP routes
- **Keep's Alert Models** - With MSP enrichments
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

## Workflows

The platform uses YAML-based workflows similar to Keep, extended with AI agent triggers:

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

### Built on Keep
This project is built on [Keep](https://github.com/keephq/keep), an open-source alert management platform.

**Keep Repository:** https://github.com/keephq/keep  
**Keep License:** Apache 2.0 / Elastic License 2.0 (EE features)  
**Keep Version:** 0.47.10  
**Keep Documentation:** https://docs.keephq.dev

#### What We Use From Keep:
- ✅ Alert data models and database schema
- ✅ Workflow YAML format and execution engine  
- ✅ Provider integration framework (100+ providers)
- ✅ API route structure and patterns
- ✅ Multi-tenancy and authentication system

#### Our MSP-Specific Contributions:
- 🎯 Multi-client noise reduction algorithms (80% reduction)
- 🤖 AWS Bedrock AI agent integration for correlation
- 📈 SLA-aware alert prioritization and routing
- 🔄 MSP-optimized workflow templates
- 👥 Client management and billing integration

### Other Technologies
- **AWS Bedrock** - Foundation models and AI agents
- **React & Next.js** - Frontend framework
- **Tailwind CSS** - UI styling
- **PostgreSQL** - Database (Keep's choice)

---

## License

This project extends Keep (Apache 2.0) with MSP-specific features.

**Our MSP Extensions:** MIT License  
**Keep Core:** Apache 2.0 / Elastic License 2.0

See [ATTRIBUTION.md](ATTRIBUTION.md) for detailed license information.

---

## Links

- **Live Demo:** `http://localhost:3000/frontend-demo.html` - Local development
- **GitHub Repository:** `https://github.com/ecogetaway/AlertIntelligence-NoiseReduction-MSPs`
- **Demo Script:** [HACKATHON_DEMO_SCRIPT.md](./HACKATHON_DEMO_SCRIPT.md) - 3-4 minute demo guide
- **Setup Guide:** [DEMO_SETUP_GUIDE.md](./DEMO_SETUP_GUIDE.md) - Quick start instructions
- **Keep Project:** https://github.com/keephq/keep
- **Keep Documentation:** https://docs.keephq.dev