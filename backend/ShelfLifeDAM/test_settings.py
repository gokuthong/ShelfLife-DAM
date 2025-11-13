"""
Test settings for running pytest with SQLite in-memory database.
This allows tests to run without requiring PostgreSQL setup.

Usage:
    python -m pytest test_wk_features.py --ds=ShelfLifeDAM.test_settings -v
"""

from .settings import *

# Use SQLite in-memory database for testing
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

# Disable migrations for faster testing
class DisableMigrations:
    def __contains__(self, item):
        return True

    def __getitem__(self, item):
        return None

# Uncomment to disable migrations (faster tests)
# MIGRATION_MODULES = DisableMigrations()

# Use faster password hasher for testing
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

# Disable debug mode for testing
DEBUG = False

# Disable logging during tests
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
}
