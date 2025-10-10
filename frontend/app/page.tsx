'use client'

import { useState, useEffect } from 'react'
import { AlertTriangle, Activity, Zap, Brain, BarChart3, Settings, Filter, CheckSquare, Square } from 'lucide-react'
import { AlertCard } from '@/components/alert-card'
import { AlertFilters } from '@/components/alert-filters'
import { AlertStats } from '@/components/alert-stats'
import { IncidentList } from '@/components/incident-list'
import { DashboardHeader } from '@/components/dashboard-header'
import { AdvancedFilter } from '@/components/advanced-filter'
import { BulkOperations, AlertSelection } from '@/components/bulk-operations'
import { ExportFunctionality } from '@/components/export-functionality'
import { useAlerts } from '@/hooks/use-alerts'
import { useIncidents } from '@/hooks/use-incidents'
import { Alert, Incident } from '@/types'

export default function Dashboard() {
  const [selectedTab, setSelectedTab] = useState<'alerts' | 'incidents' | 'analytics'>('alerts')
  const [filters, setFilters] = useState({
    severity: '',
    status: '',
    source: '',
    search: ''
  })
  const [showAdvancedFilter, setShowAdvancedFilter] = useState(false)
  const [selectedAlerts, setSelectedAlerts] = useState<string[]>([])
  const [showBulkOperations, setShowBulkOperations] = useState(false)

  const { 
    alerts, 
    loading: alertsLoading, 
    error: alertsError,
    refetch: refetchAlerts 
  } = useAlerts(filters)

  const { 
    incidents, 
    loading: incidentsLoading, 
    error: incidentsError,
    refetch: refetchIncidents 
  } = useIncidents()

  const handleFilterChange = (newFilters: typeof filters) => {
    setFilters(newFilters)
  }

  const handleAlertAction = async (alertId: string, action: string) => {
    // Handle alert actions (acknowledge, suppress, etc.)
    console.log(`Performing ${action} on alert ${alertId}`)
    await refetchAlerts()
  }

  const handleIncidentAction = async (incidentId: string, action: string) => {
    // Handle incident actions
    console.log(`Performing ${action} on incident ${incidentId}`)
    await refetchIncidents()
  }

  const handleAdvancedFilterChange = (newFilters: any) => {
    setFilters(newFilters)
    setShowAdvancedFilter(false)
  }

  const handleAlertSelection = (alertId: string) => {
    setSelectedAlerts(prev => 
      prev.includes(alertId) 
        ? prev.filter(id => id !== alertId)
        : [...prev, alertId]
    )
  }

  const handleSelectAll = () => {
    if (selectedAlerts.length === alerts?.length) {
      setSelectedAlerts([])
    } else {
      setSelectedAlerts(alerts?.map(alert => alert.id) || [])
    }
  }

  const handleBulkAction = async (action: string, alertIds: string[], reason?: string, assignee?: string) => {
    try {
      const response = await fetch('/api/v1/alerts/bulk-action', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          alert_ids: alertIds,
          action,
          reason,
          assignee
        })
      })
      
      if (response.ok) {
        const result = await response.json()
        console.log('Bulk action result:', result)
        setSelectedAlerts([])
        await refetchAlerts()
      }
    } catch (error) {
      console.error('Bulk action failed:', error)
    }
  }

  const handleExport = async (format: string, filters?: any) => {
    try {
      const params = new URLSearchParams({ format })
      if (filters) {
        Object.entries(filters).forEach(([key, value]) => {
          if (value && value.length > 0) {
            params.append(key, Array.isArray(value) ? value.join(',') : value)
          }
        })
      }
      
      const response = await fetch(`/api/v1/alerts/export?${params}`)
      const data = await response.json()
      
      // Create download link
      const blob = new Blob([data.data], { type: 'text/plain' })
      const url = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = data.filename
      document.body.appendChild(a)
      a.click()
      document.body.removeChild(a)
      URL.revokeObjectURL(url)
    } catch (error) {
      console.error('Export failed:', error)
    }
  }

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <DashboardHeader />
      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Stats Overview */}
        <AlertStats 
          alerts={alerts}
          incidents={incidents}
          loading={alertsLoading || incidentsLoading}
        />

        {/* Main Content */}
        <div className="mt-8">
          {/* Tab Navigation */}
          <div className="border-b border-gray-200 dark:border-gray-700">
            <nav className="-mb-px flex space-x-8">
              {[
                { id: 'alerts', label: 'Alerts', icon: AlertTriangle, count: alerts?.length || 0 },
                { id: 'incidents', label: 'Incidents', icon: Activity, count: incidents?.length || 0 },
                { id: 'analytics', label: 'Analytics', icon: BarChart3, count: 0 }
              ].map((tab) => {
                const Icon = tab.icon
                return (
                  <button
                    key={tab.id}
                    onClick={() => setSelectedTab(tab.id as any)}
                    className={`flex items-center space-x-2 py-2 px-1 border-b-2 font-medium text-sm ${
                      selectedTab === tab.id
                        ? 'border-blue-500 text-blue-600 dark:text-blue-400'
                        : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300 dark:text-gray-400 dark:hover:text-gray-300'
                    }`}
                  >
                    <Icon className="h-4 w-4" />
                    <span>{tab.label}</span>
                    {tab.count > 0 && (
                      <span className="bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300 px-2 py-1 rounded-full text-xs">
                        {tab.count}
                      </span>
                    )}
                  </button>
                )
              })}
            </nav>
          </div>

          {/* Tab Content */}
          <div className="mt-6">
            {selectedTab === 'alerts' && (
              <div className="space-y-6">
                {/* Alert Controls */}
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-3">
                    <button
                      onClick={() => setShowAdvancedFilter(true)}
                      className="flex items-center space-x-2 px-4 py-2 text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
                    >
                      <Filter className="h-4 w-4" />
                      <span>Advanced Filters</span>
                    </button>
                    
                    <ExportFunctionality 
                      currentFilters={filters}
                      onExport={handleExport}
                    />
                  </div>
                  
                  <div className="flex items-center space-x-2">
                    <button
                      onClick={handleSelectAll}
                      className="flex items-center space-x-2 px-3 py-2 text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
                    >
                      {selectedAlerts.length === alerts?.length ? (
                        <CheckSquare className="h-4 w-4" />
                      ) : (
                        <Square className="h-4 w-4" />
                      )}
                      <span>
                        {selectedAlerts.length === alerts?.length ? 'Deselect All' : 'Select All'}
                      </span>
                    </button>
                  </div>
                </div>

                <AlertFilters 
                  filters={filters}
                  onFilterChange={handleFilterChange}
                />
                
                <div className="grid gap-4">
                  {alertsLoading ? (
                    <div className="space-y-4">
                      {[...Array(5)].map((_, i) => (
                        <div key={i} className="bg-white dark:bg-gray-800 rounded-lg p-4 animate-pulse">
                          <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded w-3/4 mb-2"></div>
                          <div className="h-3 bg-gray-200 dark:bg-gray-700 rounded w-1/2"></div>
                        </div>
                      ))}
                    </div>
                  ) : alertsError ? (
                    <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-4">
                      <p className="text-red-600 dark:text-red-400">
                        Failed to load alerts: {alertsError.message}
                      </p>
                    </div>
                  ) : alerts && alerts.length > 0 ? (
                    alerts.map((alert) => (
                      <div key={alert.id} className="relative">
                        <div className="absolute top-2 left-2 z-10">
                          <AlertSelection
                            alertId={alert.id}
                            isSelected={selectedAlerts.includes(alert.id)}
                            onToggle={handleAlertSelection}
                          />
                        </div>
                        <AlertCard
                          alert={alert}
                          onAction={handleAlertAction}
                        />
                      </div>
                    ))
                  ) : (
                    <div className="text-center py-12">
                      <AlertTriangle className="mx-auto h-12 w-12 text-gray-400" />
                      <h3 className="mt-2 text-sm font-medium text-gray-900 dark:text-gray-100">
                        No alerts
                      </h3>
                      <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">
                        No alerts match your current filters.
                      </p>
                    </div>
                  )}
                </div>
              </div>
            )}

            {selectedTab === 'incidents' && (
              <div className="space-y-6">
                <IncidentList 
                  incidents={incidents}
                  loading={incidentsLoading}
                  error={incidentsError}
                  onAction={handleIncidentAction}
                />
              </div>
            )}

            {selectedTab === 'analytics' && (
              <div className="space-y-6">
                <div className="bg-white dark:bg-gray-800 rounded-lg p-6">
                  <h3 className="text-lg font-medium text-gray-900 dark:text-gray-100 mb-4">
                    Analytics Dashboard
                  </h3>
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    <div className="bg-blue-50 dark:bg-blue-900/20 rounded-lg p-4">
                      <div className="flex items-center">
                        <Brain className="h-8 w-8 text-blue-600 dark:text-blue-400" />
                        <div className="ml-4">
                          <p className="text-sm font-medium text-blue-600 dark:text-blue-400">
                            AI Processing
                          </p>
                          <p className="text-2xl font-bold text-blue-900 dark:text-blue-100">
                            95%
                          </p>
                        </div>
                      </div>
                    </div>
                    
                    <div className="bg-green-50 dark:bg-green-900/20 rounded-lg p-4">
                      <div className="flex items-center">
                        <Zap className="h-8 w-8 text-green-600 dark:text-green-400" />
                        <div className="ml-4">
                          <p className="text-sm font-medium text-green-600 dark:text-green-400">
                            Noise Reduction
                          </p>
                          <p className="text-2xl font-bold text-green-900 dark:text-green-100">
                            78%
                          </p>
                        </div>
                      </div>
                    </div>
                    
                    <div className="bg-purple-50 dark:bg-purple-900/20 rounded-lg p-4">
                      <div className="flex items-center">
                        <BarChart3 className="h-8 w-8 text-purple-600 dark:text-purple-400" />
                        <div className="ml-4">
                          <p className="text-sm font-medium text-purple-600 dark:text-purple-400">
                            Correlation Rate
                          </p>
                          <p className="text-2xl font-bold text-purple-900 dark:text-purple-100">
                            62%
                          </p>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Advanced Filter Modal */}
      <AdvancedFilter
        isOpen={showAdvancedFilter}
        onClose={() => setShowAdvancedFilter(false)}
        onFilterChange={handleAdvancedFilterChange}
      />

      {/* Bulk Operations */}
      {selectedAlerts.length > 0 && (
        <BulkOperations
          selectedAlerts={selectedAlerts}
          onBulkAction={handleBulkAction}
          onClearSelection={() => setSelectedAlerts([])}
        />
      )}
    </div>
  )
}
