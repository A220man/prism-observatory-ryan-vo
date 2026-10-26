export type AgentStatus = 'active' | 'inactive' | 'error';

export interface Agent {
  id: string;
  name: string;
  description: string | null;
  config: Record<string, unknown>;
  status: AgentStatus;
  created_at: string;
  updated_at: string;
}

export interface AgentCreate {
  name: string;
  description?: string;
  config?: Record<string, unknown>;
}

export interface AgentUpdate {
  name?: string;
  description?: string;
  config?: Record<string, unknown>;
  status?: AgentStatus;
}

export interface AgentListResponse {
  items: Agent[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}
