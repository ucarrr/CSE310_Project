import RPi.GPIO as GPIO
import Adafruit_DHT
import time
import sqlite3
import datetime

dht_sensor = Adafruit_DHT.DHT11
dht_pin=14

yl_channel = 21
GPIO.setmode(GPIO.BCM)
GPIO.setup(yl_channel,GPIO.IN)

#Initialize SQLite DB connection and cursor object
conn= sqlite3.connect("plant.db")
c= conn.cursor()

#Create sensor and reading tables
c.execute('''CREATE TABLE sensor
             (add_date text, sensor_text text, sensor_pin integer)''')

c.execute('''CREATE TABLE reading
             (add_date text, sensor_text text, value real)''')

#Add sensor to sensors DB table
add_date = str(datetime.date.today)
c.execute('''INSERT INTO sensor VALUES (?,?,?)'''
             (add_date,'DHT11 Temp & RH', dht_pin))
c.execute('''INSERT INTO sensor VALUES(?,?,?)'''
             (add_date, 'YL-69 Soil Moisture', yl_channel))
 


#Declare variable forsensor Outputs
while True:
    humidity, temperature = Adafruit_DHT.read_retry(dht_sensor, dht_pin)
    moisture_reading = GPIO.input(yl_channel)
    if moisture_reading == GPIO.LOW:
        moisture = "Sufficient Moisture."
        moisture_db = 1

    else:
        moisture = "Low moisture, irrigation needed."
        moisture_db = 0

#Print values to the terminal
    print("Sensor data: Humidity = {0:0.2f} % Temperature = {1:0.2f} deg C  Moisture : {2}".format(humidity,temperature,moisture))
    

#Add readings to DB reading table
    c.execute('''INSERT INTO reading VALUES (?,?,?)'''
                 (add_date, "Temperature", temperature))
    c.execute('''INSERT INTO reading VALUES (?,?,?)'''
                 (add_date, "Humidity", humidity))
    c.execute('''INSERT INTO reading VALUES (?,?,?)'''
                 (add_date, "Soil Moisture (1=sufficient moisture 0=dry", moisture_db))
    conn.commit()
    conn.close()    
    time.sleep(30)



