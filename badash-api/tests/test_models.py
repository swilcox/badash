"""test_models.py"""
import json

from models import Dashboard, Job, Event
from .base_testcase import ApiTestCase


class TestModelCreation(ApiTestCase):
    """Test Model Creation"""

    def test_dashboard(self):
        dash = Dashboard.objects.create(
            slug='testing',
            title='Testing Dashboard'
        )
        self.assertEqual(str(dash), 'Testing Dashboard')
        dash2 = Dashboard.objects.create(
            title='Testing Again The Dashböard'
        )
        self.assertEqual(dash2.slug, 'testing-again-the-dashboard')

    def test_job(self):
        job = Job.objects.create(
            slug='test-job',
            title='Test Job'
        )
        self.assertEqual(str(job), 'Test Job')

    def test_event(self):
        job = Job.objects.create(slug='test-e-job', title='Test E Job')
        event = Event.objects.create(
            job=job,
            result=0,
            extra_value=42.2,
            text_value='särskild'
        )
        self.assertEqual(str(event), 'Test E Job {}: 0 (None)'.format(event.datetimestamp))
        self.assertEqual(event.extra_value, 42.2)
        self.assertEqual(event.text_value, 'särskild')

    def test_display_field(self):
        job = Job.objects.create(
            slug='test-d-job',
            title='Test D Job',
            config={'display_field': 'value'}
        )
        event = Event.objects.create(
            job=job,
            result=0,
            value=42.0,
            extra_text='something else'
        )
        self.assertEqual(job.display_field, 'value')
        self.assertEqual(event.display_field, 42.0)
        self.assertEqual(str(event), 'Test D Job {}: 0 (42.0)'.format(event.datetimestamp))


class TestToDict(ApiTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.job = Job.objects.create(
            slug='test-job',
            title='Test Job',
            config={'display_field': 'value'}
        )
        cls.e1 = Event.objects.create(job=cls.job, result=0, value=40)
        cls.e2 = Event.objects.create(job=cls.job, result=0, value=42, extra_text='särskild')
        cls.e3 = Event.objects.create(job=cls.job, result=0, value=64)
        cls.dashboard = Dashboard.objects.create(
            slug='test-dashboard',
            title='Test Dashboard'
        )
        cls.dashboard.jobs.append(cls.job)

    def test_job(self):
        self.assertEqual(Event.objects.filter(job=self.job).count(), 3)
        self.assertEqual(json.loads(self.job.to_json())['title'], 'Test Job')
        job_dict = self.job.to_dict()
        self.assertEqual(job_dict['events'][0]['value'], self.e3.value)
        self.assertEqual(job_dict['title'], 'Test Job')
        self.assertEqual(len(job_dict['events']), 3)
        job_dict = self.job.to_dict(page_size=2)
        self.assertEqual(len(job_dict['events']), 2)
        self.assertEqual(job_dict['events'][0]['value'], self.e3.value)
        job_dict = self.job.to_dict(page_size=2, page_number=2)
        self.assertEqual(len(job_dict['events']), 1)
        self.assertEqual(job_dict['events'][0]['value'], self.e1.value)

    def test_dashboard(self):
        dash_dict = self.dashboard.to_dict()
        self.assertEqual(dash_dict['title'], 'Test Dashboard')
        self.assertEqual(len(dash_dict['jobs']), 1)
        self.assertEqual(dash_dict['jobs'][0], self.job.to_dict())

    def test_event(self):
        event_dict = Event.objects.filter(job=self.job)[1].to_dict()
        self.assertEqual(len(event_dict['_id']), 24)
        # self.assertEqual(len(event_dict['datetimestamp']), 26)
        # TODO: go back and fix this ^ datetimestamp test to work with both mongo and mongomock
        self.assertEqual(event_dict['job'], 'test-job')
        self.assertEqual(event_dict['result'], 0)
        self.assertEqual(event_dict['value'], 42)
        self.assertEqual(event_dict['extra_text'], 'särskild')
