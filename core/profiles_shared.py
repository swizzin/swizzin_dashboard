from core.util import get_uid

class autodl_meta:
    name = "irssi"
    pretty_name = "AutoDL irssi"
    systemd = "irssi@"
    multiuser = True

class bazarr_meta:
    name = "bazarr"
    pretty_name = "Bazarr"
    baseurl = "/bazarr"
    systemd = "bazarr@"
    multiuser = True

class btsync_meta:
    name = "btsync"
    pretty_name = "Resilio Sync"    
    baseurl = "/btsync"
    #scheme = "http"
    systemd = "btsync@"
    process = "rslsync"
    multiuser = True

class deluge_meta:
    name = "deluge"
    pretty_name = "Deluge"
    baseurl = "/deluge"
    systemd = "deluged@"
    multiuser = True

class delugeweb_meta:
    name = "delugeweb"
    pretty_name = "Deluge Web"
    systemd = "deluge-web@"
    multiuser = True
    process = "deluge-web"

class emby_meta:
    name = "emby"
    pretty_name = "Emby"
    baseurl = "/emby"
    systemd = "emby@"
    process = "EmbyServer"
    multiuser = True
    def __init__(self, user):
        self.baseurl = "/"+user+"/emby"

class jackett_meta:
    name = "jackett"
    pretty_name = "Jackett"
    baseurl = "/jackett"
    systemd = "jackett@"
    multiuser = True

class lidarr_meta:
    name = "lidarr"
    pretty_name = "Lidarr"
    baseurl = "/lidarr"
    systemd = "lidarr@"
    multiuser = True

class medusa_meta:
    name = "medusa"
    pretty_name = "Medusa"
    baseurl = "/medusa"
    systemd = "medusa@"
    multiuser = True

class nzbget_meta:
    name = "nzbget"
    pretty_name = "nzbGet"
    baseurl = "/nzbget"
    systemd = "nzbget@"
    multiuser = True

class ombi_meta:
    name = "ombi"
    pretty_name = "Ombi"
    baseurl = "/ombi"
    #runas = "ombi"
    systemd = "ombi@"
    multiuser = True
    def __init__(self, user):
        self.baseurl = "/"+user+"/ombi"

class plex_meta:
    name = "plex"
    pretty_name = "Plex"
    process = "Plex"
    systemd = "plex@"
    multiuser = True
    def __init__(self, user):
        handle = open("/home/"+user+"/.install/.plex.lock", 'r')
        num = handle.readlines()
        for line in num:
            self.port = [int(x) for x in line.split()]
            self.port = int(self.port[0])
        self.baseurl = ':'+self.port+'/web'

class radarr_meta:
    name = "radarr"
    pretty_name = "Radarr"
    baseurl = "/radarr"
    systemd = "radarr@"
    multiuser = True

class rtorrent_meta:
    name = "rtorrent"
    pretty_name = "rTorrent"
    systemd = "rtorrent@"
    multiuser = True

class rutorrent_meta:
    name = "rutorrent"
    pretty_name = "ruTorrent"
    baseurl = "/rutorrent"
    systemd = False
    multiuser = True

class sabnzbd_meta:
    name = "sabnzbd"
    pretty_name = "SABnzbd"
    systemd = "sabnzbd@"
    multiuser = True
    def __init__(self, user):
        self.baseurl = "/"+user+"/sabnzbd"

class sonarr_meta:
    name = "sonarr"
    pretty_name = "Sonarr"
    baseurl = "/sonarr"
    systemd = "sonarr@"
    multiuser = True


class tautulli_meta:
    name = "tautulli"
    pretty_name = "Tautulli"
    baseurl = "/tautulli"
    systemd = "tautulli@"
    multiuser = True

class wireguard_meta:
    name = "wireguard"
    pretty_name = "Wireguard"
    #systemd = "wg-quick@"
    multiuser = True
    def __init__(self, user):
        uid = str(get_uid(user))
        self.systemd = "wg-quick@wg"+uid