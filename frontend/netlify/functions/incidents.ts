import type { Handler } from '@netlify/functions'
import { getLiveAlerts } from './lib/data'

export const handler: Handler = async () => {
  const alerts = getLiveAlerts()
  // Derive simple incidents: group critical+high by source
  const groups: Record<string, string[]> = {}
  alerts
    .filter((a) => a.severity === 'critical' || a.severity === 'high')
    .forEach((a) => {
      const key = `${a.source}`
      if (!groups[key]) groups[key] = []
      groups[key].push(a.id)
    })

  const incidents = Object.keys(groups).map((k, i) => ({
    id: `incident-${i + 1}`,
    title: `Incident in ${k}`,
    status: groups[k].length > 1 ? 'open' : 'acknowledged',
    priority: groups[k].length > 2 ? 'p1' : 'p2',
    alerts: groups[k],
    ai_summary: `AI detected issues from ${k}. Correlation score: ${80 + Math.min(15, groups[k].length * 5)}%.`,
  }))

  return {
    statusCode: 200,
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ incidents }),
  }
}


