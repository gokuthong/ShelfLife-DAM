/**
 * Tests for AuthContext
 */
import React from 'react'
import { render, screen, waitFor, act } from '@testing-library/react'
import { useRouter } from 'next/navigation'
import { AuthProvider, useAuth } from './AuthContext'
import { authAPI } from '@/utils/api'

// Mock the API
jest.mock('@/utils/api', () => ({
  authAPI: {
    getProfile: jest.fn(),
    login: jest.fn(),
    register: jest.fn(),
    updateProfile: jest.fn(),
  },
}))

// Mock Next.js router
jest.mock('next/navigation', () => ({
  useRouter: jest.fn(),
}))

// Test component that uses the auth context
function TestComponent() {
  const { user, isLoading, login, register, logout, updateProfile } = useAuth()

  return (
    <div>
      <div data-testid="loading">{isLoading ? 'Loading' : 'Not Loading'}</div>
      <div data-testid="user">{user ? user.username : 'No User'}</div>
      <button onClick={() => login({ username: 'test', password: 'pass' })}>
        Login
      </button>
      <button
        onClick={() =>
          register({
            username: 'test',
            email: 'test@example.com',
            password: 'pass',
            password2: 'pass',
          })
        }
      >
        Register
      </button>
      <button onClick={logout}>Logout</button>
      <button onClick={() => updateProfile({ first_name: 'John' })}>
        Update Profile
      </button>
    </div>
  )
}

