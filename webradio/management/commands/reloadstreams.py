from django.core.management.base import BaseCommand
from webradio.models import Station


class Command(BaseCommand):
    help = "Reloads all streams from all stations."

    def handle(self, *args, **options):
        verbosity = int(options.get('verbosity', 1))
        for my_station in Station.objects.all():
            if verbosity > 0:
                self.stdout.write(
                    "Refreshing streams of station \"%s\"." %
                    my_station)
            my_station.refresh_streams()
