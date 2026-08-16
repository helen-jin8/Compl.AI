import { useState } from 'react'
import { complianceApi } from '../../api/complianceApi'
import Button from '../../components/Button'
import { useReport } from '../../store/ReportContext'

export default function SummarySection() {
  const { report } = useReport()
  const [message, setMessage] = useState('')
  const [sending, setSending] = useState(false)
  const [sentNotes, setSentNotes] = useState<string[]>([])
  if (!report) return null

  const handleSend = async () => {
    const trimmed = message.trim()
    if (!trimmed || sending) return
    setSending(true)
    try {
      await complianceApi.refineSummary(report.projectName, trimmed)
      setSentNotes((prev) => [...prev, trimmed])
      setMessage('')
    } finally {
      setSending(false)
    }
  }

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

      {sentNotes.length > 0 && (
        <div className="mt-4 max-w-3xl space-y-2">
          {sentNotes.map((note, i) => (
            <div key={i} className="rounded-lg bg-chip/40 px-3.5 py-2.5">
              <p className="font-sans text-xs font-bold text-ink">You asked to tweak</p>
              <p className="font-sans text-sm text-ink-soft">{note}</p>
            </div>
          ))}
        </div>
      )}

      <div className="mt-4 max-w-3xl">
        <textarea
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Ask the agent to tweak or correct anything in this summary…"
          className="fc-field min-h-[90px] w-full resize-none"
        />
        <div className="mt-2.5 flex justify-end">
          <Button
            type="button"
            onClick={handleSend}
            disabled={!message.trim() || sending}
            className="px-5 py-2.5 text-sm"
          >
            {sending ? 'Sending…' : 'Send'}
          </Button>
        </div>
      </div>
    </div>
  )
}
