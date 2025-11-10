# ShelfLifeDAM - GitHub Workflow & Upload Guide

**IMPORTANT: Read this entire guide before making your final commits!**

Project Timeline: November 1, 2025 - November 11, 2025 (10 Days)
Team Members: BT, WK, ZC

---

## Table of Contents

1. [File Size Issues & Solutions](#file-size-issues--solutions)
2. [Team Collaboration & Branch Strategy](#team-collaboration--branch-strategy)
3. [**CRITICAL: Final Commit Testing Requirements**](#critical-final-commit-testing-requirements)
4. [Git Workflow](#git-workflow)
5. [Commit Guidelines](#commit-guidelines)
6. [Pull Request Process](#pull-request-process)
7. [Troubleshooting](#troubleshooting)

---

## File Size Issues & Solutions

### ⚠️ Problem Identified

Your repository contains large files/folders causing upload failures:
- `.venv/` - Python virtual environment (~150-300 MB)
- `backend/venv/` - Another virtual environment (~150-300 MB)
- `frontend/node_modules/` - Node.js dependencies (~200-500 MB)
- `frontend/.next/` - Next.js build files (~50-100 MB)
- `__pycache__/` - Python bytecode cache
- `backend/media/` - Uploaded media files

**These files are ALREADY TRACKED by Git.** Simply adding them to `.gitignore` won't remove them from Git history.

### ✅ Solution Steps

#### Step 1: Update .gitignore

Ensure your `.gitignore` includes:

```gitignore
# Python
venv/
.venv/
__pycache__/
*.pyc
*.pyo
*.db
*.sqlite3

# Node.js
node_modules/
.next/
dist/
build/

# Media files
backend/media/
media/
*.jpg
*.jpeg
*.png
*.gif
*.mp4
*.avi
*.mov

# Environment
.env
.env.local
.env.development

# IDE
.vscode/
.idea/
*.code-workspace
```

#### Step 2: Remove Large Files from Git Tracking

```bash
cd "C:\Users\ASUS\Downloads\ShelfLifeDAM-main"

# Remove large files from tracking (keeps them on disk)
git rm -r --cached .venv
git rm -r --cached backend/venv
git rm -r --cached frontend/venv
git rm -r --cached frontend/node_modules
git rm -r --cached frontend/.next
git rm -r --cached backend/**/__pycache__
git rm -r --cached backend/media
```

#### Step 3: Commit the Cleanup

```bash
git add .
git commit -m "chore: Remove large files from tracking

- Removed virtual environments from tracking
- Removed node_modules from tracking
- Removed build files (.next) from tracking
- Removed cache files (__pycache__) from tracking
- Removed media files from tracking
- Updated .gitignore"
```

#### Step 4: Push to GitHub

```bash
git push origin main
```

If rejected:
```bash
git push origin main --force
```

**WARNING**: Force push overwrites remote. Use only if necessary.

---

## Team Collaboration & Branch Strategy

### Branch Naming Convention

Format: `feature/<initials>-<feature-name>`

All branches merge into: `main`
Final merge deadline: **November 11, 2025**

---

### BT - Team Member 1

**Assigned Features:**
1. Asset Upload System
2. Activity Logging
3. Profile Management
4. Dark Mode Toggle

#### Branch 1: `feature/bt-asset-upload`
- **Timeline**: November 1-3, 2025 (Days 1-2.5)
- **Files**: AssetUpload.tsx, Asset views/models/serializers
- **Merge By**: November 3, 2025 11:59 PM

#### Branch 2: `feature/bt-activity-log`
- **Timeline**: November 3-6, 2025 (Days 2.5-5)
- **Files**: ActivityLog model/views, Activity page
- **Merge By**: November 6, 2025 11:59 PM

#### Branch 3: `feature/bt-profile-management`
- **Timeline**: November 6-8, 2025 (Days 5-7.5)
- **Files**: Profile page, avatar upload
- **Merge By**: November 8, 2025 11:59 PM

#### Branch 4: `feature/bt-dark-mode` ⚠️ **FINAL COMMIT WITH TESTS**
- **Timeline**: November 8-11, 2025 (Days 7.5-10)
- **Files**: ColorModeContext, dark mode toggle
- **Merge By**: November 11, 2025 11:59 PM
- **⚠️ MUST INCLUDE**: All test files for your modules (see below)

---

### WK - Team Member 2

**Assigned Features:**
1. Authentication (Login)
2. Dashboard
3. Asset Library
4. Asset Details & Viewing

#### Branch 1: `feature/wk-authentication`
- **Timeline**: November 1-3, 2025 (Days 1-2.5)
- **Files**: Login page, AuthContext, JWT setup
- **Merge By**: November 3, 2025 11:59 PM

#### Branch 2: `feature/wk-dashboard`
- **Timeline**: November 3-6, 2025 (Days 2.5-5)
- **Files**: Dashboard page, statistics
- **Merge By**: November 6, 2025 11:59 PM

#### Branch 3: `feature/wk-asset-library`
- **Timeline**: November 6-8, 2025 (Days 5-7.5)
- **Files**: Asset library page, AssetCard
- **Merge By**: November 8, 2025 11:59 PM

#### Branch 4: `feature/wk-asset-details` ⚠️ **FINAL COMMIT WITH TESTS**
- **Timeline**: November 8-11, 2025 (Days 7.5-10)
- **Files**: Asset detail page, BabylonViewer
- **Merge By**: November 11, 2025 11:59 PM
- **⚠️ MUST INCLUDE**: All test files for your modules (see below)

---

### ZC - Team Member 3

**Assigned Features:**
1. User Registration
2. User Management (Admin)
3. Search Functionality
4. Advanced Filters & Role Guards

#### Branch 1: `feature/zc-registration`
- **Timeline**: November 1-3, 2025 (Days 1-2.5)
- **Files**: Registration page, User model
- **Merge By**: November 3, 2025 11:59 PM

#### Branch 2: `feature/zc-user-management`
- **Timeline**: November 3-6, 2025 (Days 2.5-5)
- **Files**: User management page, CRUD endpoints
- **Merge By**: November 6, 2025 11:59 PM

#### Branch 3: `feature/zc-search`
- **Timeline**: November 6-8, 2025 (Days 5-7.5)
- **Files**: Search page, search endpoints
- **Merge By**: November 8, 2025 11:59 PM

#### Branch 4: `feature/zc-advanced-filters` ⚠️ **FINAL COMMIT WITH TESTS**
- **Timeline**: November 8-11, 2025 (Days 7.5-10)
- **Files**: Advanced filters, RoleGuard, Comments
- **Merge By**: November 11, 2025 11:59 PM
- **⚠️ MUST INCLUDE**: All test files for your modules (see below)

---

## CRITICAL: Final Commit Testing Requirements

### ⚠️ MANDATORY FOR FINAL BRANCH (Branch 4)

**Each team member MUST upload comprehensive test files in their FINAL COMMIT (Branch 4) before November 11, 2025.**

This is **NOT OPTIONAL**. Your grade depends on it.

---

### BT - Testing Requirements for Final Commit

**Your Final Commit (Branch 4: `feature/bt-dark-mode`) MUST include:**

#### Backend Tests
Create these files in `backend/activity/`:
- **`test_models.py`** - ActivityLog and Comment model tests
  - Test ActivityLog creation
  - Test activity types (upload, edit, delete, view)
  - Test IP address and user agent capture
  - Test Comment model
  - Test comment creation and deletion
  - Test timestamps

- **`test_views.py`** - Activity API endpoint tests
  - Test activity log retrieval
  - Test filtering by action type
  - Test filtering by user
  - Test comment CRUD operations
  - Test permission checks
  - Test pagination

**Minimum**: 20+ tests, 75% coverage for activity module

#### Frontend Tests
- **`frontend/contexts/ColorModeContext.test.tsx`** - Dark mode tests
  - Test color mode toggle
  - Test localStorage persistence
  - Test initial theme detection
  - Test system preference

- **`frontend/components/Assets/AssetComments.test.tsx`** (if you implemented comments)
  - Test comment display
  - Test comment creation
  - Test comment deletion

**Minimum**: 10+ tests for your frontend features

#### ✅ Final Commit Checklist for BT
- [ ] All activity module tests created
- [ ] Tests run successfully: `cd backend && pytest activity/`
- [ ] Coverage ≥ 75% for activity module
- [ ] Dark mode tests created
- [ ] All tests pass: `npm test`
- [ ] Clear commit message (see below)

---

### WK - Testing Requirements for Final Commit

**Your Final Commit (Branch 4: `feature/wk-asset-details`) MUST include:**

#### Backend Tests
Already created (verify they exist):
- **`backend/users/test_models.py`** ✅ (already created)
- **`backend/users/test_serializers.py`** ✅ (already created)
- **`backend/users/test_views.py`** ✅ (already created)

**Your responsibility**: Verify these tests cover YOUR authentication work:
- Login/logout functionality
- JWT token generation
- Token refresh
- Session management

If missing coverage, add additional tests to these files.

#### Frontend Tests
Create these files:
- **`frontend/app/login/page.test.tsx`** - Login page tests
  - Test form rendering
  - Test form validation
  - Test successful login
  - Test failed login
  - Test redirect to dashboard

- **`frontend/app/dashboard/page.test.tsx`** - Dashboard tests
  - Test statistics display
  - Test role-based content
  - Test quick actions
  - Test loading states

- **`frontend/app/assets/page.test.tsx`** - Asset library tests
  - Test asset grid rendering
  - Test filtering
  - Test sorting
  - Test search integration
  - Test pagination

- **`frontend/app/assets/[id]/page.test.tsx`** - Asset details tests
  - Test asset detail display
  - Test metadata rendering
  - Test edit functionality
  - Test delete confirmation
  - Test permissions

- **`frontend/components/Assets/BabylonViewer.test.tsx`** - 3D viewer tests
  - Test viewer initialization
  - Test file loading
  - Test controls
  - Test error handling

**Minimum**: 30+ frontend tests, 70% coverage

#### ✅ Final Commit Checklist for WK
- [ ] Verify backend tests exist and pass
- [ ] All frontend page tests created
- [ ] BabylonViewer tests created
- [ ] Tests run successfully: `npm test`
- [ ] Coverage ≥ 70% for your features
- [ ] All tests pass
- [ ] Clear commit message (see below)

---

### ZC - Testing Requirements for Final Commit

**Your Final Commit (Branch 4: `feature/zc-advanced-filters`) MUST include:**

#### Backend Tests
Create or enhance these files:

**`backend/users/test_models.py`** (add to existing):
- Test User model fields
- Test role validation
- Test username uniqueness
- Test email validation

**`backend/users/test_views.py`** (add to existing):
- Test registration endpoint
- Test user management endpoints
- Test admin-only permissions
- Test user deletion rules

**`backend/assets/test_views.py`** (add to existing):
- Test search endpoint
- Test filter by file type
- Test filter by date range
- Test filter by tags
- Test combined filters
- Test search with permissions

**Minimum**: Add 15+ tests to existing files

#### Frontend Tests
Create these files:
- **`frontend/app/register/page.test.tsx`** - Registration tests
  - Test form rendering
  - Test form validation
  - Test password confirmation
  - Test successful registration
  - Test error handling
  - Test auto-login after registration

- **`frontend/app/users/page.test.tsx`** - User management tests
  - Test user list display
  - Test edit user modal
  - Test role assignment
  - Test user deletion
  - Test admin-only access
  - Test search/filter

- **`frontend/app/search/page.test.tsx`** - Search tests
  - Test search input
  - Test search results
  - Test advanced filters
  - Test date range filter
  - Test file type filter
  - Test clear filters
  - Test no results state

- **`frontend/components/Auth/RoleGuard.test.tsx`** - RoleGuard tests
  - Test admin access
  - Test editor access
  - Test viewer restrictions
  - Test unauthorized redirect

**Minimum**: 25+ frontend tests, 70% coverage

#### ✅ Final Commit Checklist for ZC
- [ ] All backend test additions completed
- [ ] Tests run successfully: `cd backend && pytest`
- [ ] All frontend tests created
- [ ] Tests run successfully: `npm test`
- [ ] Coverage ≥ 70% for your features
- [ ] All tests pass
- [ ] Clear commit message (see below)

---

### Example Final Commit Message (All Team Members)

```bash
# Stage all your test files
git add backend/activity/test_*.py  # BT
git add frontend/app/*/page.test.tsx  # WK, ZC
git add frontend/components/*/*.test.tsx  # All

# Commit with comprehensive message
git commit -m "test: Add comprehensive tests for [YOUR MODULE] - Final Submission

Team Member: [BT/WK/ZC]
Module: [Your modules]
Branch: feature/[your-branch-4]

Files Added:
Backend Tests:
- [module]/test_models.py: [X] tests
- [module]/test_views.py: [Y] tests
- [module]/test_serializers.py: [Z] tests (if applicable)

Frontend Tests:
- app/[page]/page.test.tsx: [X] tests
- components/[Component]/[Component].test.tsx: [Y] tests

Test Coverage:
- Backend [module]: [X]% coverage
- Frontend [features]: [Y]% coverage
- Total tests: [N] tests
- All tests passing ✓

Test Results:
- Backend: pytest [module]/ -v ✓
- Frontend: npm test ✓

Notes:
- [Any important notes about your tests]
- [Known limitations or areas for future improvement]"

# Push to remote
git push origin feature/[your-branch-4]
```

### Example Specific Commits

**BT's Final Commit:**
```bash
git commit -m "test: Add comprehensive activity and dark mode tests - Final Submission

Team Member: BT
Module: Activity Logging, Dark Mode
Branch: feature/bt-dark-mode

Files Added:
Backend Tests:
- activity/test_models.py: 12 tests (ActivityLog, Comment models)
- activity/test_views.py: 15 tests (Activity API, Comments API)

Frontend Tests:
- contexts/ColorModeContext.test.tsx: 8 tests
- components/Assets/AssetComments.test.tsx: 10 tests

Test Coverage:
- Backend activity module: 82% coverage
- Frontend dark mode: 90% coverage
- Total tests: 45 tests
- All tests passing ✓

Test Results:
- Backend: pytest activity/ -v --cov=activity ✓
- Frontend: npm test ✓"
```

**WK's Final Commit:**
```bash
git commit -m "test: Add authentication, dashboard, and asset tests - Final Submission

Team Member: WK
Module: Authentication, Dashboard, Asset Library, Asset Details
Branch: feature/wk-asset-details

Files Added:
Frontend Tests:
- app/login/page.test.tsx: 8 tests
- app/dashboard/page.test.tsx: 6 tests
- app/assets/page.test.tsx: 10 tests
- app/assets/[id]/page.test.tsx: 12 tests
- components/Assets/BabylonViewer.test.tsx: 7 tests

Test Coverage:
- Authentication flow: 88% coverage
- Dashboard: 75% coverage
- Asset pages: 80% coverage
- Total tests: 43 tests
- All tests passing ✓

Test Results:
- npm test ✓
- Coverage report: coverage/lcov-report/index.html"
```

**ZC's Final Commit:**
```bash
git commit -m "test: Add registration, user management, and search tests - Final Submission

Team Member: ZC
Module: User Registration, User Management, Search, Advanced Filters
Branch: feature/zc-advanced-filters

Files Added:
Backend Tests:
- Added 8 tests to users/test_models.py
- Added 10 tests to users/test_views.py
- Added 12 tests to assets/test_views.py (search/filters)

Frontend Tests:
- app/register/page.test.tsx: 9 tests
- app/users/page.test.tsx: 12 tests
- app/search/page.test.tsx: 15 tests
- components/Auth/RoleGuard.test.tsx: 8 tests

Test Coverage:
- Backend additions: 80% coverage
- Frontend features: 78% coverage
- Total new tests: 74 tests
- All tests passing ✓

Test Results:
- Backend: pytest -v ✓
- Frontend: npm test ✓"
```

---

## Git Workflow

### Daily Workflow

**Start of Day:**
```bash
git checkout main
git pull origin main
git checkout <your-branch>
git merge main
```

**During Development:**
```bash
# Make changes
git add <files>
git commit -m "type: description"
git push origin <your-branch>
```

**Before Merging:**
```bash
git checkout main
git pull origin main
git checkout <your-branch>
git merge main
# Resolve conflicts if any
git push origin <your-branch>
# Create Pull Request on GitHub
```

### Creating Your Branches

**BT:**
```bash
git checkout main
git checkout -b feature/bt-asset-upload
git push -u origin feature/bt-asset-upload

# After merging Branch 1:
git checkout main
git pull
git checkout -b feature/bt-activity-log
# ... and so on
```

**WK:**
```bash
git checkout main
git checkout -b feature/wk-authentication
git push -u origin feature/wk-authentication

# After merging Branch 1:
git checkout main
git pull
git checkout -b feature/wk-dashboard
# ... and so on
```

**ZC:**
```bash
git checkout main
git checkout -b feature/zc-registration
git push -u origin feature/zc-registration

# After merging Branch 1:
git checkout main
git pull
git checkout -b feature/zc-user-management
# ... and so on
```

---

## Commit Guidelines

### Format

```
<type>: <subject>

[optional body]
```

### Types
- `feat`: New feature
- `fix`: Bug fix
- `test`: Adding tests ⚠️ Use this for your final commit!
- `docs`: Documentation
- `refactor`: Code refactoring
- `style`: Formatting
- `chore`: Maintenance

### Examples

```bash
# Feature
git commit -m "feat: implement drag-and-drop file upload"

# Bug fix
git commit -m "fix: resolve login redirect issue"

# Tests (Final commit)
git commit -m "test: Add comprehensive tests for user authentication - Final Submission"
```

---

## Pull Request Process

### Creating a PR

**Title Format**: `[INITIALS] Feature Name - Branch X`

**Description Template**:
```markdown
## Changes Made
- List major changes
- Highlight new features
- Note bug fixes

## Files Modified
- List main files

## Testing
✅ Tests added (if final branch)
- Test coverage: X%
- All tests passing

## Screenshots
[Add if applicable]

## Notes for Reviewers
- Specific review areas
- Known limitations
```

---

## Merge Schedule

| Date | BT | WK | ZC |
|------|----|----|-----|
| **Nov 3** | asset-upload | authentication | registration |
| **Nov 6** | activity-log | dashboard | user-management |
| **Nov 8** | profile-management | asset-library | search |
| **Nov 11** | **dark-mode + TESTS** | **asset-details + TESTS** | **advanced-filters + TESTS** |

⚠️ **November 11 deadline: ALL tests must be included!**

---

## Running Tests

### Before Final Commit - Verify All Tests Pass

**Backend:**
```bash
cd backend

# Install test dependencies (if not installed)
python -m pip install -r requirements-test.txt

# Run all tests
pytest

# Run specific module
pytest activity/ -v
pytest users/ -v

# With coverage
pytest activity/ --cov=activity --cov-report=html
pytest users/ --cov=users --cov-report=term-missing

# Check coverage report
# Open: htmlcov/index.html
```

**Frontend:**
```bash
cd frontend

# Install dependencies (if not installed)
npm install

# Run all tests
npm test

# Run specific test file
npm test -- Login.test.tsx

# With coverage
npm run test:coverage

# Check coverage report
# Open: coverage/lcov-report/index.html
```

---

## Troubleshooting

### Common Errors

**Error: "Large files detected"**
- Solution: Run Step 2 commands to remove from tracking

**Error: "Permission denied"**
```bash
# Check SSH key
ssh -T git@github.com

# Or use HTTPS
git remote set-url origin https://github.com/username/repo.git
```

**Error: "Rejected - non-fast-forward"**
```bash
git pull origin your-branch --rebase
git push origin your-branch
```

**Error: "Failed to push some refs"**
```bash
git pull origin main --rebase
git push origin main
```

**Tests Failing:**
1. Check test file syntax
2. Ensure all dependencies installed
3. Check Django settings for tests
4. Review error messages carefully

---

## Final Submission Checklist (All Team Members)

### Before November 11, 2025 11:59 PM

- [ ] All 4 branches created and merged
- [ ] Branch 4 includes ALL required test files
- [ ] All tests pass locally
  - [ ] Backend: `pytest`
  - [ ] Frontend: `npm test`
- [ ] Coverage meets minimum (70-75%)
- [ ] Test files follow naming convention
- [ ] Commit message is clear and detailed
- [ ] Code is clean (no console.log, commented code)
- [ ] Pull request created with proper description
- [ ] No merge conflicts
- [ ] Large files removed from tracking
- [ ] .gitignore properly configured

---

## Important Notes

### DO ✅
- Commit often with clear messages
- Test before committing
- Pull before pushing
- Create feature branches
- Review changes before committing
- **Upload test files in final commit**
- Ask for help if stuck

### DON'T ❌
- Commit directly to main
- Push broken code
- Commit sensitive data
- Force push to shared branches
- **Forget to add tests in final commit**
- Skip testing before pushing

---

## Resources

- **Testing Guide**: [TESTING.md](./TESTING.md)
- **Test Files Index**: [TEST_FILES_INDEX.md](./TEST_FILES_INDEX.md)
- [Git Documentation](https://git-scm.com/doc)
- [GitHub Guides](https://guides.github.com/)
- [Conventional Commits](https://www.conventionalcommits.org/)

---

## Team Contacts

- **BT**: [Contact info]
- **WK**: [Contact info]
- **ZC**: [Contact info]

---

## Support

If issues arise:
1. Check this guide
2. Check TESTING.md for testing questions
3. Run `git status` to see current state
4. Ask team members
5. Create GitHub issue

---

**REMEMBER: Your final commit (Branch 4) on November 11, 2025 MUST include comprehensive tests for your modules. This is MANDATORY and affects your grade!**

---

Last Updated: November 9, 2025
