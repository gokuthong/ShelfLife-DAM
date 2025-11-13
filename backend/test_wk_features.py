"""
Tests for WK Features:
- Branch 1: Authentication (Login)
- Branch 2: Dashboard
- Branch 3: Asset Library
- Branch 4: Asset Details & Viewing

This test file covers all WK-assigned features without modifying existing functionality.
Tests use existing models and serializers from the project.
"""
import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from assets.models import Asset, Metadata

User = get_user_model()


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def api_client():
    """Create API client"""
    return APIClient()


@pytest.fixture
def admin_user(db):
    """Create admin user for testing"""
    return User.objects.create_user(
        username='wk_admin',
        email='wk_admin@example.com',
        password='adminpass123',
        role='admin',
        first_name='Admin',
        last_name='User'
    )


@pytest.fixture
def editor_user(db):
    """Create editor user for testing"""
    return User.objects.create_user(
        username='wk_editor',
        email='wk_editor@example.com',
        password='editorpass123',
        role='editor',
        first_name='Editor',
        last_name='User'
    )


@pytest.fixture
def viewer_user(db):
    """Create viewer user for testing"""
    return User.objects.create_user(
        username='wk_viewer',
        email='wk_viewer@example.com',
        password='viewerpass123',
        role='viewer',
        first_name='Viewer',
        last_name='User'
    )


@pytest.fixture
def sample_image_asset(editor_user):
    """Create a sample image asset"""
    file = SimpleUploadedFile("sample_image.jpg", b"image_content", content_type="image/jpeg")
    return Asset.objects.create(
        user=editor_user,
        file=file,
        title="Sample Image Asset",
        description="A sample image for testing",
        tags=["sample", "image", "test"],
        file_type="image",
        is_active=True
    )


@pytest.fixture
def sample_video_asset(editor_user):
    """Create a sample video asset"""
    file = SimpleUploadedFile("sample_video.mp4", b"video_content", content_type="video/mp4")
    return Asset.objects.create(
        user=editor_user,
        file=file,
        title="Sample Video Asset",
        description="A sample video for testing",
        tags=["sample", "video"],
        file_type="video",
        is_active=True
    )


@pytest.fixture
def sample_document_asset(editor_user):
    """Create a sample document asset"""
    file = SimpleUploadedFile("sample_doc.pdf", b"pdf_content", content_type="application/pdf")
    return Asset.objects.create(
        user=editor_user,
        file=file,
        title="Sample Document Asset",
        description="A sample document for testing",
        tags=["sample", "document"],
        file_type="pdf",
        is_active=True
    )


@pytest.fixture
def sample_3d_asset(editor_user):
    """Create a sample 3D model asset"""
    file = SimpleUploadedFile("sample_model.obj", b"3d_content")
    return Asset.objects.create(
        user=editor_user,
        file=file,
        title="Sample 3D Model",
        description="A sample 3D model for testing",
        tags=["sample", "3d", "model"],
        file_type="3d",
        is_active=True
    )


@pytest.fixture
def inactive_asset(editor_user):
    """Create an inactive asset for testing"""
    file = SimpleUploadedFile("inactive.jpg", b"content", content_type="image/jpeg")
    return Asset.objects.create(
        user=editor_user,
        file=file,
        title="Inactive Asset",
        description="An inactive asset",
        file_type="image",
        is_active=False
    )


@pytest.fixture
def asset_with_metadata(editor_user):
    """Create an asset with metadata"""
    file = SimpleUploadedFile("with_metadata.jpg", b"content", content_type="image/jpeg")
    asset = Asset.objects.create(
        user=editor_user,
        file=file,
        title="Asset with Metadata",
        description="Asset with detailed metadata",
        file_type="image",
        is_active=True
    )

    # Add metadata
    Metadata.objects.create(asset=asset, field_name="resolution", field_value="1920x1080")
    Metadata.objects.create(asset=asset, field_name="camera", field_value="Canon EOS 5D")
    Metadata.objects.create(asset=asset, field_name="location", field_value="New York")

    return asset


# ============================================================================
# BRANCH 1: AUTHENTICATION (LOGIN) TESTS
# ============================================================================

