#!/usr/bin/env python

from PyDisplay import *
from psutil import cpu_percent, phymem_usage, disk_usage
from time import sleep


def b2h(n):
    # http://code.activestate.com/recipes/578019
    # >>> bytes2human(10000)
    # '9.8K'
    # >>> bytes2human(100001221)
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


if __name__ == '__main__':
    lcd = PyDisplay()
    lcd.writeAt(0, 4, 'RaspberryPi')
    lcd.writeAt(3, 0, 'wlan0 192.168.1.201')

    while True:
        cpu = int(round(cpu_percent(), 0))
        mem = int(round(phymem_usage()[3], 0))
        usage = disk_usage('/')

        lcd.writeAt(1, 0, "CPU {0:>3d}% - MEM {1:>3d}%".format(cpu, mem))
        lcd.writeAt(2, 0, "'/':   {}/{}".format(b2h(usage.used), b2h(usage.total)))
        sleep(2.5)
