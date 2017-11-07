import hug

from app import api


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
