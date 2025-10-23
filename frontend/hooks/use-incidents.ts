import { useState, useEffect } from 'react'
import { Incident } from '@/types'

interface UseIncidentsReturn {
  incidents: Incident[] | null
  loading: boolean
  error: Error | null
  refetch: () => Promise<void>
}

export function useIncidents(): UseIncidentsReturn {
  const [incidents, setIncidents] = useState<Incident[] | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<Error | null>(null)

  const fetchIncidents = async () => {
    try {
      setLoading(true)
      const response = await fetch('/api/v1/incidents')
      if (!response.ok) throw new Error('Failed to fetch incidents')
      
      const data = await response.json()
      setIncidents(data.incidents || [])
      setError(null)
    } catch (err) {
      setError(err as Error)
      setIncidents([])
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchIncidents()
  }, [])

  return { incidents, loading, error, refetch: fetchIncidents }
}

