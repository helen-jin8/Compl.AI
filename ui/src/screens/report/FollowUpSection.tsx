import { useState } from 'react'
import { useReport } from '../../store/ReportContext'

export default function FollowUpSection() {
  const { report } = useReport()
  const [drafts, setDrafts] = useState<Record<string, string>>({})
  if (!report) return null

  return (
    <div>
      <h2 className="font-display text-2xl text-ink">Follow-up questions</h2>
      <p className="mt-3 max-w-3xl font-sans text-base leading-relaxed text-ink-soft">
        These are the questions our agent asked from your description. Your answers are folded into
        the report — update any of them and Patricia will re-confirm the plan.
      </p>

      <div className="mt-6 space-y-4">
        {report.followUps.map((q, i) => {
          const savedAnswer = q.answer
          const draft = drafts[q.id]
          const value = draft ?? savedAnswer ?? ''
          return (
            <div key={q.id} className="rounded-xl border border-ink/10 bg-white p-5">
              <div className="flex items-start gap-3">
                <span className="flex h-7 w-7 shrink-0 items-center justify-center rounded-full bg-deep font-body text-xs font-bold text-white">
                  {i + 1}
                </span>
                <div className="flex-1">
                  <div className="flex items-start justify-between gap-3">
                    <p className="font-body text-lg font-bold text-ink">{q.question}</p>
                    {savedAnswer ? (
                      <span className="shrink-0 rounded-full bg-emerald-100 px-2.5 py-0.5 font-body text-xs font-bold text-emerald-700">
                        answered
                      </span>
                    ) : (
                      <span className="shrink-0 rounded-full bg-amber-100 px-2.5 py-0.5 font-body text-xs font-bold text-amber-700">
                        open
                      </span>
                    )}
                  </div>
                  <p className="mt-0.5 font-body text-xs text-ink-soft">{q.rationale}</p>
                  <textarea
                    value={value}
                    onChange={(e) => setDrafts((prev) => ({ ...prev, [q.id]: e.target.value }))}
                    placeholder="Type your answer…"
                    className="mt-3 min-h-20 w-full resize-none rounded-lg border border-ink/20 bg-chip/20 px-3.5 py-2.5 font-body text-sm text-ink outline-none transition-shadow placeholder:text-ink-soft/60 focus:border-deep focus:ring-2 focus:ring-deep/30"
                  />
                  {value.trim() && (
                    <p className="mt-1.5 font-body text-xs font-bold text-emerald-600">
                      ✓ Saved — sent to expert
                    </p>
                  )}
                </div>
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )
}
