import { useState } from 'react'
import './App.css'

function App() {
  const [resume, setResume] = useState<File | null>(null)
  const [jobDescription, setJobDescription] = useState('')

  return (
    <div className="app">
      <header className="navbar">
        <a className="brand" href="#">
          <span className="brand-icon">J</span>
          JobPilot
        </a>
        <span className="nav-label">AI Career Assistant</span>
      </header>

      <main className="main-content">
        <section className="hero">
          <span className="eyebrow">YOUR CAREER, YOUR NEXT STEP</span>
          <h1>Find the right job for <span>your skills.</span></h1>
          <p>
            Upload your resume, add a job description, and prepare to
            understand how well your skills match the role.
          </p>
        </section>

        <section className="workspace">
          <div className="section-heading">
            <span className="step-number">01</span>
            <div>
              <h2>Upload your resume</h2>
              <p>Start with your existing resume in PDF format.</p>
            </div>
          </div>

          <label className="upload-box" htmlFor="resume-upload">
            <span className="upload-icon">↑</span>
            <strong>
              {resume ? resume.name : 'Choose your resume'}
            </strong>
            <span>
              {resume
                ? `${(resume.size / 1024).toFixed(1)} KB selected`
                : 'Select a PDF file from your computer'}
            </span>
            <span className="browse-button">Browse files</span>
            <input
              id="resume-upload"
              type="file"
              accept=".pdf,application/pdf"
              onChange={(event) => {
                const file = event.target.files?.[0] ?? null
                setResume(file)
              }}
            />
          </label>

          <div className="section-heading job-heading">
            <span className="step-number">02</span>
            <div>
              <h2>Add the job description</h2>
              <p>Paste the requirements for the role you want.</p>
            </div>
          </div>

          <textarea
            className="job-input"
            placeholder="Paste the job description here...&#10;&#10;Include the role, required skills, qualifications and responsibilities."
            value={jobDescription}
            onChange={(event) => setJobDescription(event.target.value)}
            rows={7}
          />

          <div className="form-footer">
            <span>PDF only · Maximum file size: 5 MB</span>
            <button
              className="analyze-button"
              type="button"
              disabled
              title="Available after the backend API is connected"
            >
              Analyze my match <span>→</span>
            </button>
          </div>

          <p className="coming-soon">
            Resume analysis will be enabled after the backend is connected.
          </p>
        </section>

        <section className="info-card">
          <span className="info-icon">✦</span>
          <div>
            <h3>Understand your strengths</h3>
            <p>
              The planned analysis will identify matching skills, highlight
              missing requirements, and suggest possible next steps.
            </p>
          </div>
        </section>

        <footer className="footer">
          JobPilot · Built to help students make informed career decisions.
        </footer>
      </main>
    </div>
  )
}

export default App