from flask import Flask 
from flask_sqlalchemy import SQLAlchemy 
from flask_restless import APIManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/abdlmalik/Desktop/Flask/UltimateFlask/Restless-Flask/api.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db = SQLAlchemy(app)
manager = APIManager(app, flask_sqlalchemy_db=db)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)
    items = db.relationship('Item', backref='user', lazy='dynamic')

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

manager.create_api(User,methods=["GET","POST","PUT"])
manager.create_api(Item,methods=["GET","POST",'DELETE','PUT'])

if __name__ == '__main__':
    app.run(debug=True)