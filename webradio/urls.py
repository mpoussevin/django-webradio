from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('stations/', views.stations, name='webradio_stations'),
    path('player/', views.player, name='webradio_player'),
    path('controls/play/(\d+)/', views.control_play_station),
    path('controls/playpause/', views.control_play_pause),
    path('controls/nextstation/', views.control_station_next),
    path('controls/previousstation/', views.control_station_previous),
    path('controls/info/', views.control_get_info),
]
