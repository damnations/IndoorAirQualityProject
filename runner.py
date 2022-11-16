import mh_z19, board, digitalio, adafruit_dht, psutil, json, asyncio, os
from datetime import datetime, timezone
from time import sleep
from bmp280 import BMP280
from smbus import SMBus
from azure.iot.device.aio import IoTHubDeviceClient

# Initialize the dht11 sensor connected to GPIO17 pin on the raspberry
dht_11 = adafruit_dht.DHT11(board.D17)

# Initialize the bmp280 sensor using I2C communication, note that I2C has to be enabled on your device
bus = SMBus(1)
bmp280 = BMP280(i2c_dev=bus)

# Define GPIO26 and GPIO19 usage as input for voc sensor measurements (ZP01-MP503)
VOC_A = digitalio.DigitalInOut(board.D26)
VOC_B = digitalio.DigitalInOut(board.D19)
VOC_A.direction = digitalio.Direction.INPUT
VOC_B.direction = digitalio.Direction.INPUT

# Function to read voc levels
# VOC level is read as two digit binary number, converting to decimal
# So:
# 00 -> 0   corresponding to Clean
# 01 -> 1   corresponding to Light pollution
# 10 -> 2   corresponding to Moderate pollution
# 11 -> 3   corresponding to Severe pollution
def read_voc():
	total_value = 0
	aValue = VOC_A.value
	bValue = VOC_B.value
	if(aValue == 1):
		total_value+=2
	if(bValue == 1):
		total_value+=1
	return total_value

# Set connection string as an environment variable beforehand
# export IOTHUB_DEVICE_CONNECTION_STRING={iothub connection string}
conn_str = os.getenv("IOTHUB_DEVICE_CONNECTION_STRING")

# Use global variable to update sleep time between measurements
# Currently measurement and post time is the same, could be developed further to support buffering measurements with smaller interval than posting
SLEEP_TIME = 5

# Main loop, code to be executed is placed in here
async def main():
    # Use global variable, so it can be updated by device twin
    global SLEEP_TIME

    # Check if a libgpiod process is running. If yes, kill it!
    for proc in psutil.process_iter():
        if proc.name() == 'libgpiod_pulsein' or proc.name() == 'libgpiod_pulsei':
            proc.kill()

    # Create an IoTHubDeviceClient object from connection string
    iot_device_client = IoTHubDeviceClient.create_from_connection_string(conn_str)
    
    # Wait for the device to connect to Azure IoTHub
    await iot_device_client.connect()

    # Infinite loop to keep taking measurements as long as device is powered on and connected to cloud
    while True:
        try:
            # Read measurement values into a dictionary
            values = mh_z19.read(serial_console_untouched=True)
            values['temp'] = dht_11.temperature
            values['humidity'] = dht_11.humidity
            values['pressure'] = bmp280.get_pressure()
            values['voc'] = read_voc() 
            values['time(UTC)'] = str(datetime.now(timezone.utc)) # Datetime is in UTC
            values['metadata'] = {"evetType": "measurement"}
            
            # Send measurement vales to Azure IoTHub
            await iot_device_client.send_message(json.dumps(values))

        # Skip over RuntimeErrors and continue to try to run the while loop
        except RuntimeError as error:
            print(error.args[0])
            sleep(SLEEP_TIME)
            continue

        # If other errors occur, device to shutdown
        except Exception as error:
            dht_11.exit()
            await iot_device_client.shutdown()
            raise error

        sleep(SLEEP_TIME)

if __name__ == "__main__":
	asyncio.run(main())