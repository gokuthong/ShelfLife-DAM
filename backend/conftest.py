import pytest
import django
from django.conf import settings

@pytest.fixture(scope='session', autouse=True)
def setup_django():
    if not settings.configured:
        django.setup()

@pytest.fixture(scope='function', autouse=True)
def enable_db_access_for_all_tests(db):
    """Enable database access for all tests"""
    pass
