# IndoorAirQualityProject

Hardware Requirements:
Raspberry Pi 4B+
DHT11 (Temperature and Humidity)
BMP280 (Pressure)
MH-Z19 (CO2)
ZP01-MP503 (VOC)
TXS0108E (logic level shifter)
Adafruit PiTFT Plus - 320x240 2.8" Capacitive

Software Requirement:
Python (3.11.0) at least 3.7
Raspberry Pi OS Bullseye
Python Librabies used in requirement.txt

Preparations:
1.	Prepare your raspberry pi. Install os (insert link to fresh install of pi)

2.	set the azure iothub connection string to env
	sudo nano /etc/environment
	IOTHUB_DEVICE_CONNECTION_STRING={iothub connection string}

2.	git clone https://github.com/damnations/IndoorAirQualityProject.git	

3.	cd IndoorAirQualityProject
	chmod +x setup.sh, ./setup.sh, note dont forget to make git copy of setup.sh executable
	or
	bash setup.sh
	Note that you might have to reboot and run the script twice

4.	sudo pip3 install -r requirements.txt
		
5.	also don't forget the libgpiod process issue, check the dht11 link for more info
 	sudo python dumper.py
	python runner.py

6.	if error: serial.serialutil.SerialException: device reports readiness to read but returned no data (device disconnected or multiple access on port?)
	use raspi-config command from https://github.com/UedaTakeyuki/mh-z19/wiki/How-to-Enable-Serial-Port-hardware-on-the-Raspberry-Pi
	
	if do this, can run dumper.py or runner.py without sudo because permission for serial device is crw-rw-rw- 1 root dialout not crw--w---- 1 root tty
	see https://github.com/UedaTakeyuki/mh-z19/wiki/How-to-Enable-Serial-Port-hardware-on-the-Raspberry-Pi
	but still need to figure out how to make python append to dumpfile.json without sudo

7.	setup your screen	
8.	sudo apt-get install --no-install-recommends xserver-xorg xinit x11-xserver-utils

set autologin
log errors
only allow ssh from one user
setting wifi connection for device   

	
Incognito mode (so it doesn't try to restart your last session after you inevitably kill the power)
Kiosk mode
Turn off pinch (so users can't zoom in/out)
Overscroll history navigation (to disable a user from scrolling left/right to go back/forward in the browser)

install Adafruit-Blinka, (CircuitPython compability library for Python in Linux SBCs), note that the script is interactive. CircuitPython is circuitry and hardware control capabilities with python
