"""test_cli.py"""

from app import create_api_key
from models import ApiKey


def test_create_api_key():
    create_api_key()
    assert ApiKey.objects.all().count() == 1
    assert ApiKey.objects.first().user == 'admin'
    assert len(ApiKey.objects.first().api_key) > 0


