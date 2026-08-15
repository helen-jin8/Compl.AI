import { useNavigate } from 'react-router'
import Shell from '../components/Shell'
import Button from '../components/Button'

const cardChecks = [
  { code: 'FCC Part 15C', label: 'Intentional radiator' },
  { code: 'UL 2054', label: 'Battery pack safety' },
  { code: 'UN 38.3', label: 'Transport testing' },
  { code: 'EN 62368-1', label: 'Product safety' },
]

export default function LandingScreen() {
  const navigate = useNavigate()

  return (
    <Shell maxWidth="max-w-[1400px]">
      <div className="grid items-center gap-10 pt-4 lg:grid-cols-[minmax(0,1fr)_minmax(0,1.1fr)] lg:pt-12">
        <div className="fc-fade-up max-w-lg">
          <h1 className="font-body text-3xl font-bold leading-tight text-white sm:text-4xl">
            Building hardware, not sure how to ship it?
          </h1>
          <p className="mt-6 max-w-md font-body text-base leading-relaxed text-white/90">
            Expert-vetted AI agents that read thousands of pages of safety standards and generate
            everything you need to get your product certified.
          </p>
          <Button className="mt-8" onClick={() => navigate('/start')}>
            Try it now
          </Button>
          <div className="mt-8 flex items-center gap-4 font-body text-xs text-white/80">
            <span>3,412 pages parsed</span>
            <span className="h-1 w-1 rounded-full bg-white/50" />
            <span>UL · FCC · CE · UN</span>
            <span className="h-1 w-1 rounded-full bg-white/50" />
            <span>Human sign-off</span>
          </div>
        </div>

        <div className="fc-fade-up rounded-2xl border border-white/40 bg-white/85 p-5 shadow-2xl shadow-deep/30 backdrop-blur-sm sm:p-6">
          <div className="flex items-center justify-between">
            <p className="font-display text-xl text-ink">Report card</p>
            <span className="rounded-full bg-chip px-2.5 py-0.5 font-sans text-xs font-bold text-deep">
              preview
            </span>
          </div>
          <p className="mt-1 font-sans text-xs text-ink-soft">
            Everfield Air Monitor · US + EU launch
          </p>
          <div className="mt-4 space-y-2.5">
            {cardChecks.map((c) => (
              <div
                key={c.code}
                className="flex items-center justify-between rounded-lg border border-ink/10 bg-white px-3.5 py-2.5"
              >
                <div>
                  <p className="font-sans text-sm font-bold text-deep">{c.code}</p>
                  <p className="font-sans text-xs text-ink-soft">{c.label}</p>
                </div>
                <span className="font-sans text-xs font-bold text-ink-soft">required</span>
              </div>
            ))}
          </div>
          <div className="mt-4 flex items-center gap-2.5 rounded-lg bg-chip/60 px-3.5 py-2.5">
            <span className="flex h-7 w-7 items-center justify-center rounded-full bg-deep font-sans text-xs font-bold text-white">
              PN
            </span>
            <p className="font-sans text-xs text-ink">
              Reviewed by <span className="font-bold">Patricia N.</span> · Senior Compliance Engineer
            </p>
          </div>
        </div>
      </div>
    </Shell>
  )
}
