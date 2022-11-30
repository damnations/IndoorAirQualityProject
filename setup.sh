#!/bin/bash
cd $HOME 
sudo apt update
sudo apt upgrade -y
sudo apt autoremove -y
git clone https://github.com/UedaTakeyuki/mh-z19.git
cd mh-z19
sudo pip3 install mh_z19 pondslider incremental_counter error_counter
git clone https://github.com/UedaTakeyuki/handlers
ln -s handlers/value/sender/send2monitor/send2monitor.py
sudo sed -i "s/^enable_uart=.*/enable_uart=1/" /boot/config.txt
cd $HOME
FILE=$HOME/raspi-blinka.py
if [[ -f "$FILE" ]]; then
    rm raspi-blinka.py
fi
sudo pip3 install --upgrade adafruit-python-shell
wget https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/raspi-blinka.py
sudo raspi-config nonint do_blanking 1
sudo sed -i "s/do_serial 0/do_serial 2/" $HOME/raspi-blinka.py
sudo sed -i "s/install -y python3-pip/install -y python3-pip git chromium-browser unclutter/" $HOME/raspi-blinka.py
sudo python3 raspi-blinka.py