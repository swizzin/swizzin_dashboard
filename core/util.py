import sys
import os
import swizzin
from flask import request, current_app
from flask_socketio import SocketIO, emit
import subprocess as sp
import json
import shutil
import datetime
import re
from pwd import getpwnam

is_shared = swizzin.app.config['SHAREDSERVER']

if is_shared is True:
    from core.profiles_shared import *
else:
    from core.profiles import *
    try:
        from core.custom.profiles import *
    except:
        pass


def get_btime_utc():
    file = open('/proc/stat', 'r')
    for line in file:
        if line.startswith("btime"):
            btime = int(line.split(" ")[1])
            return btime

boottimestamp = get_btime_utc()
boottimeutc = datetime.datetime.utcfromtimestamp(boottimestamp).strftime('%b %d, %Y %H:%M:%S')

def str_to_class(str):
    return getattr(sys.modules[__name__], str)

def get_default_interface():
    #Based on: https://stackoverflow.com/a/6556951
    """Get the default interface directly from /proc."""
    with open("/proc/net/route") as route:
        for line in route:
            fields = line.strip().split()
            #if fields[1] != '00000000' or not int(fields[3], 16) & 2:
            if fields[1] != '00000000':
                continue
            return fields[0]

def get_mounts():
    mounts = []
    with open("/proc/mounts") as mount:
        for line in mount:
            fields = line.strip().split()
            if fields[0].startswith("/dev"):
                if ("boot" in fields[1]) or ("fuse" in fields) or ("/snap/" in fields[1]) or ("/loop" in fields[0]) or ("/docker" in fields[1]):
                    continue
                else:
                    mounts.append(fields[1])
            if fields[2] == "zfs":
                mounts.append(fields[1])
    with open("/etc/fstab") as fstab:
        for line in fstab:
            fields = line.strip().split()
            if "bind" in str(fields):
                try:
                    mounts.remove(fields[1])
                except:
                    pass
    return mounts

def generate_page_list(user):
    admin_user = current_app.config['ADMIN_USER']
    pages = []
    if is_shared is True:
        locks = os.listdir('/home/'+user+'/.install')
    else:
        locks = os.listdir('/install')
    try:
        host = request.host.split(":")[0]
    except:
        host = request.host

    scheme = request.scheme
    for lock in locks:
        app = lock.split(".")[1]
        try:
            profile = str_to_class(app+"_meta")(user)
        except:
            try:
                profile = str_to_class(app+"_meta")()
            except:
                continue
        try:
            multiuser = profile.multiuser
        except:
            multiuser = False
        if multiuser == False and user != admin_user:
            continue
        try:
            scheme = profile.scheme
        except:
            scheme = request.scheme
        try:
            url = profile.urloverride
        except:
            try:
                url = scheme+"://"+host+profile.baseurl
            except:
                url = False
        try:
            systemd = profile.systemd
        except:
            systemd = profile.name
        try:
            brand = profile.img
        except:
            brand = profile.name
        pages.append({"name": profile.name, "pretty_name": profile.pretty_name, "url": url, "systemd": systemd, "img": brand})
    return pages

def apps_status(username):
    apps = []
    admin_user = current_app.config['ADMIN_USER']
    is_shared = current_app.config['SHAREDSERVER']
    if is_shared is True:
        locks = os.listdir('/home/'+username+'/.install')
    else:
        locks = os.listdir('/install')
    ps = sp.Popen(('ps', 'axo', 'user:32,comm,cmd'), stdout=sp.PIPE).communicate()[0]
    procs = ps.splitlines()
    for lock in locks:
        application = lock.split(".")[1]
        try:
            profile = str_to_class(application+"_meta")(username)
        except:
            try:
                profile = str_to_class(application+"_meta")
            except Exception as e:
                current_app.logger.debug("Encountered an error while loading the profile for %s: %s", application, e)
                continue
        try:
            multiuser = profile.multiuser
        except:
            multiuser = False
        if multiuser == False and username != admin_user:
            continue
        try:
            #If application is not run as user
            user = profile.runas
        except:
            user = username
        try:
            #If application in `ps` has another name
            application = profile.process
        except:
            application = profile.name
        try:
            systemd = profile.systemd
        except:
            systemd = profile.name
        if systemd == False:
            continue
        try:
            enabled = is_application_enabled(systemd, user)
        except:
            enabled = False
        try:
            check_theD = profile.check_theD
        except:
            check_theD = False 
        if check_theD is True:
            status = is_process_running(systemd, user, systemd=True)
        else:
            status = is_process_running(application, user, procs=procs)
        apps.append({"name": profile.name, "active": status, "enabled": enabled})
    return apps

def is_process_running(application, username, systemd=False, procs=False):
    result = False
    if systemd is True:
        if application.endswith("@"):
            service = application+username
        else:
            service = application
        returncode = sp.run(('systemctl', 'is-active', service), stdout=sp.DEVNULL).returncode
        if returncode == 0:
            result = True
    else:
        for p in procs:
            p = p.decode('utf-8').split()
            if username.lower() == str(p[0]).lower():
                if application.lower() in str(p).lower():
                    result = True
    return result

def is_application_enabled(application, user):
    if application.endswith("@"):
        result = os.path.exists('/etc/systemd/system/multi-user.target.wants/{application}{user}.service'.format(application=application, user=user))
    else:
        result = os.path.exists('/etc/systemd/system/multi-user.target.wants/{application}.service'.format(application=application))
    return result