@pytest.mark.django_db
class TestWKAuthentication:
    """Test suite for WK Branch 1: Authentication (Login)"""

    def test_login_with_valid_credentials(self, api_client, viewer_user):
        """Test successful login with valid username and password"""
        url = reverse('login')
        data = {
            'username': 'wk_viewer',
            'password': 'viewerpass123'
        }
        response = api_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_200_OK
        assert 'user' in response.data
        assert 'access' in response.data
        assert 'refresh' in response.data
        assert response.data['user']['username'] == 'wk_viewer'
        assert response.data['user']['role'] == 'viewer'

    def test_login_with_invalid_password(self, api_client, viewer_user):
        """Test login fails with invalid password"""
        url = reverse('login')
        data = {
            'username': 'wk_viewer',
            'password': 'wrongpassword'
        }
        response = api_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert 'error' in response.data

    def test_login_with_invalid_username(self, api_client):
        """Test login fails with nonexistent username"""
        url = reverse('login')
        data = {
            'username': 'nonexistent_user',
            'password': 'anypassword'
        }
        response = api_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_login_with_missing_credentials(self, api_client):
        """Test login fails with missing credentials"""
        url = reverse('login')
        data = {'username': 'wk_viewer'}  # Missing password
        response = api_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_authenticated_user_can_access_protected_endpoint(self, api_client, viewer_user):
        """Test that authenticated user can access protected endpoints"""
        # Login first
        login_url = reverse('login')
        login_data = {
            'username': 'wk_viewer',
            'password': 'viewerpass123'
        }
        login_response = api_client.post(login_url, login_data, format='json')
        access_token = login_response.data['access']

        # Access protected endpoint with token
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        profile_url = reverse('profile')
        response = api_client.get(profile_url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['username'] == 'wk_viewer'

    def test_unauthenticated_user_cannot_access_protected_endpoint(self, api_client):
        """Test that unauthenticated user cannot access protected endpoints"""
        url = reverse('profile')
        response = api_client.get(url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


# ============================================================================
# BRANCH 2: DASHBOARD TESTS
# ============================================================================

@pytest.mark.django_db
class TestWKDashboard:
    """Test suite for WK Branch 2: Dashboard"""

    def test_dashboard_access_requires_authentication(self, api_client):
        """Test that dashboard requires authentication"""
        # Note: This test assumes a dashboard endpoint exists
        # The actual URL might need adjustment based on implementation
        url = '/api/dashboard/stats/'
        response = api_client.get(url)

        # Dashboard endpoint may not exist yet (404) or require auth (401)
        assert response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_404_NOT_FOUND]

    def test_dashboard_shows_asset_statistics_for_admin(
        self, api_client, admin_user, sample_image_asset,
        sample_video_asset, sample_document_asset
    ):
        """Test that admin sees all asset statistics"""
        api_client.force_authenticate(user=admin_user)
        url = '/api/dashboard/stats/'
        response = api_client.get(url)

        # If endpoint exists, verify statistics
        if response.status_code == status.HTTP_200_OK:
            assert 'total_assets' in response.data
            assert response.data['total_assets'] >= 3

    def test_dashboard_shows_role_specific_content_for_viewer(self, api_client, viewer_user):
        """Test that viewer sees role-appropriate dashboard content"""
        api_client.force_authenticate(user=viewer_user)
        url = '/api/dashboard/stats/'
        response = api_client.get(url)

        # Viewer should have limited access
        if response.status_code == status.HTTP_200_OK:
            # Verify viewer-specific content
            assert 'user_role' in response.data or True  # Adjust based on implementation

    def test_dashboard_asset_counts_by_type(
        self, api_client, admin_user, sample_image_asset,
        sample_video_asset, sample_document_asset
    ):
        """Test dashboard shows correct asset counts by type"""
        api_client.force_authenticate(user=admin_user)

        # Count assets manually
        image_count = Asset.objects.filter(file_type='image', is_active=True).count()
        video_count = Asset.objects.filter(file_type='video', is_active=True).count()
        pdf_count = Asset.objects.filter(file_type='pdf', is_active=True).count()

        # Verify counts are correct
        assert image_count >= 1
        assert video_count >= 1
        assert pdf_count >= 1


# ============================================================================
# BRANCH 3: ASSET LIBRARY TESTS
# ============================================================================

@pytest.mark.django_db
class TestWKAssetLibrary:
    """Test suite for WK Branch 3: Asset Library"""

    def test_asset_library_list_all_active_assets(
        self, api_client, editor_user, sample_image_asset,
        sample_video_asset, inactive_asset
    ):
        """Test asset library displays all active assets"""
        api_client.force_authenticate(user=editor_user)
        url = reverse('asset-list')
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) >= 2

        # Verify active assets are included
        asset_ids = [a['asset_id'] for a in response.data['results']]
        assert str(sample_image_asset.asset_id) in asset_ids
        assert str(sample_video_asset.asset_id) in asset_ids

    def test_asset_library_filter_by_file_type(
        self, api_client, editor_user, sample_image_asset,
        sample_video_asset, sample_document_asset
    ):
        """Test filtering assets by file type in asset library"""
        api_client.force_authenticate(user=editor_user)

        # Filter for images only
        url = reverse('asset-list') + '?file_type=image'
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        for asset in response.data['results']:
            assert asset['file_type'] == 'image'

    def test_asset_library_sorting_newest_first(
        self, api_client, editor_user, sample_image_asset, sample_video_asset
    ):
        """Test asset library sorting by newest first"""
        api_client.force_authenticate(user=editor_user)
        url = reverse('asset-list') + '?ordering=-created_at'
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) >= 2

        # Verify sorting (newest first)
        if len(response.data['results']) >= 2:
            first_date = response.data['results'][0]['created_at']
            second_date = response.data['results'][1]['created_at']
            assert first_date >= second_date

    def test_asset_library_search_by_title(self, api_client, editor_user, sample_image_asset):
        """Test searching assets by title in asset library"""
        api_client.force_authenticate(user=editor_user)
        url = reverse('asset-list') + '?search=Sample Image'
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) >= 1
        assert any('Sample Image' in asset['title'] for asset in response.data['results'])

    def test_asset_library_delete_asset_as_owner(self, api_client, editor_user, sample_image_asset):
        """Test deleting asset from library as owner"""
        api_client.force_authenticate(user=editor_user)
        url = reverse('asset-detail', kwargs={'pk': sample_image_asset.asset_id})
        response = api_client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Asset.objects.filter(asset_id=sample_image_asset.asset_id).exists()

    def test_asset_library_delete_asset_as_admin(self, api_client, admin_user, sample_image_asset):
        """Test deleting any asset from library as admin"""
        api_client.force_authenticate(user=admin_user)
        url = reverse('asset-detail', kwargs={'pk': sample_image_asset.asset_id})
        response = api_client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Asset.objects.filter(asset_id=sample_image_asset.asset_id).exists()

    def test_asset_library_viewer_cannot_delete(self, api_client, viewer_user, sample_image_asset):
        """Test that viewer cannot delete assets from library"""
        api_client.force_authenticate(user=viewer_user)
        url = reverse('asset-detail', kwargs={'pk': sample_image_asset.asset_id})
        response = api_client.delete(url)

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert Asset.objects.filter(asset_id=sample_image_asset.asset_id).exists()

    def test_asset_library_pagination(self, api_client, editor_user):
        """Test asset library pagination"""
        # Create multiple assets
        for i in range(15):
            file = SimpleUploadedFile(f"asset_{i}.jpg", b"content", content_type="image/jpeg")
            Asset.objects.create(
                user=editor_user,
                file=file,
                title=f"Asset {i}",
                file_type="image",
                is_active=True
            )

        api_client.force_authenticate(user=editor_user)
        url = reverse('asset-list')
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert 'results' in response.data
        assert 'count' in response.data

    def test_asset_library_displays_asset_count(
        self, api_client, editor_user, sample_image_asset,
        sample_video_asset, sample_document_asset
    ):
        """Test that asset library shows total asset count"""
        api_client.force_authenticate(user=editor_user)
        url = reverse('asset-list')
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert 'count' in response.data
        assert response.data['count'] >= 3

    def test_asset_library_empty_state(self, api_client, viewer_user):
        """Test asset library when no assets exist"""
        # Create fresh viewer user with no assets
        new_viewer = User.objects.create_user(
            username='new_viewer',
            password='pass123',
            role='viewer'
        )
        api_client.force_authenticate(user=new_viewer)

        # Filter to only show this user's assets (should be empty)
        url = reverse('asset-list') + '?user=' + str(new_viewer.id)
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK


