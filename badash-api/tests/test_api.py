"""test_api.py"""
import json

import hug
import jwt

from app import api
from models import Dashboard, Job, Event, ApiKey
from .base_testcase import ApiTestCase
from settings import settings


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
        self.api_key = ApiKey.objects.create(
            user='test',
            api_key='my-test-key'
        )
        self.token = jwt.encode({'user': 'me'}, settings.JWT_SECRET)

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
        self.assertEqual(hug.test.post(api, url='/events').status, hug.HTTP_401)
        resp = hug.test.post(api, url='/events', params={'job': 'test-job', 'result': 0})
        self.assertEqual(resp.status, hug.HTTP_401)
        resp = hug.test.post(
            api,
            url='/events',
            headers={'X-Api-Key': 'bad-key'},
            params={'job': 'test-job', 'result': 0}
        )
        self.assertEqual(resp.status, hug.HTTP_401)
        resp = hug.test.post(
            api,
            url='/events',
            headers={'X-Api-Key': 'my-test-key'},
            params={'job': 'test-job', 'result': 0}
        )
        self.assertEqual(resp.status, hug.HTTP_201)
        self.assertEqual(Event.objects.filter(job=self.job).count(), 4)

    def test_dashboards_api(self):
        """test dashboards (all) endpoint"""
        # test invalid methods and bad calls
        self.assertEqual(hug.test.patch(api, url='/dashboards').status, hug.HTTP_405)
        self.assertEqual(hug.test.delete(api, url='/dashboards').status, hug.HTTP_405)
        self.assertEqual(hug.test.put(api, url='/dashboards').status, hug.HTTP_405)
        self.assertEqual(hug.test.post(api, url='/dashboards').status, hug.HTTP_401)
        self.assertEqual(hug.test.post(api, url='/dashboards', headers={'X-Api-Key': 'my-test-key'}).status, hug.HTTP_400)
        # test GET
        resp = hug.test.get(api, url='/dashboards')
        self.assertEqual(resp.status, hug.HTTP_200)
        self.assertEqual(len(resp.data['dashboard_list']), 1)
        self.assertEqual(resp.data['dashboard_list'][0]['slug'], 'test-dashboard')
        # test GET of Empty Dashboards
        Dashboard.objects.first().delete()
        resp = hug.test.get(api, url='/dashboards')
        self.assertEqual(resp.status, hug.HTTP_200)
        self.assertEqual(len(resp.data['dashboard_list']), 0)

    def test_dashboard_object_api(self):
        """test single dashboard object related api calls."""
        # test invalid methods and/or non-existent items
        self.assertEqual(hug.test.put(api, url='/dashboards/not-a-dashboard', headers={'X-Api-Key': 'my-test-key'}).status, hug.HTTP_400)
        self.assertEqual(hug.test.get(api, url='/dashboards/not-a-dashboard', headers={'X-Api-Key': 'my-test-key'}).status, hug.HTTP_404)
        self.assertEqual(hug.test.delete(api, url='/dashboards/not-a-dashboard', headers={'X-Api-Key': 'my-test-key'}).status, hug.HTTP_404)
        self.assertEqual(hug.test.patch(api, url='/dashboards/test-dashboard').status, hug.HTTP_405)
        self.assertEqual(hug.test.put(api, url='/dashboards/test-dashboard').status, hug.HTTP_401)
        self.assertEqual(hug.test.put(api, url='/dashboards/test-dashboard', headers={'X-Api-Key': 'my-test-key'}).status, hug.HTTP_400)
        # PUT test
        resp = hug.test.put(
            api,
            headers={'X-Api-Key': 'my-test-key'},
            url='/dashboards/test-dashboard',
            title='My Test Dashboard',
            jobs=['test-job'],
            description='Just another test!'
        )
        self.assertEqual(resp.status, hug.HTTP_200)
        self.assertEqual(resp.data, Dashboard.objects.get(slug='test-dashboard').to_dict())
        # DELETE test
        self.assertEqual(hug.test.delete(api, url='/dashboards/test-dashboard', headers={'X-Api-Key': 'my-test-key'}).status, hug.HTTP_200)
        self.assertEqual(Dashboard.objects.all().count(), 0)
        # POST test
        resp = hug.test.post(
            api,
            headers={'X-Api-Key': 'my-test-key'},
            url='/dashboards',
            title='Test Dashboard',
            jobs=['test-job'],
            description='Just another test!'
        )
        self.assertEqual(resp.status, hug.HTTP_201)
        self.assertEqual(Dashboard.objects.all().count(), 1)
        # GET test
        resp = hug.test.get(api, url='/dashboards/test-dashboard')
        self.assertEqual(resp.status, hug.HTTP_200)
        self.assertEqual(resp.data, Dashboard.objects.first().to_dict())

    def test_dashboard_duplicate(self):
        """test that we can't create a duplicate dashboard"""
        resp = hug.test.post(
            api,
            headers={'X-Api-Key': 'my-test-key'},
            url='/dashboards',
            title='Test Dashboard',
            slug='test-dashboard',  # dupe!
            jobs=['test-job'],
            description='Just another test!'
        )
        self.assertEqual(resp.status, hug.HTTP_409)

    def test_jobs_api(self):
        """test jobs (all) api"""
        # test invalid methods and calls
        self.assertEqual(hug.test.patch(api, url='/jobs').status, hug.HTTP_405)
        self.assertEqual(hug.test.delete(api, url='/jobs').status, hug.HTTP_405)
        self.assertEqual(hug.test.put(api, url='/jobs').status, hug.HTTP_405)
        self.assertEqual(hug.test.post(api, url='/jobs', headers={'X-Api-Key': 'my-test-key'}).status, hug.HTTP_400)
        # GET test
        resp = hug.test.get(api, url='/jobs')
        self.assertEqual(resp.status, hug.HTTP_200)
        self.assertEqual(len(resp.data['job_list']), 1)
        self.assertEqual(resp.data['job_list'][0], self.job.to_dict())
        # GET empty test
        self.job.delete()
        resp = hug.test.get(api, url='/jobs')
        self.assertEqual(resp.status, hug.HTTP_200)
        self.assertEqual(resp.data['job_list'], [])
        # POST test
        resp = hug.test.post(
            api,
            headers={'X-Api-Key': 'my-test-key'},
            url='/jobs',
            title='Test Job',
            description='This is a Test Job',
            config='{"my_option": "hello world"}'
        )
        self.assertEqual(resp.status, hug.HTTP_201)
        self.assertEqual(resp.data, Job.objects.get(slug='test-job').to_dict())
        self.assertEqual(resp.data['config'], {'my_option': 'hello world'})
    
    def test_job_duplicate(self):
        """make sure we can't post a duplicate"""
        resp = hug.test.post(
            api,
            headers={'X-Api-Key': 'my-test-key'},
            url='/jobs',
            title='Test Job',
            slug='test-job',  # duplicate!
            description='This is a Test Job',
            config='{"my_option": "hello world"}'
        )
        self.assertEqual(resp.status, hug.HTTP_409)
        self.assertEqual(
            resp.data,
            {'error': 'Tried to save duplicate unique keys (Duplicate Key Error)'}
        )

    def test_job_object_api(self):
        """test single job object api"""
        # test invalid methods and calls
        self.assertEqual(hug.test.patch(api, url='/jobs/test-job').status, hug.HTTP_405)
        self.assertEqual(hug.test.put(api, url='/jobs/test-job', headers={'X-Api-Key': 'my-test-key'}).status, hug.HTTP_400)
        self.assertEqual(hug.test.post(api, url='/jobs/test-job').status, hug.HTTP_405)
        # GET Test
        resp = hug.test.get(
            api,
            url='/jobs/test-job'
        )
        self.assertEqual(resp.status, hug.HTTP_200)
        self.assertEqual(resp.data, self.job.to_dict())
        # PUT Test
        resp = hug.test.put(
            api,
            headers={'X-Api-Key': 'my-test-key'},
            url='/jobs/test-job',
            title='Changing my title',
            description='this is my new description'
        )
        self.assertEqual(resp.status, hug.HTTP_200)
        self.assertEqual(resp.data['title'], 'Changing my title')
        self.assertEqual(resp.data['description'], 'this is my new description')
        self.assertEqual(resp.data['config'], {})
        # DELETE Test
        self.assertEqual(hug.test.delete(api, url='/jobs/test-job', headers={'X-Api-Key': 'my-test-key'}).status, hug.HTTP_200)
        self.assertEqual(Job.objects.all().count(), 0)
        self.assertEqual(Event.objects.all().count(), 0)
    
    def test_api_keys_api(self):
        """test api_keys endpoint(s)"""
        self.assertEqual(hug.test.patch(api, url='/api_keys').status, hug.HTTP_405)
        self.assertEqual(hug.test.delete(api, url='/api_keys').status, hug.HTTP_405)
        self.assertEqual(hug.test.get(api, url='/api_keys').status, hug.HTTP_401)
        self.assertEqual(hug.test.put(api, url='/api_keys').status, hug.HTTP_405)
        self.assertEqual(hug.test.post(api, url='/api_keys').status, hug.HTTP_401)
        self.assertEqual(
            hug.test.post(
                api,
                url='/api_keys',
                headers={'Authorization': self.token}
            ).status,
            hug.HTTP_201
        )
        self.assertEqual(ApiKey.objects.all().count(), 2)
        resp = hug.test.get(api, url='/api_keys', headers={'Authorization': self.token})
        self.assertEqual(resp.status, hug.HTTP_200)
        self.assertEqual(resp.data, [ApiKey.objects.filter(user='me').first().to_dict()])
