#!/bin/bash
DATE=$(date +"%Y-%m-%d_%H%M")
libcamera-jpeg -o /home/pi/Desktop/timelapse/$DATE.jpg --tuning-file /usr/share/libcamera/ipa/raspberrypi/imx219_noir.json
