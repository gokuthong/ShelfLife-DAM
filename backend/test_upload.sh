#!/bin/bash
# Test asset upload as admin

# First, login to get token
echo "Logging in as admin..."
TOKEN=$(curl -s -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "your_admin_password"}' \
  | python -c "import sys, json; print(json.load(sys.stdin)['access'])")

echo "Token: $TOKEN"

# Create a test image file
echo "Creating test image..."
echo "test image content" > test_image.jpg

# Upload the asset
echo "Uploading asset..."
curl -X POST http://localhost:8000/api/assets/assets/ \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@test_image.jpg" \
  -F "title=Test Upload" \
  -F "file_type=image" \
  -F "description=Test description" \
  -F 'tags=["test", "upload"]'

# Clean up
rm test_image.jpg

echo "Done!"
