"""Hug app"""
from marshmallow import fields
import mongoengine
import hug
from settings import settings
from models import Dashboard, Job, Event


mongoengine.connect(host=settings.MONGODB_URI)

api = hug.API(__name__)
api.http.add_middleware(hug.middleware.CORSMiddleware(api, max_age=10))


@hug.exception(mongoengine.DoesNotExist)
def handle_does_not_exist(exception, response=None):
    """object doesn't exist exception handler"""
    if response:
        response.status = hug.falcon.HTTP_404
    return {'error': str(exception)}


@hug.get(('/dashboards', '/dashboards/{dashboard_slug}/'))
def dashboards_get(dashboard_slug=''):
    """dashboards view"""
    if dashboard_slug:
        d = Dashboard.objects.get(slug=dashboard_slug)
        return d.to_dict()
    else:
        return {'dashboard_list': [d.to_dict() for d in Dashboard.objects.all()]}


@hug.post('/dashboards', status=hug.HTTP_201)
def dashboards_post(response, title: str, jobs: hug.types.multiple, slug='', description=''):
    """create new dashboard"""
    dashboard = Dashboard.objects.create(
        title=title,
        slug=slug,
        description=description,
        jobs=[Job.objects.get(slug=j) for j in jobs] if jobs else list()
    )
    response.status = hug.falcon.HTTP_201
    return dashboard.to_dict()


@hug.put('/dashboards/{dashboard_slug}/')
def dashboards_put(dashboard_slug: str, title: str, description: str, jobs: hug.types.multiple):
    """update a dashboard"""
    dashboard = Dashboard.objects.get(slug=dashboard_slug)
    dashboard.title = title
    dashboard.description = description
    dashboard.jobs = [Job.objects.get(slug=j) for j in jobs]
    dashboard.save()
    return dashboard.to_dict()


@hug.delete('/dashboards/{dashboard_slug}/')
def dashboards_delete(dashboard_slug: str):
    """delete a dashboard"""
    dashboard = Dashboard.objects.get(slug=dashboard_slug)
    dashboard.delete()
    return {'status': 'deleted', 'slug': dashboard_slug}


@hug.get(('/jobs', '/jobs/{job_slug}'))
def jobs_get(job_slug='', page_size=settings.DEFAULT_PAGE_SIZE, page_number=1):
    """jobs view"""
    if job_slug:
        j = Job.objects.get(slug=job_slug)
        return j.to_dict(page_size=page_size, page_number=page_number)
    else:
        return {'job_list': [j.to_dict() for j in Job.objects.skip((page_number - 1) * page_size).limit(page_size)]}


@hug.post('/jobs', status=hug.HTTP_201)
def jobs_post(title: str, config: hug.types.json = None, description='', slug=''):
    """create a new Job"""
    job = Job.objects.create(
        title=title,
        slug=slug,
        description=description,
        config=config if config else dict(),
    )
    return job.to_dict()


@hug.put('/jobs/{job_slug}')
def jobs_put(job_slug: str, title: str, description: str, config: hug.types.json = None):
    """Update a job"""
    job = Job.objects.get(slug=job_slug)
    job.title = title
    job.description = description
    job.config = config if config else dict()
    job.save()
    return job.to_dict()


@hug.delete('/jobs/{job_slug}')
def jobs_delete(job_slug: str):
    """Update a job"""
    job = Job.objects.get(slug=job_slug)
    job.delete()
    return {'status': 'deleted', 'slug': job_slug}


@hug.post('/events', status=hug.HTTP_201)
def events_post(job: str, result: int, **kwargs):
    """create a new event"""
    event_job = Job.objects.get(slug=job)
    event = Event.objects.create(
        job=event_job,
        result=result,
        **kwargs
    )
    return event.to_dict()
