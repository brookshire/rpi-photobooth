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

    def __init__(self, q=None):
        self.q = q

        if not os.path.exists(local_save_directory):
            print "Creating {0} directory to save pics locally".format(local_save_directory)
            os.mkdir(local_save_directory)

        self.camera = Camera()
        self.tweakCamera()
        self.button_light = Relay(BUTTON_LIGHT_GPIO)
        self.button_input = Button(BUTTON_INPUT_GPIO)
        self.quit_input = Button(QUIT_INPUT_GPIO)
        self.flash = Relay(FLASH_GPIO)

    def tweakCamera(self):
        print ("Tweaking camera settings")
        self.camera.brightness = 60
        self.camera.saturation = 60
        # self.camera.iSO = 400

    def setReady(self):
        self.flash.off()
        self.button_light.on()
        self.camera.setup()

    def setOff(self):
        self.flash.off()
        self.button_light.off()
        self.camera.stop_preview()

    def takePic(self, fname):
        self.button_light.off()

        if use_flash:
            self.flash.on()

        self.camera.start_preview()
        sleep(button_delay)

        self.camera.capture(fname)

        if self.q is not None:
            queueLock.acquire()
            self.q.put(fname)
            queueLock.release()

        self.camera.stop_preview()
        self.flash.off()

        self.button_light.on()


class UploaderThread(threading.Thread):
    def __init__(self, id, q):
        threading.Thread.__init__(self)
        self.id = id
        self.q = q

    def run(self):
        while not exitFlag:
            queueLock.acquire()
            if not self.q.empty():
                fname = self.q.get()
                print("{0} Found {1} on queue to upload".format(self.id,
                                                                fname))
                try:
                    self.uploadPic(fname)
                    print("{0} Successfully uploaded {1}".format(self.id,
                                                                 fname))
                except paramiko.ssh_exception.SSHException:
                    print("{0} Failed to upload {1}, requeuing".format(self.id,
                                                                       fname))
                    self.q.put(fname)
            queueLock.release()

    def uploadPic(self, fname):
        base_fname = os.path.basename(fname)

        if upload_type == "ssh":
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

    if upload_images is not None:
        uploadQueue = Queue.Queue(10)
        threads = []
        for i in range(1, upload_threads):
            new_t = UploaderThread(i, uploadQueue)
            new_t.start()
            print("Started upload thread {0}".format(i))
            threads.append(new_t)

        boothbox = Booth(uploadQueue)
    else:
        boothbox = Booth(None)

    boothbox.setReady()

    try:
        while True:

            input_state = boothbox.button_input.get_state()
            input_quit = boothbox.quit_input.get_state()

            if not input_quit:
                exitFlag = True
                boothbox.setOff()
                GPIO.cleanup()

                if upload_images is not None:
                    for t in threads:
                        t.join()
                sys.exit(0)

            if not input_state:
                now = datetime.datetime.now()
                ts = now.strftime("%Y.%m.%d.%H.%M.%S")
                fname = "{0}/{1}{2}.jpg".format(local_save_directory,
                                                local_save_prefix,
                                                ts)
                boothbox.takePic(fname)

    except KeyboardInterrupt:
        print("Shutting down")
        boothbox.camera.stop_preview()
        GPIO.cleanup()
        print("Exiting")
