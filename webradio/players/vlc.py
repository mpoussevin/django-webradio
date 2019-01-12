import vlc
from webradio.players import AbstractAudioPlayer

META_TITLE = 0
META_ARTIST = 1
META_GENRE = 2
META_ALBUM = 4
META_DESCRIPTION = 6
META_NOW_PLAYING = 12


class VlcPlayer(AbstractAudioPlayer):
    """
    This is a wrapper class around VLC (through cttypes and libvlc).
    
    You need to place a vlc.py to webradio.players.contrib which
    matches your system's VLC version.
    
    See: http://liris.cnrs.fr/advene/download/python-ctypes/
    """

    def _setup_once(self):
        self.__media_set = False
        self._vlc_instance = vlc.Instance()
        self._player = self._vlc_instance.media_player_new()

    def play_station(self, station):
        self._station = station
        self._player.set_mrl(station.url)
        self.__media_set = True
        self._player.play()

    def get_now_playing(self):
        if not self.is_playing():
            return ''

        media = self._player.get_media()
        now_playing = media.get_meta(META_NOW_PLAYING)
        if now_playing is not None and now_playing != '':
            return now_playing

        title = media.get_meta(META_TITLE)
        if title is not None and title != '':
            return title

        return self._station.name

    def get_meta(self):
        media = self._player.get_media()
        meta = {}
        try:
            meta['title'] = media.get_meta(META_TITLE)
        except:
            return meta
        meta['artist'] = media.get_meta(META_ARTIST)
        meta['genre'] = media.get_meta(META_GENRE)
        meta['album'] = media.get_meta(META_ALBUM)
        meta['description'] = media.get_meta(META_DESCRIPTION)
        meta['now_playing'] = media.get_meta(META_NOW_PLAYING)
        return meta

    def is_playing(self):
        return self._player.is_playing() == 1

    def play(self):
        if not self.__media_set:
            return
        self._player.play()

    def stop(self):
        self._player.stop()
        self.__isplaying = False
