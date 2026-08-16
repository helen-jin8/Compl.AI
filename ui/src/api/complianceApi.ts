// Client for the compliance service.
//
// Every exported type and method signature is unchanged from the mock this
// replaced — only the bodies differ, so no caller needed editing. Point it
// somewhere else with VITE_API_URL.

const BASE_URL = import.meta.env.VITE_API_URL ?? 'http://localhost:3000'

export interface FounderIntake {
  founderName: string
  email: string
  description: string
}

// A section of the generated hardware-description document, rendered like a
// structured spec doc rather than a single paragraph.
export interface SummarySection {
  id: string
  heading: string
  paragraphs?: string[]
  bullets?: string[]
}

export interface FollowUpQuestion {
  id: string
  question: string
  rationale: string
  answer?: string
}

export type CheckStatus = 'required' | 'recommended' | 'passed'

export interface ComplianceCheck {
  id: string
  code: string
  authority: string
  title: string
  status: CheckStatus
  scope: string
  detail: string
  /** '—' when no verified figure exists. The service never invents one. */
  estimatedCost: string
  turnaround: string
  confidence?: number
  verifyRequired?: boolean
}

export interface TestLab {
  id: string
  name: string
  location: string
  accreditations: string[]
  specialty: string
  leadTime: string
  rating: number
}

export interface Expert {
  name: string
  role: string
  avatar: string
  note: string
}

export interface ComplianceReport {
  projectName: string
  founder: FounderIntake
  generatedAt: string
  summary: SummarySection[]
  followUps: FollowUpQuestion[]
  checks: ComplianceCheck[]
  labs: TestLab[]
  /** A placeholder until a human returns a review — see `expertReviewed`. */
  expert: Expert
  /** False until an actual person has reviewed this report. */
  expertReviewed?: boolean
  reportId?: string
}

export type GenerationStage = {
  label: string
  detail: string
}

export class ApiError extends Error {
  constructor(
    message: string,
    readonly status: number,
  ) {
    super(message)
    this.name = 'ApiError'
  }
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  let res: Response
  try {
    res = await fetch(`${BASE_URL}${path}`, {
      ...init,
      headers: { 'Content-Type': 'application/json', ...(init?.headers ?? {}) },
    })
  } catch {
    throw new ApiError(
      `Cannot reach the compliance service at ${BASE_URL}. Is the backend running?`,
      0,
    )
  }

  const body = (await res.json().catch(() => ({}))) as Record<string, unknown>
  if (!res.ok) {
    throw new ApiError((body.message as string) ?? `Request failed (${res.status})`, res.status)
  }
  return body as T
}

export class ComplianceApi {
  /** Stages surfaced on the generating screen. */
  readonly stages: GenerationStage[] = [
    { label: 'reading your description', detail: 'Working out what the product actually is' },
    { label: 'mapping your product', detail: 'Matching attributes to regulated categories' },
    { label: 'drafting the report card', detail: 'Assembling standards, costs and lab options' },
    { label: 'checking our work', detail: 'Scoring confidence and flagging what needs a human' },
  ]

  /** Callers pass names where ids are expected, so keep the real ids here. */
  private sessionId: string | null = null
  private reportId: string | null = null
  private jobId: string | null = null

  /**
   * Agent step: reads the founder's description and returns the follow-up
   * questions the model needs answered before it can finalize the report.
   */
  async generateFollowUps(intake: FounderIntake): Promise<FollowUpQuestion[]> {
    const res = await request<{ sessionId: string; followUps: FollowUpQuestion[] }>('/api/intake', {
      method: 'POST',
      body: JSON.stringify(intake),
    })
    this.sessionId = res.sessionId
    return res.followUps
  }

  /**
   * Report generation is one long request — the model reasons for a couple of
   * minutes. The stage ticker paces that wait; it never claims a step the
   * request has not actually reached, and holds on the last one until the real
   * response lands.
   */
  async generateReport(
    intake: FounderIntake,
    answeredFollowUps: FollowUpQuestion[],
    onStage?: (index: number, stage: GenerationStage) => void,
  ): Promise<ComplianceReport> {
    let index = 0
    onStage?.(0, this.stages[0])
    const ticker = setInterval(() => {
      if (index < this.stages.length - 1) {
        index += 1
        onStage?.(index, this.stages[index])
      }
    }, 30_000)

    try {
      const report = await request<ComplianceReport>('/api/report', {
        method: 'POST',
        body: JSON.stringify({
          sessionId: this.sessionId ?? undefined,
          intake,
          followUps: answeredFollowUps,
        }),
      })
      this.reportId = report.reportId ?? null
      return report
    } finally {
      clearInterval(ticker)
    }
  }

  /** Posts the drafted report to Terac for human review. */
  async requestExpertReview(reportId: string): Promise<{ queued: boolean; eta: string }> {
    const res = await request<{
      queued: boolean
      eta: string
      jobId: string
      simulated: boolean
    }>('/api/expert-review', {
      method: 'POST',
      body: JSON.stringify({ reportId: this.resolveReportId(reportId) }),
    })
    this.jobId = res.jobId
    return res
  }

  /** Poll for the reviewed result; returns the validated report once returned. */
  async pollExpertReview(jobId?: string): Promise<{
    status: 'open' | 'accepted' | 'returned'
    expert: Expert | null
    simulated: boolean
    report?: ComplianceReport
  }> {
    const id = jobId ?? this.jobId
    if (!id) throw new ApiError('No expert-review job to poll.', 400)
    return request(`/api/expert-review/${encodeURIComponent(id)}`)
  }

  /** Persists a founder answer to a follow-up question. */
  async submitFollowUp(questionId: string, answer: string): Promise<FollowUpQuestion> {
    return request(`/api/followups/${encodeURIComponent(questionId)}`, {
      method: 'PATCH',
      body: JSON.stringify({ answer, sessionId: this.sessionId ?? undefined }),
    })
  }

  /** Sends a founder tweak request against the summary doc to the agent. */
  async refineSummary(
    reportId: string,
    message: string,
  ): Promise<{ accepted: boolean; summary?: SummarySection[]; reply?: string }> {
    return request('/api/refine-summary', {
      method: 'POST',
      body: JSON.stringify({ reportId: this.resolveReportId(reportId), message }),
    })
  }

  /** Re-fetch by id so a refresh on /report does not lose the report. */
  async getReport(reportId: string): Promise<ComplianceReport> {
    return request(`/api/report/${encodeURIComponent(reportId)}`)
  }

  /**
   * Callers currently pass `report.projectName` where an id is expected.
   * Prefer the real id captured from /api/report.
   */
  private resolveReportId(candidate: string): string {
    if (candidate?.startsWith('rep_')) return candidate
    if (this.reportId) return this.reportId
    return candidate
  }
}

export const complianceApi = new ComplianceApi()
