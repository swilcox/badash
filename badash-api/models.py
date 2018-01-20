"""Models
"""
import json
import secrets

from mongoengine import (
    Document,
    DynamicDocument,
    fields,
    CASCADE,
    PULL,
)

from utils import utcnow, slugify
from settings import settings


class Job(Document):
    """Job Model"""
    slug = fields.StringField(default=None, unique=True)
    title = fields.StringField()
    description = fields.StringField()
    config = fields.DictField()

    def __str__(self):
        return self.title

    def to_dict(self, page_size=settings.DEFAULT_PAGE_SIZE, page_number=1):
        """return a json serializable dictionary representation of the model instance."""
        return {
            'slug': self.slug,
            'title': self.title,
            'description': self.description,
            'config': self.config,
            'events': [event.to_dict() for event in Event.objects.filter(job=self).skip((page_number - 1) * page_size).limit(page_size)]
        }

    @property
    def display_field(self):
        """the display_field property."""
        return self.config.get('display_field')

    def clean(self):
        if not self.slug:
            self.slug = slugify(self.title)


class Dashboard(Document):
    """Dashboard Model"""
    slug = fields.StringField(default=None, unique=True)
    title = fields.StringField()
    description = fields.StringField()
    jobs = fields.ListField(fields.ReferenceField(Job, reverse_delete_rule=PULL))

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
    job = fields.ReferenceField(Job, related_name='events', reverse_delete_rule=CASCADE)
    result = fields.IntField()
    datetimestamp = fields.DateTimeField(default=utcnow)

    meta = {
        'ordering': ['-datetimestamp']
    }

    @property
    def display_field(self):
        """display field property."""
        if self.job.display_field:
            return self.__dict__.get(self.job.display_field)
        else:
            return self.result

    def __str__(self):
        return "{} {}: {} ({})".format(self.job, self.datetimestamp, self.result, self.display_field)

    def to_dict(self):
        """return model as a json serializable dictionary"""
        result_dict = json.loads(self.to_json())
        result_dict.update({
            'datetimestamp': str(self.datetimestamp.isoformat()) + 'Z',
            '_id': str(self.id),
            'job': self.job.slug,
            'display_field': self.display_field
        })
        return result_dict


class ApiKey(Document):
    """ApiKey Model"""
    api_key = fields.StringField(max_length=256, default=lambda: secrets.token_urlsafe())
    user = fields.StringField()
    meta = {
        'indexes': [
            'api_key'
        ]
    }

    def __str__(self):
        return '{} ({})'.format(self.api_key, self.user)

    def to_dict(self):
        """return model as a json serializable dictionary"""
        result_dict = json.loads(self.to_json())
        result_dict.update(
            {
                '_id': str(self.id)
            }
        )
        return result_dict
