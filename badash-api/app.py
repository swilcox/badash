"""Hug app"""
import mongoengine
import hug
from settings import settings
from models import Dashboard, Job, Event


mongoengine.connect(host=settings.MONGODB_URI)

api = hug.API(__name__)


@hug.exception(mongoengine.DoesNotExist)
def handle_does_not_exist(exception, response=None):
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
def dashboards_post(response, title: str, slug='', description='', jobs=None):
    """create new dashboard"""
    dashboard = Dashboard.objects.create(
        title=title,
        slug=slug,
        description=description,
        jobs=jobs if jobs else list()
    )
    response.status = hug.falcon.HTTP_201
    return dashboard.to_dict()


@hug.get(('/jobs', '/jobs/{job_slug}/'))
def jobs_get(job_slug='', page_size=settings.DEFAULT_PAGE_SIZE, page_number=1):
    """jobs view"""
    if job_slug:
        j = Job.objects.get(slug=job_slug)
        return j.to_dict(page_size=page_size, page_number=page_number)
    else:
        return {'job_list': [j.to_dict() for j in Job.objects.skip((page_number - 1) * page_size).limit(page_size)]}


@hug.post('/jobs', status=hug.HTTP_201)
def jobs_post(title: str, description='', slug='', config=None):
    """create a new Job"""
    job = Job.objects.create(
        title=title,
        slug=slug,
        description=description,
        config=config if config else dict(),
    )
    return job.to_dict()


@hug.put('/jobs/{job_slug}')
def jobs_put(job_slug: str, title: str, description: str, config: dict):
    """Update a job"""
    job = Job.objects.get(slug=job_slug)
    job.title = title
    job.description = description
    job.config = config
    job.save()
    return job.to_dict()


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
