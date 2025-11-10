"""
Tests for Asset models
"""
import pytest
import os
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from assets.models import Asset, Metadata, AssetVersion

User = get_user_model()


@pytest.fixture
def user():
    """Create a test user"""
    return User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='pass123',
        role='editor'
    )


@pytest.fixture
def asset(user):
    """Create a test asset"""
    file = SimpleUploadedFile(
        "test.jpg",
        b"file_content",
        content_type="image/jpeg"
    )
    return Asset.objects.create(
        user=user,
        file=file,
        title="Test Asset",
        description="Test description",
        tags=["tag1", "tag2"],
        file_type="image"
    )


@pytest.mark.django_db
class TestAssetModel:
    """Test suite for Asset model"""

    def test_create_asset(self, user):
        """Test creating an asset"""
        file = SimpleUploadedFile("test.pdf", b"file_content", content_type="application/pdf")
        asset = Asset.objects.create(
            user=user,
            file=file,
            title="Test PDF",
            description="PDF document",
            tags=["document", "test"],
            file_type="pdf"
        )

        assert asset.title == "Test PDF"
        assert asset.user == user
        assert asset.file_type == "pdf"
        assert asset.tags == ["document", "test"]
        assert asset.version == 1
        assert asset.is_active is True

    def test_asset_file_type_auto_detection_image(self, user):
        """Test automatic file type detection for images"""
        file = SimpleUploadedFile("test.png", b"file_content", content_type="image/png")
        asset = Asset.objects.create(
            user=user,
            file=file,
            title="Test Image"
        )
        assert asset.file_type == "image"

    def test_asset_file_type_auto_detection_video(self, user):
        """Test automatic file type detection for videos"""
        file = SimpleUploadedFile("test.mp4", b"file_content", content_type="video/mp4")
        asset = Asset.objects.create(
            user=user,
            file=file,
            title="Test Video"
        )
        assert asset.file_type == "video"

    def test_asset_file_type_auto_detection_pdf(self, user):
        """Test automatic file type detection for PDFs"""
        file = SimpleUploadedFile("test.pdf", b"file_content", content_type="application/pdf")
        asset = Asset.objects.create(
            user=user,
            file=file,
            title="Test PDF"
        )
        assert asset.file_type == "pdf"

    def test_asset_file_type_auto_detection_doc(self, user):
        """Test automatic file type detection for documents"""
        file = SimpleUploadedFile("test.docx", b"file_content", content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
        asset = Asset.objects.create(
            user=user,
            file=file,
            title="Test Document"
        )
        assert asset.file_type == "doc"

    def test_asset_file_type_auto_detection_audio(self, user):
        """Test automatic file type detection for audio"""
        file = SimpleUploadedFile("test.mp3", b"file_content", content_type="audio/mpeg")
        asset = Asset.objects.create(
            user=user,
            file=file,
            title="Test Audio"
        )
        assert asset.file_type == "audio"

    def test_asset_file_type_auto_detection_3d(self, user):
        """Test automatic file type detection for 3D models"""
        file = SimpleUploadedFile("test.obj", b"file_content")
        asset = Asset.objects.create(
            user=user,
            file=file,
            title="Test 3D Model"
        )
        assert asset.file_type == "3d"

    def test_asset_file_type_auto_detection_other(self, user):
        """Test automatic file type detection for unknown types"""
        file = SimpleUploadedFile("test.xyz", b"file_content")
        asset = Asset.objects.create(
            user=user,
            file=file,
            title="Test Unknown"
        )
        assert asset.file_type == "other"

    def test_asset_file_size_auto_set(self, user):
        """Test that file size is automatically set"""
        content = b"x" * 1000  # 1000 bytes
        file = SimpleUploadedFile("test.txt", content)
        asset = Asset.objects.create(
            user=user,
            file=file,
            title="Test File Size"
        )
        assert asset.file_size > 0

    def test_asset_string_representation(self, asset):
        """Test __str__ method"""
        assert str(asset) == "Test Asset (v1)"

    def test_asset_file_extension_property(self, asset):
        """Test file_extension property"""
        assert asset.file_extension == ".jpg"

    def test_asset_ordering(self, user):
        """Test that assets are ordered by created_at descending"""
        asset1 = Asset.objects.create(
            user=user,
            file=SimpleUploadedFile("test1.jpg", b"content"),
            title="First Asset"
        )
        asset2 = Asset.objects.create(
            user=user,
            file=SimpleUploadedFile("test2.jpg", b"content"),
            title="Second Asset"
        )

        assets = Asset.objects.all()
        assert assets[0] == asset2  # Most recent first
        assert assets[1] == asset1

    def test_asset_default_values(self, user):
        """Test default values for asset fields"""
        file = SimpleUploadedFile("test.jpg", b"content")
        asset = Asset.objects.create(
            user=user,
            file=file,
            title="Test"
        )

        assert asset.description is None or asset.description == ""
        assert asset.tags == []
        assert asset.version == 1
        assert asset.is_active is True


@pytest.mark.django_db
class TestMetadataModel:
    """Test suite for Metadata model"""

    def test_create_metadata(self, asset):
        """Test creating metadata for an asset"""
        metadata = Metadata.objects.create(
            asset=asset,
            field_name="resolution",
            field_value="1920x1080"
        )

        assert metadata.asset == asset
        assert metadata.field_name == "resolution"
        assert metadata.field_value == "1920x1080"

    def test_metadata_unique_together(self, asset):
        """Test that asset+field_name must be unique"""
        Metadata.objects.create(
            asset=asset,
            field_name="resolution",
            field_value="1920x1080"
        )

        # Trying to create duplicate should raise error
        from django.db import IntegrityError
        with pytest.raises(IntegrityError):
            Metadata.objects.create(
                asset=asset,
                field_name="resolution",
                field_value="3840x2160"
            )

    def test_metadata_string_representation(self, asset):
        """Test __str__ method"""
        metadata = Metadata.objects.create(
            asset=asset,
            field_name="camera",
            field_value="Canon EOS 5D"
        )
        assert str(metadata) == "Test Asset - camera"

    def test_multiple_metadata_fields(self, asset):
        """Test creating multiple metadata fields for one asset"""
        Metadata.objects.create(
            asset=asset,
            field_name="resolution",
            field_value="1920x1080"
        )
        Metadata.objects.create(
            asset=asset,
            field_name="camera",
            field_value="Canon EOS 5D"
        )
        Metadata.objects.create(
            asset=asset,
            field_name="location",
            field_value="New York"
        )

        assert asset.metadata_fields.count() == 3


@pytest.mark.django_db
class TestAssetVersionModel:
    """Test suite for AssetVersion model"""

    def test_create_asset_version(self, asset, user):
        """Test creating an asset version"""
        file = SimpleUploadedFile("test_v2.jpg", b"new_content")
        version = AssetVersion.objects.create(
            asset=asset,
            version_number=2,
            file=file,
            file_size=len(b"new_content"),
            changes="Updated image quality",
            created_by=user
        )

        assert version.asset == asset
        assert version.version_number == 2
        assert version.changes == "Updated image quality"
        assert version.created_by == user

    def test_version_unique_together(self, asset, user):
        """Test that asset+version_number must be unique"""
        file1 = SimpleUploadedFile("test_v2.jpg", b"content")
        AssetVersion.objects.create(
            asset=asset,
            version_number=2,
            file=file1,
            created_by=user
        )

        # Trying to create duplicate version number should raise error
        from django.db import IntegrityError
        with pytest.raises(IntegrityError):
            file2 = SimpleUploadedFile("test_v2_duplicate.jpg", b"content")
            AssetVersion.objects.create(
                asset=asset,
                version_number=2,
                file=file2,
                created_by=user
            )

    def test_version_string_representation(self, asset, user):
        """Test __str__ method"""
        file = SimpleUploadedFile("test_v2.jpg", b"content")
        version = AssetVersion.objects.create(
            asset=asset,
            version_number=2,
            file=file,
            created_by=user
        )
        assert str(version) == "Test Asset - v2"

    def test_version_ordering(self, asset, user):
        """Test that versions are ordered by version_number descending"""
        file1 = SimpleUploadedFile("v2.jpg", b"content")
        file2 = SimpleUploadedFile("v3.jpg", b"content")

        version2 = AssetVersion.objects.create(
            asset=asset,
            version_number=2,
            file=file1,
            created_by=user
        )
        version3 = AssetVersion.objects.create(
            asset=asset,
            version_number=3,
            file=file2,
            created_by=user
        )

        versions = AssetVersion.objects.filter(asset=asset)
        assert versions[0] == version3  # Highest version first
        assert versions[1] == version2

    def test_version_file_size(self, asset, user):
        """Test version file_size field"""
        content = b"x" * 500
        file = SimpleUploadedFile("test.jpg", content)
        version = AssetVersion.objects.create(
            asset=asset,
            version_number=2,
            file=file,
            file_size=len(content),
            created_by=user
        )
        assert version.file_size == 500
