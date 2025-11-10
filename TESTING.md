# Testing Guide for ShelfLifeDAM

This document provides comprehensive information about testing in the ShelfLifeDAM project.

## Table of Contents

- [Overview](#overview)
- [Backend Testing](#backend-testing)
- [Frontend Testing](#frontend-testing)
- [Running Tests](#running-tests)
- [Test Coverage](#test-coverage)
- [Team Member Responsibilities](#team-member-responsibilities)
- [Best Practices](#best-practices)

## Overview

ShelfLifeDAM uses comprehensive testing to ensure code quality and reliability:

- **Backend**: pytest with Django integration
- **Frontend**: Jest with React Testing Library
- **Coverage Goals**: Aim for 80%+ code coverage

## Backend Testing

### Setup

1. Install test dependencies:
```bash
cd backend
pip install -r requirements-test.txt
```

2. Configure pytest (already configured in `pytest.ini`)

### Test Structure

Backend tests are organized by module:

```
backend/
├── users/
│   ├── test_models.py      # User model tests
│   ├── test_serializers.py # Serializer tests
│   └── test_views.py        # API endpoint tests
└── assets/
    ├── test_models.py      # Asset, Metadata, Version model tests
    └── test_views.py        # Asset API tests
```

### Running Backend Tests

```bash
# Run all tests
cd backend
pytest

# Run specific test file
pytest users/test_models.py

# Run with coverage
pytest --cov=. --cov-report=html

# Run tests with verbose output
pytest -v

# Run specific test
pytest users/test_models.py::TestUserModel::test_create_user
```

### Backend Test Coverage

The backend tests cover:

#### Users Module
- ✅ User model creation and properties
- ✅ Role-based permissions (admin, editor, viewer)
- ✅ User registration and validation
- ✅ Login/logout functionality
- ✅ Password change
- ✅ Profile management
- ✅ Admin user management
- ✅ Permission checks

#### Assets Module
- ✅ Asset CRUD operations
- ✅ File type detection
- ✅ File upload handling
- ✅ Asset versioning
- ✅ Metadata management
- ✅ Search and filtering
- ✅ Role-based asset access
- ✅ Permissions (IsOwnerOrAdmin, IsEditorOrAdmin)

## Frontend Testing

### Setup

1. Install dependencies:
```bash
cd frontend
npm install
```

2. Jest configuration is in `jest.config.js` and `jest.setup.js`

### Test Structure

Frontend tests are co-located with source files:

```
frontend/
├── contexts/
│   ├── AuthContext.tsx
│   └── AuthContext.test.tsx
├── store/
│   └── slices/
│       ├── authSlice.ts
│       ├── authSlice.test.ts
│       ├── assetsSlice.ts
│       └── assetsSlice.test.ts
└── utils/
    ├── api.ts
    └── api.test.ts
```

### Running Frontend Tests

```bash
# Run all tests
cd frontend
npm test

# Run tests in watch mode
npm run test:watch

# Run with coverage
npm run test:coverage

# Run specific test file
npm test -- AuthContext.test.tsx

# Update snapshots
npm test -- -u
```

### Frontend Test Coverage

The frontend tests cover:

#### Authentication
- ✅ AuthContext provider and hooks
- ✅ Login/logout flow
- ✅ Registration
- ✅ Profile updates
- ✅ Token management
- ✅ Auth state management (Redux)

#### Assets Management
- ✅ Assets Redux slice
- ✅ Fetch assets with pagination
- ✅ Search and filtering
- ✅ Asset CRUD operations
- ✅ Delete assets

#### API Integration
- ✅ Axios interceptors
- ✅ Token refresh mechanism
- ✅ Auth API endpoints
- ✅ Assets API endpoints
- ✅ Activity API endpoints
- ✅ Users API endpoints
- ✅ Error handling

## Test Coverage

### Viewing Coverage Reports

#### Backend
```bash
cd backend
pytest --cov=. --cov-report=html
# Open htmlcov/index.html in your browser
```

#### Frontend
```bash
cd frontend
npm run test:coverage
# Open coverage/lcov-report/index.html in your browser
```

### Coverage Goals

- **Overall**: 80%+ coverage
- **Critical paths** (auth, asset upload, permissions): 90%+ coverage
- **New features**: Must include tests before merging

## Team Member Responsibilities

### Last Commit Requirements (Final Stretch)

**IMPORTANT**: Each team member must upload testing files for their own code sections in their **last commit** before the final deadline.

#### Assignment by Module

| Team Member | Responsibility | Test Files to Create |
|------------|---------------|---------------------|
| **Backend - Users** | User authentication, registration, profile management | `users/test_*.py` - Already created |
| **Backend - Assets** | Asset management, file uploads, versioning | `assets/test_*.py` - Already created |
| **Backend - Activity** | Activity logging, comments | `activity/test_*.py` - To be created |
| **Frontend - Auth** | Login/register UI, AuthContext | `contexts/AuthContext.test.tsx` - Already created |
| **Frontend - Assets** | Asset listing, upload UI, Redux state | `store/slices/*.test.ts` - Already created |
| **Frontend - Components** | UI components, pages | `components/**/*.test.tsx` - To be created |

### Testing Checklist for Last Commit

Before your final commit, ensure:

- [ ] All test files for your module are created
- [ ] Tests pass locally (`pytest` or `npm test`)
- [ ] Coverage is at least 70% for your module
- [ ] Tests cover:
  - [ ] Happy path (normal functionality)
  - [ ] Error cases
  - [ ] Edge cases
  - [ ] Permission checks (if applicable)
- [ ] Test file naming follows convention:
  - Backend: `test_*.py` or `*_test.py`
  - Frontend: `*.test.tsx` or `*.test.ts`
- [ ] All tests include docstrings/comments explaining what they test
- [ ] CI/CD tests pass (if configured)

### Git Commit Message for Tests

Use clear commit messages:
```bash
git add users/test_*.py
git commit -m "test: Add comprehensive tests for user authentication module"

git add assets/test_*.py
git commit -m "test: Add tests for asset CRUD and permissions"

git add frontend/contexts/AuthContext.test.tsx
git commit -m "test: Add tests for AuthContext and authentication flow"
```

## Best Practices

### General

1. **Test Naming**: Use descriptive names that explain what is being tested
   ```python
   # Good
   def test_admin_can_delete_user():

   # Bad
   def test_delete():
   ```

2. **Arrange-Act-Assert**: Structure tests clearly
   ```python
   def test_create_asset():
       # Arrange
       user = create_test_user()
       file = create_test_file()

       # Act
       asset = Asset.objects.create(user=user, file=file, title="Test")

       # Assert
       assert asset.title == "Test"
       assert asset.user == user
   ```

3. **Use Fixtures**: Reuse common test data
   ```python
   @pytest.fixture
   def admin_user():
       return User.objects.create_user(
           username='admin',
           password='pass123',
           role='admin'
       )
   ```

4. **Test Isolation**: Each test should be independent
   - Use database transactions/rollback
   - Clean up after tests
   - Don't rely on test execution order

5. **Mock External Dependencies**:
   ```python
   # Mock API calls
   @patch('requests.get')
   def test_api_call(mock_get):
       mock_get.return_value.json.return_value = {'data': 'test'}
       # ... test code
   ```

### Backend-Specific

1. **Use `@pytest.mark.django_db`** for tests that access the database
2. **Test permissions thoroughly** - users, editors, admins
3. **Test serializer validation**
4. **Test API status codes**
5. **Use `APIClient` for API tests**

### Frontend-Specific

1. **Use React Testing Library** queries (not enzyme)
2. **Test user interactions** with `userEvent`
3. **Wait for async operations** with `waitFor`
4. **Mock API calls** to avoid real network requests
5. **Test error states** and loading states
6. **Don't test implementation details**

### What NOT to Test

- Third-party library code
- Django/React framework internals
- Simple getters/setters without logic
- Exact HTML structure (test behavior instead)

## Continuous Integration

Tests should run automatically on:

- Every pull request
- Before merging to main branch
- Before deployment

Example GitHub Actions workflow:
```yaml
name: Tests
on: [push, pull_request]
jobs:
  backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run tests
        run: |
          cd backend
          pip install -r requirements.txt -r requirements-test.txt
          pytest --cov

  frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run tests
        run: |
          cd frontend
          npm install
          npm test
```

## Troubleshooting

### Backend

**Issue**: `ImportError` when running tests
- **Solution**: Ensure you're in the backend directory and virtual environment is activated

**Issue**: Database errors
- **Solution**: Tests use a separate test database. Check `pytest.ini` configuration

**Issue**: Tests pass locally but fail in CI
- **Solution**: Check for environment-specific issues (paths, env variables)

### Frontend

**Issue**: `Cannot find module` errors
- **Solution**: Check `jest.config.js` module name mapper configuration

**Issue**: Tests timeout
- **Solution**: Increase timeout or check for missing `await` in async tests

**Issue**: `localStorage is not defined`
- **Solution**: Check `jest.setup.js` has localStorage mock

## Resources

- [pytest Documentation](https://docs.pytest.org/)
- [Django Testing Guide](https://docs.djangoproject.com/en/stable/topics/testing/)
- [React Testing Library](https://testing-library.com/react)
- [Jest Documentation](https://jestjs.io/docs/getting-started)

## Questions?

If you have questions about testing:
1. Check this guide first
2. Review existing test files for examples
3. Ask team members who've completed their tests
4. Consult the official documentation linked above

---

**Remember**: Testing is not optional. Your last commit MUST include tests for your code sections!
