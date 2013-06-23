django-webradio
===============

A simple web-based GUI for playing and managing online radio streams.

Features:

* Simple UI, optimized for both desktop and mobile browsers
* Extendable Python backend
* Simple player backend API, so you can easily add your favorite player
* Supported players ATM:
    - VLC (headless version is fine)
* Basic HTTP-API can be used by external applications to interact with displays and h/w buttons 

Requirements
------------
* Django 1.4 or higher
* libvlc

Installation
------------
* Create a new Django project (or use an existing one)
* Add *webradio* to `settings.INSTALLED_APPS`
* Enable Django's built-in admin interface
* Include *webradio.urls* in your URL config
* Search for new static files (`./manage.py collectstatic`)
* *Optional:*
    - If you are **not** using VLC 2.0 download a version of vlc.py from http://liris.cnrs.fr/advene/download/python-ctypes/ and drop it into the directory *webradio/players/contrib*

Important
---------
When using the default VLC backend you cannot use multiple WSGI/fCGI threads, as every thread will use it's own VLC player instance, which will obviously break things. As long as you are only using Django's `runserver` command you are safe.

For the reference: I have deployed *django-webradio* with nginx and uWSGI and this is what a sample uWSGI configuration could look like:

```xml
<uwsgi>
  <socket>/var/run/uwsgi/django/uwsgi.sock</socket>
  <chdir>/srv/mydjangoproject/</chdir>
  <master/>
  <daemonize />
  <processes>1</processes>
  <threads>1</threads>
  <env>DJANGO_SETTINGS_MODULE=mydjangoproject.settings</env>
  <pythonpath>/srv/mydjangoproject/</pythonpath>
  <module>django.core.handlers.wsgi:WSGIHandler()</module>
</uwsgi>
```

Writing a player backend
------------------------
If you do not want to use the VLC player backend you can write your own
player class. You class simply needs to inherit from `webradio.player.AbstractAudioPlayer`
and override all of the methods that raise a `NotImplementedError`.

You can point the frontend to your custom player class by defining `WEBRADIO_PLAYER_CLASS`
in your Django project's settings.

HTTP-API
--------
There is a tiny and very simple HTTP API for controlling the audio player instance. The following URIs can be accessed from scripts and, depending on your webserver configuration, from any client on the network:

* `/webradio/controls/play/1/`

  Plays the station with ID 1

* `/webradio/controls/playpause/`

  Toggle between play/pause

* `/webradio/controls/nextstation/`

  Switch to next available radio station

* `/webradio/controls/previousstation/`

  Switch to previous radio station

* `/webradio/controls/info/`

  Returns a JSON object with the following information:
   - `obj.title`: The title of the currently played back song (`string`)
   - `obj.station`: The name of the station (`string`)
   - `obj.is_playing`: Is there a stream currently playing (`bool`)

Usage scenario
--------------
I wrote this software mainly for my Raspberry Pi. It provides the base for a simple WiFi streaming client with a 16x2 LC Display, 5 hardware buttons and local audio playback. I wanted to control the streaming client both through the hardware buttons and from my smartphone using the web-based GUI.

I have performed the initial setup of the radio stations from my computer using Django's admin interface.


