# MSP Alert Intelligence Platform - Architecture Diagrams

## High-Level System Architecture

```mermaid
graph TB
    subgraph "MSP Alert Intelligence Platform"
        subgraph "Frontend Layer"
            UI[React/Next.js Dashboard]
            Components[Alert Components]
            Analytics[Analytics Dashboard]
            Export[Export Functionality]
        end
        
        subgraph "Backend Layer"
            API[FastAPI Backend]
            Agents[AI Agents]
            Workflows[Workflow Engine]
            Filters[Noise Reduction]
        end
        
        subgraph "Data Layer"
            DB[(PostgreSQL Database)]
            Cache[(Redis Cache)]
            Storage[(File Storage)]
        end
        
        subgraph "AI Services"
            Bedrock[AWS Bedrock]
            Strands[Strands Agents]
            Models[Foundation Models]
        end
        
        subgraph "External Integrations"
            Prometheus[Prometheus]
            Datadog[Datadog]
            PagerDuty[PagerDuty]
            Slack[Slack]
        end
    end
    
    %% Connections
    UI --> API
    Components --> API
    Analytics --> API
    Export --> API
    
    API --> Agents
    API --> Workflows
    API --> Filters
    API --> DB
    API --> Cache
    
    Agents --> Bedrock
    Agents --> Strands
    Bedrock --> Models
    Strands --> Models
    
    Workflows --> Prometheus
    Workflows --> Datadog
    Workflows --> PagerDuty
    Workflows --> Slack
    
    DB --> Storage
```

## Alert Processing Pipeline

```mermaid
flowchart TD
    A[Alert Sources] --> B[Keep Ingestion API]
    B --> C[Alert Validation]
    C --> D[Keep Deduplication]
    D --> E[MSP Noise Reduction]
    E --> F{Noise Filter}
    F -->|Suppress| G[Suppressed Alert]
    F -->|Process| H[Store in Database]
    H --> I[AI Correlation Analysis]
    I --> J[Incident Creation]
    J --> K[SLA Routing]
    K --> L[Notification/Workflow]
    L --> M[Dashboard Update]
    
    subgraph "AI Processing"
        I --> N[AWS Bedrock]
        N --> O[Correlation Agent]
        O --> P[Summary Agent]
        P --> Q[Decision Agent]
    end
    
    subgraph "MSP Features"
        E --> R[Client-Specific Rules]
        K --> S[SLA Tier Routing]
        S --> T[Escalation Chain]
    end
```

## Component Architecture

```mermaid
graph LR
    subgraph "Frontend Components"
        A[AlertTable]
        B[FilterPanel]
        C[BulkOperations]
        D[AnalyticsChart]
        E[ExportButton]
    end
    
    subgraph "Backend Services"
        F[AlertService]
        G[CorrelationService]
        H[NoiseReductionService]
        I[WorkflowService]
        J[AnalyticsService]
    end
    
    subgraph "AI Agents"
        K[DeduplicationAgent]
        L[CorrelationAgent]
        M[SummaryAgent]
        N[DecisionAgent]
    end
    
    subgraph "Data Models"
        O[Alert Model]
        P[Incident Model]
        Q[Client Model]
        R[Workflow Model]
    end
    
    A --> F
    B --> F
    C --> F
    D --> J
    E --> F
    
    F --> K
    G --> L
    H --> M
    I --> N
    
    F --> O
    G --> P
    H --> Q
    I --> R
```

## Data Flow Architecture

