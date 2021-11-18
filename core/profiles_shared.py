from pwd import getpwnam

class autobrr_meta:
    name = "autobrr"
    pretty_name = "autobrr"
    baseurl = "/autobrr"
    process = "autobrr"
    systemd = "autobrr@"
    multiuser = True

class autodl_meta:
    name = "autodl"
    pretty_name = "AutoDL irssi"
    process = "irssi"
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
    process = "deluged"
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
        self.baseurl = "/"+user+"/emby/"

class jackett_meta:
    name = "jackett"
    pretty_name = "Jackett"
    baseurl = "/jackett"
    systemd = "jackett@"
    multiuser = True

class jellyfin_meta:
    name = "jellyfin"
    pretty_name = "Jellyfin"
    systemd = "jellyfin@"
    multiuser = True
    def __init__(self, user):
        self.baseurl = "/"+user+"/jellyfin/"

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
    
class navidrome_meta:
    name = "navidrome"
    pretty_name = "Navidrome"
    baseurl = "/navidrome"
    systemd = "navidrome"
    img = "navidrome"

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
    process = "plexmediaserver"
    systemd = "plex@"
    multiuser = True
    def __init__(self, user):
        handle = open("/home/"+user+"/.install/.plex.lock", 'r')
        num = handle.readlines()
        for line in num:
            self.port = [int(x) for x in line.split()]
            self.port = int(self.port[0])
        self.baseurl = ':'+str(self.port)+'/web'

class plexpy_meta:
    name = "plexpy"
    pretty_name = "Tautulli"
    baseurl = "/plexpy"
    systemd = "plexpy@"
    process = "plexpy"
    multiuser = True

class qbittorrent_meta:
    name = "qbittorrent"
    pretty_name = "qBittorrent"
    baseurl = "/qbittorrent"
    systemd = "qbittorrent@"
    multiuser = True

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
    process = "Sonarr"
    multiuser = True

class wireguard_meta:
    name = "wireguard"
    pretty_name = "Wireguard"
    #systemd = "wg-quick@"
    multiuser = True
    runas = "root"
    def __init__(self, user):
        uid = getpwnam(user).pw_uid
        self.systemd = "wg-quick@wg"+str(uid)
        self.process = "wg"+str(uid)
