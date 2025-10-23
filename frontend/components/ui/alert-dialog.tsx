'use client'

import * as React from 'react'

const AlertDialog = ({
  open,
  onOpenChange,
  children
}: {
  open: boolean
  onOpenChange: (open: boolean) => void
  children: React.ReactNode
}) => {
  if (!open) return null
  
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center">
      <div className="fixed inset-0 bg-black/50" onClick={() => onOpenChange(false)} />
      <div className="relative bg-white dark:bg-gray-800 rounded-lg shadow-xl max-w-md w-full mx-4">
        {children}
      </div>
    </div>
  )
}

const AlertDialogContent = ({ children }: { children: React.ReactNode }) => {
  return <div className="p-6">{children}</div>
}

const AlertDialogHeader = ({ children }: { children: React.ReactNode }) => {
  return <div className="mb-4">{children}</div>
}

const AlertDialogTitle = ({ children }: { children: React.ReactNode }) => {
  return <h2 className="text-lg font-semibold text-gray-900 dark:text-gray-100">{children}</h2>
}

const AlertDialogDescription = ({ children }: { children: React.ReactNode }) => {
  return <p className="mt-2 text-sm text-gray-600 dark:text-gray-400">{children}</p>
}

const AlertDialogFooter = ({ children }: { children: React.ReactNode }) => {
  return <div className="mt-6 flex justify-end space-x-3">{children}</div>
}

const AlertDialogAction = ({
  children,
  onClick
}: {
  children: React.ReactNode
  onClick?: () => void
}) => {
  return (
    <button
      onClick={onClick}
      className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors"
    >
      {children}
    </button>
  )
}

const AlertDialogCancel = ({ children }: { children: React.ReactNode }) => {
  return (
    <button className="px-4 py-2 bg-gray-100 dark:bg-gray-700 text-gray-900 dark:text-gray-100 rounded-md hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors">
      {children}
    </button>
  )
}

export {
  AlertDialog,
  AlertDialogContent,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogAction,
  AlertDialogCancel
}

