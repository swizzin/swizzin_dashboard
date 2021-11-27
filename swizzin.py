#!/usr/bin/env python
import flask
from core.htpasswd import HtPasswdAuth
from core.middleware import PrefixMiddleware
from flask_socketio import SocketIO, emit
from threading import Thread, Lock
from packaging import version
import os
import core.config
import requests
import time
from werkzeug.middleware.proxy_fix import ProxyFix
import calendar
import eventlet

#Prep the websockets with eventlet workers
eventlet.monkey_patch()
async_mode = None

#Prep flask
app = flask.Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)

#Config the app
app.config.from_object('core.config.Config')
app.config.from_pyfile('swizzin.cfg', silent=True)
admin_user = app.config['ADMIN_USER']
htpasswd = HtPasswdAuth(app)

#Config the base url
if app.config['URLBASE'] == "/":
    app.config['URLBASE'] = ""

app.wsgi_app = PrefixMiddleware(app.wsgi_app, prefix=app.config['URLBASE'])
socketio = SocketIO(app,  path='{}/socket.io'.format(app.config['URLBASE']), async_mode=async_mode)

#Config rate limiting
def check_authorization():
    if flask.request.authorization:
        try:
            authreq = flask.request.authorization.username 
            return True
        except:
            return False
    else:
        return False


if app.config['RATELIMIT_ENABLED'] == True:
    from flask_limiter import Limiter
    from flask_limiter.util import get_remote_address
    limiter = Limiter(
        app,
        key_func=get_remote_address,
        default_limits=[app.config['RATELIMIT_DEFAULT']],
        default_limits_exempt_when=check_authorization,
        default_limits_per_method=True
    )

from core.util import *

#Prepare the background threads
thread = None
thread_lock = Lock()
thread2 = None
thread2_lock = Lock()


#Background thread functions
def current_speed(app):
    """ Thread for interface speed """
    #Modified for our uses from https://stackoverflow.com/a/26853086
    with app.app_context():
        #print("Starting current speed for", interface)
        interface = get_default_interface()
        (tx_prev, rx_prev, total_prev) = (0, 0, 0)
        while(True):
            tx = get_nic_bytes('tx', interface)
            rx = get_nic_bytes('rx', interface)
            total = tx + rx
            if tx_prev > 0:
                tx_speed = tx - tx_prev
                #print('TX: ', tx_speed, 'bps')
                tx_speed = str(GetHumanReadableB(tx_speed)) + "/s"
            if rx_prev > 0:
                rx_speed = rx - rx_prev
                #print('RX: ', rx_speed, 'bps')
                rx_speed = str(GetHumanReadableB(rx_speed)) + "/s"
            if total_prev > 0:
                total_speed = total - total_prev
                #print("TOTAL: ', total_speed, 'bps')
                total_speed = str(GetHumanReadableB(total_speed)) + "/s"
                emit('speed', {'interface': interface, 'tx': tx_speed, 'rx': rx_speed, 'total': total_speed}, namespace='/websocket', broadcast=True)
            time.sleep(1)
            tx_prev = tx
            rx_prev = rx
            total_prev = total

def io_wait(app):
    """ Thread for iowait emission """
    #https://stackoverflow.com/a/7299268
    tick = os.sysconf(os.sysconf_names['SC_CLK_TCK'])
    numcpu = os.cpu_count()
    interval = 10
    with app.app_context():
        while(True):
            readstats = open('/proc/stat')
            procstats = readstats.readlines()[0].split()
            user, nice, sys, idle, iowait, irq, sirq = ( float(procstats[1]), float(procstats[2]),
                                            float(procstats[3]), float(procstats[4]),
                                            float(procstats[5]), float(procstats[6]),
                                            float(procstats[7]) )
            readstats.close()
            time.sleep(interval)
            readstats = open('/proc/stat')
            procstats = readstats.readlines()[0].split()
            userd, niced, sysd, idled, iowaitd, irqd, sirqd = ( float(procstats[1]), float(procstats[2]),
                                            float(procstats[3]), float(procstats[4]),
                                            float(procstats[5]), float(procstats[6]),
                                            float(procstats[7]) )
            readstats.close()
            iowait = '{0:.1f}'.format(((iowaitd - iowait)* 100 / tick ) / numcpu / interval)
            #times = psutil.cpu_times_percent(interval=10)
            emit('iowait', {'iowait': iowait}, namespace='/websocket', broadcast=True)


@app.before_request
def reload_htpasswd():
    """ 
    This function ensures htpasswd is reloaded and up-to-date before every request.
    """ 
    htpasswd.load_users(app)

#@app.after_request
#def apply_headers(response):
#    if flask.request.referrer == "{}login".format(flask.request.host_url):
#        response.headers["WWW-Authenticate"] = 'basic realm="{0}"'.format(current_app.config['FLASK_AUTH_REALM'])
#    if flask.request.referrer == "{}login/auth".format(flask.request.host_url):
#        response.headers["WWW-Authenticate"] = 'basic realm="{0}"'.format(current_app.config['FLASK_AUTH_REALM'])
#    if flask.request.referrer == "{}logout".format(flask.request.host_url):
#        response.headers["WWW-Authenticate"] = 'basic realm="{0}"'.format(current_app.config['FLASK_AUTH_REALM'])
#    return response

