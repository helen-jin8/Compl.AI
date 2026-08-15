// Mock backend for hardware.check.
// A single class stands in for the real compliance-analysis service so the UI
// can be built and demoed end to end without a live backend.

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
  estimatedCost: string
  turnaround: string
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
  expert: Expert
}

export type GenerationStage = {
  label: string
  detail: string
}

const wait = (ms: number) => new Promise<void>((resolve) => setTimeout(resolve, ms))

export class ComplianceApi {
  /** Stages surfaced on the generating screen. */
  readonly stages: GenerationStage[] = [
    { label: 'reading compliance docs', detail: 'Parsing 3,412 pages of UL, FCC & IEC standards' },
    { label: 'mapping your product', detail: 'Matching your description to regulated categories' },
    { label: 'drafting the report card', detail: 'Assembling required tests and lab options' },
    { label: 'letting experts know', detail: 'Queuing a human reviewer for final sign-off' },
  ]

  /**
   * Agent step: reads the founder's description and returns the follow-up
   * questions it needs answered before it can finalize the report. Questions
   * are selected based on signals detected in the description.
   */
  async generateFollowUps(intake: FounderIntake): Promise<FollowUpQuestion[]> {
    await wait(1600)
    return deriveFollowUps(intake.description)
  }

  /** Kicks off report generation, streaming stage updates as it works. */
  async generateReport(
    intake: FounderIntake,
    answeredFollowUps: FollowUpQuestion[],
    onStage?: (index: number, stage: GenerationStage) => void,
  ): Promise<ComplianceReport> {
    for (let i = 0; i < this.stages.length; i++) {
      onStage?.(i, this.stages[i])
      await wait(1150)
    }
    return this.buildReport(intake, answeredFollowUps)
  }

  /** Fire-and-forget: loops a human expert in on the generated report. */
  async requestExpertReview(reportId: string): Promise<{ queued: boolean; eta: string }> {
    await wait(600)
    void reportId
    return { queued: true, eta: '2–3 hours' }
  }

  /** Persists a founder answer to a follow-up question. */
  async submitFollowUp(questionId: string, answer: string): Promise<FollowUpQuestion> {
    await wait(400)
    return { id: questionId, question: '', rationale: '', answer }
  }

  /** Sends a founder tweak request against the summary doc to the agent. */
  async refineSummary(reportId: string, message: string): Promise<{ accepted: boolean }> {
    await wait(500)
    void reportId
    void message
    return { accepted: true }
  }

