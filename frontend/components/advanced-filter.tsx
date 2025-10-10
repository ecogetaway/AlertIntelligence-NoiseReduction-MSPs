'use client'

import React, { useState, useEffect } from 'react'
import { Filter, X, Calendar, Tag, Search, SortAsc, SortDesc } from 'lucide-react'

interface FilterOptions {
  severities: string[]
  statuses: string[]
  sources: string[]
  tags: string[]
  time_ranges: string[]
}

interface AdvancedFilterProps {
  onFilterChange: (filters: FilterState) => void
  onClose: () => void
  isOpen: boolean
}

interface FilterState {
  severity: string[]
  status: string[]
  source: string[]
  time_range: string
  tags: string[]
  search: string
  sort_by: string
  sort_order: string
}

export function AdvancedFilter({ onFilterChange, onClose, isOpen }: AdvancedFilterProps) {
  const [filters, setFilters] = useState<FilterState>({
    severity: [],
    status: [],
    source: [],
    time_range: '',
    tags: [],
    search: '',
    sort_by: 'created_at',
    sort_order: 'desc'
  })

  const [filterOptions, setFilterOptions] = useState<FilterOptions>({
    severities: [],
    statuses: [],
    sources: [],
    tags: [],
    time_ranges: []
  })

  const [loading, setLoading] = useState(false)

  // Load filter options on mount
  useEffect(() => {
    loadFilterOptions()
  }, [])

  const loadFilterOptions = async () => {
    try {
      const response = await fetch('/api/v1/alerts/advanced-filter')
      const data = await response.json()
      setFilterOptions(data.filter_options)
    } catch (error) {
      console.error('Error loading filter options:', error)
    }
  }

  const handleFilterChange = (key: keyof FilterState, value: any) => {
    const newFilters = { ...filters, [key]: value }
    setFilters(newFilters)
    onFilterChange(newFilters)
  }

  const handleMultiSelect = (key: 'severity' | 'status' | 'source' | 'tags', value: string) => {
    const currentValues = filters[key] as string[]
    const newValues = currentValues.includes(value)
      ? currentValues.filter(v => v !== value)
      : [...currentValues, value]
    
    handleFilterChange(key, newValues)
  }

  const clearFilters = () => {
    const clearedFilters = {
      severity: [],
      status: [],
      source: [],
      time_range: '',
      tags: [],
      search: '',
      sort_by: 'created_at',
      sort_order: 'desc'
    }
    setFilters(clearedFilters)
    onFilterChange(clearedFilters)
  }

  const getActiveFilterCount = () => {
    return filters.severity.length + 
           filters.status.length + 
           filters.source.length + 
           filters.tags.length + 
           (filters.time_range ? 1 : 0) + 
           (filters.search ? 1 : 0)
  }

  if (!isOpen) return null

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4">
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-xl max-w-4xl w-full max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-gray-200 dark:border-gray-700">
          <div className="flex items-center space-x-2">
            <Filter className="h-5 w-5 text-blue-600" />
            <h2 className="text-xl font-semibold text-gray-900 dark:text-white">
              Advanced Filters
            </h2>
            {getActiveFilterCount() > 0 && (
              <span className="bg-blue-100 text-blue-800 text-xs font-medium px-2.5 py-0.5 rounded-full">
                {getActiveFilterCount()} active
              </span>
            )}
          </div>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
          >
            <X className="h-6 w-6" />
          </button>
        </div>

        {/* Filter Content */}
        <div className="p-6 space-y-6">
          {/* Search */}
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Search
            </label>
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
              <input
                type="text"
                value={filters.search}
                onChange={(e) => handleFilterChange('search', e.target.value)}
                placeholder="Search alerts..."
                className="w-full pl-10 pr-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
              />
            </div>
          </div>

          {/* Time Range */}
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              <Calendar className="inline h-4 w-4 mr-1" />
              Time Range
            </label>
            <select
              value={filters.time_range}
              onChange={(e) => handleFilterChange('time_range', e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
            >
              <option value="">All time</option>
              {filterOptions.time_ranges.map(range => (
                <option key={range} value={range}>
                  {range.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}
                </option>
              ))}
            </select>
          </div>

          {/* Severity */}
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Severity
            </label>
            <div className="grid grid-cols-2 gap-2">
              {filterOptions.severities.map(severity => (
                <label key={severity} className="flex items-center space-x-2 cursor-pointer">
                  <input
                    type="checkbox"
                    checked={filters.severity.includes(severity)}
                    onChange={() => handleMultiSelect('severity', severity)}
                    className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                  />
                  <span className="text-sm text-gray-700 dark:text-gray-300 capitalize">
                    {severity}
                  </span>
                </label>
              ))}
            </div>
          </div>

          {/* Status */}
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Status
            </label>
            <div className="grid grid-cols-2 gap-2">
              {filterOptions.statuses.map(status => (
                <label key={status} className="flex items-center space-x-2 cursor-pointer">
                  <input
                    type="checkbox"
                    checked={filters.status.includes(status)}
                    onChange={() => handleMultiSelect('status', status)}
                    className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                  />
                  <span className="text-sm text-gray-700 dark:text-gray-300 capitalize">
                    {status}
                  </span>
                </label>
              ))}
            </div>
          </div>

          {/* Source */}
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Source
            </label>
            <div className="grid grid-cols-2 gap-2">
              {filterOptions.sources.map(source => (
                <label key={source} className="flex items-center space-x-2 cursor-pointer">
                  <input
                    type="checkbox"
                    checked={filters.source.includes(source)}
                    onChange={() => handleMultiSelect('source', source)}
                    className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                  />
                  <span className="text-sm text-gray-700 dark:text-gray-300 capitalize">
                    {source}
                  </span>
                </label>
              ))}
            </div>
          </div>

          {/* Tags */}
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              <Tag className="inline h-4 w-4 mr-1" />
              Tags
            </label>
            <div className="flex flex-wrap gap-2">
              {filterOptions.tags.map(tag => (
                <button
                  key={tag}
                  onClick={() => handleMultiSelect('tags', tag)}
                  className={`px-3 py-1 rounded-full text-sm font-medium transition-colors ${
                    filters.tags.includes(tag)
                      ? 'bg-blue-100 text-blue-800 border border-blue-200'
                      : 'bg-gray-100 text-gray-700 border border-gray-200 hover:bg-gray-200'
                  }`}
                >
                  {tag}
                </button>
              ))}
            </div>
          </div>

          {/* Sorting */}
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Sort By
              </label>
              <select
                value={filters.sort_by}
                onChange={(e) => handleFilterChange('sort_by', e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
              >
                <option value="created_at">Created Date</option>
                <option value="severity">Severity</option>
                <option value="title">Title</option>
                <option value="status">Status</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Order
              </label>
              <div className="flex space-x-2">
                <button
                  onClick={() => handleFilterChange('sort_order', 'desc')}
                  className={`flex items-center space-x-1 px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                    filters.sort_order === 'desc'
                      ? 'bg-blue-100 text-blue-800 border border-blue-200'
                      : 'bg-gray-100 text-gray-700 border border-gray-200 hover:bg-gray-200'
                  }`}
                >
                  <SortDesc className="h-4 w-4" />
                  <span>Desc</span>
                </button>
                <button
                  onClick={() => handleFilterChange('sort_order', 'asc')}
                  className={`flex items-center space-x-1 px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                    filters.sort_order === 'asc'
                      ? 'bg-blue-100 text-blue-800 border border-blue-200'
                      : 'bg-gray-100 text-gray-700 border border-gray-200 hover:bg-gray-200'
                  }`}
                >
                  <SortAsc className="h-4 w-4" />
                  <span>Asc</span>
                </button>
              </div>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="flex items-center justify-between p-6 border-t border-gray-200 dark:border-gray-700">
          <button
            onClick={clearFilters}
            className="text-sm text-gray-600 hover:text-gray-800 dark:text-gray-400 dark:hover:text-gray-200"
          >
            Clear all filters
          </button>
          <div className="flex space-x-3">
            <button
              onClick={onClose}
              className="px-4 py-2 text-sm font-medium text-gray-700 dark:text-gray-300 bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 rounded-lg transition-colors"
            >
              Cancel
            </button>
            <button
              onClick={onClose}
              className="px-4 py-2 text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 rounded-lg transition-colors"
            >
              Apply Filters
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}
