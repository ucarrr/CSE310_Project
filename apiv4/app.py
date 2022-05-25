from calendar import c
import json
from flask import Flask, jsonify, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import datetime 
from flask_marshmallow import Marshmallow
from flask_mysqldb import MySQL
import RPi.GPIO as GPIO
import Adafruit_DHT as dht
import mysql.connector
import time



app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456@localhost/flask'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Required
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "123456"
app.config["MYSQL_DB"] = "flask"
app.config["MYSQL_HOST"] = "localhost"
# Extra configs, optional:
app.config["MYSQL_CURSORCLASS"] = "DictCursor"
app.config["MYSQL_CUSTOM_OPTIONS"] = {"ssl": {"ca": "/path/to/ca-file"}}  

db = SQLAlchemy(app)
ma = Marshmallow(app)
mysql = MySQL(app)


# Breadbord setting section

GPIO.setmode(GPIO.BCM)

DHT11_pin = 14

yl_channel = 21

GPIO.setmode(GPIO.BCM)

GPIO.setup(yl_channel,GPIO.IN)
 
ledGreen = 23 
ledRed = 24


pump=4

heat=29

GPIO.setup(pump,GPIO.OUT)

# Set each pin as an output and make it low:
GPIO.setup(ledGreen, GPIO.OUT)
GPIO.setup(ledRed, GPIO.OUT)




class SensorData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    temperature = db.Column(db.Text())
    humidity = db.Column(db.Text())
    moisture = db.Column(db.Text())
    date = db.Column(db.DateTime, default = datetime.datetime.now)


    def __init__(self, temperature, humidity, moisture):
        self.temperature = temperature
        self.humidity = humidity
        self.moisture = moisture
        




class SensorDataSchema(ma.Schema):
    class Meta:
        fields = ('id', 'temperature', 'humidity','moisture', 'date')


article_schema = ArticleSchema()
articles_schema = ArticleSchema(many=True)



def pump_on():
    GPIO.output(pump,GPIO.HIGH)
    print("Bitki sulanıyor")
    time.sleep(3)
    GPIO.output(pump,GPIO.LOW)
    
    
    
def pump_off():
    GPIO.output(pump,GPIO.LOW)
    print("pump kapalı. Bitkinin suya ihtiyacı yok.")
    


@app.route('/addData')
def addData():
  
    
    
   
    humi, temp = dht.read_retry(dht.DHT11, DHT11_pin)  # Reading humidity and temperature
    inttemp = int(temp)
    humidity = '{0:0.1f}' .format(humi)
    temperature = '{0:0.1f}' .format(temp)
    
    if inttemp < 29 :
          
          GPIO.output(ledGreen, GPIO.HIGH)
          GPIO.output(ledRed, GPIO.LOW)
    else :
          GPIO.output(ledGreen, GPIO.LOW)
          GPIO.output(ledRed, GPIO.HIGH)

    
    moisture_reading = GPIO.input(yl_channel)
    if moisture_reading == GPIO.LOW:
        
        moisture = 'Sufficient Moisture.'
        pump_off()
         
         
    else:
        moisture = 'Low moisture, irrigation needed.'
        pump_on()
     
    
  
    
    articles = Articles(temperature, humidity, moisture)
    db.session.add(articles)
    db.session.commit()
    
    all_articles = Articles.query.all()
    results = articles_schema.dump(all_articles)
    
    
    return jsonify(results)
    

     


@app.route("/postData", methods=["POST"], strict_slashes=False)
def postData():
    print(request)
    termheat=request.json['heat']
    print('heat: ',heat)
    heat=int(termheat)
    return 'heat: '+ termheat


@app.route('/get', methods = ['GET'])
def get_articles():
    all_articles = Articles.query.all()
    results = articles_schema.dump(all_articles)
    return jsonify(results)

@app.route('/get/<id>/', methods = ['GET'])
def post_details(id):
    article = Articles.query.get(id)
    return article_schema.jsonify(article)

@app.route("/page", methods=["POST", "GET"])
def index():
    
    
    cur = mysql.connection.cursor()
    cur.execute('''SELECT * FROM articles''')
    data = cur.fetchall()
    cur.close()
    
    return render_template("index.html", data=data)

@app.route("/chart", methods=["POST", "GET"])
def chart():
    

    cur = mysql.connection.cursor()
    cur.execute('''SELECT * FROM articles''')
    data = cur.fetchall()
    cur.close()
    
    return render_template("chart.html", data=data)

@app.route("/page2", methods=["POST", "GET"])
def get():
    article = Articles.query.all()    
    return render_template("get.html",article=article)

@app.route('/a')
def users():
    cur = mysql.connection.cursor()
    cur.execute('''SELECT * FROM articles''')
    rv = cur.fetchall()
    cur.close()  
    output = json.dumps(rv, default = str)
    
    return output


@app.route('/add', methods = ['POST'])
def add_article():
    title = request.json['title']
    body = request.json['body']

    articles = Articles(title, body)
    db.session.add(articles)
    db.session.commit()
    return article_schema.jsonify(articles)



@app.route('/update/<id>/', methods = ['PUT'])
def update_article(id):
    article = Articles.query.get(id)

    title = request.json['title']
    body = request.json['body']

    article.title = title
    article.body = body 

    db.session.commit()
    return article_schema.jsonify(article)


@app.route('/delete/<id>/', methods = ['DELETE'])
def article_delete(id):
    article = Articles.query.get(id)
    db.session.delete(article)
    db.session.commit()

    return article_schema.jsonify(article)



if __name__ == "__main__":
    app.run(debug=True)