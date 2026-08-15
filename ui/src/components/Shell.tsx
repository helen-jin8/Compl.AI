import type { ReactNode } from 'react'
import { Link } from 'react-router'

// Every screen shares the soft blue gradient + dot-grid ground and the wordmark.
export default function Shell({
  children,
  maxWidth = 'max-w-5xl',
}: {
  children: ReactNode
  maxWidth?: string
}) {
  return (
    <div className="fc-ground w-full">
      <header className="mx-auto flex max-w-[1400px] items-center justify-between px-6 py-5 sm:px-10">
        <Link
          to="/"
          className="font-display text-2xl text-white transition-opacity hover:opacity-80 sm:text-3xl"
        >
          hardware<span className="text-chip">.check</span>
        </Link>
        <span className="hidden font-body text-xs text-white/80 sm:block">
          AI compliance reports · expert reviewed
        </span>
      </header>
      <main className={`mx-auto ${maxWidth} px-6 pb-16 sm:px-10`}>{children}</main>
    </div>
  )
}
