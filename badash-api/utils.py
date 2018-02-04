"""utils.py"""
from datetime import datetime

from slugify import slugify as _slugify
import bson


def slugify(input_string):
    """custom slugify"""
    return _slugify(input_string)


def utcnow():
    """Quick UTC Now for default purposes"""
    return datetime.utcnow().replace(tzinfo=bson.utc)
