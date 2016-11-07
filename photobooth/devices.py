#
#  Copyright (C) 2016 David Brookshire <dave@brookshire.org>
#
import RPi.GPIO as GPIO


class Relay():
    state = False  # True==On, False==Off
    gpio = None

    def __init__(self, gpio):
        self.gpio = gpio
        GPIO.setup(self.gpio, GPIO.OUT)

    def __repr__(self):
        return "Relay-%d" % self.gpio

    def on(self):
        GPIO.output(self.gpio, True)
        self.state = True

    def off(self):
        GPIO.output(self.gpio, False)
        self.state = False


class Lamp():
    state = False  # True==On, False==Off
    gpio = None

    def __init__(self, gpio):
        self.gpio = gpio
        GPIO.setup(self.gpio, GPIO.OUT)

    def __repr__(self):
        return "LAMP-%d" % self.gpio

    def on(self):
        GPIO.output(self.gpio, True)

    def off(self):
        GPIO.output(self.gpio, False)


class Button():
    gpio = None

    def __init__(self, gpio):
        self.gpio = gpio
        GPIO.setup(self.gpio, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def __repr__(self):
        return "BUTTON-%d" % self.gpio

    def get_state(self):
        return GPIO.input(self.gpio)
