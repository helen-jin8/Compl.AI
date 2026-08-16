import { useReport } from '../../store/ReportContext'

interface FeedbackGroup {
  heading: string
  items: string[]
}

const FEEDBACK_GROUPS: FeedbackGroup[] = [
  {
    heading: 'What looks solid',
    items: [
      'Enclosure meets IP54 for indoor use — no changes needed there.',
      'The 2.4 GHz radio module can cite its existing FCC ID instead of retesting from scratch.',
    ],
  },
  {
    heading: 'Things to consider',
    items: [
      'Battery pack will need a UN 38.3 test report before it can ship air freight to the EU lab.',
      'Label the charger input voltage range on the enclosure per UL 62368-1.',
      'Bench-test the repeated Bluetooth pairing failures from your intake — could be an antenna placement issue.',
    ],
  },
  {
    heading: 'Questions for you',
    items: [
      'Is the EU launch simultaneous with the US, or staggered? That changes which lab we book first.',
      "Do you have a target ship date? I'll pace the test schedule around it.",
    ],
  },
]

export default function FeedbackSection() {
  const { report } = useReport()
  if (!report) return null

  const firstName = report.founder.founderName.split(' ')[0]

  return (
    <div>
      <h2 className="font-display text-2xl text-ink">Patricia's feedback</h2>
      <p className="mt-3 font-sans text-base leading-relaxed text-ink-soft">
        Notes from your assigned compliance expert as she reviews the generated report.
      </p>

      <div className="relative mt-6 w-full overflow-hidden rounded-xl border border-ink/10 bg-white">
        <div className="space-y-6 p-6 sm:p-8">
          <p className="font-sans text-sm leading-relaxed text-ink">Hi {firstName},</p>
          <p className="font-sans text-sm leading-relaxed text-ink">
            I spent some time going through what hardware.check pulled together for{' '}
            <span className="font-bold">{report.projectName}</span> — here's where things stand.
          </p>

          {FEEDBACK_GROUPS.map((group, gi) => (
            <div key={group.heading}>
              <h3 className="font-sans text-sm font-extrabold uppercase tracking-wide text-ink">
                {group.heading}
              </h3>
              <ul className="mt-2 space-y-2">
                {group.items.map((item, i) => (
                  <li
                    key={i}
                    className={`flex gap-2.5 font-sans text-sm leading-relaxed text-ink ${
                      gi > 1 || (gi === 1 && i > 0) ? 'select-none blur-sm' : ''
                    }`}
                  >
                    <span className="mt-1.5 h-1.5 w-1.5 shrink-0 rounded-full bg-deep" />
                    <span>{item}</span>
                  </li>
                ))}
              </ul>
            </div>
          ))}

          <p className="select-none font-sans text-sm leading-relaxed text-ink blur-sm">
            — Patricia
          </p>
        </div>

        <div className="absolute inset-x-0 bottom-0 flex h-2/3 flex-col items-center justify-end gap-3 bg-gradient-to-t from-white via-white/95 to-transparent pb-6">
          <p className="font-sans text-sm text-ink">Unlock the rest of Patricia's feedback</p>
          <button className="rounded-full bg-deep px-5 py-2 font-sans text-sm font-bold text-white transition-transform hover:-translate-y-0.5">
            Upgrade to see full review
          </button>
        </div>
      </div>
    </div>
  )
}

