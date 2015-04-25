# coding=utf-8
from __future__ import unicode_literals

from django.core.exceptions import ValidationError


class RangeValidator(object):
    def __init__(self, min_value, max_value):
        self.min_value = min_value
        self.max_value = max_value

    def __call__(self, value):
        if value < self.min_value or value > self.max_value:
                raise ValidationError(u"Значение должно быть в диапазоне от %s до %s (сейчас: %s)" %
                                      (self.min_value, self.max_value, value))