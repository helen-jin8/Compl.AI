import { useState } from 'react'
import { useNavigate } from 'react-router'
import Shell from '../components/Shell'
import Button from '../components/Button'
import { useReport } from '../store/ReportContext'

export default function FormScreen() {
  const navigate = useNavigate()
  const { analyze } = useReport()

  const [founderName, setFounderName] = useState('')
  const [email, setEmail] = useState('')
  const [description, setDescription] = useState('')
  const [touched, setTouched] = useState(false)

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

  const fieldClass =
    'w-full rounded-lg border border-ink/70 bg-white px-4 py-3 font-body text-sm text-ink outline-none transition-shadow placeholder:text-ink-soft/60 focus:border-deep focus:ring-2 focus:ring-deep/30'

  return (
    <Shell maxWidth="max-w-2xl">
      <div className="fc-fade-up pt-4">
        <h1 className="font-body text-3xl font-bold leading-tight text-white sm:text-4xl">
          Tell us about what you're building
        </h1>
        <p className="mt-3 font-body text-base text-white/85">
          Three quick fields. Our agents do the rest and an expert reviews the result.
        </p>

        <div className="mt-8 space-y-4">
          <div>
            <label className="mb-1.5 block font-body text-xs font-bold text-white">
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
            <label className="mb-1.5 block font-body text-xs font-bold text-white">Email</label>
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
            <label className="mb-1.5 block font-body text-xs font-bold text-white">
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
          <span className="font-body text-xs text-white/70">
            Takes about 20 seconds to generate
          </span>
          <Button onClick={submit} disabled={touched && !valid}>
            Submit
          </Button>
        </div>
      </div>
    </Shell>
  )
}
