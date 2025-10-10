'use client'

import React, { useState } from 'react'
import { Download, FileText, FileJson, File, Loader } from 'lucide-react'

interface ExportFunctionalityProps {
  currentFilters?: any
  onExport: (format: string, filters?: any) => Promise<void>
}

export function ExportFunctionality({ currentFilters, onExport }: ExportFunctionalityProps) {
  const [showExportOptions, setShowExportOptions] = useState(false)
  const [exporting, setExporting] = useState(false)
  const [exportFormat, setExportFormat] = useState('csv')
  const [includeEnrichments, setIncludeEnrichments] = useState(true)

  const handleExport = async (format: string) => {
    setExporting(true)
    try {
      await onExport(format, currentFilters)
      setShowExportOptions(false)
    } catch (error) {
      console.error('Export failed:', error)
    } finally {
      setExporting(false)
    }
  }

  const getFormatIcon = (format: string) => {
    switch (format) {
      case 'csv':
        return <FileText className="h-4 w-4" />
      case 'json':
        return <FileJson className="h-4 w-4" />
      case 'pdf':
        return <File className="h-4 w-4" />
      default:
        return <Download className="h-4 w-4" />
    }
  }

  const getFormatDescription = (format: string) => {
    switch (format) {
      case 'csv':
        return 'Comma-separated values for Excel/Google Sheets'
      case 'json':
        return 'JSON format for API integration'
      case 'pdf':
        return 'PDF report for sharing and printing'
      default:
        return 'Download alerts data'
    }
  }

  return (
    <div className="relative">
      {/* Export Button */}
      <button
        onClick={() => setShowExportOptions(!showExportOptions)}
        className="flex items-center space-x-2 px-4 py-2 text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
      >
        <Download className="h-4 w-4" />
        <span>Export</span>
      </button>

      {/* Export Options Dropdown */}
      {showExportOptions && (
        <div className="absolute right-0 top-full mt-2 w-80 bg-white dark:bg-gray-800 rounded-lg shadow-lg border border-gray-200 dark:border-gray-700 z-50">
          <div className="p-4">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
              Export Alerts
            </h3>

            {/* Format Selection */}
            <div className="space-y-3 mb-4">
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
                Export Format
              </label>
              <div className="space-y-2">
                {['csv', 'json', 'pdf'].map(format => (
                  <label key={format} className="flex items-center space-x-3 cursor-pointer">
                    <input
                      type="radio"
                      name="exportFormat"
                      value={format}
                      checked={exportFormat === format}
                      onChange={(e) => setExportFormat(e.target.value)}
                      className="text-blue-600 focus:ring-blue-500"
                    />
                    <div className="flex items-center space-x-2">
                      {getFormatIcon(format)}
                      <span className="text-sm font-medium text-gray-900 dark:text-white capitalize">
                        {format.toUpperCase()}
                      </span>
                    </div>
                    <span className="text-xs text-gray-500 dark:text-gray-400">
                      {getFormatDescription(format)}
                    </span>
                  </label>
                ))}
              </div>
            </div>

            {/* Options */}
            <div className="space-y-3 mb-4">
              <label className="flex items-center space-x-2 cursor-pointer">
                <input
                  type="checkbox"
                  checked={includeEnrichments}
                  onChange={(e) => setIncludeEnrichments(e.target.checked)}
                  className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                />
                <span className="text-sm text-gray-700 dark:text-gray-300">
                  Include AI enrichments and correlations
                </span>
              </label>
            </div>

            {/* Current Filters Info */}
            {currentFilters && Object.keys(currentFilters).length > 0 && (
              <div className="mb-4 p-3 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
                <h4 className="text-sm font-medium text-blue-900 dark:text-blue-100 mb-2">
                  Exporting with current filters:
                </h4>
                <div className="text-xs text-blue-700 dark:text-blue-200 space-y-1">
                  {currentFilters.severity && currentFilters.severity.length > 0 && (
                    <div>Severity: {currentFilters.severity.join(', ')}</div>
                  )}
                  {currentFilters.status && currentFilters.status.length > 0 && (
                    <div>Status: {currentFilters.status.join(', ')}</div>
                  )}
                  {currentFilters.source && currentFilters.source.length > 0 && (
                    <div>Source: {currentFilters.source.join(', ')}</div>
                  )}
                  {currentFilters.time_range && (
                    <div>Time Range: {currentFilters.time_range}</div>
                  )}
                  {currentFilters.tags && currentFilters.tags.length > 0 && (
                    <div>Tags: {currentFilters.tags.join(', ')}</div>
                  )}
                </div>
              </div>
            )}

            {/* Action Buttons */}
            <div className="flex space-x-2">
              <button
                onClick={() => setShowExportOptions(false)}
                className="flex-1 px-3 py-2 text-sm font-medium text-gray-700 dark:text-gray-300 bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 rounded-lg transition-colors"
              >
                Cancel
              </button>
              <button
                onClick={() => handleExport(exportFormat)}
                disabled={exporting}
                className="flex-1 px-3 py-2 text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed rounded-lg transition-colors flex items-center justify-center space-x-2"
              >
                {exporting ? (
                  <>
                    <Loader className="h-4 w-4 animate-spin" />
                    <span>Exporting...</span>
                  </>
                ) : (
                  <>
                    <Download className="h-4 w-4" />
                    <span>Export {exportFormat.toUpperCase()}</span>
                  </>
                )}
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Backdrop */}
      {showExportOptions && (
        <div
          className="fixed inset-0 z-40"
          onClick={() => setShowExportOptions(false)}
        />
      )}
    </div>
  )
}

// Export Preview Component
interface ExportPreviewProps {
  data: any
  format: string
  onClose: () => void
}

export function ExportPreview({ data, format, onClose }: ExportPreviewProps) {
  const downloadFile = () => {
    const blob = new Blob([data.data], { type: 'text/plain' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = data.filename
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
    onClose()
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4">
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-xl max-w-4xl w-full max-h-[90vh] overflow-hidden">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-gray-200 dark:border-gray-700">
          <div className="flex items-center space-x-2">
            {getFormatIcon(format)}
            <h2 className="text-xl font-semibold text-gray-900 dark:text-white">
              Export Preview - {data.filename}
            </h2>
          </div>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
          >
            ×
          </button>
        </div>

        {/* Content */}
        <div className="p-6">
          <div className="mb-4 text-sm text-gray-600 dark:text-gray-400">
            Total records: {data.total_records}
          </div>
          
          <div className="bg-gray-50 dark:bg-gray-900 rounded-lg p-4 max-h-96 overflow-y-auto">
            <pre className="text-xs text-gray-800 dark:text-gray-200 whitespace-pre-wrap">
              {data.data}
            </pre>
          </div>
        </div>

        {/* Footer */}
        <div className="flex items-center justify-end space-x-3 p-6 border-t border-gray-200 dark:border-gray-700">
          <button
            onClick={onClose}
            className="px-4 py-2 text-sm font-medium text-gray-700 dark:text-gray-300 bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 rounded-lg transition-colors"
          >
            Close
          </button>
          <button
            onClick={downloadFile}
            className="px-4 py-2 text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 rounded-lg transition-colors flex items-center space-x-2"
          >
            <Download className="h-4 w-4" />
            <span>Download</span>
          </button>
        </div>
      </div>
    </div>
  )
}

function getFormatIcon(format: string) {
  switch (format) {
    case 'csv':
      return <FileText className="h-5 w-5 text-green-600" />
    case 'json':
      return <FileJson className="h-5 w-5 text-blue-600" />
    case 'pdf':
      return <File className="h-5 w-5 text-red-600" />
    default:
      return <Download className="h-5 w-5 text-gray-600" />
  }
}
