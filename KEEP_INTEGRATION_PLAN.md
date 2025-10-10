# Keep Integration Plan - Full Implementation

## 🎯 **Goal: Build MSP Alert Intelligence on Keep's Foundation**

This document outlines the complete integration of Keep's open-source alert management platform with our MSP-specific features.

---

## 📋 **Phase 1: Keep Core Integration (Current)**

### **1.1 Backend Structure**
- ✅ **Copy Keep's core modules** to our backend
- ✅ **Use Keep's FastAPI structure** as foundation
- ✅ **Import Keep's alert models** and database schema
- ✅ **Integrate Keep's workflow engine**
- ✅ **Use Keep's provider system** for integrations

### **1.2 Database & Models**
```
backend/
├── keep_core/              # Keep's core code (imported)
│   ├── api/
│   │   ├── models/         # Alert, Incident, Workflow models
│   │   ├── core/           # DB, config, dependencies
│   │   └── routes/         # Alert, incident, workflow routes
│   ├── workflowmanager/    # Workflow execution engine
│   └── providers/          # Provider integrations
├── msp_extensions/         # Our MSP-specific additions
│   ├── agents/             # AWS Bedrock, Strands agents
│   ├── noise_reduction/    # MSP-focused filtering
│   └── workflows/          # MSP-specific workflows
└── main.py                 # Entry point (extends Keep)
```

### **1.3 Key Keep Components to Use**

