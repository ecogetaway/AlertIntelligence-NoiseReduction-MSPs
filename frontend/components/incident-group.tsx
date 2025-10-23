'use client'

import { useMemo } from 'react'
import { Activity } from 'lucide-react'
import type { Alert } from '@/types'

interface Props {
  alerts: Alert[]
  onOpenDetail: (alert: Alert) => void
}

function maxSeverity(a: Alert['severity'], b: Alert['severity']): Alert['severity'] {
  const order: Alert['severity'][] = ['info', 'low', 'medium', 'high', 'critical']
  return order.indexOf(a) >= order.indexOf(b) ? a : b
}

export function IncidentGroup({ alerts, onOpenDetail }: Props) {
  const groups = useMemo(() => {
    const map = new Map<string, { alerts: Alert[]; severity: Alert['severity']; updated_at?: string }>()
    for (const a of alerts) {
      const key = a.incident_id || a.fingerprint
      const existing = map.get(key)
      if (!existing) {
        map.set(key, { alerts: [a], severity: a.severity, updated_at: a.updated_at || a.created_at })
        continue
      }
      existing.alerts.push(a)
      existing.severity = maxSeverity(existing.severity, a.severity)
      const t = (a.updated_at || a.created_at)
      if (!existing.updated_at || t > existing.updated_at) existing.updated_at = t
    }
    return Array.from(map.entries()).map(([id, v]) => ({ id, ...v }))
  }, [alerts])

  if (!alerts || alerts.length === 0) return null

  return (
    <div className="space-y-3">
      {groups.map(group => {
        const top = group.alerts[0]
        return (
          <div
            key={group.id}
            className="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-4"
            role="button"
            tabIndex={0}
            aria-label={`Open incident ${group.id}`}
            onClick={() => onOpenDetail(top)}
            onKeyDown={(e) => { if (e.key === 'Enter') onOpenDetail(top) }}
          >
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <Activity className="h-4 w-4 text-gray-500" />
                <span className="text-sm font-medium text-gray-900 dark:text-gray-100">
                  {top.title || 'Incident'}
                </span>
              </div>
              <div className="flex items-center gap-3">
                <span className="text-xs px-2 py-1 rounded bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-200">{group.alerts.length} alerts</span>
                <span className={`text-xs px-2 py-1 rounded ${group.severity === 'critical' ? 'bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-300' : group.severity === 'high' ? 'bg-orange-100 text-orange-700 dark:bg-orange-900/30 dark:text-orange-300' : 'bg-gray-100 text-gray-700 dark:bg-gray-700 dark:text-gray-200'}`}>
                  {group.severity}
                </span>
                {top.enrichments?.length > 0 && (
                  <span className="text-xs px-2 py-1 rounded bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-300">AI</span>
                )}
              </div>
            </div>
            <div className="mt-2 text-xs text-gray-500 dark:text-gray-400">
              Updated {new Date(group.updated_at || top.created_at).toLocaleString()}
            </div>
          </div>
        )
      })}
    </div>
  )
}

export default IncidentGroup


