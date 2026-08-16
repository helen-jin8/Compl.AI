import { useReport } from '../../store/ReportContext'

export default function LabsSection() {
  const { report } = useReport()
  if (!report) return null

  return (
    <div>
      <h2 className="font-display text-2xl text-ink">Labs</h2>
      <p className="mt-3 max-w-3xl font-sans text-base leading-relaxed text-ink-soft">
        Accredited test labs that can run the standards above, ranked by how much of your scope
        each one covers in a single engagement. Reach out through us and we'll coordinate the
        booking.
      </p>

      <div className="mt-6 grid gap-3 sm:grid-cols-2">
        {report.labs.map((lab) => (
          <div
            key={lab.id}
            className="rounded-xl border border-ink/10 bg-white p-4 transition-all hover:border-2 hover:border-ink/30 hover:shadow-md"
          >
            <div className="flex items-start justify-between gap-3">
              <div>
                <p className="font-sans text-base font-bold text-ink">{lab.name}</p>
                <p className="font-sans text-xs text-ink-soft">{lab.location}</p>
              </div>
              {/* Scope coverage, not a review score — a star would read as one. */}
              <span
                className="shrink-0 rounded-full bg-chip px-2.5 py-0.5 font-sans text-xs font-bold text-deep"
                title="How much of your compliance scope this lab covers in one engagement. Not a customer rating."
              >
                {lab.rating.toFixed(1)}/5 scope fit
              </span>
            </div>
            <p className="mt-2.5 font-sans text-sm leading-relaxed text-ink-soft">
              {lab.specialty}
            </p>
            <div className="mt-3 flex flex-wrap gap-1.5">
              {lab.accreditations.map((a) => (
                <span
                  key={a}
                  className="rounded-md border border-ink/15 bg-chip/30 px-2 py-0.5 font-sans text-xs font-bold text-ink"
                >
                  {a}
                </span>
              ))}
            </div>
            <p className="mt-3 font-sans text-xs text-ink-soft">
              Typical industry lead time ·{' '}
              <span className="font-bold text-ink">{lab.leadTime}</span>
            </p>
          </div>
        ))}
      </div>

      <p className="mt-6 max-w-3xl font-sans text-xs leading-relaxed text-ink-soft">
        Lead times are industry-typical ranges for this kind of testing, not quotes from these
        labs. Confirm accreditation scope and current availability directly before booking.
      </p>
    </div>
  )
}
