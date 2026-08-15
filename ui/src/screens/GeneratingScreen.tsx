import Shell from '../components/Shell'
import type { GenerationStage } from '../api/complianceApi'

export default function GeneratingScreen({
  stages,
  activeIndex,
}: {
  stages: GenerationStage[]
  activeIndex: number
}) {
  return (
    <Shell maxWidth="max-w-3xl">
      <div className="fc-fade-up mt-10 rounded-2xl border border-ink/10 bg-white p-8 shadow-2xl shadow-deep/25 sm:p-12">
        <div className="flex items-center gap-3">
          <span className="flex gap-1">
            {[0, 1, 2].map((i) => (
              <span
                key={i}
                className="h-2 w-2 animate-bounce rounded-full bg-deep"
                style={{ animationDelay: `${i * 0.15}s` }}
              />
            ))}
          </span>
          <h1 className="font-body text-3xl text-ink sm:text-4xl">generating report …</h1>
        </div>
        <p className="mt-3 font-body text-ink-soft">
          Reading standards and building your compliance report card. Hang tight — this usually takes
          under a minute.
        </p>

        <div className="mt-10 space-y-3">
          {stages.map((stage, i) => {
            const done = i < activeIndex
            const active = i === activeIndex
            return (
              <div
                key={stage.label}
                className={`flex items-start gap-4 rounded-xl border px-5 py-4 transition-all ${
                  active
                    ? 'border-deep/40 bg-chip/50'
                    : done
                      ? 'border-ink/10 bg-white'
                      : 'border-ink/5 bg-white opacity-50'
                }`}
              >
                <span
                  className={`mt-0.5 flex h-6 w-6 shrink-0 items-center justify-center rounded-full text-xs font-bold ${
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
                    className={`font-body text-lg font-bold ${
                      active || done ? 'text-ink' : 'text-ink-soft'
                    }`}
                  >
                    {stage.label}
                    {active && <span className="ml-1 animate-pulse">…</span>}
                  </p>
                  <p className="font-body text-sm text-ink-soft">{stage.detail}</p>
                </div>
              </div>
            )
          })}
        </div>
      </div>
    </Shell>
  )
}
