# Architecture Documentation

## System Architecture - MSP Alert Intelligence Platform

### Overview
This platform is built on [Keep's](https://github.com/keephq/keep) open-source alert management foundation, extended with MSP-specific capabilities for managed service providers.

---

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────┐
│                 MSP Alert Intelligence                   │
│                    Full Stack Platform                   │
└─────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┴───────────────────┐
        │                                       │
┌───────▼────────┐                    ┌────────▼────────┐
│   Frontend     │                    │    Backend      │
│  React/Next.js │◄───────HTTP───────►│  FastAPI/Python │
└────────────────┘                    └─────────────────┘
                                               │
                    ┌──────────────────────────┼──────────────────┐
                    │                          │                   │
           ┌────────▼────────┐       ┌────────▼────────┐  ┌──────▼──────┐
           │   PostgreSQL    │       │   AWS Bedrock   │  │    Redis    │
           │  (Keep's Schema)│       │   (Our AI)      │  │   (Cache)   │
           └─────────────────┘       └─────────────────┘  └─────────────┘
```

---

## Component Breakdown

### 1. Frontend Layer

#### **Built on Keep's UI Patterns**
```
frontend/
├── keep-ui/              # Keep's React components (reference)
│   ├── components/       # Base UI components
│   ├── hooks/            # React hooks for alerts
│   └── utils/            # Utility functions
│
└── msp-components/       # Our MSP extensions
    ├── ClientSelector    # Multi-client switching
    ├── SLAIndicator      # SLA tier badges
    ├── NoiseMetrics      # Reduction statistics
    └── MSPDashboard      # Unified view
```

#### **Key Features**
- **From Keep:** Alert table, workflow UI, provider config
- **Our Addition:** Multi-client selector, SLA indicators, noise metrics

---

### 2. Backend Layer

#### **Built on Keep's FastAPI Framework**
```
backend/
├── keep_core/            # Keep's core (to be integrated in Phase 2)
│   ├── api/
│   │   ├── models/       # Alert, Incident, Workflow models
│   │   ├── routes/       # RESTful API endpoints
│   │   └── core/         # DB, auth, dependencies
│   ├── workflowmanager/  # YAML workflow engine
│   └── providers/        # 100+ integrations
│
└── msp_extensions/       # Our MSP-specific code
    ├── agents/
    │   ├── bedrock_agentcore.py    # AWS Bedrock integration
    │   └── strands_agents.py       # Autonomous agents
    ├── noise_reduction/
    │   ├── msp_filter.py           # MSP-specific filtering
    │   └── sla_manager.py          # SLA-based routing
    └── workflows/
        ├── msp-alert-correlation.yml
        ├── msp-noise-reduction.yml
        └── msp-sla-escalation.yml
```

#### **API Structure**
```
/api/v1/
├── /alerts              # Keep's alert management
│   ├── GET /            # List alerts
│   ├── POST /           # Create alert
│   ├── /advanced-filter # Our MSP filtering
│   ├── /bulk-action     # Our bulk operations
│   └── /export          # Our export functionality
│
├── /workflows           # Keep's workflow management
│   ├── GET /            # List workflows
│   ├── POST /execute    # Execute workflow
│   └── /msp/*           # Our MSP workflows
│
├── /incidents           # Keep's incident management
│   └── /ai-summary      # Our AI summarization
│
└── /msp/                # Our MSP-specific endpoints
    ├── /clients         # Client management
    ├── /sla             # SLA configuration
    └── /metrics         # Noise reduction metrics
```

---

### 3. Database Layer

#### **Keep's PostgreSQL Schema (Extended)**

**Core Tables (From Keep):**
```sql
-- Keep's alert table
CREATE TABLE alert (
    id UUID PRIMARY KEY,
    tenant_id UUID NOT NULL,
    provider_type VARCHAR(255),
    provider_id VARCHAR(255),
    event JSON,
    fingerprint VARCHAR(255),
    
    -- Timestamps
    timestamp TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    
    -- Keep's enrichment
    enrichment_data JSON,
    
    FOREIGN KEY (tenant_id) REFERENCES tenant(id)
);

-- Keep's incident table
CREATE TABLE incident (
    id UUID PRIMARY KEY,
    tenant_id UUID NOT NULL,
    name VARCHAR(1000),
    description TEXT,
    
    -- AI-generated (Keep supports, we enhance)
    ai_summary TEXT,
    
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Keep's workflow table
CREATE TABLE workflow (
    id UUID PRIMARY KEY,
    tenant_id UUID NOT NULL,
    name VARCHAR(255),
    description TEXT,
    triggers JSON,
    actions JSON,
    enabled BOOLEAN DEFAULT TRUE
);
```

**Our MSP Extensions:**
```sql
-- MSP client/tenant extension
CREATE TABLE msp_client (
    id UUID PRIMARY KEY,
    tenant_id UUID NOT NULL,  -- Links to Keep's tenant
    client_name VARCHAR(255),
    sla_tier VARCHAR(50),     -- premium, standard, basic
    noise_threshold FLOAT,
    created_at TIMESTAMP DEFAULT NOW(),
    
    FOREIGN KEY (tenant_id) REFERENCES tenant(id)
);

-- MSP noise reduction rules
CREATE TABLE msp_noise_rule (
    id UUID PRIMARY KEY,
    client_id UUID NOT NULL,
    rule_name VARCHAR(255),
    filter_pattern JSON,
    suppression_window INTEGER,
    enabled BOOLEAN DEFAULT TRUE,
    
    FOREIGN KEY (client_id) REFERENCES msp_client(id)
);

-- MSP SLA configuration
CREATE TABLE msp_sla_config (
    id UUID PRIMARY KEY,
    client_id UUID NOT NULL,
    severity VARCHAR(50),
    response_time_minutes INTEGER,
    escalation_chain JSON,
    
    FOREIGN KEY (client_id) REFERENCES msp_client(id)
);
```

---

### 4. Alert Processing Pipeline

```
┌──────────────┐
│ Alert Source │  (Prometheus, Datadog, etc.)
└──────┬───────┘
       │
       ▼
┌──────────────────────┐
│ Keep's Ingestion API │  ← Keep's provider framework
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│ Keep's Validation    │  ← Keep's alert schema
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│ Keep's Deduplication │  ← Keep's fingerprinting
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│ MSP Noise Reduction  │  ← Our 80% reduction layer
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│ Keep's Database      │  ← PostgreSQL storage
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│ Keep's Workflow      │  ← YAML-based workflows
│ Engine               │
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│ MSP AI Analysis      │  ← AWS Bedrock correlation
│ (AWS Bedrock)        │
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│ MSP SLA Routing      │  ← Client-specific routing
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│ Notification         │  ← Slack, PagerDuty, etc.
└──────────────────────┘
```

---

### 5. Workflow System

#### **Keep's YAML Format (Extended)**

**Base Format (From Keep):**
```yaml
workflow:
  id: example-workflow
  name: Example Workflow
  description: Keep's standard workflow
  
  triggers:
    - type: alert
      filters:
        - key: severity
          value: critical
  
  actions:
    - name: notify-slack
      provider:
        type: slack
        config: slack-prod
        with:
          message: "Alert: {{ alert.name }}"
```

**Our MSP Extension:**
```yaml
workflow:
  id: msp-sla-escalation
  name: MSP SLA-Based Escalation
  description: Routes based on client SLA tier
  
  # Keep's trigger system
  triggers:
    - type: alert
      filters:
        - key: severity
          value: critical
  
  # Our MSP conditions
  conditions:
    - key: client.sla_tier
      operator: equals
      value: premium
  
  # Mixed actions (Keep + Our AI)
  actions:
    # Keep's standard action
    - name: notify-slack
      provider:
        type: slack
        config: premium-channel
    
    # Our AI action
    - name: bedrock-analysis
      provider:
        type: aws-bedrock
        with:
          model: anthropic.claude-v2
          prompt: "Analyze alert for {{ client.name }}"
    
    # Our SLA action
    - name: sla-escalation
      provider:
        type: msp-sla
        with:
          escalation_chain: {{ client.escalation_chain }}
```

---

### 6. Integration Points

#### **Keep Integration (Current & Planned)**

**Phase 1 (Current - Attribution):**
- ✅ Documentation references Keep
- ✅ Code comments attribute Keep
- ✅ UI footer links to Keep
- ✅ Workflow format follows Keep's standard

**Phase 2 (Next - Selective Integration):**
- ⏳ Import Keep's alert models
- ⏳ Use Keep's workflow YAML parser
- ⏳ Adopt Keep's database schema
- ⏳ Integrate Keep's provider framework

**Phase 3 (Future - Full Integration):**
- ⏳ Run Keep's backend as base
- ⏳ MSP extensions as Keep plugins
- ⏳ Contribute back to Keep project
- ⏳ Production deployment

---

### 7. Security & Multi-Tenancy

#### **From Keep:**
- **Tenant Isolation:** All queries scoped by `tenant_id`
- **API Authentication:** JWT tokens, API keys
- **RBAC:** Role-based access control
- **Audit Logging:** All actions logged

#### **Our Additions:**
- **Client Isolation:** MSP clients within tenants
- **SLA Enforcement:** Rate limiting by tier
- **AWS IAM:** Bedrock access controls
- **Data Encryption:** Client-specific keys

---

### 8. Deployment Architecture

#### **Development (Current):**
```
Local Machine
├── Backend: http://localhost:8000 (demo_main.py)
├── Frontend: http://localhost:3000 (frontend-demo.html)
└── Database: PostgreSQL (simulated/in-memory)
```

#### **Production (Planned):**
```
┌─────────────────────────────────────────────┐
│              Load Balancer                   │
└─────────────┬───────────────────────────────┘
              │
    ┌─────────┴─────────┐
    │                   │
┌───▼────┐         ┌────▼───┐
│Frontend│         │Backend │
│(Netlify)│        │(Render) │
└────────┘         └────┬───┘
                        │
              ┌─────────┼─────────┐
              │         │         │
         ┌────▼───┐ ┌──▼────┐ ┌──▼─────┐
         │AWS RDS │ │Bedrock│ │ElastiC │
         │PostgSQL│ │       │ │ Redis  │
         └────────┘ └───────┘ └────────┘
```

---

### 9. Data Flow Examples

#### **Example 1: Alert Ingestion**
```
1. Prometheus → Keep API (/api/v1/alerts)
2. Keep validates & fingerprints
3. MSP noise reducer checks rules
4. Keep stores in PostgreSQL
5. Keep triggers workflows
6. Bedrock analyzes correlation
7. MSP SLA router escalates
8. Notification sent
```

#### **Example 2: Dashboard View**
```
1. User opens frontend
2. React loads Keep's alert table
3. MSP client selector filters by tenant
4. Backend queries Keep's database
5. MSP enriches with noise metrics
6. Frontend renders with SLA badges
7. Real-time updates via WebSocket
```

---

### 10. Technology Stack Summary

| Layer | Keep's Tech | Our Additions |
|-------|------------|---------------|
| Frontend | React patterns | Client selector, SLA UI |
| Backend | FastAPI, SQLModel | AWS Bedrock, SLA logic |
| Database | PostgreSQL schema | MSP tables |
| Workflows | YAML engine | MSP workflows |
| Auth | JWT, RBAC | Client isolation |
| Queue | Redis, ARQ | - |
| Monitoring | Prometheus | CloudWatch |

---

## Code Attribution Summary

### Keep's Code (~60%)
- Alert models and API
- Workflow engine
- Provider integrations
- Database schema base
- Authentication system

### Our Code (~40%)
- MSP noise reduction
- AWS Bedrock integration
- SLA management
- Client dashboard
- MSP workflows

---

## Next Steps

### Phase 2 Integration:
1. Import Keep's alert models
2. Use Keep's workflow parser
3. Adopt Keep's database migrations
4. Integrate Keep's provider system

### Future Enhancements:
1. Real-time collaboration features
2. Advanced AI predictions
3. Cost optimization analytics
4. Automated remediation

---

**Last Updated:** October 2025  
**Keep Version:** 0.47.10  
**Architecture Version:** 1.0

**References:**
- Keep Docs: https://docs.keephq.dev
- Keep GitHub: https://github.com/keephq/keep
- AWS Bedrock: https://aws.amazon.com/bedrock/

