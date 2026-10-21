import { useState, useEffect } from 'react'
import './App.css'

interface HealthResponse {
  status: string
  service: string
}

function App() {
  const [health, setHealth] = useState<HealthResponse | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    async function fetchHealth() {
      try {
        const response = await fetch('/api/healthz')
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`)
        }
        const data = await response.json()
        setHealth(data)
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Unknown error')
      } finally {
        setLoading(false)
      }
    }
    fetchHealth()
  }, [])

  if (loading) {
    return (
      <div className="app">
        <header>
          <h1>Prism Observatory</h1>
        </header>
        <main>
          <div className="loading">Loading...</div>
        </main>
      </div>
    )
  }

  return (
    <div className="app">
      <header>
        <h1>Prism Observatory</h1>
        <p className="subtitle">The open-source app everyone uses to manage agents at work</p>
      </header>
      <main>
        {error && (
          <div className="error">
            <h2>Error</h2>
            <pre>{error}</pre>
          </div>
        )}
        {health && (
          <div className="health-card">
            <h2>Backend Health</h2>
            <dl>
              <dt>Status</dt>
              <dd className={health.status === 'ok' ? 'status-ok' : 'status-error'}>
                {health.status}
              </dd>
              <dt>Service</dt>
              <dd>{health.service}</dd>
            </dl>
          </div>
        )}
        <section className="info">
          <h2>Quick Links</h2>
          <ul>
            <li><a href="/api/healthz" target="_blank" rel="noopener noreferrer">Health Check API</a></li>
            <li><a href="/docs" target="_blank" rel="noopener noreferrer">API Documentation (Swagger)</a></li>
          </ul>
        </section>
      </main>
      <footer>
        <p>Prism Observatory &copy; 2024 Ryan Vo</p>
      </footer>
    </div>
  )
}

export default App