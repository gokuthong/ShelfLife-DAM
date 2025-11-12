"""
Diagnostic script for asset upload issues
Run with: python diagnose_upload.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ShelfLifeDAM.settings')
django.setup()

from django.urls import get_resolver, URLPattern, URLResolver

def list_urls(patterns, prefix=''):
    """Recursively list all URL patterns"""
    urls = []
    for pattern in patterns:
        if isinstance(pattern, URLResolver):
            urls.extend(list_urls(pattern.url_patterns, prefix + str(pattern.pattern)))
        elif isinstance(pattern, URLPattern):
            urls.append((prefix + str(pattern.pattern), pattern.name, pattern.callback))
    return urls

# Get all URLs
resolver = get_resolver()
all_urls = list_urls(resolver.url_patterns)

# Filter for asset URLs
asset_urls = [(url, name, callback) for url, name, callback in all_urls if 'asset' in url.lower()]

print("="*80)
print("ASSET UPLOAD ENDPOINTS DIAGNOSTIC")
print("="*80)

print("\nAvailable Asset Endpoints:")
print("-"*80)
for url, name, callback in sorted(asset_urls):
    print(f"  URL: {url}")
    print(f"  Name: {name}")
    print(f"  Callback: {callback}")
    print()

print("\n" + "="*80)
print("CORRECT ENDPOINTS FOR ASSET UPLOAD:")
print("="*80)
print("\nOption 1 (RECOMMENDED): ViewSet Endpoint")
print("  URL: POST http://localhost:8000/api/assets/assets/")
print("  Headers:")
print("    - Authorization: Bearer YOUR_JWT_TOKEN")
print("    - Content-Type: multipart/form-data")
print("  Body (multipart/form-data):")
print("    - file: [your file]")
print("    - title: 'Asset Title'")
print("    - file_type: 'image' (or video/pdf/doc/audio/3d/other)")
print("    - description: 'Optional description'")
print("    - tags: [\"tag1\", \"tag2\"] (optional)")

print("\nOption 2: Function View Endpoint")
print("  URL: POST http://localhost:8000/api/assets/upload/")
print("  Same headers and body as Option 1")

print("\n" + "="*80)
print("COMMON ISSUES:")
print("="*80)
print("\n1. Wrong URL")
print("   - Make sure you're using /api/assets/assets/ (note the double 'assets')")
print("   - NOT /api/assets/ (missing '/assets')")

print("\n2. Wrong HTTP Method")
print("   - Must be POST, not GET")

print("\n3. Missing Authentication")
print("   - Include 'Authorization: Bearer YOUR_TOKEN' header")
print("   - Token must be for an admin or editor user (not viewer)")

print("\n4. Wrong Content-Type")
print("   - Use multipart/form-data for file uploads")
print("   - DO NOT use application/json")

print("\n5. Missing Required Fields")
print("   - 'file' field is REQUIRED")
print("   - 'title' field is REQUIRED")
print("   - 'file_type' field is REQUIRED")

print("\n" + "="*80)
print("TESTING:")
print("="*80)
print("\nTo test if the endpoint works, run:")
print("  cd C:\\Users\\ASUS\\Downloads\\ShelfLifeDAM-main\\backend")
print("  python manage.py shell")
print("\nThen in the shell:")
print("""
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile

User = get_user_model()
admin = User.objects.filter(role='admin').first()
print(f"Using admin: {admin.username}")

client = APIClient()
client.force_authenticate(user=admin)

file = SimpleUploadedFile("test.jpg", b"file_content", content_type="image/jpeg")
response = client.post('/api/assets/assets/', {
    'file': file,
    'title': 'Test',
    'file_type': 'image'
}, format='multipart')

print(f"Status: {response.status_code}")
print(f"Response: {response.data if hasattr(response, 'data') else response.content}")
""")

print("\n" + "="*80)
