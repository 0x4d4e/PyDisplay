#!/usr/bin/env python

from datetime import datetime
from Monitor import *
import requests
import sys


def getBitstamp():
    req = requests.get('https://www.bitstamp.net/api/ticker/')
    return req.json()


def getTime():
    now = datetime.now()
    return {'time': now.strftime("%d.%m.%y %H:%M:%S")}

def initBitstamp():
    out = [Output(0,3, 'BitStamp Ticker'),
           Output(1,0, 'A:{ask:>6} - B:{bid:>6}'),
           Output(2,0, 'H:{high:>6} - L:{low:>6}'),
           Output(3,0, 'T: {time}')]
    return Monitor([getBitstamp, getTime], out, 30)


def main():
    m = initBitstamp()
    daemon = MonitorDaemon('/tmp/coinwatch.pid', monitors=[m])

    if len(sys.argv) == 2:
        arg = sys.argv[1]
        if arg == 'd' or arg == 'daemonize':
            daemon.start()
        elif arg == 'k' or arg == 'kill':
            daemon.stop()
        elif arg == 'r' or arg == 'restart':
            daemon.restart()
        else:
            print('Unkown argument "{}". \nUse without argument or d(aemonize)|k(ill)|r(estart).'.format(arg))
            sys.exit(2)
    else:
        # don't daemonize
        daemon.run()


if __name__ == '__main__':
    main()
