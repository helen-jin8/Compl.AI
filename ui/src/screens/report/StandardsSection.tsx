import { useState } from 'react'
import { useReport } from '../../store/ReportContext'
import type { ComplianceCheck } from '../../api/complianceApi'

const statusStyle: Record<string, string> = {
  required: 'bg-red-100 text-red-700',
  recommended: 'bg-amber-100 text-amber-700',
  passed: 'bg-emerald-100 text-emerald-700',
}

export default function StandardsSection() {
  const { report } = useReport()
  const [open, setOpen] = useState<string | null>(report?.checks[0]?.id ?? null)
  if (!report) return null

  return (
    <div>
      <h2 className="font-display text-2xl text-ink">Standards</h2>
      <p className="mt-3 max-w-3xl font-sans text-base leading-relaxed text-ink-soft">
        The following standards are necessary for testing. Tap any row to expand the scope, cost,
        and timeline.
      </p>

      <div className="mt-6 space-y-2.5">
        {report.checks.map((check) => (
          <CheckRow
            key={check.id}
            check={check}
            expanded={open === check.id}
            onToggle={() => setOpen(open === check.id ? null : check.id)}
          />
        ))}
      </div>

      <AskExpert />
    </div>
  )
}

function CheckRow({
  check,
  expanded,
  onToggle,
}: {
  check: ComplianceCheck
  expanded: boolean
  onToggle: () => void
}) {
  return (
    <div className="overflow-hidden rounded-xl border border-ink/10 bg-white transition-all hover:border-2 hover:border-ink/30 hover:shadow-md">
      <button onClick={onToggle} className="flex w-full items-center gap-3 px-4 py-3 text-left">
        <div className="flex-1">
          <p className="font-sans text-base font-bold text-ink">{check.code}</p>
          <p className="font-sans text-xs text-ink-soft">{check.title}</p>
        </div>
        <span
          className={`hidden rounded-full px-2.5 py-0.5 font-sans text-xs font-bold uppercase sm:block ${statusStyle[check.status]}`}
        >
          {check.status}
        </span>
        <span
          className={`font-sans text-sm text-ink-soft transition-transform ${expanded ? 'rotate-180' : ''}`}
        >
          ▾
        </span>
      </button>
      {expanded && (
        <div className="border-t border-ink/10 bg-chip/20 px-4 py-4">
          <p className="font-sans text-sm leading-relaxed text-ink">{check.detail}</p>
          <div className="mt-3 grid gap-3 sm:grid-cols-3">
            <Meta label="Scope" value={check.scope} />
            <Meta label="Est. cost" value={check.estimatedCost} />
            <Meta label="Turnaround" value={check.turnaround} />
          </div>
        </div>
      )}
    </div>
  )
}

function Meta({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-lg bg-white px-3.5 py-2.5">
      <p className="font-sans text-xs uppercase tracking-wide text-ink-soft">{label}</p>
      <p className="mt-0.5 font-sans text-sm font-bold text-ink">{value}</p>
    </div>
  )
}

function AskExpert() {
  const [value, setValue] = useState('')
  const [sent, setSent] = useState(false)

  const send = () => {
    if (!value.trim()) return
    setSent(true)
    setValue('')
    setTimeout(() => setSent(false), 3500)
  }

  return (
    <div className="mt-6 rounded-xl border border-ink/20 bg-white p-4">
      <div className="flex items-center justify-between">
        <p className="font-sans text-sm font-bold text-ink">Ask an expert</p>
        <p className="font-sans text-xs text-ink-soft">gets back to you in 2–3 hours</p>
      </div>
      <div className="mt-2.5 flex items-center gap-2.5">
        <input
          value={value}
          onChange={(e) => setValue(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && send()}
          placeholder="e.g. Can I bundle the Part 15B and 15C testing in one visit?"
          className="fc-field flex-1"
        />
        <button
          onClick={send}
          aria-label="Send question to expert"
          className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-deep text-white transition-transform hover:-translate-y-0.5"
        >
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
            <path
              d="M3.4 20.4 21 12 3.4 3.6 3.4 10.2 15 12 3.4 13.8 3.4 20.4Z"
              fill="currentColor"
            />
          </svg>
        </button>
      </div>
      {sent && (
        <p className="mt-2.5 font-sans text-xs font-bold text-emerald-600">
          ✓ Sent to Patricia — she'll reply by email.
        </p>
      )}
    </div>
  )
}
