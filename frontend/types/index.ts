export interface Alert {
  id: string
  title: string
  description?: string
  severity: 'critical' | 'high' | 'medium' | 'low' | 'info'
  status: 'active' | 'acknowledged' | 'resolved' | 'suppressed' | 'dismissed'
  source: 'prometheus' | 'datadog' | 'sentry' | 'new_relic' | 'grafana' | 'custom'
  source_id: string
  fingerprint: string
  labels: Record<string, string>
  annotations: Record<string, string>
  started_at: string
  updated_at?: string
  resolved_at?: string
  created_at: string
  enrichments: AlertEnrichment[]
  correlations: AlertCorrelation[]
  incident_id?: string
}

export interface AlertEnrichment {
  id: string
  key: string
  value: string
  source: string
  created_at: string
}

export interface AlertCorrelation {
  id: string
  correlated_alert_id: string
  correlation_type: string
  confidence: number
  created_at: string
}

export interface Incident {
  id: string
  title: string
  description?: string
  status: 'open' | 'investigating' | 'identified' | 'monitoring' | 'resolved' | 'closed'
  priority: 'p1' | 'p2' | 'p3' | 'p4'
  incident_type: 'infrastructure' | 'application' | 'security' | 'performance' | 'availability' | 'custom'
  assignee?: string
  tags: string[]
  metadata: Record<string, any>
  started_at: string
  updated_at?: string
  resolved_at?: string
  created_at: string
  ai_summary?: string
  ai_root_cause?: string
  ai_impact_assessment?: string
  ai_recommendations?: string
  alerts: Alert[]
  updates: IncidentUpdate[]
}

export interface IncidentUpdate {
  id: string
  author: string
  content: string
  update_type: string
  metadata: Record<string, any>
  created_at: string
}

export interface AlertFilters {
  severity?: string
  status?: string
  source?: string
  search?: string
}

export interface AlertStats {
  total: number
  active: number
  acknowledged: number
  resolved: number
  suppressed: number
  by_severity: {
    critical: number
    high: number
    medium: number
    low: number
    info: number
  }
  by_source: Record<string, number>
}

export interface IncidentStats {
  total: number
  open: number
  investigating: number
  resolved: number
  closed: number
  by_priority: {
    p1: number
    p2: number
    p3: number
    p4: number
  }
}

export interface Workflow {
  id: string
  name: string
  description: string
  triggers: WorkflowTrigger[]
  actions: WorkflowAction[]
  enabled: boolean
  created_at: string
  updated_at: string
}

export interface WorkflowTrigger {
  type: 'alert' | 'incident' | 'schedule'
  conditions?: Record<string, any>
}

export interface WorkflowAction {
  name: string
  provider: {
    type: string
    with: Record<string, any>
  }
}

export interface Agent {
  id: string
  name: string
  description: string
  type: 'bedrock' | 'strands'
  status: 'active' | 'inactive' | 'error'
  capabilities: string[]
  last_used?: string
}

export interface ApiResponse<T> {
  data: T
  message?: string
  error?: string
}

export interface PaginatedResponse<T> {
  items: T[]
  total: number
  page: number
  page_size: number
  has_next: boolean
  has_previous: boolean
}