```mermaid
sequenceDiagram
    participant Client as MSP Client
    participant Frontend as React Dashboard
    participant Backend as FastAPI
    participant AI as AI Agents
    participant DB as PostgreSQL
    participant External as External APIs
    
    Client->>Frontend: View Dashboard
    Frontend->>Backend: GET /api/alerts
    Backend->>DB: Query Alerts
    DB-->>Backend: Alert Data
    Backend->>AI: Analyze Alerts
    AI-->>Backend: Correlation Results
    Backend-->>Frontend: Processed Alerts
    Frontend-->>Client: Display Dashboard
    
    Note over Client,External: Alert Processing Flow
    
    External->>Backend: New Alert
    Backend->>AI: Deduplication Check
    AI-->>Backend: Is Duplicate?
    Backend->>AI: Noise Reduction
    AI-->>Backend: Filter Decision
    Backend->>DB: Store Alert
    Backend->>AI: Correlation Analysis
    AI-->>Backend: Incident Creation
    Backend->>External: Notifications
    Backend-->>Frontend: Real-time Update
```

## Deployment Architecture

```mermaid
graph TB
    subgraph "Production Environment"
        subgraph "Load Balancer"
            LB[NGINX Load Balancer]
        end
        
        subgraph "Application Tier"
            FE1[Frontend Instance 1]
            FE2[Frontend Instance 2]
            BE1[Backend Instance 1]
            BE2[Backend Instance 2]
        end
        
        subgraph "Data Tier"
            DB1[(PostgreSQL Primary)]
            DB2[(PostgreSQL Replica)]
            REDIS[(Redis Cluster)]
        end
        
        subgraph "AI Services"
            BEDROCK[AWS Bedrock]
            LAMBDA[Lambda Functions]
        end
        
        subgraph "Monitoring"
            PROM[Prometheus]
            GRAF[Grafana]
            LOGS[ELK Stack]
        end
    end
    
    LB --> FE1
    LB --> FE2
    LB --> BE1
    LB --> BE2
    
    BE1 --> DB1
    BE2 --> DB1
    BE1 --> REDIS
    BE2 --> REDIS
    
    BE1 --> BEDROCK
    BE2 --> BEDROCK
    BE1 --> LAMBDA
    BE2 --> LAMBDA
    
    DB1 --> DB2
    
    BE1 --> PROM
    BE2 --> PROM
    PROM --> GRAF
    BE1 --> LOGS
    BE2 --> LOGS
```

## Technology Stack Architecture

```mermaid
graph TB
    subgraph "Frontend Stack"
        REACT[React 19]
        NEXT[Next.js 15]
        TAILWIND[Tailwind CSS]
        SHADCN[Shadcn/ui]
        RECHARTS[Recharts]
    end
    
    subgraph "Backend Stack"
        FASTAPI[FastAPI]
        PYTHON[Python 3.11]
        SQLMODEL[SQLModel]
        PYDANTIC[Pydantic]
        ASYNCIO[AsyncIO]
    end
    
    subgraph "Database Stack"
        POSTGRES[PostgreSQL]
        REDIS[Redis]
        ALEMBIC[Alembic Migrations]
        SQLALCHEMY[SQLAlchemy]
    end
    
    subgraph "AI Stack"
        BEDROCK[AWS Bedrock]
        STRANDS[Strands Agents]
        CLAUDE[Claude-3-Sonnet]
        OPENAI[OpenAI GPT-4]
    end
    
    subgraph "Infrastructure"
        DOCKER[Docker]
        K8S[Kubernetes]
        AWS[AWS Services]
        CDN[CloudFront CDN]
    end
    
    REACT --> FASTAPI
    NEXT --> FASTAPI
    TAILWIND --> REACT
    SHADCN --> REACT
    RECHARTS --> REACT
    
    FASTAPI --> POSTGRES
    FASTAPI --> REDIS
    FASTAPI --> BEDROCK
    FASTAPI --> STRANDS
    
    BEDROCK --> CLAUDE
    STRANDS --> OPENAI
    
    DOCKER --> K8S
    K8S --> AWS
    AWS --> CDN
```

## Keep Integration Architecture

