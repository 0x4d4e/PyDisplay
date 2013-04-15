#!/usr/bin/env python

from PyDisplay import *
from time import sleep

lcd = PyDisplay()

lcd.writeAt(0, 0, '1st test')

sleep(1)

lcd.clear()
lcd.write('2nd test')

sleep(1)

lcd.home()
lcd.write('3rd test')

sleep(1)

lcd.writeAt(0, 0, 'this long line is going to be truncated at the end')

sleep(1)

lcd.writeAt(0, 0, 'this is another long text. it is going to be wrapped to the next line', mode = 'w')

sleep(1)

lcd.clear()
lcd.writeAt(0, 10, 'this long line is only using the right half of the display to show this very long line', mode = 'b')