@app.errorhandler(401)
def unauthorized(e):
    if app.config['FORMS_LOGIN']:
        if app.config['URLBASE'] == "":
            urlbase = app.config['URLBASE']
        elif app.config['URLBASE'].startswith("/"):
            urlbase = app.config['URLBASE'][1:]
        if not urlbase == "" and not urlbase.endswith("/"):
            urlbase = urlbase + "/"
        if flask.request.referrer == "{host}{urlbase}login".format(host=flask.request.host_url, urlbase=urlbase):
            return authenticate()
        elif flask.request.referrer == "{host}{urlbase}login/auth".format(host=flask.request.host_url, urlbase=urlbase):
            return authenticate()
        else:
            return flask.redirect(flask.url_for('login'))
    else:
        return authenticate()

def authenticate():
    """
    Sends a 401 response that enables basic auth
    """
    return flask.Response(
        'Could not verify your access level for that URL.\n'
        'You have to login with proper credentials',
        401,
        {'WWW-Authenticate': 'basic realm="{0}"'.format(
            current_app.config['FLASK_AUTH_REALM']
        )}
    )

#Begin routes
@app.route('/')
@htpasswd.required
def index(user):
    #global thread
    #if thread is None:
    #    thread = Thread(target=current_speed)
    #    thread.start()
    pages = generate_page_list(user)
    mounts = get_mounts()
    if os.path.isfile("/install/.quota.lock"):
        quota = True
    else:
        quota = False
    if os.path.isfile("/install/.sbio.lock"):
        vendor = "sbio"
    else:
        vendor = "swizzin"
    return flask.render_template('index.html', title='{user} - swizzin dashboard'.format(user=user), user=user, pages=pages, quota=quota, vendor=vendor, mounts=mounts, async_mode=socketio.async_mode)

@socketio.on('connect', namespace='/websocket')
def socket_connect():
    global thread
    global thread2
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(current_speed, (flask.current_app._get_current_object()))
    with thread2_lock:
        if thread2 is None:
            thread2 = socketio.start_background_task(io_wait, (flask.current_app._get_current_object()))
    emit('my_response', {'data': 'Connected', 'count': 0})

@app.route('/stats')
@app.route('/stats/')
@htpasswd.required
def stats(user):
    pages = generate_page_list(user)
    return flask.render_template('stats.html', title='Stats', user=user, pages=pages)

@app.route('/stats/netdata/')
@app.route('/stats/netdata/<path:p>',methods=['GET'])
@htpasswd.required
def netdataproxy(user, p = ''):
    SITE = 'http://127.0.0.1:19999/{}'.format(p)
    if flask.request.method=='GET':
        if flask.request.args:
            querystring = flask.request.query_string.decode('utf-8')
            resp = requests.get("{SITE}?{querystring}".format(SITE=SITE,querystring=querystring))
        else:
            resp = requests.get("{SITE}".format(SITE=SITE))
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        headers = [(name, value) for (name, value) in  resp.raw.headers.items() if name.lower() not in excluded_headers]
        response = flask.Response(resp.content, resp.status_code, headers)
        return response
    #elif flask.request.method=='POST':
    #    resp = requests.post(f'{SITE}',json=request.get_json())
    #    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
    #    headers = [(name, value) for (name, value) in resp.raw.headers.items() if name.lower() not in excluded_headers]
    #    response = flask.Response(resp.content, resp.status_code, headers)
    #    return response
    #elif flask.request.method=='DELETE':
    #    resp = requests.delete(f'{SITE}').content
    #    response = flask.Response(resp.content, resp.status_code, headers)
    #    return response


@app.route('/apps/status')
@htpasswd.required
def app_status(user):
    apps = apps_status(user)
    return flask.jsonify(apps)

@app.route('/apps/service', methods=['POST'])
@htpasswd.required
def service(user):
    if flask.request.method == 'POST':
        data = flask.request.get_json()
        application = data['application']
        try:
            profile = str_to_class(application+"_meta")(user)
        except:
            try:
                profile = str_to_class(application+"_meta")
            except:
                return """Application profile not found."""
        try:
            multiuser = profile.multiuser
        except:
            multiuser = False
        if multiuser == False and user != admin_user:
            return """Access denied"""
        try:
            application = profile.systemd
        except:
            pass

        if application.endswith("@"):
            application = application+user
        result = systemctl(data['function'], application)
        return str(result)


@app.route('/stats/loadavg')
@htpasswd.required
def loadavg(user):
    loadavg = open("/proc/loadavg").readline().split(" ")[:3]
    numcpu = os.cpu_count()
    perutil = '{0:.2f}'.format((float(loadavg[0]) / numcpu) * 100)
    return flask.jsonify({"1m": loadavg[0], "5m": loadavg[1], "15m": loadavg[2], "perutil": perutil})

