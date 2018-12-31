from django.urls import path
from . import views

app_name = 'webradio'

urlpatterns = [
    path('', views.index, name='home'),
    path('stations/', views.stations, name='stations'),
    path('player/', views.player, name='player'),
    path('controls/play/<int:station_id>/', views.control_play_station,
         name='control_play_station'),
    path('controls/playpause/', views.control_play_pause,
         name='control_play_pause'),
    path('controls/nextstation/', views.control_station_next,
         name='control_station_next'),
    path('controls/previousstation/', views.control_station_previous,
         name='control_station_previous'),
    path('controls/info/', views.control_get_info, name='control_get_info'),
]
