from django.db import models
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

    def __str__(self):
        return self.name

    def get_stations(self):
        return Station.objects.filter(category=self)


class Station(models.Model):
    """
    Represents a web radio station.
    """
    name = models.CharField(max_length=100, unique=True)
    url = models.URLField(unique=True)
    category = models.ForeignKey(
        Category, blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def play(self):
        """
        Plays this station.
        """
        p = get_player_instance()
        return p.play_station(self)
