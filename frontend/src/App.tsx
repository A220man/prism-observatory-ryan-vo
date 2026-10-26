import { useState, useEffect } from 'react';
import { AgentList } from './components/AgentList';
import { AgentForm } from './components/AgentForm';
import type { Agent } from './types/agent';
import './App.css';

interface HealthResponse {
  status: string;
  service: string;
}

type Tab = 'health' | 'agents';

function App() {
  const [activeTab, setActiveTab] = useState<Tab>('health');
  const [health, setHealth] = useState<HealthResponse | null>(null);
  const [healthLoading, setHealthLoading] = useState(true);
  const [healthError, setHealthError] = useState<string | null>(null);
  const [showForm, setShowForm] = useState(false);
  const [editingAgent, setEditingAgent] = useState<Agent | null>(null);

  useEffect(() => {
    async function fetchHealth() {
      try {
        const response = await fetch('/api/healthz');
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        setHealth(data);
      } catch (err) {
        setHealthError(err instanceof Error ? err.message : 'Unknown error');
      } finally {
        setHealthLoading(false);
      }
    }
    fetchHealth();
  }, []);

  const handleCreateAgent = () => {
    setEditingAgent(null);
    setShowForm(true);
  };

  const handleEditAgent = (agent: Agent) => {
    setEditingAgent(agent);
    setShowForm(true);
  };

  const handleFormSuccess = () => {
    setShowForm(false);
    setEditingAgent(null);
  };

  const handleFormClose = () => {
    setShowForm(false);
    setEditingAgent(null);
  };

  if (healthLoading) {
    return (
      <div className="app">
        <header>
          <h1>Prism Observatory</h1>
        </header>
        <main>
          <div className="loading">Loading...</div>
        </main>
      </div>
    );
  }

  return (
    <div className="app">
      <header>
        <h1>Prism Observatory</h1>
        <p className="subtitle">The open-source app everyone uses to manage agents at work</p>
      </header>
      <nav className="tabs" role="tablist" aria-label="Main navigation">
        <button
          role="tab"
          aria-selected={activeTab === 'health'}
          onClick={() => setActiveTab('health')}
          className={activeTab === 'health' ? 'active' : ''}
        >
          Health
        </button>
        <button
          role="tab"
          aria-selected={activeTab === 'agents'}
          onClick={() => setActiveTab('agents')}
          className={activeTab === 'agents' ? 'active' : ''}
        >
          Agents
        </button>
      </nav>
      <main>
        {activeTab === 'health' && (
          <section className="tab-panel">
            {healthError && (
              <div className="error">
                <h2>Error</h2>
                <pre>{healthError}</pre>
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
                <li>
                  <a href="/api/healthz" target="_blank" rel="noopener noreferrer">
                    Health Check API
                  </a>
                </li>
                <li>
                  <a href="/docs" target="_blank" rel="noopener noreferrer">
                    API Documentation (Swagger)
                  </a>
                </li>
              </ul>
            </section>
          </section>
        )}

        {activeTab === 'agents' && (
          <section className="tab-panel">
            <div className="panel-header">
              <h2>Agent Management</h2>
              <button className="btn btn-primary" onClick={handleCreateAgent}>
                Create Agent
              </button>
            </div>
            <AgentList onEdit={handleEditAgent} />
          </section>
        )}
      </main>
      <footer>
        <p>Prism Observatory &copy; 2024 Ryan Vo</p>
      </footer>

      {showForm && (
        <AgentForm
          agent={editingAgent}
          onClose={handleFormClose}
          onSuccess={handleFormSuccess}
        />
      )}
    </div>
  );
}

export default App;
