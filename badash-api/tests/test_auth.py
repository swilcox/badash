"""test_auth.py"""
import jwt
import pytest

import auth
from models import ApiKey
from settings import settings


@pytest.fixture(scope='function')
def token():
    return jwt.encode({'user': 'tester'}, settings.JWT_SECRET)


@pytest.fixture(scope='function')
def api_key():
    yield ApiKey.objects.create(user='test_me').api_key
    ApiKey.objects.all().delete() 


def test_token_verify(token):
    """test token auth verify"""
    assert auth.token_verify(token) == {'user': 'tester'}
    token = jwt.encode({'user': 'invalid'}, 'not-the-real-secret')
    assert auth.token_verify(token) is False


def test_api_key_verify(api_key):
    """test api_key auth verify"""
    assert auth.api_key_verify(api_key).user == 'test_me'
    assert auth.api_key_verify('invalid-api-key') is False


def test_multi_verify(token, api_key):
    assert auth.multi_verify(token, api_key) == {'user': 'tester'}
    assert auth.multi_verify(None, api_key).user == 'test_me'
    assert auth.multi_verify(None, None) is None

