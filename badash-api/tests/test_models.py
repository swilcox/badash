"""test_models.py"""
import json

from mongoengine.errors import NotUniqueError

from models import Dashboard, Job, Event, ApiKey
from .base_testcase import ApiTestCase


class TestApiKey(ApiTestCase):
    """Test ApiKey related stuff"""

    def test_api_key_default(self):
        """test key defaulting works"""
        api_key = ApiKey.objects.create(user='me')
        self.assertNotEqual(api_key.api_key, '')

    def test_api_key_to_dict(self):
        """test to_dict output"""
        api_key = ApiKey.objects.create(user='me')
        self.assertEqual(
            api_key.to_dict(),
            {'user': 'me', 'api_key': api_key.api_key, '_id': str(api_key.id)}
        )


class TestModelCreation(ApiTestCase):
    """Test Model Creation"""

    def test_dashboard(self):
        """test creating a Dashboard model."""
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
        """test creating a Job model."""
        job = Job.objects.create(
            slug='test-job',
            title='Test Job'
        )
        self.assertEqual(str(job), 'Test Job')

    def test_event(self):
        """test creating an Event model."""
        job = Job.objects.create(slug='test-e-job', title='Test E Job')
        event = Event.objects.create(
            job=job,
            result=0,
            extra_value=42.2,
            text_value='särskild'
        )
        self.assertEqual(str(event), 'Test E Job {}: 0 (0)'.format(event.datetimestamp))
        self.assertEqual(event.extra_value, 42.2)
        self.assertEqual(event.text_value, 'särskild')

    def test_display_field(self):
        """test display_field property method"""
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


class TestDelete(ApiTestCase):
    """Test Deletion Logic"""
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
        cls.dashboard.save()

    def test_delete(self):
        """test delete cascade"""
        # dashboard deletes should not cascade
        self.assertEqual(1, Job.objects.all().count())
        self.dashboard.delete()
        self.assertEqual(1, Job.objects.all().count())
        # job deletes *should* cascade
        self.assertEqual(3, Event.objects.all().count())
        self.job.delete()
        self.assertEqual(0, Event.objects.all().count())


class TestToDict(ApiTestCase):
    """Test `to_dict` logic on Models"""
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
        """test job.to_dict() method"""
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

    def test_no_job_dupes(self):
        """test that we can't create duplicate jobs"""
        with self.assertRaises(NotUniqueError):
            Job.objects.create(
                title='Another test job',
                slug='test-job', # dupe!
                description='ha ha'
            )

    def test_dashboard(self):
        """test dashboard.to_dict() method"""
        dash_dict = self.dashboard.to_dict()
        self.assertEqual(dash_dict['title'], 'Test Dashboard')
        self.assertEqual(len(dash_dict['jobs']), 1)
        self.assertEqual(dash_dict['jobs'][0], self.job.to_dict())

    def test_no_dashboard_dupes(self):
        """test that we can't create a duplicate"""
        with self.assertRaises(NotUniqueError):
            Dashboard.objects.create(
                title='Dupe Dashboard',
                slug='test-dashboard', # dupe!
                description='Blah'
            )

    def test_event(self):
        """test event.to_dict() method"""
        event_dict = Event.objects.filter(job=self.job)[1].to_dict()
        self.assertEqual(len(event_dict['_id']), 24)
        # TODO: resolve differences between mongomock and regular mongo
        # self.assertEqual(len(event_dict['datetimestamp']), 27)
        self.assertEqual(event_dict['job'], 'test-job')
        self.assertEqual(event_dict['result'], 0)
        self.assertEqual(event_dict['value'], 42)
        self.assertEqual(event_dict['extra_text'], 'särskild')
