'use client'

import { X, Info } from 'lucide-react'
import type { Alert } from '@/types'

interface Props {
  alert: Alert | null
  isOpen: boolean
  onClose: () => void
}

export function AlertDetailDrawer({ alert, isOpen, onClose }: Props) {
  if (!isOpen || !alert) return null

  const ai = (() => {
    const aiEnrich = alert.enrichments?.find(e => e.key === 'ai_triage')
    try {
      return aiEnrich ? JSON.parse(aiEnrich.value) : null
    } catch {
      return aiEnrich ? { summary: aiEnrich.value } : null
    }
  })()

  return (
    <div className="fixed inset-0 z-50 flex">
      <div className="fixed inset-0 bg-black/40" aria-hidden="true" onClick={onClose} />
      <aside
        className="ml-auto h-full w-full max-w-xl bg-white dark:bg-gray-900 border-l border-gray-200 dark:border-gray-700 shadow-xl"
        role="dialog"
        aria-modal="true"
        aria-label="Alert details"
      >
        <div className="flex items-center justify-between p-4 border-b border-gray-200 dark:border-gray-700">
          <div>
            <h3 className="text-base font-semibold text-gray-900 dark:text-gray-100">{alert.title}</h3>
            <p className="text-xs text-gray-500 dark:text-gray-400">{alert.fingerprint}</p>
          </div>
          <button
            onClick={onClose}
            aria-label="Close details"
            className="p-2 rounded hover:bg-gray-100 dark:hover:bg-gray-800"
          >
            <X className="h-4 w-4" />
          </button>
        </div>

        <div className="p-4 space-y-4 overflow-y-auto h-[calc(100%-64px)]">
          <section className="space-y-1">
            <div className="text-sm text-gray-700 dark:text-gray-300">{alert.description || 'No description provided.'}</div>
            <div className="flex gap-2 text-xs">
              <span className="px-2 py-1 rounded bg-gray-100 dark:bg-gray-800 text-gray-800 dark:text-gray-200">{alert.severity}</span>
              <span className="px-2 py-1 rounded bg-gray-100 dark:bg-gray-800 text-gray-800 dark:text-gray-200">{alert.status}</span>
              <span className="px-2 py-1 rounded bg-gray-100 dark:bg-gray-800 text-gray-800 dark:text-gray-200">{alert.source}</span>
            </div>
          </section>

          <section className="space-y-2">
            <h4 className="text-sm font-semibold text-gray-900 dark:text-gray-100 flex items-center gap-2">
              <Info className="h-4 w-4" /> AI Triage
            </h4>
            {ai ? (
              <div className="space-y-2 text-sm text-gray-800 dark:text-gray-200">
                {ai.severity_classification && (
                  <div>
                    <span className="font-medium">Severity:</span> {ai.severity_classification}
                  </div>
                )}
                {ai.summary && (
                  <div>
                    <span className="font-medium">Summary:</span> {ai.summary}
                  </div>
                )}
                {Array.isArray(ai.remediation_steps) && ai.remediation_steps.length > 0 && (
                  <div>
                    <span className="font-medium">Remediation:</span>
                    <ul className="list-disc pl-5 mt-1 space-y-1">
                      {ai.remediation_steps.map((s: string, i: number) => (
                        <li key={i}>{s}</li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            ) : (
              <div className="text-sm text-gray-500 dark:text-gray-400">No AI triage available.</div>
            )}
          </section>

          <section>
            <h4 className="text-sm font-semibold text-gray-900 dark:text-gray-100">Labels</h4>
            <div className="mt-2 flex flex-wrap gap-2">
              {Object.entries(alert.labels || {}).map(([k, v]) => (
                <span key={k} className="text-xs px-2 py-1 rounded bg-gray-100 dark:bg-gray-800 text-gray-800 dark:text-gray-200">
                  {k}: {v}
                </span>
              ))}
              {Object.keys(alert.labels || {}).length === 0 && (
                <span className="text-xs text-gray-500 dark:text-gray-400">None</span>
              )}
            </div>
          </section>

          <section>
            <h4 className="text-sm font-semibold text-gray-900 dark:text-gray-100">Annotations</h4>
            <div className="mt-2 flex flex-wrap gap-2">
              {Object.entries(alert.annotations || {}).map(([k, v]) => (
                <span key={k} className="text-xs px-2 py-1 rounded bg-gray-100 dark:bg-gray-800 text-gray-800 dark:text-gray-200">
                  {k}: {String(v)}
                </span>
              ))}
              {Object.keys(alert.annotations || {}).length === 0 && (
                <span className="text-xs text-gray-500 dark:text-gray-400">None</span>
              )}
            </div>
          </section>
        </div>
      </aside>
    </div>
  )
}

export default AlertDetailDrawer


