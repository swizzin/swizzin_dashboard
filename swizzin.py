#!/usr/bin/env python
import flask
from flask_htpasswd import HtPasswdAuth
from flask_socketio import SocketIO, emit
from threading import Thread, Lock
import os
from core.util import *
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
socketio = SocketIO(app, async_mode=async_mode)

#Config the app
app.config.from_object('core.config.Config')
app.config.from_pyfile('swizzin.cfg', silent=True)
admin_user = app.config['ADMIN_USER']
htpasswd = HtPasswdAuth(app)

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
        (tx_prev, rx_prev) = (0, 0)
        while(True):
            tx = get_nic_bytes('tx', interface)
            rx = get_nic_bytes('rx', interface)
            if tx_prev > 0:
                tx_speed = tx - tx_prev
                #print('TX: ', tx_speed, 'bps')
                tx_speed = str(GetHumanReadableB(tx_speed)) + "/s"
            if rx_prev > 0:
                rx_speed = rx - rx_prev
                #print('RX: ', rx_speed, 'bps')
                rx_speed = str(GetHumanReadableB(rx_speed)) + "/s"
                emit('speed', {'interface': interface, 'tx': tx_speed, 'rx': rx_speed}, namespace='/websocket', broadcast=True)
            time.sleep(1)
            tx_prev = tx
            rx_prev = rx

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

#Begin routes
@app.route('/')
@htpasswd.required
def index(user):
    #global thread
    #if thread is None:
    #    thread = Thread(target=current_speed)
    #    thread.start()
    pages = generate_page_list(user)
    return flask.render_template('index.html', title='{user} - swizzin dashboard'.format(user=user), user=user, pages=pages, async_mode=socketio.async_mode)

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
@app.route('/stats/netdata/<path:p>',methods=['GET','POST',"DELETE"])
@htpasswd.required
def netdataproxy(user, p = ''):
    SITE = 'http://127.0.0.1:19999/{}'.format(p)
    if flask.request.method=='GET':
        if flask.request.args:
            querystring = flask.request.query_string.decode('utf-8')
            resp = requests.get(f'{SITE}?{querystring}')
        else:
            resp = requests.get(f'{SITE}')
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        headers = [(name, value) for (name, value) in  resp.raw.headers.items() if name.lower() not in excluded_headers]
        response = flask.Response(resp.content, resp.status_code, headers)
        return response
    elif flask.request.method=='POST':
        resp = requests.post(f'{SITE}',json=request.get_json())
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        headers = [(name, value) for (name, value) in resp.raw.headers.items() if name.lower() not in excluded_headers]
        response = flask.Response(resp.content, resp.status_code, headers)
        return response
    elif flask.request.method=='DELETE':
        resp = requests.delete(f'{SITE}').content
        response = flask.Response(resp.content, resp.status_code, headers)
        return response


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

        if "@" in application:
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
    stats = []
    interface = "eno1"
    statsh = vnstat_parse(interface, "h", "hours", 0)
    statslh = vnstat_parse(interface, "h", "hours", 1)
    statsd = vnstat_parse(interface, "d", "days", 0)
    statsm = vnstat_parse(interface, "m", "months", 0)
    statsa = vnstat_parse(interface, "h", "total")
    #statsa = vnstat_parse(interface, "m", "total", 0)
    tops = vnstat_data(interface, "t")['interfaces'][0]['traffic']['tops']
    top = []
    for t in tops:
        date = t['date']
        year = date['year']
        month = calendar.month_abbr[date['month']]
        day = date['day']
        date = "{month} {day}, {year}".format(year=year, month=month, day=day)
        rx = GetHumanReadableKB(t['rx'])
        tx = GetHumanReadableKB(t['tx'])
        top.append({"date": date, "rx": rx, "tx": tx})
    columns = {"date", "rx", "tx"}
    #stats = []
    #stats.extend([statsh, statslh, statsd, statsm, top])
    #print(stats)
    return flask.render_template('top.html', top=top, day=statsd, month=statsm, hour=statsh, lasthour=statslh, alltime=statsa, colnames=columns)
    
@app.route('/stats/disk')
@htpasswd.required
def disk_free(user):
    location = "/"
    if os.path.isfile("/install/.quota.lock"):
        total, used, free, usage = quota_usage(user)
    else:
        total, used, free, usage = disk_usage(location)
    return flask.jsonify({"disktotal": total, "diskused": used, "diskfree": free, "perutil": usage})

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


if __name__ == '__main__':
    socketio.run(app, host=app.config['HOST'], port=app.config['PORT'])

    #app.run(debug=True,host='0.0.0.0', port=8333)
