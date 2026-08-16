import { useReport } from '../../store/ReportContext'

export default function SummarySection() {
  const { report } = useReport()
  if (!report) return null

  return (
    <div>
      <h2 className="font-display text-2xl text-ink">Project summary</h2>
      <p className="mt-3 max-w-3xl font-sans text-base leading-relaxed text-ink-soft">
        A structured description of the hardware, as understood for certification scoping.
      </p>

      <article className="mt-6 max-w-3xl bg-white">
        {report.summary.map((section, i) => (
          <section key={section.id} className={i > 0 ? 'mt-6' : ''}>
            <h3 className="font-display text-lg text-ink">{section.heading}</h3>
            {section.paragraphs?.map((p, pi) => (
              <p key={pi} className="mt-2 font-sans text-sm leading-relaxed text-ink-soft">
                {p}
              </p>
            ))}
            {section.bullets && (
              <ul className="mt-2 list-disc space-y-1 pl-5">
                {section.bullets.map((b, bi) => (
                  <li key={bi} className="font-sans text-sm leading-relaxed text-ink-soft">
                    {b}
                  </li>
                ))}
              </ul>
            )}
          </section>
        ))}
      </article>
    </div>
  )
}

