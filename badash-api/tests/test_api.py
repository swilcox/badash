"""test_api.py"""
import json

import hug

from app import api
from models import Dashboard, Job, Event
from .base_testcase import ApiTestCase


class TestApi(ApiTestCase):
    """Test Event API calls class"""

    def setUp(self):
        self.job = Job.objects.create(
            slug='test-job',
            title='Test Job',
            config={'display_field': 'value'}
        )
        self.event_1 = Event.objects.create(job=self.job, result=0, value=40)
        self.event_2 = Event.objects.create(job=self.job, result=0, value=42, extra_text='särskild')
        self.event_3 = Event.objects.create(job=self.job, result=0, value=64)
        self.dashboard = Dashboard.objects.create(
            slug='test-dashboard',
            title='Test Dashboard'
        )
        self.dashboard.jobs.append(self.job)
        self.dashboard.save()

    def tearDown(self):
        Event.drop_collection()
        Dashboard.drop_collection()
        Job.drop_collection()

    def test_event_api(self):
        """test event api"""
        self.assertEqual(hug.test.get(api, url='/events').status, hug.HTTP_405)
        self.assertEqual(hug.test.put(api, url='/events').status, hug.HTTP_405)
        self.assertEqual(hug.test.patch(api, url='/events').status, hug.HTTP_405)
        self.assertEqual(hug.test.delete(api, url='/events').status, hug.HTTP_405)
        self.assertEqual(hug.test.post(api, url='/events').status, hug.HTTP_400)
        resp = hug.test.post(api, url='/events', params={'job': 'test-job', 'result': 0})
        self.assertEqual(resp.status, hug.HTTP_201)
        self.assertEqual(Event.objects.filter(job=self.job).count(), 4)

    def test_dashboards_api(self):
        self.assertEqual(hug.test.patch(api, url='/dashboards').status, hug.HTTP_405)
        self.assertEqual(hug.test.delete(api, url='/dashboards').status, hug.HTTP_405)
        self.assertEqual(hug.test.put(api, url='/dashboards').status, hug.HTTP_405)
        self.assertEqual(hug.test.post(api, url='/dashboards').status, hug.HTTP_400)
        resp = hug.test.get(api, url='/dashboards')
        self.assertEqual(resp.status, hug.HTTP_200)
        self.assertEqual(len(resp.data['dashboard_list']), 1)
        self.assertEqual(resp.data['dashboard_list'][0]['slug'], 'test-dashboard')
        self.assertEqual(hug.test.post(api, url='/dashboards').status, hug.HTTP_400)

    def test_dashboard_object_api(self):
        self.assertEqual(hug.test.put(api, url='/dashboards/not-a-dashboard').status, hug.HTTP_400)
        self.assertEqual(hug.test.get(api, url='/dashboards/not-a-dashboard').status, hug.HTTP_404)
        self.assertEqual(hug.test.delete(api, url='/dashboards/not-a-dashboard').status, hug.HTTP_404)
        self.assertEqual(hug.test.patch(api, url='/dashboards/test-dashboard').status, hug.HTTP_405)      
        self.assertEqual(hug.test.put(api, url='/dashboards/test-dashboard').status, hug.HTTP_400)
        resp = hug.test.put(
            api,
            url='/dashboards/test-dashboard',
            title='My Test Dashboard',
            jobs=['test-job'],
            description='Just another test!'
        )
        self.assertEqual(resp.status, hug.HTTP_200)
        self.assertEqual(resp.data, Dashboard.objects.get(slug='test-dashboard').to_dict())
        self.assertEqual(hug.test.delete(api, url='/dashboards/test-dashboard').status, hug.HTTP_200)
        self.assertEqual(Dashboard.objects.all().count(), 0)
        resp = hug.test.post(
            api,
            url='/dashboards',
            title='My Test Dashboard',
            jobs=['test-job'],
            description='Just another test!'
        )
        self.assertEqual(resp.status, hug.HTTP_201)
        self.assertEqual(Dashboard.objects.all().count(), 1)

def test_api():
    resp = hug.test.get(api, url='/dashboards')
    assert resp.status == hug.HTTP_200
    assert resp.data == {'dashboard_list': []}


def test_dashboards_delete():
    # make sure delete works...
    # make sure delete doesn't delete jobs
    pass


def test_dashboards_get():
    # get all vs. get specific one
    pass

def test_dashboards_post():
    # post a new dashboard
    pass

def test_dashboards_put():
    # put an update
    pass

def test_jobs_get():
    # get a single job
    # get all jobs
    pass

def test_jobs_post():
    pass

def test_jobs_put():
    pass

def test_jobs_delete():
    pass

def test_event_post():
    pass
