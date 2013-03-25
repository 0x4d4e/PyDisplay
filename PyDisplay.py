#!/usr/bin/python

#
# based on code from Adafruit_CharLCD which is based on lrvick's Raspberry GPIO display code and LiquidCrystal
# CharLCD - https://github.com/adafruit/Adafruit-Raspberry-Pi-Python-Code/tree/master/Adafruit_CharLCD
# lrvic - https://github.com/lrvick/raspi-hd44780/blob/master/hd44780.py
# LiquidCrystal - https://github.com/arduino/Arduino/blob/master/libraries/LiquidCrystal/LiquidCrystal.cpp
#

from time import sleep

# commands
LCD_CLEARDISPLAY = 0x01
LCD_RETURNHOME = 0x02
LCD_ENTRYMODESET = 0x04
LCD_DISPLAYCONTROL = 0x08
LCD_CURSORSHIFT = 0x10
LCD_FUNCTIONSET = 0x20
LCD_SETCGRAMADDR = 0x40
LCD_SETDDRAMADDR = 0x80
LCD_ROWOFFSETS = [0x00, 0x40, 0x14, 0x54]

# flags for display entry mode
LCD_ENTRYRIGHT = 0x00
LCD_ENTRYLEFT = 0x02
LCD_ENTRYSHIFTINCREMENT = 0x01
LCD_ENTRYSHIFTDECREMENT = 0x00

# flags for display on/off control
LCD_DISPLAYON = 0x04
LCD_DISPLAYOFF = 0x00
LCD_CURSORON = 0x02
LCD_CURSOROFF = 0x00
LCD_BLINKON = 0x01
LCD_BLINKOFF = 0x00

# flags for display/cursor shift
LCD_DISPLAYMOVE = 0x08
LCD_CURSORMOVE = 0x00

# flags for display/cursor shift
LCD_DISPLAYMOVE = 0x08
LCD_CURSORMOVE = 0x00
LCD_MOVERIGHT = 0x04
LCD_MOVELEFT = 0x00

# flags for function set
LCD_8BITMODE = 0x10
LCD_4BITMODE = 0x00
LCD_2LINE = 0x08
LCD_1LINE = 0x00
LCD_5x10DOTS = 0x04
LCD_5x8DOTS = 0x00


def sleepMicroseconds(microseconds):
    sleep(microseconds / 1e6)


