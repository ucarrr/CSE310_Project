from calendar import c
import json
from flask import Flask, jsonify, request,render_template,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
import datetime 
from flask_marshmallow import Marshmallow
from flask_mysqldb import MySQL


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/flask'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Required
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "flask"
app.config["MYSQL_HOST"] = "localhost"
# Extra configs, optional:
app.config["MYSQL_CURSORCLASS"] = "DictCursor"
app.config["MYSQL_CUSTOM_OPTIONS"] = {"ssl": {"ca": "/path/to/ca-file"}}  

db = SQLAlchemy(app)
ma = Marshmallow(app)
mysql = MySQL(app)


class Articles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    body = db.Column(db.Text())
    date = db.Column(db.DateTime, default = datetime.datetime.now)


    def __init__(self, title, body):
        self.title = title
        self.body = body



class ArticleSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'body', 'date')


article_schema = ArticleSchema()
articles_schema = ArticleSchema(many=True)


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
    
    article = Articles.query.get(id)
    cur = mysql.connection.cursor()
    cur.execute('''SELECT * FROM articles''')
    data = cur.fetchall()
    cur.close()
    
    return render_template("index.html", data=data)

@app.route("/chart", methods=["POST", "GET"])
def chart():
    
    article = Articles.query.get(id)
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