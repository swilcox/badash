"""Configuration Settings!
"""
import os
import sys


class BaseConfig(object):
    """Base Configuration settings"""
    MONGODB_URI = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/badash')
    DEFAULT_PAGE_SIZE = 10
    JWT_SECRET = os.environ.get('JWT_SECRET', None)
    JWT_AUDIENCE = os.environ.get('JWT_AUDIENCE', '')
    JWT_ALGORITHMS = ["RS256"]
    JWKS_URL = os.environ.get('JWKS_URL', '')


class LocalConfig(BaseConfig):
    """Local Configuration settings"""
    pass


class TestingConfig(BaseConfig):
    """Settings to use while running tests"""
    MONGODB_URI = 'mongomock://localhost:27017/test_badash'
    JWT_SECRET = 'test_secret'
    JWT_AUDIENCE = 'test'
    JWKS_URL = 'http://www.example.com/jwks'


class ProductionConfig(BaseConfig):
    """Production Settings"""
    pass


class DevConfig(BaseConfig):
    """Dev Settings"""
    pass


STAGE = 'testing' if sys.__dict__.get('_called_from_test') else os.environ.get('HUG_SETTINGS', 'local').lower()
print(STAGE)

CONFIG_STAGES = {
    'local': LocalConfig,
    'testing': TestingConfig,
    'prod': ProductionConfig,
    'dev': DevConfig,
}


settings = CONFIG_STAGES[STAGE]
