import re

from urllib.request import urlopen
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from webradio.players import get_player_instance


class Category(models.Model):
    """
    Can be used to group radio stations, e.g. by genre.
    """
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ['name']
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    def get_stations(self):
        return Station.objects.filter(category=self)


class Station(models.Model):
    """
    Represents a web radio station.
    """
    name = models.CharField(max_length=100, unique=True)
    playlist = models.URLField(unique=True)
    category = models.ForeignKey(
        Category, blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    def get_default_stream(self):
        """
        Returns the default stream associated with the station.
        """
        try:
            return Stream.objects.get(station=self, default=True)
        except:
            return None

    def play(self):
        """
        Plays this station.
        """
        p = get_player_instance()
        return p.play_station(self)

    def refresh_streams(self):
        """
        Loads and parses the playlist.
        """
        response = urlopen(self.playlist, timeout=10)
        if not response:
            return

        pattern_file = r'^file(\d+)\s?='
        pattern_title = r'^title(\d+)\s?='

        urls = {}
        titles = {}

        for line in response.read().decode("utf-8").splitlines():
            line = line.lower()

            if re.match(pattern_file, line):
                stream_id = re.findall(pattern_file, line)[0]
                stream_url = re.sub(pattern_file, '', line, count=1).strip()
                urls[stream_id] = stream_url
            elif re.match(pattern_title, line):
                stream_id = re.findall(pattern_title, line)[0]
                stream_title = re.sub(pattern_title, '', line, count=1).strip()
                titles[stream_id] = stream_title

        for stream_id in urls:
            stream = Stream.objects.get_or_create(
                url=urls[stream_id],
                station=self
            )[0]
            if stream_id in titles:
                name = titles[stream_id]
            else:
                # Some playlists do not include titles for files
                name = "Stream %s" % stream_id

            if stream.name != name:
                stream.name = name
                stream.save()

        Stream.objects.filter(station=self).exclude(
            url__in=urls.values()).delete()
        if Stream.objects.filter(station=self).count() == 1 and not stream.default:
            Stream.objects.filter(station=self).update(default=True)


class Stream(models.Model):
    """
    A stream of a particular radio stations. Streams are discovered
    automatically by parsing the playlist of a station.
    """
    name = models.CharField(max_length=100, default='')
    url = models.URLField(unique=True)
    default = models.BooleanField(default=False)
    station = models.ForeignKey(Station, on_delete=models.CASCADE)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    def clean(self):
        # Make sure there is only one default stream per station
        if self.default:
            Stream.objects.filter(station=self.station).exclude(
                id=self.id).update(default=False)


@receiver(post_save, sender=Station)
def _refresh_streams(instance, **kwargs):
    """
    Refreshes all the streams from the radio station.
    """
    instance.refresh_streams()
