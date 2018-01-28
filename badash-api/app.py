"""Hug app"""
import hug
import mongoengine

from settings import settings
from auth import authenticated, api_key_auth, jwt_auth
from models import Dashboard, Job, Event, ApiKey

mongoengine.connect(host=settings.MONGODB_URI)

api = hug.API(__name__)
api.http.add_middleware(hug.middleware.CORSMiddleware(api, max_age=10))


@hug.exception(mongoengine.DoesNotExist)
def handle_does_not_exist(exception, response=None):
    """object doesn't exist exception handler"""
    if response:
        response.status = hug.HTTP_404
    return {'error': str(exception)}


@hug.exception(mongoengine.NotUniqueError)
def handle_not_unique_error(exception, response=None):
    """duplicate object already exists handler"""
    if response:
        response.status = hug.HTTP_409
    return {'error': str(exception)}


@hug.get(('/dashboards', '/dashboards/{dashboard_slug}/'))
def dashboards_get(dashboard_slug: hug.types.text = ''):
    """dashboards view"""
    if dashboard_slug:
        dashboard = Dashboard.objects.get(slug=dashboard_slug)
        return dashboard.to_dict()
    else:
        return {'dashboard_list': [d.to_dict() for d in Dashboard.objects.all()]}


@hug.post('/dashboards', status=hug.HTTP_201, requires=authenticated)
def dashboards_post(title: hug.types.text, jobs: hug.types.multiple, slug: hug.types.text = '', description: hug.types.text = ''):
    """create new dashboard"""
    dashboard = Dashboard.objects.create(
        title=title,
        slug=slug,
        description=description,
        jobs=[Job.objects.get(slug=j) for j in jobs] if jobs else list()
    )
    return dashboard.to_dict()


@hug.put('/dashboards/{dashboard_slug}/', requires=authenticated)
def dashboards_put(dashboard_slug: hug.types.text, title: hug.types.text, description: hug.types.text, jobs: hug.types.multiple):
    """update a dashboard"""
    dashboard = Dashboard.objects.get(slug=dashboard_slug)
    dashboard.title = title
    dashboard.description = description
    dashboard.jobs = [Job.objects.get(slug=j) for j in jobs]
    dashboard.save()
    return dashboard.to_dict()


@hug.delete('/dashboards/{dashboard_slug}/', requires=authenticated)
def dashboards_delete(dashboard_slug: hug.types.text):
    """delete a dashboard"""
    dashboard = Dashboard.objects.get(slug=dashboard_slug)
    dashboard.delete()
    return {'status': 'deleted', 'slug': dashboard_slug}


@hug.get(('/jobs', '/jobs/{job_slug}'))
def jobs_get(job_slug: hug.types.text = '', page_size: hug.types.number = settings.DEFAULT_PAGE_SIZE, page_number: hug.types.number = 1):
    """jobs view"""
    if job_slug:
        j = Job.objects.get(slug=job_slug)
        return j.to_dict(page_size=page_size, page_number=page_number)
    else:
        return {'job_list': [j.to_dict() for j in Job.objects.skip((page_number - 1) * page_size).limit(page_size)]}


@hug.post('/jobs', status=hug.HTTP_201, requires=authenticated)
def jobs_post(title: hug.types.text, config: hug.types.json = None, description: hug.types.text = '', slug: hug.types.text = ''):
    """create a new Job"""
    job = Job.objects.create(
        title=title,
        slug=slug,
        description=description,
        config=config if config else dict(),
    )
    return job.to_dict()


@hug.put('/jobs/{job_slug}', requires=authenticated)
def jobs_put(job_slug: hug.types.text, title: hug.types.text, description: hug.types.text, config: hug.types.json = None):
    """Update a job"""
    job = Job.objects.get(slug=job_slug)
    job.title = title
    job.description = description
    job.config = config if config else dict()
    job.save()
    return job.to_dict()


@hug.delete('/jobs/{job_slug}', requires=authenticated)
def jobs_delete(job_slug: hug.types.text):
    """Update a job"""
    job = Job.objects.get(slug=job_slug)
    job.delete()
    return {'status': 'deleted', 'slug': job_slug}


@hug.post('/events', status=hug.HTTP_201, requires=api_key_auth)
def events_post(user: hug.directives.user, job: hug.types.text, result: hug.types.number, **kwargs):
    """create a new event"""
    event_job = Job.objects.get(slug=job)
    event = Event.objects.create(
        job=event_job,
        result=result,
        **kwargs
    )
    return event.to_dict()


@hug.post('/api_keys', status=hug.HTTP_201, requires=jwt_auth)
def api_keys_post(user: hug.directives.user):
    """create a new api_key for a user"""
    a_key = ApiKey.objects.create(user=user['user'])
    return a_key.to_dict()


@hug.get('/api_keys', requires=jwt_auth)
def api_keys_get(user: hug.directives.user):
    """get api_keys"""
    return [a_key.to_dict() for a_key in ApiKey.objects.filter(user=user['user'])]


@hug.cli()
def create_api_key(user='admin'):
    """create a new api_key"""
    a_key = ApiKey.objects.create(user=user)
    return a_key.to_dict()


if __name__ == '__main__':
    create_api_key.interface.cli()
