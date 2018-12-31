from django.urls import path
from . import views

urlpatterns = [
    path(r'^$', views.index, name='home'),
    path(r'^stations/$', views.stations, name='webradio_stations'),
    path(r'^player/$', views.player, name='webradio_player'),
    path(r'^controls/play/(\d+)/$', views.control_play_station),
    path(r'^controls/playpause/$', views.control_play_pause),
    path(r'^controls/nextstation/$', views.control_station_next),
    path(r'^controls/previousstation/$', views.control_station_previous),
    path(r'^controls/info/$', views.control_get_info),
]
