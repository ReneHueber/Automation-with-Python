#!/bin/bash

xdotool key Super+4
sleep 1
gnome-terminal -- /bin/sh -c  'python3 /home/ich/Documents/Progammieren/Python/Projects/Automation/Watchdog_File_System/DownloadWatcher.py'
sleep 1
xdotool key Super+1
