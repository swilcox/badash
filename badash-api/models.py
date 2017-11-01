"""Models
"""
import json
from mongoengine import (
    Document,
    DynamicDocument,
    fields
)

from utils import utcnow, slugify
from settings import settings


class Job(Document):
    """Job Model"""
    slug = fields.StringField(default=None)
    title = fields.StringField()
    description = fields.StringField()
    config = fields.DictField()

    def __str__(self):
        return self.title

    def to_dict(self, page_size=settings.DEFAULT_PAGE_SIZE, page_number=1):
        return {
            'slug': self.slug,
            'title': self.title,
            'description': self.description,
            'config': self.config,
            'events': [event.to_dict() for event in Event.objects.filter(job=self).skip((page_number - 1) * page_size).limit(page_size)]
            #'events': [event.to_dict() for event in Event.objects.filter(job=self).skip((page_number - 1) * page_size).limit(page_size)]
        }

    @property
    def display_field(self):
        return self.config.get('display_field')

    def clean(self):
        if not self.slug:
            self.slug = slugify(self.title)


class Dashboard(Document):
    """Dashboard Model"""
    slug = fields.StringField(default=None)
    title = fields.StringField()
    description = fields.StringField()
    jobs = fields.ListField(fields.ReferenceField)

    def __str__(self):
        return self.title

    def clean(self):
        if not self.slug:
            self.slug = slugify(self.title)

    def to_dict(self):
        return {
            'slug': self.slug,
            'title': self.title,
            'description': self.description,
            'jobs': [job.to_dict() for job in self.jobs]
        }


class Event(DynamicDocument):
    """Event Model"""
    job = fields.ReferenceField(Job, related_name='events')
    result = fields.IntField()
    datetimestamp = fields.DateTimeField(default=utcnow)

    meta = {
        'ordering': ['-datetimestamp']
    }

    @property
    def display_field(self):
        if self.job.display_field:
            return self.__dict__.get(self.job.display_field)
        else:
            return None

    def __str__(self):
        return "{} {}: {} ({})".format(self.job, self.datetimestamp, self.result, self.display_field)

    def to_dict(self):
        result_dict = json.loads(self.to_json())
        result_dict.update({
            'datetimestamp': str(self.datetimestamp.isoformat()),
            '_id': str(self.id),
            'job': self.job.slug
        })
        return result_dict