import { useState } from 'react'
import { useNavigate, useSearchParams } from 'react-router'
import Shell from '../components/Shell'
import Button from '../components/Button'
import { useReport } from '../store/ReportContext'

export default function FormScreen() {
  const navigate = useNavigate()
  const { analyze } = useReport()
  const [searchParams] = useSearchParams()

  // Prefill from URL params, e.g. ?first=Ada&last=Okafor&email=ada@x.io&description=...
  const [founderName, setFounderName] = useState(() =>
    [searchParams.get('first'), searchParams.get('last')].filter(Boolean).join(' '),
  )
  const [email, setEmail] = useState(() => searchParams.get('email') ?? '')
  const [description, setDescription] = useState(() => searchParams.get('description') ?? '')
  const [touched, setTouched] = useState(false)

  const hasPrefill = Boolean(
    searchParams.get('first') ||
      searchParams.get('last') ||
      searchParams.get('email') ||
      searchParams.get('description'),
  )

  const emailValid = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)
  const valid = founderName.trim() && emailValid && description.trim().length > 12

  const submit = () => {
    setTouched(true)
    if (!valid) return
    navigate('/questions')
    void analyze({
      founderName: founderName.trim(),
      email: email.trim(),
      description: description.trim(),
    })
  }

  const fieldClass = 'fc-field py-3'

  return (
    <Shell maxWidth="max-w-4xl">
      <div className="fc-fade-up pt-4">
        <h1 className="font-body text-3xl font-bold leading-tight text-white sm:text-4xl">
          Tell us about what you're building
        </h1>
        <p className="mt-3 font-body text-base text-white/85">
          {hasPrefill
            ? "We've pre-filled what we already know — just double-check it and fill in anything missing."
            : 'Our agents do the rest and an expert reviews the result.'}
        </p>

        <div className="mt-8 space-y-4">
          <div>
            <label className="mb-1.5 block font-body text-sm font-extrabold uppercase tracking-wide text-white">
              Founder name
            </label>
            <input
              className={fieldClass}
              placeholder="Ada Okafor"
              value={founderName}
              onChange={(e) => setFounderName(e.target.value)}
            />
          </div>
          <div>
            <label className="mb-1.5 block font-body text-sm font-extrabold uppercase tracking-wide text-white">Email</label>
            <input
              className={fieldClass}
              placeholder="ada@everfield.io"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
            {touched && !emailValid && (
              <p className="mt-1.5 font-body text-xs text-white">Enter a valid email address.</p>
            )}
          </div>
          <div>
            <label className="mb-1.5 block font-body text-sm font-extrabold uppercase tracking-wide text-white">
              Describe your startup &amp; product
            </label>
            <textarea
              className={`${fieldClass} min-h-44 resize-none`}
              placeholder="We're building a connected indoor air-quality monitor with a rechargeable lithium-ion battery and a 2.4 GHz radio, selling to consumers in the US and EU..."
              value={description}
              onChange={(e) => setDescription(e.target.value)}
            />
            {touched && description.trim().length <= 12 && (
              <p className="mt-1.5 font-body text-xs text-white">
                Add a sentence or two so the agents have something to work with.
              </p>
            )}
          </div>
        </div>

        <div className="mt-6 flex items-center justify-end gap-3">
          <Button onClick={submit} disabled={touched && !valid}>
            Submit
          </Button>
        </div>
      </div>
    </Shell>
  )
}
