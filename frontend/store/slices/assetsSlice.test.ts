/**
 * Tests for Assets Redux Slice
 */
import assetsReducer, {
  fetchAssets,
  fetchAssetById,
  deleteAsset,
  setSearchQuery,
  setFilters,
  setCurrentPage,
  clearCurrentAsset,
  clearError,
} from './assetsSlice'
import { configureStore } from '@reduxjs/toolkit'

// Mock fetch
global.fetch = jest.fn()

describe('assetsSlice', () => {
  let store: any

  beforeEach(() => {
    store = configureStore({
      reducer: {
        assets: assetsReducer,
      },
    })
    ;(fetch as jest.Mock).mockClear()
    localStorage.clear()
    localStorage.setItem('token', 'test-token')
  })

  describe('Initial State', () => {
    it('should have correct initial state', () => {
      const state = store.getState().assets
      expect(state).toEqual({
        assets: [],
        currentAsset: null,
        isLoading: false,
        error: null,
        totalCount: 0,
        currentPage: 1,
        pageSize: 20,
        searchQuery: '',
        filters: {},
      })
    })
  })

  describe('Reducers', () => {
    it('should handle setSearchQuery', () => {
      store.dispatch(setSearchQuery('test query'))
      const state = store.getState().assets

      expect(state.searchQuery).toBe('test query')
      expect(state.currentPage).toBe(1) // Should reset to page 1
    })

    it('should handle setFilters', () => {
      const filters = { fileType: 'image', tags: ['test'] }
      store.dispatch(setFilters(filters))
      const state = store.getState().assets

      expect(state.filters).toEqual(filters)
      expect(state.currentPage).toBe(1) // Should reset to page 1
    })

    it('should handle setCurrentPage', () => {
      store.dispatch(setCurrentPage(3))
      const state = store.getState().assets

      expect(state.currentPage).toBe(3)
    })

    it('should handle clearCurrentAsset', () => {
      // Set a current asset first
      store.dispatch({ type: 'assets/fetchAssetById/fulfilled', payload: { asset_id: '123', title: 'Test' } })

      store.dispatch(clearCurrentAsset())
      const state = store.getState().assets

      expect(state.currentAsset).toBeNull()
    })

    it('should handle clearError', () => {
      // Set error first
      store.dispatch({ type: 'assets/fetchAssets/rejected', payload: 'Error message' })

      store.dispatch(clearError())
      const state = store.getState().assets

      expect(state.error).toBeNull()
    })
  })

  describe('fetchAssets thunk', () => {
    it('should fetch assets successfully', async () => {
      const mockAssets = {
        results: [
          { asset_id: '1', title: 'Asset 1' },
          { asset_id: '2', title: 'Asset 2' },
        ],
        count: 2,
      }

      ;(fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: async () => mockAssets,
      })

      await store.dispatch(fetchAssets({ page: 1, pageSize: 20 }))

      const state = store.getState().assets
      expect(state.isLoading).toBe(false)
      expect(state.assets).toEqual(mockAssets.results)
      expect(state.totalCount).toBe(2)
      expect(state.error).toBeNull()
    })

    it('should handle fetch with search query', async () => {
      const mockAssets = {
        results: [{ asset_id: '1', title: 'Searched Asset' }],
        count: 1,
      }

      ;(fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: async () => mockAssets,
      })

      await store.dispatch(fetchAssets({ search: 'searched', page: 1, pageSize: 20 }))

      expect(fetch).toHaveBeenCalledWith(
        expect.stringContaining('search=searched'),
        expect.any(Object)
      )

      const state = store.getState().assets
      expect(state.assets).toHaveLength(1)
    })

    it('should handle fetch with filters', async () => {
      const mockAssets = { results: [], count: 0 }

      ;(fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: async () => mockAssets,
      })

      await store.dispatch(
        fetchAssets({
          page: 1,
          pageSize: 20,
          filters: { fileType: 'image' },
        })
      )

      expect(fetch).toHaveBeenCalledWith(
        expect.stringContaining('fileType=image'),
        expect.any(Object)
      )
    })

    it('should handle missing token', async () => {
      localStorage.removeItem('token')

      await store.dispatch(fetchAssets({ page: 1, pageSize: 20 }))

      const state = store.getState().assets
      expect(state.isLoading).toBe(false)
      expect(state.error).toBe('No authentication token')
    })

    it('should handle fetch failure', async () => {
      ;(fetch as jest.Mock).mockResolvedValueOnce({
        ok: false,
      })

      await store.dispatch(fetchAssets({ page: 1, pageSize: 20 }))

      const state = store.getState().assets
      expect(state.isLoading).toBe(false)
      expect(state.error).toBe('Failed to fetch assets')
    })

    it('should handle network error', async () => {
      ;(fetch as jest.Mock).mockRejectedValueOnce(new Error('Network error'))

      await store.dispatch(fetchAssets({ page: 1, pageSize: 20 }))

      const state = store.getState().assets
      expect(state.error).toBe('Network error. Please try again.')
    })

    it('should set loading state while fetching', () => {
      ;(fetch as jest.Mock).mockImplementation(
        () => new Promise(resolve => setTimeout(resolve, 1000))
      )

      store.dispatch(fetchAssets({ page: 1, pageSize: 20 }))

      const state = store.getState().assets
      expect(state.isLoading).toBe(true)
      expect(state.error).toBeNull()
    })
  })

  describe('fetchAssetById thunk', () => {
    it('should fetch single asset successfully', async () => {
      const mockAsset = {
        asset_id: '123',
        title: 'Test Asset',
        description: 'Test description',
      }

      ;(fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: async () => mockAsset,
      })

      await store.dispatch(fetchAssetById('123'))

      const state = store.getState().assets
      expect(state.isLoading).toBe(false)
      expect(state.currentAsset).toEqual(mockAsset)
      expect(state.error).toBeNull()
    })

    it('should handle missing token', async () => {
      localStorage.removeItem('token')

      await store.dispatch(fetchAssetById('123'))

      const state = store.getState().assets
      expect(state.error).toBe('No authentication token')
    })

    it('should handle fetch failure', async () => {
      ;(fetch as jest.Mock).mockResolvedValueOnce({
        ok: false,
      })

      await store.dispatch(fetchAssetById('123'))

      const state = store.getState().assets
      expect(state.error).toBe('Failed to fetch asset')
    })

    it('should handle network error', async () => {
      ;(fetch as jest.Mock).mockRejectedValueOnce(new Error('Network error'))

      await store.dispatch(fetchAssetById('123'))

      const state = store.getState().assets
      expect(state.error).toBe('Network error. Please try again.')
    })
  })

  describe('deleteAsset thunk', () => {
    it('should delete asset successfully', async () => {
      // Set initial state with assets
      store.dispatch({
        type: 'assets/fetchAssets/fulfilled',
        payload: {
          results: [
            { asset_id: '1', title: 'Asset 1' },
            { asset_id: '2', title: 'Asset 2' },
            { asset_id: '3', title: 'Asset 3' },
          ],
          count: 3,
        },
      })

      ;(fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
      })

      await store.dispatch(deleteAsset('2'))

      const state = store.getState().assets
      expect(state.isLoading).toBe(false)
      expect(state.assets).toHaveLength(2)
      expect(state.assets.find((a: any) => a.asset_id === '2')).toBeUndefined()
      expect(state.error).toBeNull()
    })

    it('should handle missing token', async () => {
      localStorage.removeItem('token')

      await store.dispatch(deleteAsset('123'))

      const state = store.getState().assets
      expect(state.error).toBe('No authentication token')
    })

    it('should handle delete failure', async () => {
      ;(fetch as jest.Mock).mockResolvedValueOnce({
        ok: false,
      })

      await store.dispatch(deleteAsset('123'))

      const state = store.getState().assets
      expect(state.error).toBe('Failed to delete asset')
    })

    it('should handle network error', async () => {
      ;(fetch as jest.Mock).mockRejectedValueOnce(new Error('Network error'))

      await store.dispatch(deleteAsset('123'))

      const state = store.getState().assets
      expect(state.error).toBe('Network error. Please try again.')
    })
  })
})
