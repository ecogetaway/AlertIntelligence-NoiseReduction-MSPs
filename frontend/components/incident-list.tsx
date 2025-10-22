'use client'

import { Activity, Clock, User } from 'lucide-react'
import { Incident } from '@/types'

interface IncidentListProps {
  incidents: Incident[] | null
  loading: boolean
  error: Error | null
  onAction: (incidentId: string, action: string) => void
}

export function IncidentList({ incidents, loading, error, onAction }: IncidentListProps) {
  if (loading) {
    return (
      <div className="space-y-4">
        {[...Array(3)].map((_, i) => (
          <div key={i} className="bg-white dark:bg-gray-800 rounded-lg p-6 animate-pulse">
            <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded w-3/4 mb-2"></div>
            <div className="h-3 bg-gray-200 dark:bg-gray-700 rounded w-1/2"></div>
          </div>
        ))}
      </div>
    )
  }

  if (error) {
    return (
      <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-4">
        <p className="text-red-600 dark:text-red-400">
          Failed to load incidents: {error.message}
        </p>
      </div>
    )
  }

  if (!incidents || incidents.length === 0) {
    return (
      <div className="text-center py-12 bg-white dark:bg-gray-800 rounded-lg">
        <Activity className="mx-auto h-12 w-12 text-gray-400" />
        <h3 className="mt-2 text-sm font-medium text-gray-900 dark:text-gray-100">
          No incidents
        </h3>
        <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">
          No active incidents at the moment.
        </p>
      </div>
    )
  }

  return (
    <div className="space-y-4">
      {incidents.map((incident) => (
        <div key={incident.id} className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-sm">
          <div className="flex items-start justify-between">
            <div className="flex-1">
              <div className="flex items-center space-x-2">
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
                  {incident.title}
                </h3>
                <span className={`px-2 py-1 text-xs font-medium rounded-full ${
                  incident.status === 'open' ? 'bg-red-100 text-red-700' : 'bg-green-100 text-green-700'
                }`}>
                  {incident.status}
                </span>
              </div>
              
              <p className="mt-2 text-sm text-gray-600 dark:text-gray-400">
                {incident.description}
              </p>
              
              <div className="mt-4 flex items-center space-x-4 text-sm text-gray-500 dark:text-gray-400">
                <div className="flex items-center space-x-1">
                  <Clock className="h-4 w-4" />
                  <span>{new Date(incident.created_at).toLocaleString()}</span>
                </div>
                {incident.assignee && (
                  <div className="flex items-center space-x-1">
                    <User className="h-4 w-4" />
                    <span>{incident.assignee}</span>
                  </div>
                )}
              </div>
            </div>
            
            <div className="ml-4 flex space-x-2">
              <button
                onClick={() => onAction(incident.id, 'resolve')}
                className="px-3 py-1 text-sm font-medium text-green-700 bg-green-50 hover:bg-green-100 rounded-lg transition-colors"
              >
                Resolve
              </button>
            </div>
          </div>
        </div>
      ))}
    </div>
  )
}

