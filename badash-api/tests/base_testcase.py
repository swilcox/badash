"""base testcase"""
from unittest import TestCase
from models import Dashboard, Job, Event, ApiKey


class ApiTestCase(TestCase):
    """API TestCase Base Class"""
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        Dashboard.drop_collection()
        Job.drop_collection()
        Event.drop_collection()
        ApiKey.drop_collection()
        super().tearDownClass()

    def setUp(self):
        pass

    def tearDown(self):
        pass
