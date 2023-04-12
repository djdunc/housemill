import RPi.GPIO as GPIO
import time
from subprocess import call


GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.OUT)

GPIO.output(4, GPIO.HIGH)

time.sleep(2) # seconds

rc = call("./timelapse.sh")

GPIO.output(4, GPIO.LOW)
