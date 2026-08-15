import { useEffect } from 'react'
import { NavLink, Outlet, useNavigate } from 'react-router'
import Shell from '../../components/Shell'
import { useReport } from '../../store/ReportContext'

export default function ReportLayout() {
  const navigate = useNavigate()
  const { report, expertEta } = useReport()

  // Deep-linked without a generated report → send to the form.
  useEffect(() => {
    if (!report) navigate('/start', { replace: true })
  }, [report, navigate])

  if (!report) return null

  const requiredCount = report.checks.filter((c) => c.status === 'required').length

  const navItems: { to: string; label: string; badge?: number }[] = [
    { to: '/report/summary', label: 'Project summary' },
    { to: '/report/standards', label: 'Standards', badge: requiredCount },
    { to: '/report/labs', label: 'Labs' },
  ]

  return (
    <Shell maxWidth="max-w-[1400px]">
      <div className="fc-fade-up grid gap-5 lg:grid-cols-[260px_minmax(0,1fr)]">
        {/* Sidebar */}
        <aside className="h-fit rounded-2xl border border-ink/10 bg-white p-5 shadow-xl shadow-deep/15">
          <p className="font-display text-xl text-ink">{report.projectName}</p>
          <p className="mt-0.5 font-sans text-xs text-ink-soft">Generated {report.generatedAt}</p>
          <nav className="mt-5 space-y-1">
            {navItems.map((item) => (
              <NavLink
                key={item.to}
                to={item.to}
                className={({ isActive }) =>
                  `flex w-full items-center justify-between rounded-lg px-3.5 py-2.5 text-left font-sans text-sm transition-colors ${
                    isActive ? 'bg-deep font-bold text-white' : 'text-ink hover:bg-chip/60'
                  }`
                }
              >
                {({ isActive }) => (
                  <>
                    <span>{item.label}</span>
                    {item.badge ? (
                      <span
                          className={`ml-2 flex h-5 min-w-5 items-center justify-center rounded-full px-1.5 font-sans text-xs font-bold ${
                          isActive ? 'bg-white/25 text-white' : 'bg-chip text-deep'
                        }`}
                      >
                        {item.badge}
                      </span>
                    ) : null}
                  </>
                )}
              </NavLink>
            ))}
          </nav>

          <div className="mt-6 rounded-xl border border-ink/10 bg-chip/40 p-4">
            <div className="flex items-center gap-2.5">
              <img
                src={report.expert.avatar}
                alt={report.expert.name}
                className="h-9 w-9 rounded-full border border-ink/20 bg-ink/10 object-cover"
              />
              <div>
                <p className="font-sans text-sm font-bold text-ink">{report.expert.name}</p>
                <p className="font-sans text-xs text-ink-soft">{report.expert.role}</p>
              </div>
            </div>
            <p className="mt-2.5 font-sans text-xs leading-relaxed text-ink">
              {report.expert.note}
            </p>
            <div className="mt-2.5 flex items-center gap-2 rounded-lg bg-white px-2.5 py-1.5">
              <span className="h-1.5 w-1.5 animate-pulse rounded-full bg-emerald-500" />
              <p className="font-sans text-xs text-ink-soft">
                {expertEta
                  ? `Expert review in progress · back in ${expertEta}`
                  : 'Queuing expert review…'}
              </p>
            </div>
          </div>
        </aside>

        {/* Main panel */}
        <section className="rounded-2xl border border-ink/10 bg-white p-6 shadow-xl shadow-deep/15 sm:p-8">
          <Outlet />
        </section>
      </div>
    </Shell>
  )
}
