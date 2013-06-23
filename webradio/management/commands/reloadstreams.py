from django.core.management.base import NoArgsCommand
from webradio.models import Station

class Command(NoArgsCommand):
    help = "Reloads all streams from all stations."
    
    def handle_noargs(self, **options):
        verbosity = int(options.get('verbosity', 1))
        for my_station in Station.objects.all():
            if verbosity > 0:
                self.stdout.write("Refreshing streams of station \"%s\"." %my_station)
            my_station.refresh_streams()