import { useState, useEffect } from 'react';
import { agentsApi } from '../services/api';
import type { Agent, AgentListResponse, AgentStatus } from '../types/agent';
import './AgentList.css';

interface AgentListProps {
  onEdit?: (agent: Agent) => void;
}

export function AgentList({ onEdit }: AgentListProps) {
  const [agents, setAgents] = useState<Agent[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [pagination, setPagination] = useState({
    page: 1,
    page_size: 10,
    total: 0,
    total_pages: 1,
  });
  const [filters, setFilters] = useState({ status: '', name: '' });

  const fetchAgents = async () => {
    setLoading(true);
    setError(null);
    try {
      const data: AgentListResponse = await agentsApi.list({
        page: pagination.page,
        page_size: pagination.page_size,
        status: filters.status || undefined,
        name: filters.name || undefined,
      });
      setAgents(data.items);
      setPagination((prev) => ({
        ...prev,
        total: data.total,
        total_pages: data.total_pages,
      }));
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch agents');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAgents();
  }, [pagination.page, filters]);

  const handlePageChange = (newPage: number) => {
    if (newPage >= 1 && newPage <= pagination.total_pages) {
      setPagination((prev) => ({ ...prev, page: newPage }));
    }
  };

  const handleFilterChange = (key: 'status' | 'name', value: string) => {
    setFilters((prev) => ({ ...prev, [key]: value }));
    setPagination((prev) => ({ ...prev, page: 1 }));
  };

  const handleDelete = async (agent: Agent) => {
    if (!confirm(`Delete agent "${agent.name}"?`)) return;
    try {
      await agentsApi.delete(agent.id);
      fetchAgents();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to delete agent');
    }
  };

  const handleStatusChange = async (agent: Agent, newStatus: AgentStatus) => {
    try {
      await agentsApi.update(agent.id, { status: newStatus });
      fetchAgents();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to update agent status');
    }
  };

  if (loading) {
    return <div className="agent-list loading">Loading agents...</div>;
  }

  return (
    <div className="agent-list">
      <div className="agent-list-header">
        <h2>Agents</h2>
        <div className="agent-filters">
          <input
            type="text"
            placeholder="Filter by name..."
            value={filters.name}
            onChange={(e) => handleFilterChange('name', e.target.value)}
            className="filter-input"
          />
          <select
            value={filters.status}
            onChange={(e) => handleFilterChange('status', e.target.value)}
            className="filter-select"
          >
            <option value="">All Statuses</option>
            <option value="active">Active</option>
            <option value="inactive">Inactive</option>
            <option value="error">Error</option>
          </select>
        </div>
      </div>

      {error && <div className="error-message">{error}</div>}

      <table className="agent-table">
        <thead>
          <tr>
            <th>Name</th>
            <th>Description</th>
            <th>Status</th>
            <th>Created</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {agents.length === 0 ? (
            <tr>
              <td colSpan={5} className="empty-state">
                No agents found. Click "Create Agent" to add one.
              </td>
            </tr>
          ) : (
            agents.map((agent) => (
              <tr key={agent.id}>
                <td className="agent-name">{agent.name}</td>
                <td className="agent-description">
                  {agent.description || '<em>No description</em>'}
                </td>
                <td>
                  <select
                    value={agent.status}
                    onChange={(e) => handleStatusChange(agent, e.target.value as AgentStatus)}
                    className={`status-badge status-${agent.status}`}
                  >
                    <option value="active">Active</option>
                    <option value="inactive">Inactive</option>
                    <option value="error">Error</option>
                  </select>
                </td>
                <td className="agent-date">{new Date(agent.created_at).toLocaleDateString()}</td>
                <td className="agent-actions">
                  <button onClick={() => onEdit?.(agent)} className="btn btn-edit">
                    Edit
                  </button>
                  <button onClick={() => handleDelete(agent)} className="btn btn-delete">
                    Delete
                  </button>
                </td>
              </tr>
            ))
          )}
        </tbody>
      </table>

      {pagination.total_pages > 1 && (
        <div className="pagination">
          <button
            onClick={() => handlePageChange(pagination.page - 1)}
            disabled={pagination.page === 1}
            className="btn btn-page"
          >
            Previous
          </button>
          <span className="page-info">
            Page {pagination.page} of {pagination.total_pages} ({pagination.total} total)
          </span>
          <button
            onClick={() => handlePageChange(pagination.page + 1)}
            disabled={pagination.page === pagination.total_pages}
            className="btn btn-page"
          >
            Next
          </button>
        </div>
      )}
    </div>
  );
}