  private buildReport(
    intake: FounderIntake,
    answeredFollowUps: FollowUpQuestion[],
  ): ComplianceReport {
    const projectName = deriveProjectName(intake.description)
    return {
      projectName,
      founder: intake,
      generatedAt: new Date().toLocaleDateString('en-US', {
        month: 'long',
        day: 'numeric',
        year: 'numeric',
      }),
      summary: [
        {
          id: 'sec-overview',
          heading: 'Product overview',
          paragraphs: [
            `${projectName} is a mains- and battery-powered connected consumer device intended for the ` +
              'US and EU markets. This document summarizes the hardware as understood from your description ' +
              'and follow-up answers, for the purpose of scoping certification requirements.',
          ],
        },
        {
          id: 'sec-power',
          heading: 'Power system',
          paragraphs: [
            'The device is fitted with a lithium-ion battery pack alongside an external mains power supply, ' +
              'giving it two independent power sources that each carry their own compliance obligations.',
          ],
          bullets: [
              'Rechargeable lithium-ion cell/pack',
              'External AC/DC power supply or USB-C adapter',
              'On-device charge and protection circuitry',
            ],
        },
        {
          id: 'sec-connectivity',
          heading: 'Wireless & connectivity',
          paragraphs: [
            'A 2.4 GHz radio module provides the primary wireless link. As an intentional radiator, this ' +
              'subsystem is the main driver of the RF certification scope below.',
          ],
          bullets: ['2.4 GHz intentional radiator (Wi-Fi/BLE class module)', 'No cellular or LTE modem detected'],
        },
        {
          id: 'sec-enclosure',
          heading: 'Enclosure & mechanical',
          paragraphs: [
            'The described housing is treated as a standard consumer-grade enclosure until confirmed otherwise ' +
              'in the follow-up questions — material and flammability rating affect the safety test scope.',
          ],
        },
        {
          id: 'sec-markets',
          heading: 'Target markets',
          paragraphs: [
            'Distribution is planned for the United States and European Union, which sets the certification ' +
              'bodies and marks (FCC/UL for the US, CE/RED for the EU) this report covers.',
          ],
        },
        {
          id: 'sec-cert-summary',
          heading: 'Certification scope summary',
          paragraphs: [
            'Based on the subsystems above, we drafted the required standards, flagged two open follow-up ' +
              'questions, and reserved a slot with an expert reviewer to confirm the final plan.',
          ],
        },
      ],
      followUps: answeredFollowUps.length
        ? answeredFollowUps
        : deriveFollowUps(intake.description),
      checks: [
        {
          id: 'chk-fcc',
          code: 'FCC Part 15C',
          authority: 'FCC',
          title: 'Intentional radiator certification',
          status: 'required',
          scope: '2.4 GHz radio · US market',
          detail:
            'Full certification with an FCC-recognized lab, including radiated emissions, RF exposure (SAR/MPE), and an FCC ID grant. Test report and grant must be on file before marketing.',
          estimatedCost: '$8,000 – $15,000',
          turnaround: '4–6 weeks',
        },
        {
          id: 'chk-ul2054',
          code: 'UL 2054 / UL 62133-2',
          authority: 'UL',
          title: 'Lithium battery pack safety',
          status: 'required',
          scope: 'Li-ion cell & pack',
          detail:
            'Household & commercial battery safety evaluation covering overcharge, short circuit, crush, and thermal abuse. Pairs with cell-level UL 1642 if cells are not already listed.',
          estimatedCost: '$10,000 – $20,000',
          turnaround: '6–10 weeks',
        },
        {
          id: 'chk-un383',
          code: 'UN 38.3',
          authority: 'UNECE',
          title: 'Lithium battery transport testing',
          status: 'required',
          scope: 'Shipping & logistics',
          detail:
            'Eight-test sequence (altitude, thermal, vibration, shock, external short, impact, overcharge, forced discharge) required to legally ship lithium batteries by air or sea.',
          estimatedCost: '$3,000 – $5,000',
          turnaround: '3–4 weeks',
        },
        {
          id: 'chk-62368',
          code: 'UL / EN 62368-1',
          authority: 'UL / IEC',
          title: 'Audio/video & IT equipment safety',
          status: 'required',
          scope: 'Product + power supply',
          detail:
            'Hazard-based safety standard that has replaced UL 60950-1 and UL 60065. Covers electrical, thermal, and energy-source hazards for the device and its external supply.',
          estimatedCost: '$7,000 – $12,000',
          turnaround: '5–7 weeks',
        },
        {
          id: 'chk-ce',
          code: 'CE — RED 2014/53/EU',
          authority: 'EU',
          title: 'EU Radio Equipment Directive',
          status: 'recommended',
          scope: 'EU market entry',
          detail:
            'Self-declaration route using EN 300 328 (radio), EN 301 489 (EMC), and EN 62368-1 (safety). Needed before affixing the CE mark for European sales.',
          estimatedCost: '$6,000 – $11,000',
          turnaround: '4–6 weeks',
        },
        {
          id: 'chk-fcc15b',
          code: 'FCC Part 15B',
          authority: 'FCC',
          title: 'Unintentional emissions (digital device)',
          status: 'passed',
          scope: 'Digital electronics',
          detail:
            'Covers emissions from the MCU and digital circuitry. Your reference design already carries pre-scan data indicating a comfortable margin — bundled into the Part 15C test session.',
          estimatedCost: 'Included above',
          turnaround: 'Concurrent',
        },
      ],
      labs: [
        {
          id: 'lab-intertek',
          name: 'Intertek',
          location: 'Boxborough, MA',
          accreditations: ['NRTL', 'FCC TCB', 'A2LA'],
          specialty: 'Full EMC + product safety under one roof; strong for combined 15B/15C sessions.',
          leadTime: '3–4 weeks',
          rating: 4.7,
        },
        {
          id: 'lab-ul',
          name: 'UL Solutions',
          location: 'Fremont, CA',
          accreditations: ['NRTL', 'CB Scheme'],
          specialty: 'Authoritative for UL 2054 / 62133-2 battery listings and CB reports for EU.',
          leadTime: '6–8 weeks',
          rating: 4.5,
        },
        {
          id: 'lab-tuv',
          name: 'TÜV SÜD',
          location: 'Wakefield, MA',
          accreditations: ['NRTL', 'EU Notified Body'],
          specialty: 'One-stop for CE/RED plus US marks; issues EU-recognized certificates directly.',
          leadTime: '4–6 weeks',
          rating: 4.6,
        },
        {
          id: 'lab-element',
          name: 'Element Materials',
          location: 'San Diego, CA',
          accreditations: ['A2LA', 'FCC TCB'],
          specialty: 'Fast UN 38.3 transport testing and pre-scan slots for early prototypes.',
          leadTime: '2–3 weeks',
          rating: 4.4,
        },
      ],
      expert: {
        name: 'Patricia Nguyen',
        role: 'Senior Compliance Engineer · 12 yrs at NRTLs',
        avatar:
          'https://images.unsplash.com/photo-1573497019940-1c28c88b4f3e?w=160&h=160&fit=crop&auto=format',
        note:
          'Hi, thanks for trying hardware.check! I reviewed your compliance docs and added a couple of ' +
          'follow-up questions so we can tighten the battery and enclosure scope. The standards on your ' +
          'report card look correct for a US + EU launch — answer the two questions and I will confirm the final plan.',
      },
    }
  }
}

