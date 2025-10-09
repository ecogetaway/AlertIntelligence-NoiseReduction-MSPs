# MSP Alert Intelligence & Noise Reduction Platform

A hackathon prototype for an Alert Intelligence & Noise Reduction application targeted at Managed Service Providers (MSPs) for IT infrastructure services. This platform provides alert deduplication, filtering, correlation analysis, and automated processing with AWS Agentic AI integration.

## Features

- 🔍 **Alert Deduplication** - Intelligent deduplication of similar alerts
- 🎯 **Smart Filtering** - AI-powered filtering to reduce noise
- 🔗 **Correlation Analysis** - Automatic correlation of related alerts
- 🤖 **Agentic AI Processing** - AWS Bedrock AgentCore and Strands Agents integration
- 📊 **Real-time Dashboards** - Single pane of glass for alert management
- ⚡ **Automated Workflows** - YAML-based workflows with AI triggers

## Architecture

### Backend
- **Python FastAPI** - Core API server
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

## Acknowledgments

- Built on top of [Keep](https://github.com/keephq/keep) - Open source AIOps platform
- AWS Bedrock AgentCore and Strands Agents for AI integration
- React and Next.js for the frontend framework