"""
Test asset upload API
Run with: python test_upload.py
"""
import os
import django
import io
from PIL import Image

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ShelfLifeDAM.settings')
django.setup()

from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from django.core.files.uploadedfile import SimpleUploadedFile

User = get_user_model()

print("=" * 80)
print("ASSET UPLOAD TEST")
print("=" * 80)

# Get admin user
try:
    admin = User.objects.filter(role='admin').first()
    if not admin:
        print("[ERROR] No admin user found. Creating one...")
        admin = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123',
            role='admin'
        )
    print(f"[OK] Using admin user: {admin.username}")
except Exception as e:
    print(f"[ERROR] Failed to get admin user: {e}")
    exit(1)

# Create API client
client = APIClient()
client.force_authenticate(user=admin)
print("[OK] API client authenticated")

# Create a test image file
print("\n[INFO] Creating test image...")
image = Image.new('RGB', (100, 100), color='red')
image_io = io.BytesIO()
image.save(image_io, format='JPEG')
image_io.seek(0)

test_file = SimpleUploadedFile(
    "test_upload.jpg",
    image_io.read(),
    content_type="image/jpeg"
)

# Test endpoint: /api/assets/ (based on URL pattern api/assets/^$)
print("\n[INFO] Testing endpoint: POST /api/assets/")
response = client.post(
    '/api/assets/',
    {
        'file': test_file,
        'title': 'Test Upload',
        'file_type': 'image',
        'description': 'This is a test upload',
    },
    format='multipart'
)

print(f"\n[RESULT] Response Status: {response.status_code}")
if response.status_code == 201:
    print("[SUCCESS] Asset uploaded successfully!")
    print(f"Response data: {response.data}")
elif response.status_code == 405:
    print("[FAILED] Method POST not allowed")
    print(f"Error: {response.data if hasattr(response, 'data') else response.content}")
    print("\n[INFO] This means the ViewSet is not configured to accept POST requests")
    print("[INFO] Check assets/views.py - AssetViewSet should allow 'create' action")
else:
    print(f"[FAILED] Upload failed with status {response.status_code}")
    print(f"Error: {response.data if hasattr(response, 'data') else response.content}")

print("\n" + "=" * 80)
