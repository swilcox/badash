"""test_cli.py"""
import pytest

from app import create_api_key
from models import ApiKey



@pytest.fixture()
def api_key_scope():
    yield None
    ApiKey.objects.all().delete()


def test_create_api_key(api_key_scope):
    api_key_info = create_api_key()
    assert ApiKey.objects.all().count() == 1
    assert ApiKey.objects.first().user == 'admin'
    assert len(ApiKey.objects.first().api_key) > 0
