import RPi.GPIO as GPIO
import Adafruit_DHT
import time

dht_sensor = Adafruit_DHT.DHT11
dht_pin=14

yl_channel = 21
GPIO.setmode(GPIO.BCM) #Represents pin numbers specific to the Broadcom chip.
GPIO.setup(yl_channel,GPIO.IN) #21. pinden veri geleceğini belirtir. Veri gelişi olduğu için "in" kullanılır.


while True:
    humidity, temperature = Adafruit_DHT.read_retry(dht_sensor, dht_pin)
    moisture_reading = GPIO.input(yl_channel)
    if moisture_reading == GPPIO.LOW:
        moisture = "Sufficient Moisture."

    else:
        moisture = "Low moisture, irrigation needed."

    print("Sensor data: Humidity = {0:0.2f} % Temperature = {1:0.2f} deg C  Moisture : {2}".format(humidity,temperature,moisture))
    time.sleep(5)