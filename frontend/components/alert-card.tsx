'use client'

import { useState } from 'react'
import { formatDistanceToNow } from 'date-fns'
import { 
  AlertTriangle, 
  Clock, 
  User, 
  Tag, 
  MoreVertical, 
  CheckCircle, 
  XCircle, 
  Eye,
  Brain,
  Link
} from 'lucide-react'
import { Alert } from '@/types'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from '@/components/ui/dropdown-menu'
import { AlertDialog, AlertDialogAction, AlertDialogCancel, AlertDialogContent, AlertDialogDescription, AlertDialogFooter, AlertDialogHeader, AlertDialogTitle } from '@/components/ui/alert-dialog'

interface AlertCardProps {
  alert: Alert
  onAction: (alertId: string, action: string) => void
}

export function AlertCard({ alert, onAction }: AlertCardProps) {
  const [showDetails, setShowDetails] = useState(false)
  const [actionDialog, setActionDialog] = useState<{ action: string; open: boolean }>({ action: '', open: false })

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'critical':
        return 'bg-red-100 text-red-800 dark:bg-red-900/20 dark:text-red-400'
      case 'high':
        return 'bg-orange-100 text-orange-800 dark:bg-orange-900/20 dark:text-orange-400'
      case 'medium':
        return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/20 dark:text-yellow-400'
      case 'low':
        return 'bg-green-100 text-green-800 dark:bg-green-900/20 dark:text-green-400'
      case 'info':
        return 'bg-blue-100 text-blue-800 dark:bg-blue-900/20 dark:text-blue-400'
      default:
        return 'bg-gray-100 text-gray-800 dark:bg-gray-900/20 dark:text-gray-400'
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active':
        return 'bg-red-100 text-red-800 dark:bg-red-900/20 dark:text-red-400'
      case 'acknowledged':
        return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/20 dark:text-yellow-400'
      case 'resolved':
        return 'bg-green-100 text-green-800 dark:bg-green-900/20 dark:text-green-400'
      case 'suppressed':
        return 'bg-gray-100 text-gray-800 dark:bg-gray-900/20 dark:text-gray-400'
      case 'dismissed':
        return 'bg-gray-100 text-gray-800 dark:bg-gray-900/20 dark:text-gray-400'
      default:
        return 'bg-gray-100 text-gray-800 dark:bg-gray-900/20 dark:text-gray-400'
    }
  }

  const handleAction = (action: string) => {
    setActionDialog({ action, open: true })
  }

  const confirmAction = () => {
    onAction(alert.id, actionDialog.action)
    setActionDialog({ action: '', open: false })
  }

  const formatTime = (timestamp: string) => {
    return formatDistanceToNow(new Date(timestamp), { addSuffix: true })
  }

  return (
    <>
      <div className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 hover:shadow-md transition-shadow">
        <div className="p-4">
          <div className="flex items-start justify-between">
            <div className="flex-1 min-w-0">
              <div className="flex items-center space-x-3 mb-2">
                <AlertTriangle className={`h-5 w-5 ${
                  alert.severity === 'critical' ? 'text-red-500' :
                  alert.severity === 'high' ? 'text-orange-500' :
                  alert.severity === 'medium' ? 'text-yellow-500' :
                  alert.severity === 'low' ? 'text-green-500' :
                  'text-blue-500'
                }`} />
                <h3 className="text-lg font-medium text-gray-900 dark:text-gray-100 truncate">
                  {alert.title}
                </h3>
                <Badge className={getSeverityColor(alert.severity)}>
                  {alert.severity.toUpperCase()}
                </Badge>
                <Badge className={getStatusColor(alert.status)}>
                  {alert.status.toUpperCase()}
                </Badge>
              </div>
              
              {alert.description && (
                <p className="text-sm text-gray-600 dark:text-gray-400 mb-3 line-clamp-2">
                  {alert.description}
                </p>
              )}

              <div className="flex items-center space-x-4 text-xs text-gray-500 dark:text-gray-400">
                <div className="flex items-center space-x-1">
                  <Clock className="h-3 w-3" />
                  <span>{formatTime(alert.started_at)}</span>
                </div>
                <div className="flex items-center space-x-1">
                  <Tag className="h-3 w-3" />
                  <span>{alert.source}</span>
                </div>
                {alert.assignee && (
                  <div className="flex items-center space-x-1">
                    <User className="h-3 w-3" />
                    <span>{alert.assignee}</span>
                  </div>
                )}
              </div>

              {/* Labels */}
              {Object.keys(alert.labels).length > 0 && (
                <div className="mt-3 flex flex-wrap gap-1">
                  {Object.entries(alert.labels).slice(0, 3).map(([key, value]) => (
                    <Badge key={key} variant="outline" className="text-xs">
                      {key}: {value}
                    </Badge>
                  ))}
                  {Object.keys(alert.labels).length > 3 && (
                    <Badge variant="outline" className="text-xs">
                      +{Object.keys(alert.labels).length - 3} more
                    </Badge>
                  )}
                </div>
              )}

              {/* AI Features */}
              {(alert.enrichments.length > 0 || alert.correlations.length > 0) && (
                <div className="mt-3 flex items-center space-x-2">
                  {alert.enrichments.length > 0 && (
                    <div className="flex items-center space-x-1 text-xs text-blue-600 dark:text-blue-400">
                      <Brain className="h-3 w-3" />
                      <span>AI Enriched</span>
                    </div>
                  )}
                  {alert.correlations.length > 0 && (
                    <div className="flex items-center space-x-1 text-xs text-purple-600 dark:text-purple-400">
                      <Link className="h-3 w-3" />
                      <span>{alert.correlations.length} Correlations</span>
                    </div>
                  )}
                </div>
              )}
            </div>

            <div className="flex items-center space-x-2">
              <Button
                variant="ghost"
                size="sm"
                onClick={() => setShowDetails(!showDetails)}
              >
                <Eye className="h-4 w-4" />
              </Button>
              
              <DropdownMenu>
                <DropdownMenuTrigger asChild>
                  <Button variant="ghost" size="sm">
                    <MoreVertical className="h-4 w-4" />
                  </Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent align="end">
                  {alert.status === 'active' && (
                    <>
                      <DropdownMenuItem onClick={() => handleAction('acknowledge')}>
                        <CheckCircle className="h-4 w-4 mr-2" />
                        Acknowledge
                      </DropdownMenuItem>
                      <DropdownMenuItem onClick={() => handleAction('suppress')}>
                        <XCircle className="h-4 w-4 mr-2" />
                        Suppress
                      </DropdownMenuItem>
                    </>
                  )}
                  {alert.status === 'acknowledged' && (
                    <DropdownMenuItem onClick={() => handleAction('resolve')}>
                      <CheckCircle className="h-4 w-4 mr-2" />
                      Resolve
                    </DropdownMenuItem>
                  )}
                  <DropdownMenuItem onClick={() => handleAction('enrich')}>
                    <Brain className="h-4 w-4 mr-2" />
                    AI Enrich
                  </DropdownMenuItem>
                </DropdownMenuContent>
              </DropdownMenu>
            </div>
          </div>

          {/* Expanded Details */}
          {showDetails && (
            <div className="mt-4 pt-4 border-t border-gray-200 dark:border-gray-700">
              <div className="space-y-3">
                {/* Annotations */}
                {Object.keys(alert.annotations).length > 0 && (
                  <div>
                    <h4 className="text-sm font-medium text-gray-900 dark:text-gray-100 mb-2">
                      Annotations
                    </h4>
                    <div className="space-y-1">
                      {Object.entries(alert.annotations).map(([key, value]) => (
                        <div key={key} className="text-sm">
                          <span className="font-medium text-gray-700 dark:text-gray-300">{key}:</span>
                          <span className="ml-2 text-gray-600 dark:text-gray-400">{value}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Enrichments */}
                {alert.enrichments.length > 0 && (
                  <div>
                    <h4 className="text-sm font-medium text-gray-900 dark:text-gray-100 mb-2">
                      AI Enrichments
                    </h4>
                    <div className="space-y-1">
                      {alert.enrichments.map((enrichment) => (
                        <div key={enrichment.id} className="text-sm">
                          <span className="font-medium text-gray-700 dark:text-gray-300">{enrichment.key}:</span>
                          <span className="ml-2 text-gray-600 dark:text-gray-400">{enrichment.value}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Correlations */}
                {alert.correlations.length > 0 && (
                  <div>
                    <h4 className="text-sm font-medium text-gray-900 dark:text-gray-100 mb-2">
                      Correlations
                    </h4>
                    <div className="space-y-1">
                      {alert.correlations.map((correlation) => (
                        <div key={correlation.id} className="text-sm">
                          <span className="text-gray-600 dark:text-gray-400">
                            {correlation.correlation_type} (confidence: {Math.round(correlation.confidence * 100)}%)
                          </span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Action Confirmation Dialog */}
      <AlertDialog open={actionDialog.open} onOpenChange={(open) => setActionDialog({ action: '', open })}>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>Confirm Action</AlertDialogTitle>
            <AlertDialogDescription>
              Are you sure you want to {actionDialog.action} this alert? This action cannot be undone.
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel>Cancel</AlertDialogCancel>
            <AlertDialogAction onClick={confirmAction}>
              Confirm
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </>
  )
}