describe('AuthContext', () => {
  let mockPush: jest.Mock
  let mockLocalStorage: { [key: string]: string }

  beforeEach(() => {
    mockPush = jest.fn()
    ;(useRouter as jest.Mock).mockReturnValue({ push: mockPush })

    // Reset localStorage mock
    mockLocalStorage = {}
    Storage.prototype.getItem = jest.fn((key) => mockLocalStorage[key] || null)
    Storage.prototype.setItem = jest.fn((key, value) => {
      mockLocalStorage[key] = value
    })
    Storage.prototype.removeItem = jest.fn((key) => {
      delete mockLocalStorage[key]
    })

    jest.clearAllMocks()
  })

  describe('Initialization', () => {
    it('should start with loading state', async () => {
      ;(authAPI.getProfile as jest.Mock).mockResolvedValue({
        username: 'testuser',
        email: 'test@example.com',
      })

      render(
        <AuthProvider>
          <TestComponent />
        </AuthProvider>
      )

      expect(screen.getByTestId('loading')).toHaveTextContent('Loading')
    })

    it('should check auth on mount if token exists', async () => {
      mockLocalStorage['accessToken'] = 'test-token'
      ;(authAPI.getProfile as jest.Mock).mockResolvedValue({
        username: 'testuser',
        email: 'test@example.com',
      })

      render(
        <AuthProvider>
          <TestComponent />
        </AuthProvider>
      )

      await waitFor(() => {
        expect(authAPI.getProfile).toHaveBeenCalled()
        expect(screen.getByTestId('user')).toHaveTextContent('testuser')
        expect(screen.getByTestId('loading')).toHaveTextContent('Not Loading')
      })
    })

    it('should not load user if no token exists', async () => {
      render(
        <AuthProvider>
          <TestComponent />
        </AuthProvider>
      )

      await waitFor(() => {
        expect(authAPI.getProfile).not.toHaveBeenCalled()
        expect(screen.getByTestId('user')).toHaveTextContent('No User')
        expect(screen.getByTestId('loading')).toHaveTextContent('Not Loading')
      })
    })

    it('should handle auth check failure', async () => {
      mockLocalStorage['accessToken'] = 'invalid-token'
      ;(authAPI.getProfile as jest.Mock).mockRejectedValue(new Error('Unauthorized'))

      render(
        <AuthProvider>
          <TestComponent />
        </AuthProvider>
      )

      await waitFor(() => {
        expect(mockLocalStorage['accessToken']).toBeUndefined()
        expect(mockLocalStorage['refreshToken']).toBeUndefined()
        expect(screen.getByTestId('user')).toHaveTextContent('No User')
      })
    })
  })

  describe('Login', () => {
    it('should login successfully', async () => {
      const mockResponse = {
        user: { username: 'testuser', email: 'test@example.com' },
        access: 'access-token',
        refresh: 'refresh-token',
      }
      ;(authAPI.login as jest.Mock).mockResolvedValue(mockResponse)

      render(
        <AuthProvider>
          <TestComponent />
        </AuthProvider>
      )

      await waitFor(() => {
        expect(screen.getByTestId('loading')).toHaveTextContent('Not Loading')
      })

      await act(async () => {
        screen.getByText('Login').click()
      })

      await waitFor(() => {
        expect(authAPI.login).toHaveBeenCalledWith({
          username: 'test',
          password: 'pass',
        })
        expect(mockLocalStorage['accessToken']).toBe('access-token')
        expect(mockLocalStorage['refreshToken']).toBe('refresh-token')
        expect(mockPush).toHaveBeenCalledWith('/dashboard')
        expect(screen.getByTestId('user')).toHaveTextContent('testuser')
      })
    })

    it('should handle login failure', async () => {
      const mockError = {
        response: { data: { error: 'Invalid credentials' } },
      }
      ;(authAPI.login as jest.Mock).mockRejectedValue(mockError)

      render(
        <AuthProvider>
          <TestComponent />
        </AuthProvider>
      )

      await waitFor(() => {
        expect(screen.getByTestId('loading')).toHaveTextContent('Not Loading')
      })

      await expect(async () => {
        await act(async () => {
          screen.getByText('Login').click()
        })
      }).rejects.toThrow('Invalid credentials')
    })
  })

  describe('Register', () => {
    it('should register successfully', async () => {
      const mockResponse = {
        user: { username: 'newuser', email: 'new@example.com' },
        access: 'access-token',
        refresh: 'refresh-token',
      }
      ;(authAPI.register as jest.Mock).mockResolvedValue(mockResponse)

      render(
        <AuthProvider>
          <TestComponent />
        </AuthProvider>
      )

      await waitFor(() => {
        expect(screen.getByTestId('loading')).toHaveTextContent('Not Loading')
      })

      await act(async () => {
        screen.getByText('Register').click()
      })

      await waitFor(() => {
        expect(authAPI.register).toHaveBeenCalled()
        expect(mockLocalStorage['accessToken']).toBe('access-token')
        expect(mockLocalStorage['refreshToken']).toBe('refresh-token')
        expect(mockPush).toHaveBeenCalledWith('/dashboard')
        expect(screen.getByTestId('user')).toHaveTextContent('newuser')
      })
    })

    it('should handle registration field errors', async () => {
      const mockError = {
        response: {
          data: {
            username: ['This username is already taken'],
            email: ['Invalid email format'],
          },
        },
      }
      ;(authAPI.register as jest.Mock).mockRejectedValue(mockError)

      render(
        <AuthProvider>
          <TestComponent />
        </AuthProvider>
      )

      await waitFor(() => {
        expect(screen.getByTestId('loading')).toHaveTextContent('Not Loading')
      })

      await expect(async () => {
        await act(async () => {
          screen.getByText('Register').click()
        })
      }).rejects.toThrow()
    })
  })

  describe('Logout', () => {
    it('should logout successfully', async () => {
      mockLocalStorage['accessToken'] = 'test-token'
      mockLocalStorage['refreshToken'] = 'test-refresh'
      ;(authAPI.getProfile as jest.Mock).mockResolvedValue({
        username: 'testuser',
        email: 'test@example.com',
      })

      render(
        <AuthProvider>
          <TestComponent />
        </AuthProvider>
      )

      await waitFor(() => {
        expect(screen.getByTestId('user')).toHaveTextContent('testuser')
      })

      await act(async () => {
        screen.getByText('Logout').click()
      })

      expect(mockLocalStorage['accessToken']).toBeUndefined()
      expect(mockLocalStorage['refreshToken']).toBeUndefined()
      expect(mockPush).toHaveBeenCalledWith('/login')
      expect(screen.getByTestId('user')).toHaveTextContent('No User')
    })
  })

  describe('Update Profile', () => {
    it('should update profile successfully', async () => {
      mockLocalStorage['accessToken'] = 'test-token'
      ;(authAPI.getProfile as jest.Mock).mockResolvedValue({
        username: 'testuser',
        email: 'test@example.com',
      })
      ;(authAPI.updateProfile as jest.Mock).mockResolvedValue({
        username: 'testuser',
        email: 'test@example.com',
        first_name: 'John',
      })

      render(
        <AuthProvider>
          <TestComponent />
        </AuthProvider>
      )

      await waitFor(() => {
        expect(screen.getByTestId('user')).toHaveTextContent('testuser')
      })

      await act(async () => {
        screen.getByText('Update Profile').click()
      })

      await waitFor(() => {
        expect(authAPI.updateProfile).toHaveBeenCalledWith({ first_name: 'John' })
      })
    })

    it('should handle profile update failure', async () => {
      mockLocalStorage['accessToken'] = 'test-token'
      ;(authAPI.getProfile as jest.Mock).mockResolvedValue({
        username: 'testuser',
        email: 'test@example.com',
      })
      ;(authAPI.updateProfile as jest.Mock).mockRejectedValue(
        new Error('Update failed')
      )

      render(
        <AuthProvider>
          <TestComponent />
        </AuthProvider>
      )

      await waitFor(() => {
        expect(screen.getByTestId('user')).toHaveTextContent('testuser')
      })

      await expect(async () => {
        await act(async () => {
          screen.getByText('Update Profile').click()
        })
      }).rejects.toThrow()
    })
  })

  describe('useAuth hook', () => {
    it('should throw error when used outside AuthProvider', () => {
      // Suppress console.error for this test
      const consoleSpy = jest.spyOn(console, 'error').mockImplementation()

      expect(() => {
        render(<TestComponent />)
      }).toThrow('useAuth must be used within an AuthProvider')

      consoleSpy.mockRestore()
    })
  })
})