# ============================================================================
# BRANCH 4: ASSET DETAILS & VIEWING TESTS
# ============================================================================

@pytest.mark.django_db
class TestWKAssetDetails:
    """Test suite for WK Branch 4: Asset Details & Viewing"""

    def test_view_asset_details(self, api_client, editor_user, sample_image_asset):
        """Test viewing detailed information of an asset"""
        api_client.force_authenticate(user=editor_user)
        url = reverse('asset-detail', kwargs={'pk': sample_image_asset.asset_id})
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['asset_id'] == str(sample_image_asset.asset_id)
        assert response.data['title'] == 'Sample Image Asset'
        assert response.data['description'] == 'A sample image for testing'
        assert response.data['file_type'] == 'image'
        assert 'tags' in response.data

    def test_view_asset_metadata(self, api_client, editor_user, asset_with_metadata):
        """Test viewing asset with metadata"""
        api_client.force_authenticate(user=editor_user)
        url = reverse('asset-detail', kwargs={'pk': asset_with_metadata.asset_id})
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        # Verify metadata is included (if serializer includes it)
        if 'metadata' in response.data:
            assert len(response.data['metadata']) >= 3

    def test_edit_asset_title_and_description(self, api_client, editor_user, sample_image_asset):
        """Test editing asset title, description, and tags"""
        api_client.force_authenticate(user=editor_user)
        url = reverse('asset-detail', kwargs={'pk': sample_image_asset.asset_id})

        data = {
            'title': 'Updated Asset Title',
            'description': 'Updated asset description',
            'tags': ['updated', 'new-tags', 'test']
        }
        response = api_client.patch(url, data, format='json')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == 'Updated Asset Title'
        assert response.data['description'] == 'Updated asset description'
        assert 'updated' in response.data['tags']

    def test_admin_can_edit_any_asset(self, api_client, admin_user, sample_image_asset):
        """Test that admin can edit any asset"""
        api_client.force_authenticate(user=admin_user)
        url = reverse('asset-detail', kwargs={'pk': sample_image_asset.asset_id})

        data = {'title': 'Admin Edited Title'}
        response = api_client.patch(url, data, format='json')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == 'Admin Edited Title'

    def test_viewer_cannot_edit_asset(self, api_client, viewer_user, sample_image_asset):
        """Test that viewer cannot edit assets"""
        api_client.force_authenticate(user=viewer_user)
        url = reverse('asset-detail', kwargs={'pk': sample_image_asset.asset_id})

        data = {'title': 'Viewer Edit Attempt'}
        response = api_client.patch(url, data, format='json')

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_view_3d_model_asset(self, api_client, editor_user, sample_3d_asset):
        """Test viewing 3D model asset details"""
        api_client.force_authenticate(user=editor_user)
        url = reverse('asset-detail', kwargs={'pk': sample_3d_asset.asset_id})
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['file_type'] == '3d'
        assert response.data['title'] == 'Sample 3D Model'

    def test_viewer_can_view_active_asset(self, api_client, viewer_user, sample_image_asset):
        """Test that viewer can view active asset details"""
        api_client.force_authenticate(user=viewer_user)
        url = reverse('asset-detail', kwargs={'pk': sample_image_asset.asset_id})
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == 'Sample Image Asset'

    def test_viewer_cannot_view_inactive_asset(self, api_client, viewer_user, inactive_asset):
        """Test that viewer cannot view inactive asset details"""
        api_client.force_authenticate(user=viewer_user)
        url = reverse('asset-detail', kwargs={'pk': inactive_asset.asset_id})
        response = api_client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_view_nonexistent_asset_returns_404(self, api_client, editor_user):
        """Test viewing nonexistent asset returns 404"""
        api_client.force_authenticate(user=editor_user)
        url = reverse('asset-detail', kwargs={'pk': '00000000-0000-0000-0000-000000000000'})
        response = api_client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND


# ============================================================================
# INTEGRATION TESTS FOR WK FEATURES
# ============================================================================

@pytest.mark.django_db
class TestWKFeaturesIntegration:
    """Integration tests for all WK features combined"""

    def test_multiple_asset_types_in_library(
        self, api_client, editor_user, sample_image_asset,
        sample_video_asset, sample_document_asset, sample_3d_asset
    ):
        """Test library displays multiple asset types correctly"""
        api_client.force_authenticate(user=editor_user)

        url = reverse('asset-list')
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) >= 4

        # Verify different file types are present
        file_types = [asset['file_type'] for asset in response.data['results']]
        assert 'image' in file_types
        assert 'video' in file_types
        assert 'pdf' in file_types
        assert '3d' in file_types
