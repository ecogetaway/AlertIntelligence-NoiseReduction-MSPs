'use client'

import React, { useState } from 'react'
import { CheckSquare, Square, MoreHorizontal, CheckCircle, XCircle, AlertTriangle, User } from 'lucide-react'

interface BulkOperationsProps {
  selectedAlerts: string[]
  onBulkAction: (action: string, alertIds: string[], reason?: string, assignee?: string) => Promise<void>
  onClearSelection: () => void
}

export function BulkOperations({ selectedAlerts, onBulkAction, onClearSelection }: BulkOperationsProps) {
  const [showActions, setShowActions] = useState(false)
  const [action, setAction] = useState('')
  const [reason, setReason] = useState('')
  const [assignee, setAssignee] = useState('')
  const [loading, setLoading] = useState(false)

  if (selectedAlerts.length === 0) return null

  const handleBulkAction = async () => {
    if (!action) return

    setLoading(true)
    try {
      await onBulkAction(action, selectedAlerts, reason || undefined, assignee || undefined)
      setShowActions(false)
      setAction('')
      setReason('')
      setAssignee('')
    } catch (error) {
      console.error('Bulk action failed:', error)
    } finally {
      setLoading(false)
    }
  }

  const getActionIcon = (actionType: string) => {
    switch (actionType) {
      case 'acknowledge':
        return <CheckCircle className="h-4 w-4" />
      case 'suppress':
        return <XCircle className="h-4 w-4" />
      case 'resolve':
        return <CheckCircle className="h-4 w-4" />
      case 'assign':
        return <User className="h-4 w-4" />
      default:
        return <AlertTriangle className="h-4 w-4" />
    }
  }

  const getActionColor = (actionType: string) => {
    switch (actionType) {
      case 'acknowledge':
        return 'text-blue-600 bg-blue-100'
      case 'suppress':
        return 'text-orange-600 bg-orange-100'
      case 'resolve':
        return 'text-green-600 bg-green-100'
      case 'assign':
        return 'text-purple-600 bg-purple-100'
      default:
        return 'text-gray-600 bg-gray-100'
    }
  }

  return (
    <div className="fixed bottom-4 left-1/2 transform -translate-x-1/2 z-40">
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg border border-gray-200 dark:border-gray-700 p-4 min-w-[400px]">
        {/* Selection Summary */}
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center space-x-2">
            <CheckSquare className="h-5 w-5 text-blue-600" />
            <span className="text-sm font-medium text-gray-900 dark:text-white">
              {selectedAlerts.length} alert{selectedAlerts.length !== 1 ? 's' : ''} selected
            </span>
          </div>
          <button
            onClick={onClearSelection}
            className="text-sm text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200"
          >
            Clear
          </button>
        </div>

        {/* Action Buttons */}
        <div className="flex space-x-2 mb-4">
          <button
            onClick={() => setAction('acknowledge')}
            className={`flex items-center space-x-2 px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
              action === 'acknowledge'
                ? 'bg-blue-100 text-blue-800 border border-blue-200'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            <CheckCircle className="h-4 w-4" />
            <span>Acknowledge</span>
          </button>

          <button
            onClick={() => setAction('suppress')}
            className={`flex items-center space-x-2 px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
              action === 'suppress'
                ? 'bg-orange-100 text-orange-800 border border-orange-200'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            <XCircle className="h-4 w-4" />
            <span>Suppress</span>
          </button>

          <button
            onClick={() => setAction('resolve')}
            className={`flex items-center space-x-2 px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
              action === 'resolve'
                ? 'bg-green-100 text-green-800 border border-green-200'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            <CheckCircle className="h-4 w-4" />
            <span>Resolve</span>
          </button>

          <button
            onClick={() => setAction('assign')}
            className={`flex items-center space-x-2 px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
              action === 'assign'
                ? 'bg-purple-100 text-purple-800 border border-purple-200'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            <User className="h-4 w-4" />
            <span>Assign</span>
          </button>
        </div>

        {/* Action Details */}
        {action && (
          <div className="space-y-3">
            <div className="flex items-center space-x-2">
              <div className={`p-2 rounded-lg ${getActionColor(action)}`}>
                {getActionIcon(action)}
              </div>
              <span className="text-sm font-medium text-gray-900 dark:text-white">
                {action.charAt(0).toUpperCase() + action.slice(1)} {selectedAlerts.length} alert{selectedAlerts.length !== 1 ? 's' : ''}
              </span>
            </div>

            {(action === 'suppress' || action === 'assign') && (
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                  {action === 'suppress' ? 'Reason' : 'Assignee'}
                </label>
                <input
                  type="text"
                  value={action === 'suppress' ? reason : assignee}
                  onChange={(e) => action === 'suppress' ? setReason(e.target.value) : setAssignee(e.target.value)}
                  placeholder={action === 'suppress' ? 'Enter suppression reason...' : 'Enter assignee email...'}
                  className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
                />
              </div>
            )}

            <div className="flex space-x-2">
              <button
                onClick={() => {
                  setAction('')
                  setReason('')
                  setAssignee('')
                }}
                className="flex-1 px-3 py-2 text-sm font-medium text-gray-700 dark:text-gray-300 bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 rounded-lg transition-colors"
              >
                Cancel
              </button>
              <button
                onClick={handleBulkAction}
                disabled={loading || (action === 'suppress' && !reason) || (action === 'assign' && !assignee)}
                className="flex-1 px-3 py-2 text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed rounded-lg transition-colors"
              >
                {loading ? 'Processing...' : `Confirm ${action}`}
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

interface AlertSelectionProps {
  alertId: string
  isSelected: boolean
  onToggle: (alertId: string) => void
}

export function AlertSelection({ alertId, isSelected, onToggle }: AlertSelectionProps) {
  return (
    <button
      onClick={() => onToggle(alertId)}
      className="p-1 hover:bg-gray-100 dark:hover:bg-gray-700 rounded transition-colors"
    >
      {isSelected ? (
        <CheckSquare className="h-4 w-4 text-blue-600" />
      ) : (
        <Square className="h-4 w-4 text-gray-400" />
      )}
    </button>
  )
}
