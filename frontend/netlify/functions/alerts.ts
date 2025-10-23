import type { Handler } from '@netlify/functions'
import { getLiveAlerts, filterAlerts, paginate } from './lib/data'

export const handler: Handler = async (event) => {
  const url = new URL(event.rawUrl)
  const severity = url.searchParams.get('severity') || undefined
  const status = url.searchParams.get('status') || undefined
  const source = url.searchParams.get('source') || undefined
  const search = url.searchParams.get('search') || undefined
  const page = Math.max(1, parseInt(url.searchParams.get('page') || '1', 10))
  const pageSize = Math.min(100, Math.max(1, parseInt(url.searchParams.get('pageSize') || '20', 10)))

  const alerts = getLiveAlerts()
  const filtered = filterAlerts(alerts, { severity, status, source, search })
  const p = paginate(filtered, page, pageSize)

  return {
    statusCode: 200,
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ alerts: p.items, total: p.total, page: p.page, page_size: p.page_size, has_next: p.has_next, has_previous: p.has_previous }),
  }
}


