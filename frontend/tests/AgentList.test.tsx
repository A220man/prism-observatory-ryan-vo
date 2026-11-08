import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, waitFor, fireEvent } from '@testing-library/react'
import { AgentList } from '../src/components/AgentList'
import type { Agent } from '../src/types/agent'

const mockAgents: Agent[] = [
  {
    id: '1',
    name: 'Test Agent 1',
    description: 'First test agent',
    config: {},
    status: 'active',
    created_at: '2024-01-01T00:00:00Z',
    updated_at: '2024-01-01T00:00:00Z',
  },
  {
    id: '2',
    name: 'Test Agent 2',
    description: 'Second test agent',
    config: {},
    status: 'inactive',
    created_at: '2024-01-02T00:00:00Z',
    updated_at: '2024-01-02T00:00:00Z',
  },
]

const mockListResponse = {
  items: mockAgents,
  total: 2,
  page: 1,
  page_size: 10,
  total_pages: 1,
}

describe('AgentList', () => {
  beforeEach(() => {
    vi.resetAllMocks()
  })

  it('renders loading state initially', () => {
    const promise = Promise.resolve({ ok: true, json: async () => mockListResponse })
    vi.spyOn(global, 'fetch').mockReturnValue(promise as Promise<Response>)
    render(<AgentList />)
    expect(screen.getByText('Loading agents...')).toBeInTheDocument()
  })

  it('renders agent list when fetch succeeds', async () => {
    vi.spyOn(global, 'fetch').mockResolvedValue({
      ok: true,
      json: async () => mockListResponse,
    })
    render(<AgentList />)
    await waitFor(() => {
      expect(screen.getByText('Test Agent 1')).toBeInTheDocument()
      expect(screen.getByText('Test Agent 2')).toBeInTheDocument()
    })
  })

  it('renders empty state when no agents', async () => {
    vi.spyOn(global, 'fetch').mockResolvedValue({
      ok: true,
      json: async () => ({ ...mockListResponse, items: [], total: 0 }),
    })
    render(<AgentList />)
    await waitFor(() => {
      expect(screen.getByText('No agents found. Click "Create Agent" to add one.')).toBeInTheDocument()
    })
  })

  it('calls onEdit when edit button clicked', async () => {
    const onEdit = vi.fn()
    vi.spyOn(global, 'fetch').mockResolvedValue({
      ok: true,
      json: async () => mockListResponse,
    })
    render(<AgentList onEdit={onEdit} />)
    await waitFor(() => {
      expect(screen.getByText('Test Agent 1')).toBeInTheDocument()
    })
    fireEvent.click(screen.getAllByText('Edit')[0])
    expect(onEdit).toHaveBeenCalledWith(mockAgents[0])
  })

  it('shows filter inputs', async () => {
    vi.spyOn(global, 'fetch').mockResolvedValue({
      ok: true,
      json: async () => mockListResponse,
    })
    render(<AgentList />)
    await waitFor(() => {
      expect(screen.getByPlaceholderText('Filter by name...')).toBeInTheDocument()
      expect(screen.getByText('All Statuses')).toBeInTheDocument()
    })
  })
})
