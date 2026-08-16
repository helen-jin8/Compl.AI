import { useEffect } from 'react'
import { NavLink, Outlet, useNavigate } from 'react-router'
import FindingExpert from '../../components/FindingExpert'
import Shell from '../../components/Shell'
import { useReport } from '../../store/ReportContext'
import { useExpertStore } from '../../store/expertStore'

export default function ReportLayout() {
  const navigate = useNavigate()
  const { report, expertEta } = useReport()
  const matched = useExpertStore((s) => s.matched)

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

  // Only shows up once the expert has actually matched with this project.
  if (matched) {
    navItems.push({ to: '/report/feedback', label: "Patricia's feedback" })
  }

  return (
    <Shell
      maxWidth="max-w-[1400px]"
      headerRight={<FindingExpert expert={report.expert} eta={expertEta} />}
    >
      <div className="fc-fade-up grid gap-5 lg:grid-cols-[260px_minmax(0,1fr)]">
        {/* Sidebar */}
        <aside className="h-fit rounded-2xl border border-ink/10 bg-white p-5 shadow-xl shadow-deep/15">
          <p className="font-display text-xl leading-snug break-words text-ink">{report.projectName}</p>
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
        </aside>

        {/* Main panel */}
        <section className="rounded-2xl border border-ink/10 bg-white p-6 shadow-xl shadow-deep/15 sm:p-8">
          <Outlet />
        </section>
      </div>
    </Shell>
  )
}