class HD44780:

    def __init__(self, num_lines, num_cols, pin_rs=7, pin_en=8, pins_db=[25, 24, 23, 18], GPIO=None):
        # Emulate the old behavior of using RPi.GPIO if we haven't been given
        # an explicit GPIO interface to use
        if not GPIO:
            import RPi.GPIO as GPIO
        self.GPIO = GPIO

        self.pin_rs = pin_rs
        self.pin_en = pin_en
        self.pins_db = pins_db

        self.GPIO.setmode(GPIO.BCM)
        self.GPIO.setup(self.pin_en, GPIO.OUT)
        self.GPIO.setup(self.pin_rs, GPIO.OUT)
        for pin in self.pins_db:
            self.GPIO.setup(pin, GPIO.OUT)

        self.num_lines = num_lines
        self.num_cols = num_cols

        self.display_function = LCD_4BITMODE | LCD_1LINE | LCD_5x8DOTS
        if(self.num_lines > 1):
            self.display_function |= LCD_2LINE
        self.display_control = LCD_DISPLAYON | LCD_CURSOROFF | LCD_BLINKOFF
        self.display_mode = LCD_ENTRYLEFT | LCD_ENTRYSHIFTDECREMENT

    def initDisplay(self):
        self.setPin(self.pin_rs, False)
        self.setPin(self.pin_en, False)

        self.write4bit(0x3)
        sleepMicroseconds(5000)

        self.write4bit(0x3)
        sleepMicroseconds(200)

        self.write4bit(0x3)
        sleepMicroseconds(200)

        self.write4bit(0x2)
        sleepMicroseconds(5000)

        # should be in 4bit mode now

        self.write(LCD_FUNCTIONSET | self.display_function)

        self.displayOn()
        self.clear()

        self.write(LCD_ENTRYMODESET | self.display_mode)  # set the entry mode

    def home(self):
        self.write(LCD_RETURNHOME)  # set cursor position to zero
        sleepMicroseconds(2000)     # this command takes a long time!

    def clear(self):
        self.write(LCD_CLEARDISPLAY)  # command to clear display
        sleepMicroseconds(2000)       # takes a long time

    def setCursor(self, line, col):
        if (line > self.num_lines):
            # TODO: do something useful here
            pass
        self.write(LCD_SETDDRAMADDR | (col + LCD_ROWOFFSETS[line]))

    def noDisplay(self):
        """ Turn the display off (quickly) """

        self.display_control &= ~LCD_DISPLAYON
        self.write(LCD_DISPLAYCONTROL | self.display_control)

    def displayOn(self):
        """ Turn the display on (quickly) """

        self.display_control |= LCD_DISPLAYON
        self.write(LCD_DISPLAYCONTROL | self.display_control)

    def noCursor(self):
        """ Turns the underline cursor on/off """

        self.display_control &= ~LCD_CURSORON
        self.write(LCD_DISPLAYCONTROL | self.display_control)

    def cursor(self):
        """ Cursor On """

        self.display_control |= LCD_CURSORON
        self.write(LCD_DISPLAYCONTROL | self.display_control)

    def noBlink(self):
        """ Turn on and off the blinking cursor """

        self.display_control &= ~LCD_BLINKON
        self.write(LCD_DISPLAYCONTROL | self.display_control)

    def DisplayLeft(self):
        """ These commands scroll the display without changing the RAM """

        self.write(
            LCD_CURSORSHIFT | LCD_DISPLAYMOVE | LCD_MOVELEFT)

    def scrollDisplayRight(self):
        """ These commands scroll the display without changing the RAM """

        self.write(
            LCD_CURSORSHIFT | LCD_DISPLAYMOVE | LCD_MOVERIGHT)

    def leftToRight(self):
        """ This is for text that flows Left to Right """

        self.displaymode |= LCD_ENTRYLEFT
        self.write(LCD_ENTRYMODESET | self.displaymode)

    def rightToLeft(self):
        """ This is for text that flows Right to Left """
        self.displaymode &= ~LCD_ENTRYLEFT
        self.write(LCD_ENTRYMODESET | self.displaymode)

    def autoscroll(self):
        """ This will 'right justify' text from the cursor """

        self.displaymode |= LCD_ENTRYSHIFTINCREMENT
        self.write(LCD_ENTRYMODESET | self.displaymode)

    def noAutoscroll(self):
        """ This will 'left justify' text from the cursor """

        self.displaymode &= ~LCD_ENTRYSHIFTINCREMENT
        self.write(LCD_ENTRYMODESET | self.displaymode)

    def write(self, byte, char_mode=False):
        """ Send command/char to LCD """
        self.setPin(self.pin_rs, char_mode)
        self.write4bit(byte >> 4)
        self.write4bit(byte)

    def write4bit(self, value):
        for i in range(4):
            self.setPin(self.pins_db[i], (value >> i) & 0x01)
        self.toggleEnable()

    def setPin(self, pin, state):
        self.GPIO.output(pin, state)

    def toggleEnable(self):
        self.setPin(self.pin_en, False)
        sleepMicroseconds(1)        # enable pulse must be > 450ns
        self.setPin(self.pin_en, True)
        sleepMicroseconds(1)        # enable pulse must be > 450ns
        self.setPin(self.pin_en, False)
        sleepMicroseconds(50)      # commands need > 37us to settle


class PyDisplay:

    def __init__(self, num_lines=4, num_cols=20, display=HD44780):
        self.num_lines = num_lines
        self.num_cols = num_cols

        self.display = display(num_lines, num_cols)
        self.display.initDisplay()

    def clear(self):
        self.display.clear()

    def write(self, message):
        for c in message:
            self.display.write(ord(c), True)

    def writeAt(self, line, column, message):
        if line >= self.num_lines or column >= self.num_cols:
            return

        self.display.setCursor(line, column)
        for i, c in enumerate(message):
            if i + column >= self.num_cols:
                break
            self.display.write(ord(c), True)

