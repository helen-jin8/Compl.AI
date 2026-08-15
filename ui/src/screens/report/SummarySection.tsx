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
      <p className="mt-3 font-sans text-xs text-ink-soft">
        A structured description of the hardware, as understood for certification scoping.
      </p>

      <article className="mt-6 max-w-3xl rounded-xl border border-ink/10 bg-white p-6 sm:p-8">
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

      <div className="mt-4 flex max-w-3xl items-end gap-2.5">
        <textarea
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
              e.preventDefault()
              handleSend()
            }
          }}
          placeholder="Ask the agent to tweak or correct anything in this summary…"
          className="min-h-[46px] flex-1 resize-none rounded-lg border border-ink/20 bg-chip/20 px-3.5 py-2.5 font-sans text-sm text-ink outline-none transition-shadow placeholder:text-ink-soft/60 focus:border-deep focus:ring-2 focus:ring-deep/30"
        />
        <Button
          type="button"
          onClick={handleSend}
          disabled={!message.trim() || sending}
          className="shrink-0 px-5 py-2.5 text-sm"
        >
          {sending ? 'Sending…' : 'Send'}
        </Button>
      </div>
    </div>
  )
}
