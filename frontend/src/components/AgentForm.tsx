import { useState, useEffect } from 'react';
import { agentsApi } from '../services/api';
import type { Agent, AgentCreate, AgentUpdate, AgentStatus } from '../types/agent';
import './AgentForm.css';

interface AgentFormProps {
  agent?: Agent | null;
  onClose: () => void;
  onSuccess: () => void;
}

interface AgentFormData {
  name: string;
  description: string;
  config: Record<string, unknown>;
  status: AgentStatus;
}

export function AgentForm({ agent, onClose, onSuccess }: AgentFormProps) {
  const isEditing = !!agent;
  const [formData, setFormData] = useState<AgentFormData>({
    name: '',
    description: '',
    config: {},
    status: 'active',
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [configJson, setConfigJson] = useState('{}');

  useEffect(() => {
    if (agent) {
      setFormData({
        name: agent.name,
        description: agent.description || '',
        config: agent.config,
        status: agent.status,
      });
      setConfigJson(JSON.stringify(agent.config, null, 2));
    } else {
      setFormData({
        name: '',
        description: '',
        config: {},
        status: 'active',
      });
      setConfigJson('{}');
    }
    setError(null);
  }, [agent]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    let config: Record<string, unknown> = {};
    try {
      config = JSON.parse(configJson);
    } catch {
      setError('Invalid JSON in config');
      setLoading(false);
      return;
    }

    const submitData = { ...formData, config };

    try {
      if (isEditing && agent) {
        await agentsApi.update(agent.id, submitData as AgentUpdate);
      } else {
        await agentsApi.create(submitData as AgentCreate);
      }
      onSuccess();
      onClose();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to save agent');
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    if (name === 'status') {
      setFormData((prev) => ({ ...prev, status: value as AgentStatus }));
    } else {
      setFormData((prev) => ({ ...prev, [name]: value }));
    }
  };

  const handleConfigChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setConfigJson(e.target.value);
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2>{isEditing ? 'Edit Agent' : 'Create Agent'}</h2>
          <button className="modal-close" onClick={onClose} aria-label="Close">
            ×
          </button>
        </div>

        <form onSubmit={handleSubmit} className="modal-body">
          {error && <div className="error-message">{error}</div>}

          <div className="form-group">
            <label htmlFor="name">Name <span className="required">*</span></label>
            <input
              type="text"
              id="name"
              name="name"
              value={formData.name}
              onChange={handleChange}
              required
              maxLength={100}
              placeholder="Enter agent name"
            />
          </div>

          <div className="form-group">
            <label htmlFor="description">Description</label>
            <textarea
              id="description"
              name="description"
              value={formData.description}
              onChange={handleChange}
              maxLength={500}
              rows={3}
              placeholder="Enter agent description (optional)"
            />
          </div>

          <div className="form-group">
            <label htmlFor="status">Status</label>
            <select id="status" name="status" value={formData.status} onChange={handleChange}>
              <option value="active">Active</option>
              <option value="inactive">Inactive</option>
              <option value="error">Error</option>
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="config">Config (JSON)</label>
            <textarea
              id="config"
              name="config"
              value={configJson}
              onChange={handleConfigChange}
              rows={6}
              className="json-input"
              placeholder='{"model": "gpt-4", "temperature": 0.7}'
            />
            <small className="form-hint">Valid JSON object. Leave empty for default.</small>
          </div>

          <div className="modal-footer">
            <button type="button" className="btn btn-secondary" onClick={onClose} disabled={loading}>
              Cancel
            </button>
            <button type="submit" className="btn btn-primary" disabled={loading}>
              {loading ? 'Saving...' : isEditing ? 'Update' : 'Create'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
