from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
import json
from webradio.models import Station, Category
from webradio.players import get_player_instance


def index(request):
    return HttpResponseRedirect('./player/')


def player(request):
    stations = Station.objects.all()
    p = get_player_instance()
    return render(request, 'webradio/player.html',
                  {'stations': stations, 'player': p})


def stations(request):
    categories = Category.objects.all()
    stations = Station.objects.all()
    return render(request, 'webradio/stations.html',
                  {'categories': categories, 'stations': stations, })


def control_get_info(request):
    """
    Returns information about the currently played back station/track.
    
    @return: JSON
    """
    p = get_player_instance()
    station = p.get_current_station()
    info = {}
    info['title'] = p.get_now_playing()

    if station is None:
        info['station'] = 'No Station'
    else:
        info['station'] = station.name

    info['is_playing'] = p.is_playing()
    return HttpResponse(json.dumps(info), content_type="application/json")


def control_play_station(request, station_id):
    station = get_object_or_404(Station, pk=station_id)
    station.play()
    return HttpResponseRedirect(reverse('webradio:player'))


def control_play_pause(request):
    p = get_player_instance()
    p.play_pause()
    return HttpResponseRedirect(reverse('webradio:player'))


def control_station_next(request):
    """
    Plays the next station.
    """
    if Station.objects.count() == 0:
        return HttpResponseRedirect(reverse('webradio:player'))

    p = get_player_instance()
    current_station = p.get_current_station()
    try:
        next_station = \
        Station.objects.filter(id__gt=current_station.id).order_by('id')[0]
    except:
        next_station = Station.objects.all().order_by('id')[0]

    next_station.play()
    return HttpResponseRedirect(reverse('webradio:player'))


def control_station_previous(request):
    """
    Plays the previous station.
    """
    if Station.objects.count() == 0:
        return HttpResponseRedirect(reverse('webradio:player'))

    p = get_player_instance()
    current_station = p.get_current_station()
    try:
        previous_station = \
        Station.objects.filter(id__lt=current_station.id).order_by('-id')[0]
    except:
        previous_station = Station.objects.all().order_by('-id')[0]

    previous_station.play()
    return HttpResponseRedirect(reverse('webradio:player'))
