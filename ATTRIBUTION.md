# Attribution & Acknowledgments

## 🎯 Project Overview

**MSP Alert Intelligence & Noise Reduction Platform** is built on [Keep](https://github.com/keephq/keep), an open-source alert management platform. This project extends Keep's core capabilities with MSP-specific features for managed service providers.

---

## 💎 Keep - Open Source Alert Management Platform

### Project Information
- **Project Name:** Keep
- **Repository:** https://github.com/keephq/keep
- **Website:** https://www.keephq.dev
- **Documentation:** https://docs.keephq.dev
- **Company:** KeepHQ Ltd.
- **License:** Apache License 2.0 / Elastic License 2.0 (Enterprise features)

### Version Used
- **Keep Version:** 0.47.10
- **Integration Date:** October 2025
- **Repository Reference:** `keep-reference/` directory

---

## ✅ What We Use From Keep

### 1. Core Alert Management
Keep provides the foundational alert management system that we build upon:

- **Alert Data Models** (`keep/api/models/alert.py`)
  - Alert schema with fingerprinting
  - Enrichment data structures
  - Deduplication keys
  - Correlation fields

- **Database Schema** (`keep/api/models/db/`)
  - PostgreSQL models via SQLModel
  - Alert history and audit logs
  - Incident management tables
  - Workflow execution logs

### 2. Workflow Engine
- **YAML-based Workflows** (`keep/workflowmanager/`)
  - Trigger system (alert-based, scheduled, manual)
  - Condition evaluation engine
  - Action execution framework
  - Workflow state management

- **Workflow Format**
  ```yaml
  # Keep's workflow format that we extend
  workflow:
    id: example
    triggers:
      - type: alert
    actions:
      - name: process
        provider: slack
  ```

### 3. Provider Framework
- **Integration System** (`keep/providers/`)
  - 100+ pre-built provider integrations
  - Standard provider interface
  - Authentication management
  - Rate limiting and retry logic

- **Providers We Use:**
  - Prometheus
  - Datadog
  - PagerDuty
  - Slack
  - Email

### 4. API Structure
- **FastAPI Framework** (`keep/api/api.py`)
  - RESTful API patterns
  - Authentication middleware
  - CORS configuration
  - WebSocket support for real-time updates

- **Route Organization** (`keep/api/routes/`)
  - `/alerts` - Alert CRUD operations
  - `/workflows` - Workflow management
  - `/incidents` - Incident handling
  - `/providers` - Provider configuration

### 5. Multi-Tenancy
- **Tenant Isolation** (`keep/api/core/`)
  - Tenant-scoped database queries
  - API key management
  - Role-based access control (RBAC)
  - Tenant configuration

---

## 🎯 Our MSP-Specific Extensions

### What We Built (Not From Keep)

#### 1. MSP Noise Reduction Engine
**Location:** `backend/msp_extensions/noise_reduction/`

```python
# Our custom noise reduction that extends Keep's deduplication
class MSPNoiseReducer:
    """
    MSP-specific noise reduction achieving 80% alert reduction
    - Client-specific thresholds
    - SLA-aware filtering
    - Time-based suppression
    - Business hours awareness
    """
```

**Key Features:**
- Multi-client filtering rules
- SLA tier-based prioritization
- Maintenance window integration
- Client-specific suppression rules

#### 2. AWS Bedrock AI Integration
**Location:** `backend/msp_extensions/agents/`

```python
# Our AWS Bedrock agent integration
class BedrockAlertAnalyzer:
    """
    Uses AWS Bedrock for advanced alert correlation
    - Pattern detection across clients
    - Root cause analysis
    - Automated incident creation
    - Natural language summaries
    """
```

**Key Features:**
- Claude 3 Sonnet for analysis
- Multi-alert correlation
- Incident prediction
- Automated runbook suggestions

#### 3. SLA Management System
**Location:** `backend/msp_extensions/sla/`

```python
# Client SLA management
class SLAManager:
    """
    Manages client SLA tiers and escalations
    - Premium/Standard/Basic tiers
    - Automatic escalation rules
    - SLA breach notifications
    - Response time tracking
    """
```

#### 4. MSP Dashboard
**Location:** `frontend/msp-components/`

- Multi-client selector
- SLA tier indicators
- Noise reduction metrics
- Client billing integration
- MSP-specific analytics

#### 5. Custom Workflows
**Location:** `workflows/`

MSP-optimized workflow templates:
- `msp-alert-correlation.yml` - Cross-client correlation
- `msp-noise-reduction.yml` - Intelligent filtering
- `msp-sla-escalation.yml` - SLA-based routing
- `msp-infrastructure-drift.yml` - Config monitoring

---

## 📊 Code Attribution Breakdown

### Keep's Code (Foundation)
- **Alert Management:** ~70% Keep's models and API
- **Workflow Engine:** ~90% Keep's engine, 10% our extensions
- **Provider System:** ~95% Keep's providers, 5% our custom providers
- **Database:** ~80% Keep's schema, 20% our MSP tables
- **Authentication:** ~100% Keep's auth system

### Our Code (Extensions)
- **Noise Reduction:** ~100% our algorithms
- **AWS Bedrock:** ~100% our integration
- **SLA Management:** ~100% our system
- **MSP Dashboard:** ~70% our components, 30% Keep's UI base
- **MSP Workflows:** ~100% our workflow definitions

### Overall Ratio
- **Keep Foundation:** ~60% of codebase
- **Our MSP Extensions:** ~40% of codebase

---

## 📄 License Information

### Keep's License
Keep is dual-licensed:

1. **Apache License 2.0** (Core features)
   - Alert management
   - Workflow engine
   - Basic providers
   - API framework

2. **Elastic License 2.0** (Enterprise features)
   - Advanced RBAC
   - SSO integration
   - Enterprise providers
   - Premium support

**Full Keep License:** https://github.com/keephq/keep/blob/main/LICENSE

### Our License
Our MSP-specific extensions are licensed under:

**MIT License**
```
MIT License

Copyright (c) 2025 MSP Alert Intelligence Project

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction...
```

### Combined Licensing
- **Keep Core:** Apache 2.0 (compatible with commercial use)
- **Our Extensions:** MIT (permissive, commercial-friendly)
- **Result:** Commercial use allowed with attribution

---

## 🔗 References & Links

### Keep Project
- **GitHub:** https://github.com/keephq/keep
- **Website:** https://www.keephq.dev
- **Documentation:** https://docs.keephq.dev
- **Community:** https://slack.keephq.dev
- **Blog:** https://www.keephq.dev/blog

### Keep Maintainers
- **Company:** KeepHQ Ltd.
- **Team:** https://github.com/orgs/keephq/people
- **Contact:** https://www.keephq.dev/contact

### Our Project
- **Repository:** https://github.com/ecogetaway/AlertIntelligence-NoiseReduction-MSPs
- **Demo:** [Your Netlify URL]
- **Documentation:** See README.md

---

## 🙏 Acknowledgments

### Special Thanks

**To the Keep Team:**
- For building an excellent open-source alert management platform
- For clean, well-documented code that's easy to extend
- For the comprehensive provider ecosystem
- For active community support

**To the Community:**
- Keep community for workflow examples
- AWS Bedrock team for AI agent documentation
- Open-source contributors

---

## 🤝 Contributing Back to Keep

We plan to contribute the following back to Keep's open-source project:

### Potential Contributions
1. **MSP Provider Templates** - Workflow templates for MSP use cases
2. **Noise Reduction Patterns** - Filtering patterns that could be generalized
3. **Documentation** - MSP-specific setup guides
4. **Bug Fixes** - Any bugs we discover while integrating

### Contribution Process
1. Open issue in Keep's repository
2. Discuss with Keep maintainers
3. Submit pull request with tests
4. Follow Keep's contribution guidelines

---

## 📝 Required Attribution

When using this project, please include attribution to Keep:

### In Documentation
```markdown
Built on [Keep](https://github.com/keephq/keep) - 
Open-source alert management platform
```

### In UI
```
Powered by Keep Alert Management
https://www.keephq.dev
```

### In Code
```python
# Based on Keep's alert management system
# https://github.com/keephq/keep
# Licensed under Apache 2.0
```

---

## 📧 Contact

### For Keep-Related Questions
- **Keep Slack:** https://slack.keephq.dev
- **Keep GitHub Issues:** https://github.com/keephq/keep/issues

### For Our MSP Extensions
- **GitHub Issues:** [Your issues URL]
- **Email:** [Your contact email]

---

**Last Updated:** October 2025  
**Keep Version:** 0.47.10  
**Our Version:** 1.0.0 (Hackathon Prototype)

