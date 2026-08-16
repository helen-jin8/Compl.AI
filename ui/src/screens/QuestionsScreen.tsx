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
            <div className="flex items-center gap-3">
              <span className="fc-spinner" aria-hidden="true" />
              <p className="font-body text-xl text-ink">Reading your description …</p>
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
                          className="fc-field mt-3 min-h-20 resize-none"
                        />
                      </div>
                    </div>
                  </div>
                )
              })}
            </div>

            <div className="mt-6 flex items-center justify-end gap-3">
              <Button onClick={submit}>Generate report</Button>
            </div>
          </>
        )}
      </div>
    </Shell>
  )
}
