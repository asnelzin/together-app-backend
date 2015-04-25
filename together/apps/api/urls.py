from django.conf.urls import patterns, url

from together.apps.api.views import (CreateRoom, JoinRoom, UpdateCoordinates,
                                     GetAllMembersCoordinates)

urlpatterns = patterns(
    '',
    url(r'create/$', CreateRoom.as_view(), name='create_room'),
    url(r'join/$', JoinRoom.as_view(), name='join_room'),
    url(r'update/$', UpdateCoordinates.as_view(), name='update_coordinates'),
    url(r'get/$', GetAllMembersCoordinates.as_view(), name='get_all_coordinates'),
)