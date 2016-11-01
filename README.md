# laser-timer

NFL scouting combine style laser timer.

Timer is started manually and stopped when laser goes off.
In our case we use laser device that is built using USB-mouse.
Listening the laser device is implemented in separate thread with help from:
https://www.orangecoat.com/how-to/read-and-decode-data-from-your-mouse-using-this-pyusb-hack
