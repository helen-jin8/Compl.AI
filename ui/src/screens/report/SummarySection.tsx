import { useReport } from '../../store/ReportContext'

const impactStyle: Record<string, string> = {
  high: 'bg-red-100 text-red-700',
  medium: 'bg-amber-100 text-amber-700',
  low: 'bg-emerald-100 text-emerald-700',
}

export default function SummarySection() {
  const { report } = useReport()
  if (!report) return null

  return (
    <div>
      <h2 className="font-display text-2xl text-ink">Project summary</h2>
      <p className="mt-3 max-w-3xl font-sans text-base leading-relaxed text-ink-soft">
        {report.summary}
      </p>

      <h3 className="mt-8 font-body text-lg font-bold text-ink">What we changed</h3>
      <p className="font-body text-xs text-ink-soft">
        How the plan shifted as the agents read your description against the standards.
      </p>
      <ul className="mt-4 space-y-3">
        {report.changes.map((change) => (
          <li
            key={change.id}
            className="rounded-xl border border-ink/10 bg-white p-4 transition-shadow hover:shadow-md"
          >
            <div className="flex items-start justify-between gap-3">
              <p className="font-body text-base font-bold text-ink">{change.title}</p>
              <span
                className={`shrink-0 rounded-full px-2.5 py-0.5 font-body text-xs font-bold uppercase ${impactStyle[change.impact]}`}
              >
                {change.impact}
              </span>
            </div>
            <p className="mt-1.5 font-sans text-sm leading-relaxed text-ink-soft">
              {change.detail}
            </p>
          </li>
        ))}
      </ul>
    </div>
  )
}
