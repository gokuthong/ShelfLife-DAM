/**
 * Tests for API utils and interceptors
 */
import axios from 'axios'
import MockAdapter from 'axios-mock-adapter'
import api, { authAPI, assetsAPI, activityAPI, usersAPI } from './api'

// Create mock axios adapter
const mock = new MockAdapter(axios)

describe('API Utils', () => {
  let mockLocalStorage: { [key: string]: string }

  beforeEach(() => {
    // Reset mock
    mock.reset()

    // Mock localStorage
    mockLocalStorage = {}
    Storage.prototype.getItem = jest.fn((key) => mockLocalStorage[key] || null)
    Storage.prototype.setItem = jest.fn((key, value) => {
      mockLocalStorage[key] = value
    })
    Storage.prototype.removeItem = jest.fn((key) => {
      delete mockLocalStorage[key]
    })
  })

  afterEach(() => {
    jest.clearAllMocks()
  })

  describe('Request Interceptor', () => {
    it('should add authorization header when token exists', async () => {
      mockLocalStorage['accessToken'] = 'test-token'

      mock.onGet('/test').reply(200, { success: true })

      const response = await api.get('/test')

      expect(response.config.headers?.Authorization).toBe('Bearer test-token')
    })

    it('should not add authorization header when token does not exist', async () => {
      mock.onGet('/test').reply(200, { success: true })

      const response = await api.get('/test')

      expect(response.config.headers?.Authorization).toBeUndefined()
    })
  })

  describe('Response Interceptor - Token Refresh', () => {
    it('should refresh token on 401 error', async () => {
      mockLocalStorage['accessToken'] = 'old-token'
      mockLocalStorage['refreshToken'] = 'refresh-token'

      // First request fails with 401
      mock.onGet('/test').replyOnce(401)

      // Token refresh succeeds
      mock.onPost('/auth/token/refresh/').reply(200, { access: 'new-token' })

      // Retry request succeeds
      mock.onGet('/test').replyOnce(200, { success: true })

      const response = await api.get('/test')

      expect(mockLocalStorage['accessToken']).toBe('new-token')
      expect(response.data).toEqual({ success: true })
    })

    it('should redirect to login if refresh fails', async () => {
      mockLocalStorage['accessToken'] = 'old-token'
      mockLocalStorage['refreshToken'] = 'invalid-refresh'

      // Mock window.location.href
      delete (window as any).location
      ;(window as any).location = { href: '' }

      // First request fails with 401
      mock.onGet('/test').replyOnce(401)

      // Token refresh fails
      mock.onPost('/auth/token/refresh/').reply(401)

      try {
        await api.get('/test')
      } catch (error) {
        // Should redirect to login
        expect(window.location.href).toBe('/login')
        expect(mockLocalStorage['accessToken']).toBeUndefined()
        expect(mockLocalStorage['refreshToken']).toBeUndefined()
      }
    })

    it('should not retry if request already retried', async () => {
      mockLocalStorage['accessToken'] = 'token'
      mockLocalStorage['refreshToken'] = 'refresh'

      // Both requests fail with 401
      mock.onGet('/test').reply(401)
      mock.onPost('/auth/token/refresh/').reply(200, { access: 'new-token' })

      try {
        await api.get('/test')
      } catch (error) {
        // Should fail after one retry
        expect(mock.history.get.length).toBeLessThanOrEqual(2)
      }
    })
  })

  describe('authAPI', () => {
    it('should login successfully', async () => {
      const loginData = { username: 'testuser', password: 'password123' }
      const mockResponse = { user: { username: 'testuser' }, access: 'token', refresh: 'refresh' }

      mock.onPost('/auth/login/').reply(200, mockResponse)

      const result = await authAPI.login(loginData)

      expect(result).toEqual(mockResponse)
    })

    it('should register successfully', async () => {
      const registerData = {
        username: 'newuser',
        email: 'new@example.com',
        password: 'password123',
        password2: 'password123',
      }
      const mockResponse = { user: { username: 'newuser' }, access: 'token', refresh: 'refresh' }

      mock.onPost('/auth/register/').reply(200, mockResponse)

      const result = await authAPI.register(registerData)

      expect(result).toEqual(mockResponse)
    })

    it('should get profile', async () => {
      mockLocalStorage['accessToken'] = 'token'
      const mockUser = { username: 'testuser', email: 'test@example.com' }

      mock.onGet('/auth/profile/').reply(200, mockUser)

      const result = await authAPI.getProfile()

      expect(result).toEqual(mockUser)
    })

    it('should update profile', async () => {
      mockLocalStorage['accessToken'] = 'token'
      const updateData = { first_name: 'John', last_name: 'Doe' }
      const mockResponse = { username: 'testuser', ...updateData }

      mock.onPut('/auth/profile/').reply(200, mockResponse)

      const result = await authAPI.updateProfile(updateData)

      expect(result).toEqual(mockResponse)
    })

    it('should change password', async () => {
      mockLocalStorage['accessToken'] = 'token'
      const passwordData = {
        old_password: 'oldpass',
        new_password: 'newpass',
        new_password2: 'newpass',
      }

      mock.onPost('/auth/profile/change-password/').reply(200, { message: 'Password updated' })

      const result = await authAPI.changePassword(passwordData)

      expect(result).toEqual({ message: 'Password updated' })
    })

    it('should get all users', async () => {
      mockLocalStorage['accessToken'] = 'admin-token'
      const mockUsers = [{ id: 1, username: 'user1' }, { id: 2, username: 'user2' }]

      mock.onGet('/auth/users/').reply(200, mockUsers)

      const result = await authAPI.getAllUsers()

      expect(result).toEqual(mockUsers)
    })

    it('should delete user', async () => {
      mockLocalStorage['accessToken'] = 'admin-token'

      mock.onDelete('/auth/users/1/').reply(204)

      await authAPI.deleteUser(1)

      expect(mock.history.delete.length).toBe(1)
    })
  })

  describe('assetsAPI', () => {
    beforeEach(() => {
      mockLocalStorage['accessToken'] = 'token'
    })

    it('should list assets', async () => {
      const mockAssets = {
        results: [{ asset_id: '1', title: 'Asset 1' }],
        count: 1,
      }

      mock.onGet('/assets/assets/').reply(200, mockAssets)

      const result = await assetsAPI.list()

      expect(result).toEqual(mockAssets)
    })

    it('should list assets with params', async () => {
      const mockAssets = { results: [], count: 0 }

      mock.onGet('/assets/assets/').reply(200, mockAssets)

      await assetsAPI.list({ file_type: 'image', search: 'test' })

      expect(mock.history.get[0].params).toEqual({ file_type: 'image', search: 'test' })
    })

    it('should get single asset', async () => {
      const mockAsset = { asset_id: '123', title: 'Test Asset' }

      mock.onGet('/assets/assets/123/').reply(200, mockAsset)

      const result = await assetsAPI.get('123')

      expect(result).toEqual(mockAsset)
    })

    it('should create asset', async () => {
      const formData = new FormData()
      formData.append('title', 'New Asset')
      const mockAsset = { asset_id: '456', title: 'New Asset' }

      mock.onPost('/assets/assets/').reply(200, mockAsset)

      const result = await assetsAPI.create(formData)

      expect(result).toEqual(mockAsset)
    })

    it('should update asset', async () => {
      const updateData = { title: 'Updated Title' }
      const mockAsset = { asset_id: '123', title: 'Updated Title' }

      mock.onPatch('/assets/assets/123/').reply(200, mockAsset)

      const result = await assetsAPI.update('123', updateData)

      expect(result).toEqual(mockAsset)
    })

    it('should delete asset', async () => {
      mock.onDelete('/assets/assets/123/').reply(204)

      await assetsAPI.delete('123')

      expect(mock.history.delete.length).toBe(1)
    })

    it('should upload asset', async () => {
      const formData = new FormData()
      const mockAsset = { asset_id: '789', title: 'Uploaded Asset' }

      mock.onPost('/assets/upload/').reply(200, mockAsset)

      const result = await assetsAPI.upload(formData)

      expect(result).toEqual(mockAsset)
    })

    it('should search assets', async () => {
      const mockAssets = [{ asset_id: '1', title: 'Found Asset' }]

      mock.onGet('/assets/search/').reply(200, mockAssets)

      const result = await assetsAPI.search({ q: 'found' })

      expect(result).toEqual(mockAssets)
      expect(mock.history.get[0].params).toEqual({ q: 'found' })
    })
  })

  describe('activityAPI', () => {
    beforeEach(() => {
      mockLocalStorage['accessToken'] = 'token'
    })

    it('should get activity logs', async () => {
      const mockLogs = {
        results: [{ id: '1', action: 'upload' }],
        count: 1,
      }

      mock.onGet('/activity/logs/').reply(200, mockLogs)

      const result = await activityAPI.getLogs()

      expect(result).toEqual(mockLogs)
    })

    it('should get recent activity', async () => {
      const mockActivity = [{ id: '1', action: 'edit' }]

      mock.onGet('/activity/recent/').reply(200, mockActivity)

      const result = await activityAPI.getRecent(5)

      expect(result).toEqual(mockActivity)
      expect(mock.history.get[0].params).toEqual({ limit: 5 })
    })

    it('should get comments for an asset', async () => {
      const mockComments = { results: [{ id: '1', content: 'Great!' }] }

      mock.onGet('/activity/comments/').reply(200, mockComments)

      const result = await activityAPI.getComments('asset-123')

      expect(result).toEqual(mockComments.results)
    })

    it('should create comment', async () => {
      const mockComment = { id: '2', content: 'New comment', asset: 'asset-123' }

      mock.onPost('/activity/comments/').reply(200, mockComment)

      const result = await activityAPI.createComment('asset-123', 'New comment')

      expect(result).toEqual(mockComment)
    })

    it('should delete comment', async () => {
      mock.onDelete('/activity/comments/1/').reply(204)

      await activityAPI.deleteComment('1')

      expect(mock.history.delete.length).toBe(1)
    })
  })

  describe('usersAPI', () => {
    beforeEach(() => {
      mockLocalStorage['accessToken'] = 'admin-token'
    })

    it('should list users', async () => {
      const mockUsers = [{ id: 1, username: 'user1' }]

      mock.onGet('/auth/users/').reply(200, mockUsers)

      const result = await usersAPI.list()

      expect(result).toEqual(mockUsers)
    })

    it('should get user by id', async () => {
      const mockUser = { id: 1, username: 'user1' }

      mock.onGet('/auth/users/1/').reply(200, mockUser)

      const result = await usersAPI.get(1)

      expect(result).toEqual(mockUser)
    })

    it('should update user', async () => {
      const updateData = { role: 'editor' }
      const mockUser = { id: 1, username: 'user1', role: 'editor' }

      mock.onPut('/auth/users/1/').reply(200, mockUser)

      const result = await usersAPI.update(1, updateData)

      expect(result).toEqual(mockUser)
    })

    it('should delete user', async () => {
      mock.onDelete('/auth/users/1/').reply(204)

      await usersAPI.delete(1)

      expect(mock.history.delete.length).toBe(1)
    })
  })
})