```mermaid
graph TB
    subgraph "Keep Foundation (Open Source)"
        KEEP_API[Keep API Routes]
        KEEP_MODELS[Keep Data Models]
        KEEP_WORKFLOWS[Keep Workflow Engine]
        KEEP_PROVIDERS[Keep Provider Framework]
    end
    
    subgraph "MSP Extensions (Our Code)"
        MSP_ROUTES[MSP API Routes]
        MSP_AGENTS[MSP AI Agents]
        MSP_FILTERS[MSP Noise Reduction]
        MSP_SLA[MSP SLA Management]
    end
    
    subgraph "Integration Layer"
        API_GATEWAY[API Gateway]
        WORKFLOW_ENGINE[Workflow Engine]
        AI_ORCHESTRATOR[AI Orchestrator]
    end
    
    KEEP_API --> API_GATEWAY
    MSP_ROUTES --> API_GATEWAY
    
    KEEP_WORKFLOWS --> WORKFLOW_ENGINE
    MSP_AGENTS --> AI_ORCHESTRATOR
    
    API_GATEWAY --> KEEP_MODELS
    API_GATEWAY --> MSP_FILTERS
    
    WORKFLOW_ENGINE --> KEEP_PROVIDERS
    AI_ORCHESTRATOR --> MSP_SLA
```

## Client Multi-Tenancy Architecture

```mermaid
graph TB
    subgraph "MSP Platform"
        subgraph "Client A (Premium)"
            CA_ALERTS[Client A Alerts]
            CA_SLA[Premium SLA Rules]
            CA_AI[Enhanced AI Processing]
        end
        
        subgraph "Client B (Standard)"
            CB_ALERTS[Client B Alerts]
            CB_SLA[Standard SLA Rules]
            CB_AI[Standard AI Processing]
        end
        
        subgraph "Client C (Basic)"
            CC_ALERTS[Client C Alerts]
            CC_SLA[Basic SLA Rules]
            CC_AI[Basic AI Processing]
        end
        
        subgraph "Shared Services"
            SHARED_AI[Shared AI Agents]
            SHARED_DB[Shared Database]
            SHARED_CACHE[Shared Cache]
        end
    end
    
    CA_ALERTS --> SHARED_AI
    CB_ALERTS --> SHARED_AI
    CC_ALERTS --> SHARED_AI
    
    CA_SLA --> SHARED_DB
    CB_SLA --> SHARED_DB
    CC_SLA --> SHARED_DB
    
    CA_AI --> SHARED_CACHE
    CB_AI --> SHARED_CACHE
    CC_AI --> SHARED_CACHE
```

## Performance Metrics Architecture

```mermaid
graph LR
    subgraph "Metrics Collection"
        A[Alert Processing Metrics]
        B[AI Agent Performance]
        C[Database Performance]
        D[API Response Times]
    end
    
    subgraph "Analytics Engine"
        E[Real-time Analytics]
        F[Historical Trends]
        G[Predictive Analysis]
        H[Performance Optimization]
    end
    
    subgraph "Visualization"
        I[Dashboard Charts]
        J[Alert Trends]
        K[Noise Reduction Stats]
        L[Correlation Accuracy]
    end
    
    A --> E
    B --> F
    C --> G
    D --> H
    
    E --> I
    F --> J
    G --> K
    H --> L
```

---

## Usage Instructions

To use these Mermaid diagrams:

1. **Copy the diagram code** from any section above
2. **Paste into Mermaid Live Editor**: https://mermaid.live/
3. **Or use in documentation**: GitHub, GitLab, and many platforms support Mermaid
4. **Or use in presentations**: Export as PNG/SVG for slides

## Key Architecture Benefits

- **Modular Design**: Clear separation of concerns
- **Scalable Architecture**: Horizontal scaling capabilities
- **AI-First Approach**: Intelligent processing at every layer
- **MSP-Optimized**: Built specifically for managed service providers
- **Production-Ready**: Built on proven Keep foundation
- **Cloud-Native**: Designed for modern deployment environments
