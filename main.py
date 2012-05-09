import sys
import signal
import time
import traceback

#
# temporary work around
#
sys.path.insert(0,'../')

from rescnt import collector

class CollectorTimedOut(Exception):
    pass

def alarmhandler(signum,frame):
    raise CollectorTimedOut

COLLECTION_FREQUENCY = 60
COLLECTOR_TIMEOUT = 120
EXCEPTION_SLEEP = 5

if __name__ == "__main__":
    signal.signal(signal.SIGALRM, alarmhandler)
    while True:
        try:
            c = collector.Collector()
        except:
            traceback.print_exc()
            time.sleep(EXCEPTION_SLEEP)
            continue
        tstart = time.time()
        signal.alarm(COLLECTOR_TIMEOUT)
        try:
            c.run()
        except CollectorTimedOut:
            pass
        signal.alarm(0)
        del c
        tend = time.time()
        nextrun = tstart + COLLECTION_FREQUENCY
        if nextrun > tend:
            time.sleep(nextrun - tend - 1)
