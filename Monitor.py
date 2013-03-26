#!/usr/bin/env python

from PyDisplay import *
from psutil import cpu_percent, phymem_usage, disk_usage
from time import sleep


def b2h(n):
    # http://code.activestate.com/recipes/578019
    # >>> bh2(10000)
    # '9.8K'
    # >>> b2h(100001221)
    # '95.4M'
    symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i+1)*10
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = float(n) / prefix[s]
            return '%.1f%s' % (value, s)
    return "%sB" % n


class Monitor:
    def __init__(self, line, column, fmt, funcs):
        self.line = line
        self.column = column
        self.fmt = fmt
        self.funcs = funcs

    def show(self, lcd):
        vals = [f() for f in self.funcs]
        lcd.writeAt(self.line, self.column, self.fmt.format(*vals))


class MonitorService:
    def __init__(self, lcd):
        self.lcd = lcd
        self.monitors = []

    def addMonitor(self, monitor):
        self.monitors.append(monitor)

    def start(self, delay=2.5):
        while True:
            for m in self.monitors:
                m.show(self.lcd)

            sleep(delay)


if __name__ == '__main__':
    ms = MonitorService(PyDisplay())

    # CPU & MEM
    funcs = [lambda: int(round(cpu_percent(), 0)),
             lambda: int(round(phymem_usage()[3], 0))]
    ms.addMonitor(Monitor(0, 0, "CPU {0:>3d}% - MEM {1:>3d}%", funcs))

    funcs = [lambda: b2h(disk_usage('/').used), lambda: b2h(disk_usage('/').total)]
    ms.addMonitor(Monitor(1, 0, "'/':   {}/{}", funcs))

    ms.start(1)
