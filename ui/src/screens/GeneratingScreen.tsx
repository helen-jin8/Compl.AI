import { useEffect } from 'react'
import { useNavigate } from 'react-router'
import Shell from '../components/Shell'
import { complianceApi } from '../api/complianceApi'
import { useReport } from '../store/ReportContext'

export default function GeneratingScreen() {
  const navigate = useNavigate()
  const { report, stageIndex, intake, error } = useReport()
  const stages = complianceApi.stages

  // If someone deep-links here without submitting the form, send them back.
  useEffect(() => {
    if (!intake) navigate('/start', { replace: true })
  }, [intake, navigate])

  // Advance to the report once generation finishes.
  useEffect(() => {
    if (report) navigate('/report/summary', { replace: true })
  }, [report, navigate])

  // A failed call must say so rather than spin forever.
  if (error) {
    return (
      <Shell maxWidth="max-w-2xl">
        <div className="fc-fade-up mt-8 rounded-2xl border border-rose-200 bg-white p-6 shadow-2xl shadow-deep/25 sm:p-9">
          <h1 className="font-body text-2xl font-bold text-rose-700">Report generation failed</h1>
          <p className="mt-3 font-sans text-sm leading-relaxed text-ink-soft">{error}</p>
          <button
            onClick={() => navigate('/start')}
            className="mt-5 rounded-lg bg-deep px-5 py-2.5 font-body text-sm font-bold text-white"
          >
            Start over
          </button>
        </div>
      </Shell>
    )
  }

  return (
    <Shell maxWidth="max-w-2xl">
      <div className="fc-fade-up mt-8 rounded-2xl border border-ink/10 bg-white p-6 shadow-2xl shadow-deep/25 sm:p-9">
        <div className="flex items-center gap-3">
          <span className="fc-spinner" aria-hidden="true" />
          <h1 className="font-body text-2xl text-ink sm:text-3xl">generating report …</h1>
        </div>
        <p className="mt-2 font-body text-sm text-ink-soft">
          Reading standards and building your compliance report card. Hang tight — this usually
          takes under a minute.
        </p>

        <div className="mt-8 space-y-2.5">
          {stages.map((stage, i) => {
            const done = i < stageIndex
            const active = i === stageIndex
            return (
              <div
                key={stage.label}
                className={`flex items-start gap-3 rounded-xl border px-4 py-3 transition-all ${
                  active
                    ? 'border-deep/40 bg-chip/50'
                    : done
                      ? 'border-ink/10 bg-white'
                      : 'border-ink/5 bg-white opacity-50'
                }`}
              >
                <span
                  className={`mt-0.5 flex h-5 w-5 shrink-0 items-center justify-center rounded-full text-xs font-bold ${
                    done
                      ? 'bg-deep text-white'
                      : active
                        ? 'bg-chip text-deep'
                        : 'bg-ink/10 text-ink-soft'
                  }`}
                >
                  {done ? '✓' : i + 1}
                </span>
                <div>
                  <p
                    className={`font-body text-sm font-bold ${
                      active || done ? 'text-ink' : 'text-ink-soft'
                    }`}
                  >
                    {stage.label}
                    {active && <span className="ml-1 animate-pulse">…</span>}
                  </p>
                  <p className="font-body text-xs text-ink-soft">{stage.detail}</p>
                </div>
              </div>
            )
          })}
        </div>
      </div>
    </Shell>
  )
}
