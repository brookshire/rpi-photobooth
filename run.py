#!/usr/bin/python
#
#
from photobooth.devices import Relay, Camera, Button
from photobooth.display import BoothDisplay

from time import sleep

import RPi.GPIO as GPIO

FLASH_GPIO = 17
BUTTON_LIGHT_GPIO = 18
BUTTON_INPUT_GPIO = 27

class Booth:
    flash = None
    button_light = None
    button_input = None
    display = None

    def __init__(self):
        self.camera = Camera()
        self.flash = Relay(FLASH_GPIO)
        self.button_light = Relay(BUTTON_LIGHT_GPIO)
        self.button_input = Button(BUTTON_INPUT_GPIO)
        # self.display = BoothDisplay()

    def setReady(self):
        self.flash.off()
        self.button_light.on()
        self.camera.setup()
        # self.camera.start_preview()
        # self.display.displayReadyMessage()
        # self.display.display()

    def takePic(self):
        # self.display.root.
        self.button_light.off()
        self.flash.on()
        self.camera.start_preview()
        sleep(5)
        self.camera.stop_preview()
        self.flash.off()
        self.button_light.on()
        print("OH SNAP")



if __name__=='__main__':
    GPIO.setmode(GPIO.BCM)

    funbox = Booth()
    funbox.setReady()

    try:
        while True:

            input_state = funbox.button_input.get_state()

            if not input_state:
                funbox.takePic()

    except KeyboardInterrupt:
        print("Shutting down")
        funbox.camera.stop_preview()
        GPIO.cleanup()
        print("Exiting")


