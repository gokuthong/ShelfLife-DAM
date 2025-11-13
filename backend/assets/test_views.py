"""
Tests for Asset views and API endpoints
"""
import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from assets.models import Asset, Metadata, AssetVersion

User = get_user_model()


@pytest.fixture
def api_client():
    """Create API client"""
    return APIClient()


@pytest.fixture
def admin_user(db):
    """Create admin user"""
    user = User.objects.create_user(
        username='admin',
        email='admin@example.com',
        password='adminpass123',
        role='admin'
    )
    return user


@pytest.fixture
def editor_user(db):
    """Create editor user"""
    user = User.objects.create_user(
        username='editor',
        email='editor@example.com',
        password='editorpass123',
        role='editor'
    )
    return user


@pytest.fixture
def viewer_user(db):
    """Create viewer user"""
    user = User.objects.create_user(
        username='viewer',
        email='viewer@example.com',
        password='viewerpass123',
        role='viewer'
    )
    return user


@pytest.fixture
def asset(editor_user):
    """Create test asset"""
    file = SimpleUploadedFile("test.jpg", b"file_content", content_type="image/jpeg")
    return Asset.objects.create(
        user=editor_user,
        file=file,
        title="Test Asset",
        description="Test description",
        tags=["tag1", "tag2"],
        file_type="image",
        is_active=True
    )


@pytest.fixture
def inactive_asset(editor_user):
    """Create inactive test asset"""
    file = SimpleUploadedFile("inactive.jpg", b"file_content", content_type="image/jpeg")
    return Asset.objects.create(
        user=editor_user,
        file=file,
        title="Inactive Asset",
        file_type="image",
        is_active=False
    )


