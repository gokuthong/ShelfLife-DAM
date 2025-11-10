/**
 * Tests for Auth Redux Slice
 */
import authReducer, {
  loginUser,
  registerUser,
  fetchCurrentUser,
  logout,
  clearError,
} from './authSlice'
import { configureStore } from '@reduxjs/toolkit'

// Mock fetch
global.fetch = jest.fn()

describe('authSlice', () => {
  let store: any

  beforeEach(() => {
    store = configureStore({
      reducer: {
        auth: authReducer,
      },
    })
    ;(fetch as jest.Mock).mockClear()
    localStorage.clear()
  })

  describe('Initial State', () => {
    it('should have correct initial state', () => {
      const state = store.getState().auth
      expect(state).toEqual({
        user: null,
        token: null,
        isLoading: true,
        isAuthenticated: false,
        error: null,
      })
    })
  })

  describe('Reducers', () => {
    it('should handle logout', () => {
      // Set some state first
      store.dispatch({ type: 'auth/loginUser/fulfilled', payload: { user: { username: 'test' }, token: 'token123' } })

      store.dispatch(logout())
      const state = store.getState().auth

      expect(state.user).toBeNull()
      expect(state.token).toBeNull()
      expect(state.isAuthenticated).toBe(false)
      expect(state.error).toBeNull()
    })

    it('should handle clearError', () => {
      // Set error state
      store.dispatch({ type: 'auth/loginUser/rejected', payload: 'Login failed' })

      store.dispatch(clearError())
      const state = store.getState().auth

      expect(state.error).toBeNull()
    })
  })

  describe('loginUser thunk', () => {
    it('should handle successful login', async () => {
      const mockResponse = {
        user: { id: 1, username: 'testuser', email: 'test@example.com', role: 'viewer', is_admin: false, is_editor: false },
        token: 'test-token',
      }

      ;(fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse,
      })

      await store.dispatch(loginUser({ username: 'testuser', password: 'password123' }))

      const state = store.getState().auth
      expect(state.isLoading).toBe(false)
      expect(state.isAuthenticated).toBe(true)
      expect(state.user).toEqual(mockResponse.user)
      expect(state.token).toBe('test-token')
      expect(state.error).toBeNull()
    })

    it('should handle login failure', async () => {
      ;(fetch as jest.Mock).mockResolvedValueOnce({
        ok: false,
        json: async () => ({ detail: 'Invalid credentials' }),
      })

      await store.dispatch(loginUser({ username: 'testuser', password: 'wrongpass' }))

      const state = store.getState().auth
      expect(state.isLoading).toBe(false)
      expect(state.isAuthenticated).toBe(false)
      expect(state.user).toBeNull()
      expect(state.error).toBe('Invalid credentials')
    })

    it('should handle network error on login', async () => {
      ;(fetch as jest.Mock).mockRejectedValueOnce(new Error('Network error'))

      await store.dispatch(loginUser({ username: 'testuser', password: 'password123' }))

      const state = store.getState().auth
      expect(state.isLoading).toBe(false)
      expect(state.isAuthenticated).toBe(false)
      expect(state.error).toBe('Network error. Please try again.')
    })

    it('should set loading state while login is pending', () => {
      ;(fetch as jest.Mock).mockImplementation(
        () => new Promise(resolve => setTimeout(resolve, 1000))
      )

      store.dispatch(loginUser({ username: 'testuser', password: 'password123' }))

      const state = store.getState().auth
      expect(state.isLoading).toBe(true)
      expect(state.error).toBeNull()
    })
  })

  describe('registerUser thunk', () => {
    it('should handle successful registration', async () => {
      const mockResponse = {
        user: { id: 1, username: 'newuser', email: 'new@example.com', role: 'viewer', is_admin: false, is_editor: false },
        token: 'new-token',
      }

      ;(fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse,
      })

      await store.dispatch(
        registerUser({
          username: 'newuser',
          email: 'new@example.com',
          password: 'password123',
        })
      )

      const state = store.getState().auth
      expect(state.isLoading).toBe(false)
      expect(state.isAuthenticated).toBe(true)
      expect(state.user).toEqual(mockResponse.user)
      expect(state.token).toBe('new-token')
      expect(state.error).toBeNull()
    })

    it('should handle registration failure', async () => {
      ;(fetch as jest.Mock).mockResolvedValueOnce({
        ok: false,
        json: async () => ({ detail: 'Username already exists' }),
      })

      await store.dispatch(
        registerUser({
          username: 'existinguser',
          email: 'test@example.com',
          password: 'password123',
        })
      )

      const state = store.getState().auth
      expect(state.isLoading).toBe(false)
      expect(state.isAuthenticated).toBe(false)
      expect(state.error).toBe('Username already exists')
    })

    it('should handle network error on registration', async () => {
      ;(fetch as jest.Mock).mockRejectedValueOnce(new Error('Network error'))

      await store.dispatch(
        registerUser({
          username: 'newuser',
          email: 'new@example.com',
          password: 'password123',
        })
      )

      const state = store.getState().auth
      expect(state.error).toBe('Network error. Please try again.')
    })
  })

  describe('fetchCurrentUser thunk', () => {
    it('should fetch current user successfully', async () => {
      localStorage.setItem('token', 'valid-token')

      const mockUser = {
        id: 1,
        username: 'testuser',
        email: 'test@example.com',
        role: 'editor',
        is_admin: false,
        is_editor: true,
      }

      ;(fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: async () => mockUser,
      })

      await store.dispatch(fetchCurrentUser())

      const state = store.getState().auth
      expect(state.isLoading).toBe(false)
      expect(state.isAuthenticated).toBe(true)
      expect(state.user).toEqual(mockUser)
      expect(state.error).toBeNull()
    })

    it('should handle missing token', async () => {
      localStorage.removeItem('token')

      await store.dispatch(fetchCurrentUser())

      const state = store.getState().auth
      expect(state.isLoading).toBe(false)
      expect(state.isAuthenticated).toBe(false)
      expect(state.user).toBeNull()
    })

    it('should handle authentication failure and clear token', async () => {
      localStorage.setItem('token', 'invalid-token')

      ;(fetch as jest.Mock).mockResolvedValueOnce({
        ok: false,
      })

      await store.dispatch(fetchCurrentUser())

      const state = store.getState().auth
      expect(state.isLoading).toBe(false)
      expect(state.isAuthenticated).toBe(false)
      expect(state.user).toBeNull()
      expect(state.token).toBeNull()
    })

    it('should handle network error', async () => {
      localStorage.setItem('token', 'valid-token')
      ;(fetch as jest.Mock).mockRejectedValueOnce(new Error('Network error'))

      await store.dispatch(fetchCurrentUser())

      const state = store.getState().auth
      expect(state.isLoading).toBe(false)
      expect(state.isAuthenticated).toBe(false)
    })
  })
})
