import { useEffect } from 'react'
import { useNavigate } from 'react-router'
import type { Expert } from '../api/complianceApi'
import { useExpertStore, type ExpertStage } from '../store/expertStore'

// Stock portrait standing in for the Patricia persona while the expert loop is
// mocked. The backend returns a neutral placeholder because no real reviewer is
// assigned yet; this is presentation only.
export const DEMO_EXPERT = {
  name: 'Patricia Nguyen',
  role: 'Senior Compliance Engineer',
  avatar:
    'https://images.unsplash.com/photo-1573497019940-1c28c88b4f3e?w=160&h=160&fit=crop&auto=format',
  note: '',
}

// Sidebar card showing the human-in-the-loop expert state as it progresses.
export default function FindingExpert({ expert }: { expert: Expert }) {
  const navigate = useNavigate()
  // The backend returns a placeholder until a human actually picks the job up,
  // so a first-name split on it yields "Awaiting is reviewing".
  const hasRealExpert = Boolean(expert?.name) && expert.name !== 'Awaiting reviewer'
  const shown = hasRealExpert ? expert : DEMO_EXPERT
  const stage = useExpertStore((s) => s.stage)
  const start = useExpertStore((s) => s.start)

  useEffect(() => {
    start()
  }, [start])

  const label =
    stage === 'matching'
      ? 'finding an expert…'
      : stage === 'found'
        ? `${shown.name.split(' ')[0]} is reviewing`
        : "Ask Patricia"

  // Feedback is ready once the expert has finished reviewing — the card becomes clickable.
  const ready = stage === 'reviewing'

  return (
    <div
      role={ready ? 'button' : undefined}
      tabIndex={ready ? 0 : undefined}
      onClick={ready ? () => navigate('/report/feedback') : undefined}
      onKeyDown={
        ready
          ? (e) => {
              if (e.key === 'Enter' || e.key === ' ') navigate('/report/feedback')
            }
          : undefined
      }
      className={`mt-6 flex items-center gap-3 rounded-xl border border-ink/10 bg-chip/40 p-4 ${
        ready ? 'cursor-pointer transition-colors hover:bg-chip/70' : ''
      }`}
    >
      <AvatarGroup expert={shown} stage={stage} />
      <p className="font-sans text-sm text-ink">{label}</p>
    </div>
  )
}

function AvatarGroup({ expert, stage }: { expert: Expert; stage: ExpertStage }) {
  // Placeholder persona icon while no expert has been matched yet.
  if (stage === 'matching') {
    return (
      <span className="flex h-9 w-9 items-center justify-center rounded-full border-2 border-white bg-ink/10 text-ink-soft">
        <svg viewBox="0 0 24 24" fill="currentColor" className="h-5 w-5">
          <path d="M12 12a5 5 0 1 0 0-10 5 5 0 0 0 0 10Zm0 2c-4.42 0-8 2.24-8 5v3h16v-3c0-2.76-3.58-5-8-5Z" />
        </svg>
      </span>
    )
  }

  return (
    <span className="relative">
      <img
        src={expert.avatar}
        alt={expert.name}
        className="h-9 w-9 rounded-full border-2 border-white object-cover"
      />
      <span
        className={`absolute -right-0.5 -top-0.5 h-2.5 w-2.5 rounded-full border-2 border-white ${
          stage === 'reviewing' ? 'bg-red-500' : 'bg-emerald-500'
        }`}
      />
    </span>
  )
}
