from django.conf.urls import patterns, url

urlpatterns = patterns('webradio.views',
    url(r'^$', 'index', name='home'),
    url(r'^stations/$', 'stations', name='webradio_stations'),
    url(r'^player/$', 'player', name='webradio_player'),
    url(r'^controls/play/(\d+)/$', 'control_play_station'),
    url(r'^controls/playpause/$', 'control_play_pause'),
    url(r'^controls/nextstation/$', 'control_station_next'),
    url(r'^controls/previousstation/$', 'control_station_previous'),    
    url(r'^controls/info/$', 'control_get_info'),

)