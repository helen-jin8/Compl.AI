import { useEffect } from 'react'
import type { Expert } from '../api/complianceApi'
import { useExpertStore } from '../store/expertStore'

// Stand-in colleagues shown alongside the matched expert in the presence group.
const NETWORK_AVATARS = ['https://i.pravatar.cc/64?img=12', 'https://i.pravatar.cc/64?img=47']

// A Google Docs-style presence pill: real-photo avatar group + status text,
// meant to sit top-right in the Shell header, overlapping the content below.
export default function FindingExpert({ expert, eta }: { expert: Expert; eta: string | null }) {
  const stage = useExpertStore((s) => s.stage)
  const start = useExpertStore((s) => s.start)

  useEffect(() => {
    start()
  }, [start])

  const label =
    stage === 'matching'
      ? 'finding an expert…'
      : stage === 'found'
        ? `${expert.name.split(' ')[0]} is looking at your design`
        : eta
          ? `expert review · back in ${eta}`
          : 'waiting on expert review'

  return (
    <div className="fc-pop-in relative z-10 -mb-12">
      <div className="flex items-center gap-3 rounded-full border border-ink/10 bg-white px-4 py-2.5 shadow-lg shadow-deep/20">
        <AvatarGroup expert={expert} live={stage !== 'matching'} />
        <p className="whitespace-nowrap font-sans text-sm text-ink">{label}</p>
      </div>
    </div>
  )
}

function AvatarGroup({ expert, live }: { expert: Expert; live: boolean }) {
  return (
    <span className="flex -space-x-3">
      {NETWORK_AVATARS.map((src, i) => (
        <img
          key={i}
          src={src}
          alt=""
          aria-hidden="true"
          className="h-9 w-9 rounded-full border-2 border-white object-cover"
        />
      ))}
      <span className="relative">
        <img
          src={expert.avatar}
          alt={expert.name}
          className="h-9 w-9 rounded-full border-2 border-white object-cover"
        />
        {live && (
          <span className="absolute -right-0.5 -top-0.5 h-2.5 w-2.5 rounded-full border-2 border-white bg-emerald-500" />
        )}
      </span>
    </span>
  )
}