@app.route('/stats/vnstat')
@htpasswd.required
def vnstat(user):
    #stats = []
    interface = get_default_interface()
    vnstat_info = vnstat_data(interface, "h")
    vnstat_jsonversion = vnstat_info["jsonversion"]
    if vnstat_jsonversion == "1":
        qh = "hours"
        qd = "days"
        qm = "months"
        qt = "tops"
        thisday = 0
        thismonth = 0
        hour = int(time.strftime("%H"))
        lasthour = hour - 1
        if lasthour == -1:
            lasthour = 23
        read_unit = GetHumanReadableKB
    elif vnstat_jsonversion == "2":
        qh = "hour"
        qd = "day"
        qm = "month"
        qt = "top"
        thisday = vnstat_data(interface, "d")['interfaces'][0]['traffic']['day'][-1]["id"]
        thismonth = vnstat_data(interface, "m")['interfaces'][0]['traffic']['month'][-1]["id"]
        hour = vnstat_info['interfaces'][0]['traffic']['hour'][-1]["id"]
        lasthour = vnstat_info['interfaces'][0]['traffic']['hour'][-2]["id"]
        read_unit = GetHumanReadableB
    statsh = vnstat_parse(interface, "h", qh, read_unit, hour)
    statslh = vnstat_parse(interface, "h", qh, read_unit, lasthour)
    statsd = vnstat_parse(interface, "d", qd, read_unit, thisday)
    statsm = vnstat_parse(interface, "m", qm, read_unit, thismonth)
    statsa = vnstat_parse(interface, "h", "total", read_unit)
    #statsa = vnstat_parse(interface, "m", "total", 0)
    tops = vnstat_data(interface, "t")['interfaces'][0]['traffic'][qt]
    top = []
    for t in tops[:10]:
        date = t['date']
        year = date['year']
        month = calendar.month_abbr[date['month']]
        day = date['day']
        date = "{month} {day}, {year}".format(year=year, month=month, day=day)
        rx = read_unit(t['rx'])
        tx =read_unit(t['tx'])
        total = read_unit(t['tx'] + t['rx'])
        top.append({"date": date, "rx": rx, "tx": tx, "total": total})
    columns = {"date", "rx", "tx", "total"}
    #stats = []
    #stats.extend({"statsh": statsh, "statslh": statslh, "statsd": statsd, "statsm": statsm, "statsa": statsa, "top": top})
    #print(stats)
    #return flask.jsonify({"statsh": statsh, "statslh": statslh, "statsd": statsd, "statsm": statsm, "statsa": statsa, "top": top})
    return flask.render_template('top.html', user=user, top=top, day=statsd, month=statsm, hour=statsh, lasthour=statslh, alltime=statsa, colnames=columns)

@app.route('/stats/disk')
@htpasswd.required
def disk_free(user):
    mounts = get_mounts()
    data = {}
    for mount in mounts:
        total, used, free, usage = disk_usage(mount)
        data[mount] = {"disktotal": total, "diskused": used, "diskfree": free, "perutil": usage}
    return flask.jsonify(data)

@app.route('/stats/quota')
@htpasswd.required
def quota_free(user):
    if os.path.isfile("/install/.quota.lock"):
        total, used, free, usage = quota_usage(user)
        return flask.jsonify({"quota": {"disktotal": total, "diskused": used, "diskfree": free, "perutil": usage}})
    else:
        return """Quota not installed"""

@app.route('/stats/boot')
@htpasswd.required
def boot_time(user):
    return boottimeutc

@app.route('/stats/ram')
@htpasswd.required
def ram_stats(user):
    ramstats = dict((i.split()[0].rstrip(':'),int(i.split()[1])) for i in open('/proc/meminfo').readlines())
    ramtotal = GetHumanReadableKB(ramstats['MemTotal'])
    ramfree = GetHumanReadableKB(ramstats['MemAvailable'])
    ramused = GetHumanReadableKB(ramstats['MemTotal'] - ramstats['MemAvailable'])
    perutil = '{0:.2f}'.format((ramstats['MemTotal'] - ramstats['MemAvailable']) / ramstats['MemTotal'] * 100)
    return flask.jsonify({"ramtotal": ramtotal, "ramfree": ramfree, "ramused": ramused, "perutil": perutil})

@app.route('/stats/network')
@htpasswd.required
def network_quota(user):
    if app.config['SHAREDSERVER'] is True:
        total, used, free, usage = network_quota_usage(user)
    return flask.jsonify({"nettotal": total, "netused": used, "netfree": free, "perutil": usage})


@app.route('/login')
def login():
    return flask.render_template('login.html', title='swizzin login')

@app.route('/login/auth')
@htpasswd.required
def auth(user):
    return """
        <div>You have been logged in. Redirecting to home...</div>    

<script>
    setTimeout(function () {{
        window.location.href = "{}";
    }}, 500);
</script>
    """.format(flask.url_for('index'))


@app.route('/logout')
@htpasswd.required
def logout(user):
    return flask.render_template('logout.html')

if __name__ == '__main__':
    socketio.run(app, host=app.config['HOST'], port=app.config['PORT'])

    #app.run(debug=True,host='0.0.0.0', port=8333)