#### **Alert Management (`keep/api/core/alerts.py`)**
- Alert ingestion and storage
- Alert enrichment
- Alert deduplication (Keep's existing system)
- Alert search and filtering

#### **Workflow Engine (`keep/workflowmanager/`)**
- YAML-based workflow definitions
- Trigger system
- Action execution
- Condition evaluation

#### **Database Models (`keep/api/models/db/`)**
- Alert model with enrichments
- Incident model
- Workflow model
- Provider model

#### **API Routes (`keep/api/routes/`)**
- `/alerts` - Alert CRUD operations
- `/workflows` - Workflow management
- `/incidents` - Incident management
- `/providers` - Provider integrations

---

## 📋 **Phase 2: MSP Extensions (Next)**

### **2.1 MSP-Specific Features**

#### **Noise Reduction Engine** (extends Keep's deduplication)
```python
# msp_extensions/noise_reduction/msp_filter.py
from keep.api.alert_deduplicator import alert_deduplicator
from keep.api.core.alerts import AlertManager

class MSPNoiseReducer:
    """
    Extends Keep's deduplication with MSP-specific rules:
    - Multi-tenant filtering
    - Client-specific thresholds
    - Time-based suppression
    - SLA-aware prioritization
    """
    
    def __init__(self, base_deduplicator):
        self.base_deduplicator = base_deduplicator
        self.msp_rules = self.load_msp_rules()
    
    async def process_alert(self, alert, tenant_id):
        # First, use Keep's deduplication
        is_duplicate = await self.base_deduplicator.is_duplicate(alert)
        
        if is_duplicate:
            return None
        
        # Apply MSP-specific noise reduction
        if self.should_suppress_for_msp(alert, tenant_id):
            return None
        
        # Enrich with MSP context
        alert = self.enrich_with_client_info(alert, tenant_id)
        
        return alert
```

#### **AWS Bedrock Integration**
```python
# msp_extensions/agents/bedrock_agent.py
from keep.api.core.workflows import WorkflowManager
import boto3

class BedrockAlertAnalyzer:
    """
    Uses AWS Bedrock to analyze and correlate alerts
    Integrates with Keep's workflow system
    """
    
    def __init__(self, workflow_manager: WorkflowManager):
        self.workflow_manager = workflow_manager
        self.bedrock = boto3.client('bedrock-runtime')
    
    async def analyze_alert_pattern(self, alerts):
        """
        Trigger Keep workflow with AI analysis
        """
        analysis = await self.call_bedrock_model(alerts)
        
        # Create incident via Keep's API
        incident = await self.workflow_manager.create_incident(
            title=analysis['incident_title'],
            alerts=alerts,
            ai_summary=analysis['summary']
        )
        
        return incident
```

### **2.2 MSP-Specific Workflows**

#### **Client SLA Escalation** (extends Keep workflows)
```yaml
# workflows/msp-sla-escalation.yml
id: msp-sla-escalation
name: MSP SLA-Based Escalation
description: Escalate based on client SLA tier

triggers:
  - type: alert
    filters:
      - key: severity
        value: critical

actions:
  # Use Keep's actions
  - name: check-sla-tier
    type: condition
    with:
      value: "{{ alert.tenant.sla_tier }}"
  
  - name: notify-premium-clients
    condition: "{{ alert.tenant.sla_tier == 'premium' }}"
    type: slack
    with:
      channel: "#premium-alerts"
  
  # Custom MSP action
  - name: aws-bedrock-analysis
    type: aws-bedrock
    with:
      model: "anthropic.claude-v2"
      prompt: "Analyze this alert for MSP client: {{ alert.tenant.name }}"
```

---

## 📋 **Phase 3: Frontend Integration**

### **3.1 Keep UI Components**

Keep uses Next.js with:
- `keep-ui/app/` - Next.js 13+ app directory
- `keep-ui/components/` - React components
- `keep-ui/utils/` - Utility functions

#### **Reuse Keep's Alert Table**
```typescript
// frontend/components/alert-table.tsx
// Import from Keep's UI
import { AlertTable } from '@/keep-ui/components/alerts/alert-table';
import { useAlerts } from '@/keep-ui/hooks/useAlerts';

export function MSPAlertDashboard() {
  const { alerts, loading } = useAlerts();
  
  return (
    <div>
      {/* Keep's existing alert table */}
      <AlertTable alerts={alerts} loading={loading} />
      
      {/* Add MSP-specific filters */}
      <MSPClientFilter />
      <MSPSLATierFilter />
    </div>
  );
}
```

### **3.2 MSP Dashboard Extensions**
- Client selector (multi-tenant view)
- SLA tier indicators
- Noise reduction metrics
- AWS Bedrock insights panel

---

## 📋 **Phase 4: Deployment & Configuration**

### **4.1 Docker Setup (Use Keep's structure)**
```yaml
# docker-compose.yml (extends Keep's)
version: "3.8"

services:
  keep-backend:
    build:
      context: ./keep-reference
      dockerfile: docker/Dockerfile.api
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - AWS_REGION=${AWS_REGION}
      - BEDROCK_ENDPOINT=${BEDROCK_ENDPOINT}
    volumes:
      - ./msp_extensions:/app/msp_extensions
  
  msp-frontend:
    build: ./frontend
    environment:
      - NEXT_PUBLIC_API_URL=http://keep-backend:8080
  
  keep-ui:
    build:
      context: ./keep-reference
      dockerfile: docker/Dockerfile.ui
    
  postgres:
    image: postgres:13
    # Keep's database schema
```

### **4.2 Environment Configuration**
```bash
# .env
# Keep configuration
DATABASE_URL=postgresql://user:pass@localhost:5432/keep
KEEP_API_KEY=your-api-key

# MSP Extensions
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your-key
AWS_SECRET_ACCESS_KEY=your-secret
BEDROCK_MODEL_ID=anthropic.claude-v2

# Multi-tenant support
ENABLE_MULTI_TENANT=true
DEFAULT_SLA_TIER=standard
```

---

## 📋 **Implementation Timeline**

### **Week 1: Core Integration**
- [ ] Day 1-2: Copy Keep's core modules
- [ ] Day 3-4: Set up Keep's database schema
- [ ] Day 5-7: Integrate Keep's API routes

### **Week 2: MSP Extensions**
- [ ] Day 1-2: Build noise reduction on top of Keep
- [ ] Day 3-4: Integrate AWS Bedrock agents
- [ ] Day 5-7: Create MSP-specific workflows

### **Week 3: Frontend & Testing**
- [ ] Day 1-3: Adapt Keep's UI components
- [ ] Day 4-5: Add MSP dashboard features
- [ ] Day 6-7: End-to-end testing

### **Hackathon Timeline (Accelerated)**
- [ ] Hour 1-4: Setup Keep core (use existing installation)
- [ ] Hour 5-8: Add MSP noise reduction layer
- [ ] Hour 9-12: Create demo workflows
- [ ] Hour 13-16: Frontend demo integration
- [ ] Hour 17-20: Testing & refinement
- [ ] Hour 21-24: Documentation & presentation

---

## 🔧 **Technical Architecture**

### **Request Flow**
```
1. Alert Ingestion
   → Keep's alert API endpoint
   → Keep's validation & enrichment
   → MSP noise reduction filter
   → Keep's database storage

2. Workflow Execution
   → Keep's workflow engine
   → MSP-specific actions (Bedrock)
   → Keep's notification system

3. Dashboard Display
   → Keep's UI components
   → MSP client filtering
   → Real-time updates via Keep's WebSocket
```

### **Code Organization**
```
msp-alert-app/
├── keep-reference/          # Keep repository (submodule)
├── backend/
│   ├── keep_core/          # Symlink to keep-reference/keep
│   ├── msp_extensions/     # Our additions
│   └── main.py             # Extends Keep's app
├── frontend/
│   ├── keep-ui/            # Symlink to keep-reference/keep-ui
│   └── msp-components/     # Our additions
└── docker-compose.yml      # Extends Keep's setup
```

---

## 📚 **Attribution & Licensing**

### **Keep Project**
- **Repository**: https://github.com/keephq/keep
- **License**: Apache 2.0 / Elastic License 2.0 (EE features)
- **Attribution**: "Built on Keep by KeepHQ"

### **Our MSP Extensions**
- **License**: [Your choice - compatible with Keep]
- **Features**: Noise reduction, AWS Bedrock, MSP workflows
- **Documentation**: Clear separation of Keep vs our code

### **README Example**
```markdown
# MSP Alert Intelligence Platform

Built on [Keep](https://github.com/keephq/keep), the open-source alert management platform.

## What's Keep vs What's Ours

### From Keep (✨)
- Alert ingestion & enrichment
- Workflow engine (YAML-based)
- Provider integrations
- Web UI components

### Our MSP Extensions (🚀)
- Multi-tenant noise reduction
- AWS Bedrock AI analysis
- MSP-specific workflows
- Client SLA management
```

---

## 🎯 **Success Criteria**

### **Functional**
- [ ] Alerts flow through Keep's system
- [ ] MSP noise reduction reduces by 80%
- [ ] Workflows execute with AWS Bedrock
- [ ] Dashboard shows Keep + MSP features

### **Technical**
- [ ] Keep's code properly imported
- [ ] Database uses Keep's schema
- [ ] API follows Keep's patterns
- [ ] UI extends Keep's components

### **Documentation**
- [ ] Clear attribution to Keep
- [ ] Separation of Keep vs our code
- [ ] Setup instructions
- [ ] Architecture diagram

---

## 🚀 **Next Steps**

1. **Set up Keep as Git submodule**
   ```bash
   git submodule add https://github.com/keephq/keep.git keep-reference
   ```

2. **Create symlinks to Keep's code**
   ```bash
   ln -s ../keep-reference/keep backend/keep_core
   ln -s ../keep-reference/keep-ui frontend/keep-ui
   ```

3. **Install Keep's dependencies**
   ```bash
   cd keep-reference
   pip install -e .
   ```

4. **Extend Keep's FastAPI app**
   ```python
   # backend/main.py
   from keep.api.api import get_app as get_keep_app
   from msp_extensions.routes import msp_router
   
   app = get_keep_app()
   app.include_router(msp_router, prefix="/api/msp")
   ```

5. **Start building MSP extensions**

---

**Ready to proceed with full integration!** 🚀

