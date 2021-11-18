from pwd import getpwnam
from configparser import ConfigParser

class autobrr_meta:
    name = "autobrr"
    pretty_name = "autobrr"
    baseurl = "/autobrr"
    process = "autobrr"
    systemd = "autobrr@"
    multiuser = True

class autodl_meta:
    name = "autodl"
    process = "irssi"
    pretty_name = "AutoDL irssi"
    systemd = "irssi@"
    multiuser = True

class bazarr_meta:
    name = "bazarr"
    pretty_name = "Bazarr"
    baseurl = "/bazarr"

class btsync_meta:
    name = "btsync"
    pretty_name = "Resilio Sync"    
    baseurl = ":8888/gui"
    scheme = "http"
    systemd = "resilio-sync"
    process = "rslsync"

class couchpotato_meta:
    name= "couchpotato"
    pretty_name = "CouchPotato"
    baseurl = "/couchpotato"
    systemd = "couchpotato"
    
class calibrecs_meta:
    name = "calibrecs"
    pretty_name = "Calibre Content Server"
    baseurl = "/calibrecs"
    systemd = "calibrecs"
    multiuser = True
    check_theD = True
    
class calibreweb_meta:
    name = "calibreweb"
    pretty_name = "Calibre Web"
    baseurl = "/calibreweb"
    systemd = "calibreweb"
    runas = "calibreweb"
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
    runas = "emby"
    systemd = "emby-server"

class filebrowser_meta:
    name = "filebrowser"
    pretty_name = "Filebrowser"
    baseurl = "/filebrowser"

class flood_meta:
    name = "flood"
    pretty_name = "Flood"
    baseurl = "/flood"
    systemd = "flood@"
    multiuser = True

class headphones_meta:
    name = "headphones"
    pretty_name = "Headphones"
    baseurl = "/headphones"

class jackett_meta:
    name = "jackett"
    pretty_name = "Jackett"
    baseurl = "/jackett"
    systemd = "jackett@"
    
class jellyfin_meta:
    name = "jellyfin"
    pretty_name = "Jellyfin"
    baseurl = "/jellyfin"
    systemd = "jellyfin"
    runas = "jellyfin"

class librespeed_meta:
    name = "librespeed"
    pretty_name = "LibreSpeed"
    systemd = False
    baseurl = "/librespeed"

class lidarr_meta:
    name = "lidarr"
    pretty_name = "Lidarr"
    baseurl = "/lidarr"

class lounge_meta:
    name = "lounge"
    pretty_name = "The Lounge"
    baseurl = "/irc"
    runas = "lounge"
    
class mango_meta:
    name = "mango"
    pretty_name = "Mango"
    baseurl = "/mango"
    systemd = "mango"
    runas = "mango"
    multiuser = True

class medusa_meta:
    name = "medusa"
    pretty_name = "Medusa"
    baseurl = "/medusa"
    systemd = "medusa"
    
class navidrome_meta:
    name = "navidrome"
    pretty_name = "Navidrome"
    baseurl = "/navidrome"
    process = "navidrome"
    systemd = "navidrome"
    multiuser = True

class mylar_meta:
    name = "mylar"
    pretty_name = "Mylar"
    baseurl = "/mylar"
    process = "mylar"
    systemd = "mylar"
    img = "mylar"
    
class netdata_meta:
    name = "netdata"
    pretty_name = "Netdata"
    baseurl = "/netdata"
    runas = "netdata"

class nextcloud_meta:
    name = "nextcloud"
    pretty_name = "Nextcloud"
    baseurl = "/nextcloud"
    systemd = False

class nzbget_meta:
    name = "nzbget"
    pretty_name = "nzbGet"
    baseurl = "/nzbget"
    systemd = "nzbget@"
    multiuser = True

class nzbhydra_meta:
    name = "nzbhydra"
    pretty_name = "nzbhydra"
    baseurl = "/nzbhydra"
    systemd = "nzbhydra"