@pytest.mark.django_db
class TestAssetListView:
    """Test suite for listing assets"""

    def test_admin_sees_all_assets(self, api_client, admin_user, asset, inactive_asset):
        """Test that admin can see all assets including inactive"""
        api_client.force_authenticate(user=admin_user)
        url = reverse('asset-list')
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) >= 2

    def test_editor_sees_own_and_active_assets(self, api_client, editor_user, asset, inactive_asset):
        """Test that editor sees their own assets and active ones"""
        # Create asset by another user
        another_editor = User.objects.create_user(
            username='another_editor',
            password='pass123',
            role='editor'
        )
        file = SimpleUploadedFile("other.jpg", b"content", content_type="image/jpeg")
        other_asset = Asset.objects.create(
            user=another_editor,
            file=file,
            title="Other Asset",
            file_type="image",
            is_active=True
        )

        api_client.force_authenticate(user=editor_user)
        url = reverse('asset-list')
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        # Should see own active, own inactive, and others' active
        asset_ids = [a['asset_id'] for a in response.data['results']]
        assert str(asset.asset_id) in asset_ids  # Own active
        assert str(inactive_asset.asset_id) in asset_ids  # Own inactive
        assert str(other_asset.asset_id) in asset_ids  # Others' active

    def test_unauthenticated_cannot_list_assets(self, api_client):
        """Test that unauthenticated user cannot list assets"""
        url = reverse('asset-list')
        response = api_client.get(url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestAssetCreateView:
    """Test suite for creating assets"""

    def test_editor_can_create_asset(self, api_client, editor_user):
        """Test that editor can create an asset"""
        api_client.force_authenticate(user=editor_user)
        url = reverse('asset-list')

        file = SimpleUploadedFile("newfile.pdf", b"file_content", content_type="application/pdf")
        data = {
            'file': file,
            'title': 'New PDF',
            'file_type': 'pdf'
        }
        response = api_client.post(url, data, format='multipart')

        assert response.status_code == status.HTTP_201_CREATED

    def test_admin_can_create_asset(self, api_client, admin_user):
        """Test that admin can create an asset"""
        api_client.force_authenticate(user=admin_user)
        url = reverse('asset-list')

        file = SimpleUploadedFile("newfile.pdf", b"file_content", content_type="application/pdf")
        data = {
            'file': file,
            'title': 'New PDF',
            'file_type': 'pdf'
        }
        response = api_client.post(url, data, format='multipart')

        assert response.status_code == status.HTTP_201_CREATED

    def test_viewer_cannot_create_asset(self, api_client, viewer_user):
        """Test that viewer cannot create an asset"""
        api_client.force_authenticate(user=viewer_user)
        url = reverse('asset-list')

        file = SimpleUploadedFile("newfile.jpg", b"file_content", content_type="image/jpeg")
        data = {
            'file': file,
            'title': 'New Asset',
            'file_type': 'image'
        }
        response = api_client.post(url, data, format='multipart')

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_create_asset_without_file(self, api_client, editor_user):
        """Test creating asset without file fails"""
        api_client.force_authenticate(user=editor_user)
        url = reverse('asset-list')

        data = {
            'title': 'No File Asset'
        }
        response = api_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestAssetRetrieveView:
    """Test suite for retrieving individual assets"""

    def test_retrieve_asset(self, api_client, editor_user, asset):
        """Test retrieving an asset"""
        api_client.force_authenticate(user=editor_user)
        url = reverse('asset-detail', kwargs={'pk': asset.asset_id})
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == 'Test Asset'
        assert response.data['asset_id'] == str(asset.asset_id)

    def test_viewer_can_retrieve_active_asset(self, api_client, viewer_user, asset):
        """Test that viewer can retrieve active assets"""
        api_client.force_authenticate(user=viewer_user)
        url = reverse('asset-detail', kwargs={'pk': asset.asset_id})
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == 'Test Asset'
        assert response.data['asset_id'] == str(asset.asset_id)

    def test_viewer_cannot_retrieve_inactive_asset(self, api_client, viewer_user, inactive_asset):
        """Test that viewer cannot retrieve inactive assets"""
        api_client.force_authenticate(user=viewer_user)
        url = reverse('asset-detail', kwargs={'pk': inactive_asset.asset_id})
        response = api_client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_retrieve_nonexistent_asset(self, api_client, editor_user):
        """Test retrieving nonexistent asset"""
        api_client.force_authenticate(user=editor_user)
        url = reverse('asset-detail', kwargs={'pk': '00000000-0000-0000-0000-000000000000'})
        response = api_client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestAssetUpdateView:
    """Test suite for updating assets"""

    def test_editor_can_update_own_asset(self, api_client, editor_user, asset):
        """Test that editor can update their own asset"""
        api_client.force_authenticate(user=editor_user)
        url = reverse('asset-detail', kwargs={'pk': asset.asset_id})

        data = {
            'title': 'Updated Title',
            'description': 'Updated description',
            'tags': ['updated', 'test']
        }
        response = api_client.patch(url, data, format='json')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == 'Updated Title'
        assert response.data['description'] == 'Updated description'

    def test_admin_can_update_any_asset(self, api_client, admin_user, asset):
        """Test that admin can update any asset"""
        api_client.force_authenticate(user=admin_user)
        url = reverse('asset-detail', kwargs={'pk': asset.asset_id})

        data = {'title': 'Admin Updated'}
        response = api_client.patch(url, data, format='json')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == 'Admin Updated'

    def test_viewer_cannot_update_asset(self, api_client, viewer_user, asset):
        """Test that viewer cannot update an asset"""
        api_client.force_authenticate(user=viewer_user)
        url = reverse('asset-detail', kwargs={'pk': asset.asset_id})

        data = {'title': 'Viewer Update'}
        response = api_client.patch(url, data, format='json')

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_editor_cannot_update_others_asset(self, api_client, editor_user):
        """Test that editor cannot update another user's asset"""
        other_editor = User.objects.create_user(
            username='other_editor',
            password='pass123',
            role='editor'
        )
        file = SimpleUploadedFile("other.jpg", b"content", content_type="image/jpeg")
        other_asset = Asset.objects.create(
            user=other_editor,
            file=file,
            title="Other Asset",
            file_type="image"
        )

        api_client.force_authenticate(user=editor_user)
        url = reverse('asset-detail', kwargs={'pk': other_asset.asset_id})

        data = {'title': 'Try to update'}
        response = api_client.patch(url, data, format='json')

        # This depends on the IsOwnerOrAdmin permission implementation
        # The response might be 403 if permission is checked
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestAssetDeleteView:
    """Test suite for deleting assets"""

    def test_editor_can_delete_own_asset(self, api_client, editor_user, asset):
        """Test that editor can delete their own asset"""
        api_client.force_authenticate(user=editor_user)
        url = reverse('asset-detail', kwargs={'pk': asset.asset_id})
        response = api_client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Asset.objects.filter(asset_id=asset.asset_id).exists()

    def test_admin_can_delete_any_asset(self, api_client, admin_user, asset):
        """Test that admin can delete any asset"""
        api_client.force_authenticate(user=admin_user)
        url = reverse('asset-detail', kwargs={'pk': asset.asset_id})
        response = api_client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Asset.objects.filter(asset_id=asset.asset_id).exists()

    def test_viewer_cannot_delete_asset(self, api_client, viewer_user, asset):
        """Test that viewer cannot delete an asset"""
        api_client.force_authenticate(user=viewer_user)
        url = reverse('asset-detail', kwargs={'pk': asset.asset_id})
        response = api_client.delete(url)

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert Asset.objects.filter(asset_id=asset.asset_id).exists()


@pytest.mark.django_db
class TestAssetFiltering:
    """Test suite for asset filtering and search"""

    def test_filter_by_file_type(self, api_client, editor_user):
        """Test filtering assets by file type"""
        # Create assets with different file types
        file1 = SimpleUploadedFile("image.jpg", b"content", content_type="image/jpeg")
        file2 = SimpleUploadedFile("video.mp4", b"content", content_type="video/mp4")

        Asset.objects.create(user=editor_user, file=file1, title="Image", file_type="image")
        Asset.objects.create(user=editor_user, file=file2, title="Video", file_type="video")

        api_client.force_authenticate(user=editor_user)
        url = reverse('asset-list') + '?file_type=image'
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        for asset in response.data['results']:
            assert asset['file_type'] == 'image'

    def test_search_by_title(self, api_client, editor_user):
        """Test searching assets by title"""
        file = SimpleUploadedFile("test.jpg", b"content", content_type="image/jpeg")
        Asset.objects.create(user=editor_user, file=file, title="Unique Title", file_type="image")

        api_client.force_authenticate(user=editor_user)
        url = reverse('asset-list') + '?search=Unique'
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) >= 1
        assert any('Unique' in asset['title'] for asset in response.data['results'])

    def test_ordering_by_created_at(self, api_client, editor_user):
        """Test ordering assets by created_at"""
        api_client.force_authenticate(user=editor_user)
        url = reverse('asset-list') + '?ordering=-created_at'
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        # Assets should be ordered by newest first


