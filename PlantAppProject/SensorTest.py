import RPi.GPIO as GPIO
import Adafruit_DHT
import time

dht_sensor = Adafruit_DHT.DHT11
dht_pin=14

yl_channel = 21

pump=4
#led=4




GPIO.setmode(GPIO.BCM)

GPIO.setup(yl_channel,GPIO.IN)
#GPIO.setup(led, GPIO.OUT)

GPIO.setup(pump,GPIO.OUT)

GPIO.setwarnings(False)

def pump_on():
    GPIO.output(pump,GPIO.HIGH)
    print("Bitki sulanıyor")
    time.sleep(10)
    #GPIO.output(pump,GPIO.LOW)
    
    
    
def pump_off():
    GPIO.output(pump,GPIO.LOW)
    print("pump kapatıldı. Bitki sulandı.")
    



while True:
    humidity, temperature = Adafruit_DHT.read_retry(dht_sensor, dht_pin)
    moisture_reading = GPIO.input(yl_channel)
    if moisture_reading == GPIO.LOW:
        moisture = "Sufficient Moisture."
        pump_off()
        #GPIO.output(led, GPIO.LOW)

    else:
        moisture = "Low moisture, irrigation needed."
        pump_on()
        #GPIO.output(led, GPIO.HIGH)

    print("Sensor data: Humidity = {0:0.2f} % Temperature = {1:0.2f} deg C  Moisture : {2}".format(humidity,temperature,moisture))
    time.sleep(5)
    
GPIO.cleanup()    
