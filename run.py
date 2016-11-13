#!/usr/bin/env python
#
#
from photobooth.devices import Relay, Camera, Button

import RPi.GPIO as GPIO

FLASH_GPIO = 18
BUTTON_LIGHT_GPIO = 17
BUTTON_INPUT_GPIO = 23

class Booth:
    flash = None
    button_light = None
    button_input = None

    def __init__(self):
        self.camera = Camera()
        self.flash = Relay(FLASH_GPIO)
        self.button_light = Relay(BUTTON_LIGHT_GPIO)
        self.button_input = Button(BUTTON_INPUT_GPIO)

    def setReady(self):
        self.flash.off()
        self.button_light.on()
        self.camera.setup()
        self.camera.start_preview()


if __name__=='__main__':
    GPIO.setmode(GPIO.BCM)

    funbox = Booth()
    funbox.setReady()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("Shutting down")
        funbox.camera.stop_preview()
        GPIO.cleanup()
        print("Exiting")


