#!/usr/bin/python
#
#
from photobooth.devices import Relay, Camera, Button
from photobooth.display import BoothDisplay

from boothconfig import *

from time import sleep

import os
import datetime

import RPi.GPIO as GPIO

FLASH_GPIO = 17
BUTTON_LIGHT_GPIO = 18
BUTTON_INPUT_GPIO = 27


class Booth:
    flash = None
    button_light = None
    button_input = None

    def __init__(self):
        if not os.path.exists(local_save_directory):
            print "Creating {0} directory to save pics locally".format(local_save_directory)
            os.mkdir(local_save_directory)

        self.camera = Camera()
        self.flash = Relay(FLASH_GPIO)
        self.button_light = Relay(BUTTON_LIGHT_GPIO)
        self.button_input = Button(BUTTON_INPUT_GPIO)

    def setReady(self):
        self.flash.off()
        self.button_light.on()
        self.camera.setup()

    def takePic(self, fname):
        self.button_light.off()
        self.flash.on()
        self.camera.start_preview()
        sleep(button_delay)

        self.camera.capture(fname)

        self.camera.stop_preview()
        self.flash.off()
        self.button_light.on()


if __name__ == '__main__':
    GPIO.setmode(GPIO.BCM)

    funbox = Booth()
    funbox.setReady()

    try:
        while True:

            input_state = funbox.button_input.get_state()

            if not input_state:
                now = datetime.datetime.now()
                ts = now.strftime("%Y.%m.%d.%H.%M.%S")
                fname = "{0}/{1}{2}.jpg".format(local_save_directory,
                                                local_save_prefix,
                                                ts)
                funbox.takePic(fname)

    except KeyboardInterrupt:
        print("Shutting down")
        funbox.camera.stop_preview()
        GPIO.cleanup()
        print("Exiting")
