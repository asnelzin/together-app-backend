# coding=utf-8
from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from together.apps.core.fields import LatField, LngField


@python_2_unicode_compatible
class User(models.Model):
    name = models.CharField('Имя', max_length=200)
    current_room = models.ForeignKey(Room, null=True, blank=True)
    latitude = LatField('Широта', blank=True, null=True)
    longitude = LngField('Долгота', blank=True, null=True)

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    def __str__(self):
        return self.title


@python_2_unicode_compatible
class Room(models.Model):
    creator = models.ForeignKey(User, 'Создатель комнаты', null=True, blank=True)
    password = models.CharField('Пароль', max_length=50)

    class Meta:
        verbose_name = 'комната'
        verbose_name_plural = 'комнаты'

    def __str__(self):
        return self.pk

    def get_absolute_url(self):
        pass
