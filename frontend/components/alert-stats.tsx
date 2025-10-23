'use client'

import { AlertTriangle, Activity, CheckCircle, XCircle } from 'lucide-react'
import { Alert, Incident } from '@/types'

interface AlertStatsProps {
  alerts: Alert[] | null
  incidents: Incident[] | null
  loading: boolean
}

export function AlertStats({ alerts, incidents, loading }: AlertStatsProps) {
  const stats = [
    {
      label: 'Total Alerts',
      value: alerts?.length || 0,
      icon: AlertTriangle,
      color: 'blue'
    },
    {
      label: 'Active Incidents',
      value: incidents?.filter(i => i.status === 'open').length || 0,
      icon: Activity,
      color: 'red'
    },
    {
      label: 'Resolved',
      value: alerts?.filter(a => a.status === 'resolved').length || 0,
      icon: CheckCircle,
      color: 'green'
    },
    {
      label: 'Suppressed',
      value: alerts?.filter(a => a.status === 'suppressed').length || 0,
      icon: XCircle,
      color: 'gray'
    }
  ]

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      {stats.map((stat) => {
        const Icon = stat.icon
        return (
          <div key={stat.label} className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-sm">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600 dark:text-gray-400">
                  {stat.label}
                </p>
                <p className="mt-2 text-3xl font-bold text-gray-900 dark:text-white">
                  {loading ? '...' : stat.value}
                </p>
              </div>
              <Icon className={`h-12 w-12 text-${stat.color}-500`} />
            </div>
          </div>
        )
      })}
    </div>
  )
}

