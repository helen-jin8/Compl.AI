import { useReport } from '../../store/ReportContext'

const FEEDBACK_ITEMS = [
  'Confirmed the enclosure meets IP54 for indoor use — no changes needed there.',
  'Battery pack will need a UN 38.3 test report before it can ship air freight to the EU lab.',
  'The 2.4 GHz radio module can cite its existing FCC ID instead of retesting from scratch.',
  'Label the charger input voltage range on the enclosure per UL 62368-1 before submission.',
  'Flagged one open question about the repeated Bluetooth pairing failures in your test notes.',
]

export default function FeedbackSection() {
  const { report } = useReport()
  if (!report) return null

  return (
    <div>
      <h2 className="font-display text-2xl text-ink">Patricia's feedback</h2>
      <p className="mt-3 max-w-3xl font-sans text-base leading-relaxed text-ink-soft">
        Notes from your assigned compliance expert as she reviews the generated report.
      </p>

      <div className="relative mt-6 max-w-3xl overflow-hidden rounded-xl border border-ink/10 bg-white">
        <ul className="space-y-3 p-6">
          {FEEDBACK_ITEMS.map((item, i) => (
            <li
              key={i}
              className={`flex gap-2.5 font-sans text-sm leading-relaxed text-ink ${
                i > 0 ? 'select-none blur-sm' : ''
              }`}
            >
              <span className="mt-1.5 h-1.5 w-1.5 shrink-0 rounded-full bg-deep" />
              <span>{item}</span>
            </li>
          ))}
        </ul>

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
