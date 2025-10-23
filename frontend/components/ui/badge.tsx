'use client'

import * as React from 'react'

export interface BadgeProps extends React.HTMLAttributes<HTMLDivElement> {
  variant?: 'default' | 'outline'
}

function Badge({ className = '', variant = 'default', ...props }: BadgeProps) {
  const baseStyles = 'inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-semibold transition-colors'
  
  const variants = {
    default: 'bg-blue-100 text-blue-800 dark:bg-blue-900/20 dark:text-blue-400',
    outline: 'border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300'
  }
  
  return (
    <div className={`${baseStyles} ${variants[variant]} ${className}`} {...props} />
  )
}

export { Badge }

