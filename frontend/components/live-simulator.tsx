'use client'

import { useEffect, useRef, useState } from 'react'
import type { Alert } from '@/types'

interface Props {
  onInject: (alerts: Alert[]) => void
}

function randomOf<T>(arr: T[]): T {
  return arr[Math.floor(Math.random() * arr.length)]
}

export function LiveSimulator({ onInject }: Props) {
  const [enabled, setEnabled] = useState(false)
  const [intervalMs, setIntervalMs] = useState(3000)
  const [burst, setBurst] = useState(false)
  const [mix, setMix] = useState<'balanced' | 'high' | 'critical'>('balanced')
  const timer = useRef<number | null>(null)

  useEffect(() => {
    if (!enabled) {
      if (timer.current) window.clearInterval(timer.current)
      timer.current = null
      return
    }
    const fn = () => {
      const now = Date.now()
      const severities: Alert['severity'][] = mix === 'critical' ? ['high', 'critical'] : mix === 'high' ? ['medium', 'high'] : ['info', 'low', 'medium']
      const count = burst ? 3 : 1
      const payload: Alert[] = Array.from({ length: count }).map((_, i) => {
        const sev = randomOf(severities)
        const id = `sim-${now}-${i}`
        return {
          id,
          title: `Simulated ${sev.toUpperCase()} Alert`,
          description: 'Live simulator generated alert',
          severity: sev,
          status: 'active',
          source: 'custom',
          source_id: id,
          fingerprint: id,
          labels: { environment: 'sim', host: `host-${(now % 7) + 1}` },
          annotations: { summary: 'simulation' },
          started_at: new Date(now).toISOString(),
          created_at: new Date(now).toISOString(),
          enrichments: [],
          correlations: []
        }
      })
      onInject(payload)
    }
    // @ts-ignore
    timer.current = window.setInterval(fn, intervalMs)
    return () => { if (timer.current) window.clearInterval(timer.current) }
  }, [enabled, intervalMs, burst, mix, onInject])

  return (
    <div className="bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800 rounded-lg p-3 flex items-center justify-between">
      <div className="text-sm text-yellow-800 dark:text-yellow-200">
        Live Simulator {enabled ? 'ON' : 'OFF'}
      </div>
      <div className="flex items-center gap-2">
        <label className="text-xs text-gray-700 dark:text-gray-300 flex items-center gap-1">
          <input type="checkbox" checked={enabled} onChange={e => setEnabled(e.target.checked)} /> Enable
        </label>
        <label className="text-xs text-gray-700 dark:text-gray-300 flex items-center gap-1">
          Interval
          <input
            type="number"
            className="w-20 px-2 py-1 rounded border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800"
            value={intervalMs}
            min={500}
            step={500}
            onChange={e => setIntervalMs(Number(e.target.value))}
          />
          ms
        </label>
        <label className="text-xs text-gray-700 dark:text-gray-300 flex items-center gap-1">
          <input type="checkbox" checked={burst} onChange={e => setBurst(e.target.checked)} /> Burst
        </label>
        <select
          aria-label="Severity mix"
          className="text-xs px-2 py-1 rounded border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800 text-gray-800 dark:text-gray-200"
          value={mix}
          onChange={e => setMix(e.target.value as any)}
        >
          <option value="balanced">Balanced</option>
          <option value="high">High</option>
          <option value="critical">Critical</option>
        </select>
      </div>
    </div>
  )
}

export default LiveSimulator


