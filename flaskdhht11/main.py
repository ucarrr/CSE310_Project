from flask import Flask, render_template
import RPi.GPIO as GPIO
import Adafruit_DHT as dht
 
app = Flask(__name__)
 
GPIO.setmode(GPIO.BCM)

DHT11_pin = 14

yl_channel = 21

GPIO.setmode(GPIO.BCM)

GPIO.setup(yl_channel,GPIO.IN)
 
ledGreen = 23 
ledRed = 24

# Set each pin as an output and make it low:
GPIO.setup(ledGreen, GPIO.OUT)
GPIO.setup(ledRed, GPIO.OUT)

 
@app.route("/") 
def main():
   return render_template('index.html')
 
# The function below is executed when someone requests a URL with the pin number and action in it:
@app.route("/<pin>/<action>")
def action(pin, action):
   temperature = ''
   humidity = ''
   moisture=  ''

 
   if pin == "dhtpin" and action == "get":
      humi, temp = dht.read_retry(dht.DHT11, DHT11_pin)  # Reading humidity and temperature
      inttemp = int(temp)
      humi = '{0:0.1f}' .format(humi)
      temp = '{0:0.1f}' .format(temp)
      temperature = 'Temperature: ' + temp 
      humidity =  'Humidity: ' + humi
     
      if inttemp < 27 :
          
          GPIO.output(ledGreen, GPIO.HIGH)
          GPIO.output(ledRed, GPIO.LOW)
      else :
          GPIO.output(ledGreen, GPIO.LOW)
          GPIO.output(ledRed, GPIO.HIGH)
      
      
    
   if pin == "pinmoisture" and action == "get":
       moisture_reading = GPIO.input(yl_channel)
       if moisture_reading == GPIO.LOW:
           
           moisture = 'Sufficient Moisture.'
         
         
       else:
           moisture = 'Low moisture, irrigation needed.'
     
     

    
   if pin == "pins" and action == "off":
       GPIO.output(ledGreen, GPIO.LOW)
       GPIO.output(ledRed, GPIO.LOW)
 
   templateData = {
   'temperature' : temperature,
   'humidity' : humidity,
   'moisture': moisture
   }
 
   return render_template('index.html', **templateData)
 
if __name__== "__main__":
    app.run(debug=True)

