export interface AlertRow {
  id: string
  title: string
  description?: string
  severity: 'critical' | 'high' | 'medium' | 'low' | 'info'
  status: 'active' | 'acknowledged' | 'resolved' | 'suppressed' | 'dismissed'
  source: string
  source_id: string
  fingerprint: string
  started_at: string
}

const baseAlerts: AlertRow[] = [
  {
    id: 'alert-1',
    title: 'High CPU Usage on Server-01',
    description: 'CPU usage exceeded 90% for 5 minutes',
    severity: 'high',
    status: 'active',
    source: 'prometheus',
    source_id: 'srv-01',
    fingerprint: 'fp-1',
    started_at: new Date(Date.now() - 60 * 60 * 1000).toISOString(),
  },
  {
    id: 'alert-2',
    title: 'Memory Leak Detected',
    description: 'Memory usage continuously increasing',
    severity: 'critical',
    status: 'active',
    source: 'datadog',
    source_id: 'app-22',
    fingerprint: 'fp-2',
    started_at: new Date(Date.now() - 2 * 60 * 60 * 1000).toISOString(),
  },
  {
    id: 'alert-3',
    title: 'Database Connection Timeout',
    description: 'Timeout after 30 seconds',
    severity: 'critical',
    status: 'acknowledged',
    source: 'prometheus',
    source_id: 'db-01',
    fingerprint: 'fp-3',
    started_at: new Date(Date.now() - 3 * 60 * 60 * 1000).toISOString(),
  },
  {
    id: 'alert-4',
    title: 'SSL Certificate Expiring',
    severity: 'medium',
    status: 'active',
    source: 'nagios',
    source_id: 'edge-07',
    fingerprint: 'fp-4',
    started_at: new Date(Date.now() - 5 * 60 * 60 * 1000).toISOString(),
  },
  {
    id: 'alert-5',
    title: 'API Response Time High',
    severity: 'low',
    status: 'resolved',
    source: 'newrelic',
    source_id: 'api-09',
    fingerprint: 'fp-5',
    started_at: new Date(Date.now() - 6 * 60 * 60 * 1000).toISOString(),
  },
]

export function getLiveAlerts(): AlertRow[] {
  // Add subtle time-based variations for “live” feel
  const tick = Math.floor(Date.now() / 15000) % 3
  return baseAlerts.map((a, idx) => {
    const copy = { ...a }
    if (idx === tick) {
      copy.status = copy.status === 'active' ? 'acknowledged' : 'active'
    }
    return copy
  })
}

export function filterAlerts(
  alerts: AlertRow[],
  params: { severity?: string; status?: string; source?: string; search?: string }
): AlertRow[] {
  return alerts.filter((a) => {
    if (params.severity && a.severity !== params.severity) return false
    if (params.status && a.status !== params.status) return false
    if (params.source && a.source !== params.source) return false
    if (params.search) {
      const t = `${a.title} ${a.description ?? ''} ${a.source}`.toLowerCase()
      if (!t.includes(params.search.toLowerCase())) return false
    }
    return true
  })
}

export function paginate<T>(items: T[], page: number, pageSize: number) {
  const start = (page - 1) * pageSize
  const end = start + pageSize
  const total = items.length
  return {
    items: items.slice(start, end),
    total,
    page,
    page_size: pageSize,
    has_next: end < total,
    has_previous: page > 1,
  }
}


