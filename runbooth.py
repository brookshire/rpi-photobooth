#!/usr/bin/python
#
#
from photobooth.devices import Relay, Camera, Button
from photobooth.display import BoothDisplay

from boothconfig import *

from time import sleep

import os
import datetime
import paramiko
import threading
import Queue
import sys

import RPi.GPIO as GPIO

FLASH_GPIO = 17
BUTTON_LIGHT_GPIO = 18
BUTTON_INPUT_GPIO = 27
QUIT_INPUT_GPIO = 22

queueLock = threading.Lock()
exitFlag = False


class Booth:
    flash = None
    button_light = None
    button_input = None
    quit_input = None
    q = None

    def __init__(self, q):
        self.q = q
        if not os.path.exists(local_save_directory):
            print "Creating {0} directory to save pics locally".format(local_save_directory)
            os.mkdir(local_save_directory)

        self.camera = Camera()
        self.flash = Relay(FLASH_GPIO)
        self.button_light = Relay(BUTTON_LIGHT_GPIO)
        self.button_input = Button(BUTTON_INPUT_GPIO)
        self.quit_input = Button(QUIT_INPUT_GPIO)

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

        queueLock.acquire()
        self.q.put(fname)
        queueLock.release()

        self.camera.stop_preview()
        self.flash.off()
        self.button_light.on()


class UploaderThread(threading.Thread):
    def __init__(self, q):
        super(UploaderThread, self).__init__(self)
        self.q = q

    def run(self):
        while not exitFlag:
            queueLock.acquire()
            if not self.q.empty():
                fname = self.q.get()
                print("Found {0} on queue to upload".format(fname))
                self.uploadPic(fname)
                print("Successfully uploaded {0}".format(fname))
            queueLock.release()

    def uploadPic(self, fname):
        base_fname = os.path.basename(fname)
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(remote_server,
                    username=remote_user,
                    key_filename=private_key)
        sftp = ssh.open_sftp()
        sftp.put(fname,
                 os.path.join(remote_path, base_fname))
        sftp.close()
        ssh.close()


if __name__ == '__main__':
    GPIO.setmode(GPIO.BCM)
    uploadQueue = Queue.Queue(10)
    uploadThread = UploaderThread(uploadQueue)

    funbox = Booth(uploadQueue)
    funbox.setReady()

    try:
        while True:

            input_state = funbox.button_input.get_state()
            input_quit = funbox.quit_input.get_state()

            if not input_quit:
                exitFlag = True
                uploadThread.join()
                sys.exit(0)

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
