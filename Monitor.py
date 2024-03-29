#!/usr/bin/env python

from PyDisplay import *
from time import sleep
from daemon import daemon


class Output:
    def __init__(self, line, column, fmt):
        self.line = line
        self.column = column
        self.fmt = fmt

    def show(self, lcd, data):
        msg = self.fmt.format(**data)
        lcd.writeAt(self.line, self.column, msg)


class Monitor:
    def __init__(self, sources=[], outputs=[], delay=10):
        """
        sources - list of functions which are executed for each refresh,
                  source functions must return dict with values.
        outputs - list of objects of type Output, handle positioning and
                  formatting of output strings
        delay - wait period (in seconds) until refresh/next Monitor shown
        """
        self.outputs = outputs
        self.sources = sources
        self.delay = delay

    def addOutput(self, output):
        self.outputs.append(output)

    def addSource(self, source):
        self.sources.append(source)

    def show(self, lcd):
        data = {}
        try:
            for s in self.sources:
                data.update(s())
            for o in self.outputs:
                o.show(lcd, data)
        except Exception as e:
            lcd.writeAt(0, 0, 'Exception: {}'.format(str(e)), 'w')


class MonitorDaemon(daemon):
    def __init__(self, pidfile, monitors=[]):
        super().__init__(pidfile)
        self.monitors = monitors

    def addMonitor(self, monitor):
        self.monitors.append(monitor)

    def run(self):
        lcd = PyDisplay()
        while True:
            for m in self.monitors:
                lcd.clear()
                m.show(lcd)
                sleep(m.delay)
