'use client'

import * as React from 'react'

const DropdownMenu = ({ children }: { children: React.ReactNode }) => {
  return <div className="relative inline-block">{children}</div>
}

const DropdownMenuTrigger = React.forwardRef<
  HTMLDivElement,
  { asChild?: boolean; children: React.ReactNode }
>(({ children }, ref) => {
  return <div ref={ref}>{children}</div>
})
DropdownMenuTrigger.displayName = 'DropdownMenuTrigger'

const DropdownMenuContent = ({
  children,
  align = 'start'
}: {
  children: React.ReactNode
  align?: 'start' | 'end'
}) => {
  return (
    <div className={`absolute ${align === 'end' ? 'right-0' : 'left-0'} mt-2 w-48 rounded-md shadow-lg bg-white dark:bg-gray-800 ring-1 ring-black ring-opacity-5 z-50`}>
      <div className="py-1" role="menu">
        {children}
      </div>
    </div>
  )
}

const DropdownMenuItem = ({
  children,
  onClick
}: {
  children: React.ReactNode
  onClick?: () => void
}) => {
  return (
    <button
      className="w-full text-left px-4 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 flex items-center"
      onClick={onClick}
      role="menuitem"
    >
      {children}
    </button>
  )
}

export { DropdownMenu, DropdownMenuTrigger, DropdownMenuContent, DropdownMenuItem }

