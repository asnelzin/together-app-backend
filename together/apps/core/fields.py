# coding: utf-8
from __future__ import unicode_literals

from django.db.models import DecimalField
from together.apps.core.validators import RangeValidator


class LatLngField(DecimalField):
    def __init__(self, *args, **kwargs):
        defaults = {'max_digits': 10, 'decimal_places': 6}
        defaults.update(kwargs)
        super(LatLngField, self).__init__(*args, **defaults)

class LatField(LatLngField):
    default_validators = [RangeValidator(-90, 90)]


class LngField(LatLngField):
    default_validators = [RangeValidator(-180, 180)]