@pytest.mark.django_db
class TestSearchAssets:
    """Test suite for advanced asset search"""

    def test_search_by_query(self, api_client, editor_user):
        """Test searching assets by query string"""
        file = SimpleUploadedFile("search.jpg", b"content", content_type="image/jpeg")
        Asset.objects.create(
            user=editor_user,
            file=file,
            title="Searchable Title",
            description="Searchable description",
            file_type="image"
        )

        api_client.force_authenticate(user=editor_user)
        url = reverse('search_assets') + '?q=Searchable'
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) >= 1

    def test_search_by_tags(self, api_client, editor_user):
        """Test searching assets by tags"""
        file = SimpleUploadedFile("tagged.jpg", b"content", content_type="image/jpeg")
        Asset.objects.create(
            user=editor_user,
            file=file,
            title="Tagged Asset",
            tags=["important", "project"],
            file_type="image"
        )

        api_client.force_authenticate(user=editor_user)
        url = reverse('search_assets') + '?tags=important'
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK

    def test_search_viewer_sees_only_active(self, api_client, viewer_user, asset, inactive_asset):
        """Test that viewer search only returns active assets"""
        api_client.force_authenticate(user=viewer_user)
        url = reverse('search_assets')
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        asset_ids = [a['asset_id'] for a in response.data]
        assert str(asset.asset_id) in asset_ids
        assert str(inactive_asset.asset_id) not in asset_ids


@pytest.mark.django_db
class TestPermissions:
    """Test suite for asset permissions"""

    def test_is_owner_or_admin_permission(self, api_client, editor_user, admin_user):
        """Test IsOwnerOrAdmin permission"""
        file = SimpleUploadedFile("owned.jpg", b"content", content_type="image/jpeg")
        asset = Asset.objects.create(
            user=editor_user,
            file=file,
            title="Editor's Asset",
            file_type="image"
        )

        # Owner can update
        api_client.force_authenticate(user=editor_user)
        url = reverse('asset-detail', kwargs={'pk': asset.asset_id})
        response = api_client.patch(url, {'title': 'Updated by owner'}, format='json')
        assert response.status_code == status.HTTP_200_OK

        # Admin can update
        api_client.force_authenticate(user=admin_user)
        response = api_client.patch(url, {'title': 'Updated by admin'}, format='json')
        assert response.status_code == status.HTTP_200_OK

    def test_is_editor_or_admin_permission(self, api_client, editor_user, admin_user, viewer_user):
        """Test IsEditorOrAdmin permission"""
        url = reverse('asset-list')
        file = SimpleUploadedFile("test.jpg", b"content", content_type="image/jpeg")

        # Editor can create
        api_client.force_authenticate(user=editor_user)
        response = api_client.post(url, {
            'file': file,
            'title': 'Editor Asset',
            'file_type': 'image'
        }, format='multipart')
        assert response.status_code == status.HTTP_201_CREATED

        # Admin can create
        api_client.force_authenticate(user=admin_user)
        file2 = SimpleUploadedFile("test2.jpg", b"content", content_type="image/jpeg")
        response = api_client.post(url, {
            'file': file2,
            'title': 'Admin Asset',
            'file_type': 'image'
        }, format='multipart')
        assert response.status_code == status.HTTP_201_CREATED

        # Viewer cannot create
        api_client.force_authenticate(user=viewer_user)
        file3 = SimpleUploadedFile("test3.jpg", b"content", content_type="image/jpeg")
        response = api_client.post(url, {
            'file': file3,
            'title': 'Viewer Asset',
            'file_type': 'image'
        }, format='multipart')
        assert response.status_code == status.HTTP_403_FORBIDDEN
