import type { ButtonHTMLAttributes } from 'react'

type Variant = 'primary' | 'ghost'

// The single source of truth for buttons across the app so every CTA looks
// and behaves the same.
export default function Button({
  variant = 'primary',
  className = '',
  ...props
}: ButtonHTMLAttributes<HTMLButtonElement> & { variant?: Variant }) {
  const base =
    'inline-flex items-center justify-center rounded-md font-body font-bold transition-transform duration-150 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-deep/40 disabled:cursor-not-allowed disabled:opacity-60'

  const variants: Record<Variant, string> = {
    primary:
      'bg-chip px-7 py-3 text-base text-ink shadow-md shadow-deep/20 hover:-translate-y-0.5 hover:shadow-lg disabled:hover:translate-y-0',
    ghost: 'px-4 py-2 text-sm text-white/85 hover:text-white hover:-translate-y-0.5',
  }

  return <button className={`${base} ${variants[variant]} ${className}`} {...props} />
}
