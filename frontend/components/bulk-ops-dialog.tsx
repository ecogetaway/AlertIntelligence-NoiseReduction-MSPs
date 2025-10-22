'use client'

import { useState } from 'react'
import { X, CheckCircle } from 'lucide-react'

interface Props {
  selectedCount: number
  onConfirm: (action: string, reason?: string) => void
  onCancel: () => void
}

export function BulkOpsDialog({ selectedCount, onConfirm, onCancel }: Props) {
  const [action, setAction] = useState<'acknowledge' | 'suppress'>('acknowledge')
  const [reason, setReason] = useState('')
  const [showUndo, setShowUndo] = useState(false)

  function handleConfirm() {
    onConfirm(action, reason.trim() || undefined)
    setShowUndo(true)
    setTimeout(() => setShowUndo(false), 5000)
  }

  return (
    <>
      <div className="fixed inset-0 z-50 flex items-center justify-center">
        <div className="fixed inset-0 bg-black/40" onClick={onCancel} />
        <div
          className="relative bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-lg p-6 max-w-md w-full shadow-xl"
          role="dialog"
          aria-modal="true"
          aria-labelledby="bulk-ops-title"
        >
          <div className="flex items-center justify-between mb-4">
            <h3 id="bulk-ops-title" className="text-lg font-semibold text-gray-900 dark:text-gray-100">
              Bulk Action
            </h3>
            <button
              onClick={onCancel}
              aria-label="Close dialog"
              className="p-2 rounded hover:bg-gray-100 dark:hover:bg-gray-800"
            >
              <X className="h-4 w-4" />
            </button>
          </div>

          <div className="space-y-4">
            <div>
              <p className="text-sm text-gray-700 dark:text-gray-300">
                {selectedCount} alert{selectedCount > 1 ? 's' : ''} selected
              </p>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Action
              </label>
              <select
                className="w-full px-3 py-2 rounded border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
                value={action}
                onChange={e => setAction(e.target.value as any)}
              >
                <option value="acknowledge">Acknowledge</option>
                <option value="suppress">Suppress</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Reason (optional)
              </label>
              <textarea
                className="w-full px-3 py-2 rounded border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
                rows={3}
                placeholder="Why are you performing this action?"
                value={reason}
                onChange={e => setReason(e.target.value)}
              />
            </div>

            <div className="flex gap-3 justify-end">
              <button
                onClick={onCancel}
                className="px-4 py-2 rounded bg-gray-200 dark:bg-gray-700 text-gray-800 dark:text-gray-200 hover:bg-gray-300 dark:hover:bg-gray-600"
              >
                Cancel
              </button>
              <button
                onClick={handleConfirm}
                className="px-4 py-2 rounded bg-blue-600 text-white hover:bg-blue-700"
              >
                Confirm
              </button>
            </div>
          </div>
        </div>
      </div>

      {showUndo && (
        <div className="fixed bottom-4 right-4 z-50 bg-gray-900 text-white px-4 py-3 rounded-lg shadow-lg flex items-center gap-3">
          <CheckCircle className="h-5 w-5 text-green-400" />
          <span>Action applied to {selectedCount} alert{selectedCount > 1 ? 's' : ''}</span>
          <button
            onClick={() => {
              // TODO: implement undo
              setShowUndo(false)
            }}
            className="ml-2 px-2 py-1 text-xs rounded bg-white/20 hover:bg-white/30"
          >
            Undo
          </button>
        </div>
      )}
    </>
  )
}

export default BulkOpsDialog

