import { describe, it, expect } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import App from '../src/App'

describe('App', () => {

  it('renders loading state initially', () => {
    const { promise } = Promise.withResolvers()
    ;(global.fetch as vi.Mock).mockReturnValue(promise)
    render(<App />)
    expect(screen.getByText('Loading...')).toBeInTheDocument()
  })

  it('renders health data when fetch succeeds', async () => {
    (global.fetch as vi.Mock).mockResolvedValue({
      ok: true,
      json: async () => ({ status: 'ok', service: 'prism-observatory' }),
    })
    render(<App />)
    await waitFor(() => {
      expect(screen.getByText('Backend Health')).toBeInTheDocument()
    })
    expect(screen.getByText('ok')).toBeInTheDocument()
    expect(screen.getByText('prism-observatory')).toBeInTheDocument()
  })

  it('renders error when fetch fails', async () => {
    (global.fetch as vi.Mock).mockRejectedValue(new Error('Network error'))
    render(<App />)
    await waitFor(() => {
      expect(screen.getByText('Error')).toBeInTheDocument()
    })
    expect(screen.getByText('Network error')).toBeInTheDocument()
  })
})