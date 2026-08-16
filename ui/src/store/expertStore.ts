import { create } from 'zustand'

export type ExpertStage = 'matching' | 'found' | 'reviewing'

// Full loop is ~3 minutes, then it settles into reviewing (mocked human-in-the-loop demo).
const STAGE_DURATION_MS: Record<ExpertStage, number> = {
  matching: 5_000,
  found: 2_000,
  reviewing: 3_000,
}
const NEXT_STAGE: Record<ExpertStage, ExpertStage> = {
  matching: 'found',
  found: 'reviewing',
  reviewing: 'reviewing',
}

interface ExpertState {
  stage: ExpertStage
  /** Stays true once the expert has been matched at least once, even if the demo loop cycles back. */
  matched: boolean
  started: boolean
  /** Kicks off the stage cycle once a report exists; safe to call from multiple components. */
  start: () => void
  reset: () => void
}

export const useExpertStore = create<ExpertState>((set, get) => ({
  stage: 'matching',
  matched: false,
  started: false,
  start: () => {
    if (get().started) return
    set({ started: true })
    const advance = () => {
      const next = NEXT_STAGE[get().stage]
      set({ stage: next, matched: get().matched || next !== 'matching' })
      // Once reviewing is reached, stay there instead of looping back to matching.
      if (next !== 'reviewing') {
        setTimeout(advance, STAGE_DURATION_MS[next])
      }
    }
    setTimeout(advance, STAGE_DURATION_MS[get().stage])
  },
  reset: () => set({ stage: 'matching', matched: false, started: false }),
}))
