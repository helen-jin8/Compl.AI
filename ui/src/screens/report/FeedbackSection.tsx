import { useState } from 'react'
import Button from '../../components/Button'
import { useReport } from '../../store/ReportContext'

const UPGRADE_URL = 'https://buy.stripe.com/test_00waEW43g3ILbFccvk9ws00'

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
  const [message, setMessage] = useState('')
  if (!report) return null

  const firstName = report.founder.founderName.split(' ')[0]

  const [visibleGroup, ...restGroups] = FEEDBACK_GROUPS

  return (
    <div>
      <h2 className="font-display text-2xl text-ink">Patricia's feedback</h2>
      <p className="mt-3 font-sans text-base leading-relaxed text-ink-soft">
        Notes from your assigned compliance expert as she reviews the generated report.
      </p>

      <div className="mt-6 w-full rounded-xl border border-ink/10 bg-white">
        <div className="space-y-6 p-6 sm:p-8">
          <div className="flex items-start gap-3 border-b border-ink/10 pb-5">
            <img
              src={report.expert.avatar}
              alt={report.expert.name}
              className="h-11 w-11 shrink-0 rounded-full object-cover"
            />
            <div>
              <p className="font-sans text-sm font-bold text-ink">{report.expert.name}</p>
              <p className="font-sans text-xs text-ink-soft">{report.expert.role}</p>
              <p className="mt-0.5 font-sans text-xs text-ink-soft/70">
                to {firstName} · reviewed via compl.ai
              </p>
            </div>
          </div>

          <p className="font-sans text-sm leading-relaxed text-ink">Hi {firstName},</p>
          <p className="font-sans text-sm leading-relaxed text-ink">
            I spent some time going through what compl.ai pulled together for{' '}
            <span className="font-bold">{report.projectName}</span> — here's where things stand.
          </p>

          <div key={visibleGroup.heading}>
            <h3 className="font-sans text-sm font-extrabold uppercase tracking-wide text-ink">
              {visibleGroup.heading}
            </h3>
            <ul className="mt-2 space-y-2">
              {visibleGroup.items.map((item, i) => (
                <li key={i} className="flex gap-2.5 font-sans text-sm leading-relaxed text-ink">
                  <span className="mt-1.5 h-1.5 w-1.5 shrink-0 rounded-full bg-deep" />
                  <span>{item}</span>
                </li>
              ))}
            </ul>
          </div>

          {restGroups.map((group) => (
            <div key={group.heading}>
              <h3 className="font-sans text-sm font-extrabold uppercase tracking-wide text-ink">
                {group.heading}
              </h3>
              <ul className="mt-2 space-y-2">
                {group.items.map((item, i) => (
                  <li key={i} className="flex gap-2.5 font-sans text-sm leading-relaxed text-ink">
                    <span className="mt-1.5 h-1.5 w-1.5 shrink-0 rounded-full bg-deep" />
                    <span>{item}</span>
                  </li>
                ))}
              </ul>
            </div>
          ))}

          <p className="font-sans text-sm leading-relaxed text-ink">— {report.expert.name.split(' ')[0]}</p>

          {/* The send button itself is the upsell — replying to Patricia is a paid feature. */}
          <div className="rounded-lg border border-ink/10 bg-chip/30 p-4">
            <p className="font-sans text-xs font-extrabold uppercase tracking-wide text-ink-soft">
              Ask Patricia
            </p>
            <textarea
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              placeholder="Ask a follow-up question…"
              className="fc-field mt-2 min-h-[70px] w-full resize-none"
            />
            <div className="mt-2 flex justify-end">
              <Button
                type="button"
                onClick={() => window.open(UPGRADE_URL, '_blank', 'noopener,noreferrer')}
                disabled={!message.trim()}
                className="px-4 py-2 text-xs"
              >
                Upgrade to send →
              </Button>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}


