import { createContext, useCallback, useContext, useState, type ReactNode } from 'react'
import {
  complianceApi,
  type ComplianceReport,
  type FollowUpQuestion,
  type FounderIntake,
} from '../api/complianceApi'

interface ReportState {
  intake: FounderIntake | null
  followUps: FollowUpQuestion[]
  analyzing: boolean
  report: ComplianceReport | null
  stageIndex: number
  expertEta: string | null
  /** Non-null when a backend call failed; the UI must surface it. */
  error: string | null
  /** Step 1: agent reads the description and produces follow-up questions. */
  analyze: (intake: FounderIntake) => Promise<void>
  /** Step 2: founder's answers are folded in and the full report is built. */
  finalize: (answered: FollowUpQuestion[]) => Promise<void>
  reset: () => void
}

const ReportContext = createContext<ReportState | null>(null)

export function ReportProvider({ children }: { children: ReactNode }) {
  const [intake, setIntake] = useState<FounderIntake | null>(null)
  const [followUps, setFollowUps] = useState<FollowUpQuestion[]>([])
  const [analyzing, setAnalyzing] = useState(false)
  const [report, setReport] = useState<ComplianceReport | null>(null)
  const [stageIndex, setStageIndex] = useState(0)
  const [expertEta, setExpertEta] = useState<string | null>(null)
  const [error, setError] = useState<string | null>(null)

  const analyze = useCallback(async (nextIntake: FounderIntake) => {
    setIntake(nextIntake)
    setFollowUps([])
    setReport(null)
    setStageIndex(0)
    setExpertEta(null)
    setError(null)
    setAnalyzing(true)
    try {
      const questions = await complianceApi.generateFollowUps(nextIntake)
      setFollowUps(questions)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Could not reach the compliance service.')
    } finally {
      setAnalyzing(false)
    }
  }, [])

  const finalize = useCallback(
    async (answered: FollowUpQuestion[]) => {
      if (!intake) return
      setFollowUps(answered)
      setReport(null)
      setStageIndex(0)
      setExpertEta(null)
      setError(null)

      let generated: ComplianceReport
      try {
        generated = await complianceApi.generateReport(intake, answered, (index) =>
          setStageIndex(index),
        )
      } catch (err) {
        // Without this the promise rejects unhandled and the loader spins
        // forever with nothing on screen explaining why.
        setError(err instanceof Error ? err.message : 'Report generation failed.')
        return
      }
      setReport(generated)

      // Kick off the human-in-the-loop expert review in the background.
      complianceApi
        .requestExpertReview(generated.projectName)
        .then((res) => setExpertEta(res.eta))
        .catch(() => setExpertEta(null))
    },
    [intake],
  )

  const reset = useCallback(() => {
    setIntake(null)
    setFollowUps([])
    setAnalyzing(false)
    setReport(null)
    setStageIndex(0)
    setExpertEta(null)
    setError(null)
  }, [])

  return (
    <ReportContext.Provider
      value={{
        intake,
        followUps,
        analyzing,
        report,
        stageIndex,
        expertEta,
        error,
        analyze,
        finalize,
        reset,
      }}
    >
      {children}
    </ReportContext.Provider>
  )
}

export function useReport() {
  const ctx = useContext(ReportContext)
  if (!ctx) throw new Error('useReport must be used within ReportProvider')
  return ctx
}