// A stand-in for the agent's reasoning: scans the founder's description for
// signals and returns the questions it needs answered before finalizing.
function deriveFollowUps(description: string): FollowUpQuestion[] {
  const text = description.toLowerCase()
  const has = (...terms: string[]) => terms.some((t) => text.includes(t))
  const questions: FollowUpQuestion[] = []

  if (has('battery', 'lithium', 'li-ion', 'rechargeable', 'cell', 'power bank')) {
    questions.push({
      id: 'q-battery',
      question: 'What battery chemistry and watt-hour rating does the pack use?',
      rationale:
        'Cell chemistry and Wh rating decide whether UL 2054, UL 62133-2, and UN 38.3 apply, and how the pack can legally ship.',
    })
  }
  if (has('wifi', 'wi-fi', 'bluetooth', 'ble', 'radio', 'wireless', 'zigbee', 'lte', 'cellular', 'ghz', 'rf', 'connected')) {
    questions.push({
      id: 'q-radio',
      question: 'Which wireless module(s) and frequency bands are you integrating?',
      rationale:
        'The radio and its bands determine whether you need FCC Part 15C certification and EU RED (EN 300 328) testing, and whether a pre-certified module can save you a test cycle.',
    })
  }
  if (has('plug', 'wall', 'mains', 'ac ', 'adapter', 'usb-c', 'usb c', 'charger', 'power supply', 'outlet')) {
    questions.push({
      id: 'q-power',
      question: 'How is the device powered — wall adapter, USB-C, or both?',
      rationale:
        'An external supply pulls in EN/UL 62368-1 and DoE efficiency marking obligations that change your test scope.',
    })
  }
  if (has('enclosure', 'plastic', 'housing', 'case', 'shell', 'metal', 'aluminum')) {
    questions.push({
      id: 'q-enclosure',
      question: 'What material is the enclosure, and does it house any heat-generating parts?',
      rationale:
        'Plastic enclosures need a UL 94 flammability rating; the V-0 vs HB choice affects your bill of materials and test scope.',
    })
  }
  if (has('kids', 'child', 'children', 'toy', 'baby', 'infant')) {
    questions.push({
      id: 'q-children',
      question: 'Is the product intended for or marketed to children under 12?',
      rationale:
        'Products for children trigger CPSIA, ASTM F963 toy safety, and third-party lab testing requirements in the US.',
    })
  }
  if (has('medical', 'health', 'clinical', 'patient', 'diagnostic', 'therapy', 'fda')) {
    questions.push({
      id: 'q-medical',
      question: 'Does the device make any medical or health claims?',
      rationale:
        'A medical claim moves you into FDA and IEC 60601 territory — a very different (and more expensive) pathway.',
    })
  }

  // Markets question is almost always relevant.
  questions.push({
    id: 'q-markets',
    question: 'Which markets are you launching in first (US, EU, UK, Canada, other)?',
    rationale:
      'Target markets decide which certification schemes run in parallel — FCC/UL for the US, CE/RED for the EU, UKCA for Britain.',
  })

  // Always have at least a couple of questions to work with.
  if (questions.length < 2) {
    questions.push({
      id: 'q-function',
      question: 'What is the core electrical function of the device, and what voltage does it run at?',
      rationale:
        'The operating voltage and function determine the baseline product-safety standard (e.g. EN/UL 62368-1) that applies.',
    })
  }

  return questions
}

function deriveProjectName(description: string): string {
  const cleaned = description.trim()
  if (!cleaned) return 'your device'
  const firstWords = cleaned.split(/\s+/).slice(0, 4).join(' ')
  return firstWords.length > 42 ? firstWords.slice(0, 42) + '…' : firstWords
}

export const complianceApi = new ComplianceApi()
