# coding=utf-8
from __future__ import unicode_literals

import json

from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from django.views.generic import View
from together.apps.api.forms import NamePasswordForm, NamePassCoordForm
from together.apps.rooms.models import Room, User


class JSONMixin():
    def get_form_errors(self, form):
        return dict([(k, [unicode(e) for e in v]) for k, v in form.errors.items()])

    def data_to_json(self, context_dict):
        return json.dumps(context_dict, cls=DjangoJSONEncoder)

    def handle_400(self, context_dict):
        json_content = self.data_to_json(context_dict)
        return HttpResponse(json_content, content_type='application/json', status=400)


class CreateRoom(View, JSONMixin):
    def get_json_response(self):
        if self.form.is_valid():
            name, password = self.form.data['name'], self.form.data['password']
            if Room.objects.filter(password=password).exists():
                return self.handle_400({'password': 'Комната с таким паролем уже существует'})
            room = Room(password=password)
            room.save()
            user = User(name=name, current_room=room)
            user.save()
            return HttpResponse("{}", content_type='application/json', status=200)
        return self.handle_400(self.get_form_errors(self.form))

    def post(self, request, *args, **kwargs):
        self.form = NamePasswordForm(json.loads(request.body))
        return self.get_json_response()


class JoinRoom(View, JSONMixin):
    def get_json_response(self):
        if self.form.is_valid():
            name, password = self.form.data['name'], self.form.data['password']
            room_qs = Room.objects.filter(password=password)
            if not room_qs.exists():
                return self.handle_400({'password': 'Комнаты с таким паролем не существует'})

            user_names = User.objects.filter(current_room__password=password).values_list('name', flat=True)
            if name not in user_names:
                user = User(name=name, current_room=room_qs[0])
                user.save()
            else:
                return self.handle_400({'name': 'Пользователь с таким именем уже есть в комнате'})
            return HttpResponse("{}", content_type='application/json', status=200)
        return self.handle_400(self.get_form_errors(self.form))

    def post(self, request, *args, **kwargs):
        self.form = NamePasswordForm(json.loads(request.body))
        return self.get_json_response()


class UpdateCoordinates(View, JSONMixin):
    def get_json_response(self):
        if self.form.is_valid():
            name, latitude, longitude = self.form.data['name'], self.form.data['latitude'], self.form.data['longitude']
            user_qs = User.objects.filter(name=name)
            if not user_qs.exists():
                return self.handle_400({'name': 'Пользователя с таким именем не существует'})
            user_qs.update(latitude=latitude, longitude=longitude)
            return HttpResponse("{}", content_type='application/json', status=200)
        return self.handle_400(self.get_form_errors(self.form))

    def post(self, request, *args, **kwargs):
        self.form = NamePassCoordForm(json.loads(request.body))
        return self.get_json_response()


class GetAllMembersCoordinates(View, JSONMixin):
    def get_json_response(self):
        if self.form.is_valid():
            name, password = self.form.data['name'], self.form.data['password']
            user_qs = User.objects.filter(name=name)
            if not user_qs.exists():
                return self.handle_400({'name': 'Пользователя с таким именем не существует'})
            room_qs = Room.objects.filter(password=password)
            if not room_qs.exists():
                return self.handle_400({'password': 'Комнаты с таким паролем не существует'})

            context_dict = [
                {
                    'name': user.name,
                    'coordinates': {'latitude': user.latitude, 'longitude': user.longitude}
                }
                for user in User.objects.filter(current_room__password=password).exclude(name=name)
            ]

            json_content = self.data_to_json(context_dict)
            return HttpResponse(json_content, content_type='application/json', status=200)
        return self.handle_400(self.get_form_errors(self.form))

    def get(self, request, *args, **kwargs):
        self.form = NamePasswordForm(request.GET)
        return self.get_json_response()




