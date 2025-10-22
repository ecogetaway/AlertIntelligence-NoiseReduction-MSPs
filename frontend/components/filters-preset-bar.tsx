'use client'

import { useEffect, useMemo, useState } from 'react'
import { Filter } from 'lucide-react'
import type { AlertFilters, FilterPreset } from '@/types'

interface Props {
  currentFilters: AlertFilters
  onApply: (filters: AlertFilters) => void
}

const BUILT_IN: FilterPreset[] = [
  {
    id: 'critical-only',
    name: 'Critical Only',
    filters: { severity: 'critical' },
    created_at: new Date().toISOString()
  },
  {
    id: 'active-incidents',
    name: 'Active Incidents',
    filters: { status: 'active' },
   created_at: new Date().toISOString()
  },
  {
    id: 'noisy-sources',
    name: 'Noisy Sources',
    filters: { source: 'prometheus' },
    created_at: new Date().toISOString()
  }
]

export function FiltersPresetBar({ currentFilters, onApply }: Props) {
  const [customPresets, setCustomPresets] = useState<FilterPreset[]>([])

  useEffect(() => {
    try {
      const raw = localStorage.getItem('msp-presets')
      if (raw) setCustomPresets(JSON.parse(raw))
    } catch {
      // ignore
    }
  }, [])

  useEffect(() => {
    try {
      localStorage.setItem('msp-presets', JSON.stringify(customPresets))
    } catch {
      // ignore
    }
  }, [customPresets])

  function handleSavePreset() {
    const name = prompt('Name this view (preset):')?.trim()
    if (!name) return
    const preset: FilterPreset = {
      id: `preset-${Date.now()}`,
      name,
      filters: currentFilters,
      created_at: new Date().toISOString()
    }
    setCustomPresets(p => [preset, ...p])
  }

  function handleApply(preset: FilterPreset) {
    onApply(preset.filters)
  }

  function handleDelete(id: string) {
    setCustomPresets(p => p.filter(x => x.id !== id))
  }

  const allPresets = useMemo(() => [...BUILT_IN, ...customPresets], [customPresets])

  return (
    <div className="flex items-center justify-between bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg px-3 py-2">
      <div className="flex items-center gap-2 overflow-x-auto">
        <span className="inline-flex items-center gap-1 text-gray-600 dark:text-gray-300 text-sm">
          <Filter className="h-4 w-4" /> Presets:
        </span>
        {allPresets.map(preset => (
          <button
            key={preset.id}
            onClick={() => handleApply(preset)}
            className="px-2 py-1 text-xs rounded-md bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-gray-200 hover:bg-gray-200 dark:hover:bg-gray-600 whitespace-nowrap"
            aria-label={`Apply preset ${preset.name}`}
          >
            {preset.name}
          </button>
        ))}
      </div>
      <div className="flex items-center gap-2">
        <button
          onClick={handleSavePreset}
          className="px-2 py-1 text-xs rounded-md bg-blue-600 text-white hover:bg-blue-700"
          aria-label="Save current filters as preset"
        >
          Save view
        </button>
        {customPresets.length > 0 && (
          <button
            onClick={() => {
              const id = prompt('Delete preset by name:')
              if (!id) return
              const found = customPresets.find(p => p.name === id)
              if (found) handleDelete(found.id)
            }}
            className="px-2 py-1 text-xs rounded-md bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-gray-200 hover:bg-gray-200 dark:hover:bg-gray-600"
            aria-label="Delete a saved preset"
          >
            Delete preset
          </button>
        )}
      </div>
    </div>
  )
}

export default FiltersPresetBar


