""" PyTest Configuration """
import mongoengine


def pytest_configure(config):
    """setup configuration"""
    import sys
    sys._called_from_test = True
    from settings import settings
    mongoengine.connect(host=settings.MONGODB_URI)


def pytest_unconfigure(config):
    """teardown configuration"""
    conn = mongoengine.connection.get_connection()
    conn.drop_database('test_badash')
    import sys
    del sys._called_from_test