def systemctl(function, application):
    if function in ("enable", "disable"):
        result = sp.run(('sudo', 'systemctl', function, '--now', application), stdout=sp.DEVNULL).returncode
    else:
        result = sp.run(('sudo', 'systemctl', function, application), stdout=sp.DEVNULL).returncode
    return result

def vnstat_data(interface, mode):
    vnstat = sp.run(('vnstat', '-i', interface, '--json', mode), stdout=sp.PIPE)
    data = json.loads(vnstat.stdout.decode('utf-8'))
    #data = vnstat.stdout.decode('utf-8')
    return data

def vnstat_parse(interface, mode, query, read_unit, position=False):
    if position is not False:
        #result = vnstat_data(interface, mode)['interfaces'][0]['traffic'][query][position]
        result = vnstat_data(interface, mode)['interfaces'][0]['traffic'][query]
        for p in result:
            if p["id"] == int(position):
                data = {}
                data['rx'] = read_unit(p['rx'])
                data['tx'] = read_unit(p['tx'])
                data['total'] = read_unit(p['tx'] + p['rx'])
                result = data
                break
    else:
        result = vnstat_data(interface, mode)['interfaces'][0]['traffic'][query]
        result['total'] = read_unit(result['rx'] + result['tx'])
        result['rx'] = read_unit(result['rx'])
        result['tx'] = read_unit(result['tx'])
    return result

def disk_usage(location):
    total, used, free = shutil.disk_usage(location)
    totalh = GetHumanReadableBi(total)
    usedh = GetHumanReadableBi(used)
    freeh = GetHumanReadableBi(free)
    usage = '{0:.2f}'.format((used / total * 100))
    return totalh, usedh, freeh, usage

def quota_usage(username):
    quota = sp.Popen(('sudo', 'quota', '-wpu', username), stdout=sp.PIPE)
    quota = quota.communicate()[0].decode("utf-8").split('\n')[2].split()
    fs = quota[0]
    used = int(re.sub("[^0-9]", "", quota[1]))
    total = int(quota[2])
    free = total - used
    totalh = GetHumanReadableKiB(total)
    usedh = GetHumanReadableKiB(used)
    freeh = GetHumanReadableKiB(free)
    usage = '{0:.2f}'.format((used / total * 100))
    return totalh, usedh, freeh, usage

def network_quota_usage(username):
    quota = sp.Popen(('sudo', '/etc/swizzin.xl/add-on/panelquotas.sh', 'json', username), stdout=sp.PIPE).communicate()[0].decode("utf-8")
    quota = json.loads(quota)
    try:
        total = int(quota['total'])
        totalh = GetHumanReadableB(total)
    except:
        totalh = quota['total']
    try:
        free = int(quota['remaining'])
        freeh = GetHumanReadableB(free)
    except:
        freeh = quota['remaining']
    used = int(quota['used'])
    usedh = GetHumanReadableB(used)
    try:
        usage = '{0:.2f}'.format((used / total * 100))
    except:
        usage = "N/A"
    return totalh, usedh, freeh, usage

def GetHumanReadableKiB(size,precision=2):
    #https://stackoverflow.com/a/32009595
    suffixes=['KiB','MiB','GiB','TiB','PiB']
    suffixIndex = 0
    while size > 1024 and suffixIndex < 4:
        suffixIndex += 1 #increment the index of the suffix
        size = size/1024.0 #apply the division
    return "%.*f %s"%(precision,size,suffixes[suffixIndex])

def GetHumanReadableKB(size,precision=2):
    #https://stackoverflow.com/a/32009595
    suffixes=['KB','MB','GB','TB','PB']
    suffixIndex = 0
    while size > 1024 and suffixIndex < 4:
        suffixIndex += 1 #increment the index of the suffix
        size = size/1024.0 #apply the division
    return "%.*f %s"%(precision,size,suffixes[suffixIndex])

def GetHumanReadableBi(size,precision=2):
    #https://stackoverflow.com/a/32009595
    suffixes=['B','KiB','MiB','GiB','TiB','PiB']
    suffixIndex = 0
    while size > 1024 and suffixIndex < 4:
        suffixIndex += 1 #increment the index of the suffix
        size = size/1024.0 #apply the division
    return "%.*f %s"%(precision,size,suffixes[suffixIndex])

def GetHumanReadableB(size,precision=2):
    #https://stackoverflow.com/a/32009595
    suffixes=['B','KB','MB','GB','TB','PB']
    suffixIndex = 0
    while size > 1024 and suffixIndex < 4:
        suffixIndex += 1 #increment the index of the suffix
        size = size/1024.0 #apply the division
    return "%.*f %s"%(precision,size,suffixes[suffixIndex])

def get_nic_bytes(t, interface):
    with open('/sys/class/net/' + interface + '/statistics/' + t + '_bytes', 'r') as f:
        data = f.read();
    return int(data)

def get_uid(user):
    result = getpwnam(user).pw_uid
    return result


#https://stackoverflow.com/questions/41431882/live-stream-stdout-and-stdin-with-websocket
## panel threading install idea
#async def time(websocket, path):
#    script_name = 'script.py'
#    script = await websocket.recv()
#    with open(script_name, 'w') as script_file:
#        script_file.write(script)
#    with subprocess.Popen(['python3', '-u', script_name],
#                          stdout=subprocess.PIPE,
#                          bufsize=1,
#                          universal_newlines=True) as process:
#        for line in process.stdout:
#            line = line.rstrip()
#            print(f"line = {line}")
#            await websocket.send(line)
