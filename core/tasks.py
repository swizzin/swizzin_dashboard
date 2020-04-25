import multiprocessing as mp
from multiprocessing import Pool
from time import sleep
import subprocess as sp

#http://gouthamanbalaraman.com/blog/python-multiprocessing-as-a-task-queue.html

class Tasks(object):
    _pool = None
    jobs = {}
    @staticmethod
    def pool():
        # Singleton pattern
        if Tasks._pool is None:
            Tasks._pool = Pool(processes=4)
        return Tasks._pool
    @staticmethod
    def some_job():
        sleep(5)
        return "Job done!"
    @staticmethod
    def swizzin_task(user, function, application):
        with sp.Popen(['bash', '/usr/local/bin/swizzin/'+function+'/'+application+'.sh'], stdout=sp.PIPE, bufsize=1, universal_newlines=True) as process:
            for line in process.stdout:
                line = line.rstrip()
                print("{line}".format(line=line))
                send(ident, line, namespace='/websocket', room=user)

#https://stackoverflow.com/questions/57541356/how-to-send-the-output-of-a-long-running-python-script-over-a-websocket
#https://stackoverflow.com/questions/41431882/live-stream-stdout-and-stdin-with-websocket
#https://gitlab.com/pgjones/quart
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
