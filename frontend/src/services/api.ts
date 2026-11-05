import type { Agent, AgentCreate, AgentUpdate, AgentListResponse } from '../types/agent';

const API_BASE = '/api';

async function fetchJson<T>(url: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE}${url}`, {
    headers: { 'Content-Type': 'application/json', ...options?.headers },
    ...options,
  });
  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Request failed' }));
    throw new Error(error.detail || `HTTP error! status: ${response.status}`);
  }
  if (response.status === 204) {
    return undefined as T;
  }
  return response.json();
}

export const agentsApi = {
  list: (params?: {
    page?: number;
    page_size?: number;
    status?: string;
    name?: string;
    sort_by?: string;
    sort_order?: string;
  }): Promise<AgentListResponse> => {
    const searchParams = new URLSearchParams();
    if (params?.page) searchParams.set('page', String(params.page));
    if (params?.page_size) searchParams.set('page_size', String(params.page_size));
    if (params?.status) searchParams.set('status', params.status);
    if (params?.name) searchParams.set('name', params.name);
    if (params?.sort_by) searchParams.set('sort_by', params.sort_by);
    if (params?.sort_order) searchParams.set('sort_order', params.sort_order);
    const query = searchParams.toString();
    return fetchJson<AgentListResponse>(`/agents${query ? `?${query}` : ''}`);
  },

  get: (id: string): Promise<Agent> => fetchJson<Agent>(`/agents/${id}`),

  create: (data: AgentCreate): Promise<Agent> =>
    fetchJson<Agent>('/agents', { method: 'POST', body: JSON.stringify(data) }),

  update: (id: string, data: AgentUpdate): Promise<Agent> =>
    fetchJson<Agent>(`/agents/${id}`, { method: 'PATCH', body: JSON.stringify(data) }),

  delete: (id: string): Promise<void> =>
    fetchJson<void>(`/agents/${id}`, { method: 'DELETE' }),
};
