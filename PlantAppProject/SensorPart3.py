import RPi.GPIO as GPIO
import Adafruit_DHT
import time
import smtplib, ssl

#Declare variables for SMTP mail send
password =""
port =465
smtp_server ="gmail.com"
sender_email ="smtp.gmail.com"
receiver_email ="chatnoirladybug414@gmail.com"
message = """\
Subject: Low Moisture Detected
Low Moisture has been detected on the soil moisture sensor."""

#create a secure context
context = ssl.create_default_context()


#Declare and initialize DHT11 Temperature and Humidity Sensor
dht_sensor = Adafruit_DHT.DHT11
dht_pin=14


#Declare YL69 Soil Moisture Sensor
yl_channel = 21
GPIO.setmode(GPIO.BCM)
GPIO.setup(yl_channel,GPIO.IN)


#Declare variable for sensorOutputs
while True:
    humidity, temperature = Adafruit_DHT.read_retry(dht_sensor, dht_pin)
    moisture_reading = GPIO.input(yl_channel)
    if moisture_reading == GPIO.LOW:
        moisture = "Sufficient Moisture."

    else:
        moisture = "Low moisture, irrigation needed."
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email,password)
            server.sendmail(sender_email,receiver_email,message)
        
#Print values to the terminal
    print("Sensor data: Humidity = {0:0.2f} % Temperature = {1:0.2f} deg C  Moisture : {2}".format(humidity,temperature,moisture))
    time.sleep(5)
