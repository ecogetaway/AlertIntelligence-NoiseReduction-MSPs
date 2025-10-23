import { useState, useEffect, useMemo, useCallback } from 'react'
import { Alert, AlertFilters, FilterPreset } from '@/types'

interface UseAlertsReturn {
  alerts: Alert[] | null
  loading: boolean
  error: Error | null
  refetch: () => Promise<void>
  groupedMode: boolean
  setGroupedMode: (grouped: boolean) => void
  injectSimulated: (alerts: Alert[]) => void
  clearSimulated: () => void
  applyPreset: (preset: FilterPreset) => void
  currentFilters: AlertFilters
}

export function useAlerts(filters: AlertFilters): UseAlertsReturn {
  const [realAlerts, setRealAlerts] = useState<Alert[] | null>(null)
  const [simulatedAlerts, setSimulatedAlerts] = useState<Alert[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<Error | null>(null)
  const [groupedMode, setGroupedMode] = useState(true)
  const [currentFilters, setCurrentFilters] = useState(filters)

  const fetchAlerts = useCallback(async () => {
    try {
      setLoading(true)
      const params = new URLSearchParams()
      if (currentFilters.severity) params.append('severity', currentFilters.severity)
      if (currentFilters.status) params.append('status', currentFilters.status)
      if (currentFilters.source) params.append('source', currentFilters.source)
      if (currentFilters.search) params.append('search', currentFilters.search)

      const response = await fetch(`/api/v1/alerts?${params}`)
      if (!response.ok) throw new Error('Failed to fetch alerts')
      
      const data = await response.json()
      setRealAlerts(data.alerts || [])
      setError(null)
    } catch (err) {
      setError(err as Error)
      setRealAlerts([])
    } finally {
      setLoading(false)
    }
  }, [currentFilters])

  useEffect(() => {
    fetchAlerts()
  }, [fetchAlerts])

  useEffect(() => {
    setCurrentFilters(filters)
  }, [filters])

  const alerts = useMemo(() => {
    if (!realAlerts) return null
    return [...realAlerts, ...simulatedAlerts]
  }, [realAlerts, simulatedAlerts])

  const injectSimulated = useCallback((newAlerts: Alert[]) => {
    setSimulatedAlerts(prev => [...newAlerts, ...prev].slice(0, 50)) // cap at 50
  }, [])

  const clearSimulated = useCallback(() => {
    setSimulatedAlerts([])
  }, [])

  const applyPreset = useCallback((preset: FilterPreset) => {
    setCurrentFilters(preset.filters)
  }, [])

  return { 
    alerts, 
    loading, 
    error, 
    refetch: fetchAlerts,
    groupedMode,
    setGroupedMode,
    injectSimulated,
    clearSimulated,
    applyPreset,
    currentFilters
  }
}
