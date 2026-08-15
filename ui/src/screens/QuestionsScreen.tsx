import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router'
import Shell from '../components/Shell'
import Button from '../components/Button'
import { useReport } from '../store/ReportContext'

export default function QuestionsScreen() {
  const navigate = useNavigate()
  const { intake, followUps, analyzing, finalize } = useReport()
  const [answers, setAnswers] = useState<Record<string, string>>({})

  // Deep-linked without submitting the form → back to the form.
  useEffect(() => {
    if (!intake) navigate('/start', { replace: true })
  }, [intake, navigate])

  const submit = () => {
    const answered = followUps.map((q) => ({ ...q, answer: answers[q.id]?.trim() || undefined }))
    navigate('/generating')
    void finalize(answered)
  }

  const answeredCount = followUps.filter((q) => answers[q.id]?.trim()).length

  return (
    <Shell maxWidth="max-w-4xl">
      <div className="fc-fade-up pt-4">
        <h1 className="font-body text-3xl font-bold leading-tight text-white sm:text-4xl">
          Follow-up questions
        </h1>
        <p className="mt-3 max-w-xl font-body text-base text-white/85">
          Our agent read your description and needs a little more detail to scope the right
          standards. Answer what you can — you can always refine these with an expert later.
        </p>

        {analyzing ? (
          <div className="mt-8 rounded-2xl border border-ink/10 bg-white p-6 shadow-2xl shadow-deep/25 sm:p-9">
            <div className="flex items-center gap-2.5">
              <p className="font-body text-xl text-ink">reading your description …</p>
               <span className="flex gap-1">
                {[0, 1, 2].map((i) => (
                  <span
                    key={i}
                    className="h-1.5 w-1.5 animate-bounce rounded-full bg-deep"
                    style={{ animationDelay: `${i * 0.15}s` }}
                  />
                ))}
              </span>
            </div>
            <p className="mt-2 font-body text-sm text-ink-soft">
              The agent is figuring out which details it still needs from you.
            </p>
          </div>
        ) : (
          <>
            <div className="mt-8 space-y-4">
              {followUps.map((q) => {
                const answered = answers[q.id]?.trim()
                return (
                  <div
                    key={q.id}
                    className="rounded-xl border border-ink/10 bg-white p-5 shadow-lg shadow-deep/10"
                  >
                    <div className="flex items-start gap-3">
                      <div className="flex-1">
                        <p className="font-body text-lg font-bold text-ink">{q.question}</p>
                        <p className="mt-0.5 font-body text-xs text-ink-soft">{q.rationale}</p>
                        <textarea
                          value={answers[q.id] ?? ''}
                          onChange={(e) =>
                            setAnswers((prev) => ({ ...prev, [q.id]: e.target.value }))
                          }
                          placeholder="Type your answer…"
                          className="mt-3 min-h-20 w-full resize-none rounded-lg border border-ink/20 bg-chip/20 px-3.5 py-2.5 font-body text-sm text-ink outline-none transition-shadow placeholder:text-ink-soft/60 focus:border-deep focus:ring-2 focus:ring-deep/30"
                        />
                        {answered && (
                          <p className="mt-1.5 font-body text-xs font-bold text-emerald-600">
                            ✓ Noted
                          </p>
                        )}
                      </div>
                    </div>
                  </div>
                )
              })}
            </div>

            <div className="mt-6 flex items-center justify-end gap-3">
              <span className="font-body text-xs text-white/70">
                {answeredCount} of {followUps.length} answered · you can skip any
              </span>
              <Button onClick={submit}>Generate report</Button>
            </div>
          </>
        )}
      </div>
    </Shell>
  )
}
