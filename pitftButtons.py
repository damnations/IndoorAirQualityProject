import RPi.GPIO as GPIO  
import time    
import os

# Set gpio mode
GPIO.setmode(GPIO.BCM)

# Set gpio pins
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)  
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)  
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)  
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP) 

# Set backlight GPIO configuration
os.system("echo 27 >/sys/class/gpio/export")

# 1 means backlight is off, 0 means backlight is on
buttonOnOff = 0

while True:
    # GPIO17 as shutdown button
    if (GPIO.input(17) == False):   
        print("SHUTDOWN!!!")  
        os.system("sudo shutdown -h now") 
    
    # GPIO22 currently not functional
    if (GPIO.input(22) == False):  
        print("Button 22 Working")  
        time.sleep(0.5)  

    # GPIO23 currently not functional
    if (GPIO.input(23) == False):  
        print("Button 27 working")  
        time.sleep(0.5)
    
    # GPIO27 as backlight control
    if (GPIO.input(27) == False):
        if (buttonOnOff == 0):
            os.system("echo out >/sys/class/gpio/gpio27/direction")
            buttonOnOff = 1
            print ("Setting Backlight Direction to Out")
            time.sleep(0.5)

        elif (buttonOnOff == 1 or buttonOnOff == 3):
            os.system("echo 1 >/sys/class/gpio/gpio27/value")
            buttonOnOff = 2
            print ("Backlight Off")
            time.sleep(0.5)

        elif (buttonOnOff == 2):
            os.system("echo 0 >/sys/class/gpio/gpio27/value")
            buttonOnOff = 3
            print ("Backlight On")
            time.sleep(0.5)

    GPIO.cleanup()