class ombi_meta:
    name = "ombi"
    pretty_name = "Ombi"
    baseurl = "/ombi"
    runas = "ombi"
    
class prowlarr_meta:
    name = "prowlarr"
    pretty_name = "Prowlarr"
    baseurl = "/prowlarr"
    
class organizr_meta:
    name = "organizr"
    pretty_name = "Organizr"
    baseurl = "/organizr"
    systemd = False
    multiuser = True

class plex_meta:
    name = "plex"
    pretty_name = "Plex"
    baseurl = ":32400/web"
    runas = "plex"
    process = "Plex"
    systemd = "plexmediaserver"

class pyload_meta:
    name = "pyload"
    pretty_name = "pyLoad"
    baseurl = "/pyload"
    systemd = "pyload"

class qbittorrent_meta:
    name = "qbittorrent"
    pretty_name = "qBittorrent"
    baseurl = "/qbittorrent"
    systemd = "qbittorrent@"
    multiuser = True

class quassel_meta:
    name = "quassel"
    pretty_name = "Quassel-Core"
    systemd = "quasselcore"

class radarr_meta:
    name = "radarr"
    pretty_name = "Radarr"
    baseurl = "/radarr"

class rapidleech_meta:
    name = "rapidleech"
    pretty_name = "RapidLeech"
    baseurl = "/rapidleech"
    systemd = False

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
    baseurl = "/sabnzbd"
    systemd = "sabnzbd"

class shellinabox_meta:
    name = "shellinabox"
    pretty_name = "Console"
    baseurl = "/shell"
    runas = "shellinabox"

class sickchill_meta:
    name = "sickchill"
    pretty_name = "SickChill"
    baseurl = "/sickchill"
    systemd = "sickchill"

class sickgear_meta:
    name = "sickgear"
    pretty_name = "SickGear"
    baseurl = "/sickgear"
    systemd = "sickgear"

class sonarrold_meta:
    name = "sonarrold"
    pretty_name = "Sonarr"
    process = "nzbdrone"
    baseurl = "/sonarr"
    systemd = "sonarr@"

class sonarr_meta:
    name = "sonarr"
    pretty_name = "Sonarr"
    baseurl = "/sonarr"
    process = "sonarr"
    img = "sonarr"
    systemd = "sonarr"

class subsonic_meta:
    name = "subsonic"
    pretty_name = "Subsonic"
    baseurl = "/subsonic"

class syncthing_meta:
    name = "syncthing"
    pretty_name = "Syncthing"
    baseurl = "/syncthing"
    systemd = "syncthing@"

class tautulli_meta:
    name = "tautulli"
    pretty_name = "Tautulli"
    baseurl = "/tautulli"
    runas = "tautulli"

class transmission_meta:
    name = "transmission"
    pretty_name = "Transmission"
    systemd = "transmission@"
    baseurl = "/transmission/web/"
    multiuser = True

class webmin_meta:
    name = "webmin"
    pretty_name = "Webmin"
    runas = "root"
    baseurl = "/webmin/"

class wireguard_meta:
    name = "wireguard"
    pretty_name = "Wireguard"
    runas = "root"
    #systemd = "wg-quick@"
    multiuser = True
    def __init__(self, user):
        uid = getpwnam(user).pw_uid
        self.systemd = "wg-quick@wg"+str(uid)
        self.process = "wg"+str(uid)

class xmrig_meta:
    name = "xmrig"
    pretty_name = "XMRig"
    
class znc_meta:
    name = "znc"
    pretty_name = "ZNC"
    runas = "znc"
    def __init__(self):
        parser = ConfigParser()
        with open("/install/.znc.lock") as stream:
            parser.read_string("[general]\n" + stream.read())
        port = parser['general']['Port']
        ssl = parser['general']['SSL']
        self.baseurl = ":"+port
        if ssl == "true":
            self.scheme = "https"
        else:
            self.scheme = "http"
