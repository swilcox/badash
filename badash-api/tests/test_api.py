import hug

from app import api


def test_api():
    resp = hug.test.get(api, url='/dashboards')
    assert resp.status == hug.HTTP_200
    assert resp.data == {'dashboard_list': []}
