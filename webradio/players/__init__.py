from django.conf import settings

class AbstractAudioPlayer(object):
    """Defines the basic interface for all audio players."""
    
    def __new__(cls, *args):
        """
        Singleton implementation.
        
        You shoud not override this method. 
        """
        if not '_my_instance' in cls.__dict__:
            cls._my_instance = object.__new__(cls)
        return cls._my_instance
 
    def __init__(self):
        """
        Makes sure that initialization is only performed once.
        
        You shoud not override this method. 
        """
        if not '_initialized' in dir(self):
            self._station = None
            self._setup_once()
            self._initialized = True   
    
    def _setup_once(self):
        """
        You may initialize your player instance through this method.
        """
        pass
    
    def play_station(self, station):
        self._station = station
        raise NotImplementedError
    
    def get_current_station(self):
        return self._station
    
    def get_now_playing(self):
        if not self.is_playing():
            return ''
        title = self.get_meta()['title']
        if title != '':
            return title
        else:
            return self._station.name

    def get_meta(self):
        raise NotImplementedError
    
    def is_playing(self):
        raise NotImplementedError
    
    def play_pause(self):
        if self.is_playing():
            self.stop()
        else:
            self.play()
    
    def play(self):
        raise NotImplementedError
    
    def stop(self):
        raise NotImplementedError


class PlayerLoader(object):
    PLAYER_INSTANCE = None
    
    @staticmethod
    def get_player_path():
        """ Returns the splitted path to the player class.
        
        The player class can be configured through the setting
        WEBRADIO_PLAYER_CLASS and defaults to webradio.players.vlc.VlcPlayer.
        """
        if hasattr(settings, 'WEBRADIO_PLAYER_CLASS'):
            return settings.WEBRADIO_PLAYER_CLASS.split('.')
        else:
            return 'webradio.players.vlc.VlcPlayer'.split('.')
    
    @classmethod
    def get_player_instance(cls):
        if cls.PLAYER_INSTANCE is None:
            player_path = cls.get_player_path()
            module_name = '.'.join(player_path[0:-1])
            class_name = player_path[-1]
            module = __import__(module_name, fromlist=[class_name])
            cls.PLAYER_INSTANCE = getattr(module, class_name)()
        return cls.PLAYER_INSTANCE      

def get_player_instance():
    """
    Should be used to get an instance of the currently configured
    audio player class.
    """
    return PlayerLoader.get_player_instance()
