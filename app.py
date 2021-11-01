from enum import unique
from flask import Flask,jsonify
from flask import request
from flask.helpers import make_response
from flask.json import JSONDecoder
from flask_restful import Api,Resource,fields, marshal_with,reqparse
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
import uuid
from werkzeug.security import generate_password_hash,check_password_hash
import jwt
import json
import datetime
from functools import wraps
import requests
import time
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
app=Flask(__name__)
api=Api(app)
CORS(app)
cors = CORS(app, 
resources={r"/api/*": 
{
    "origins": "*"
    }
})

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database1.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['SECRET_KEY'] = 'thisissecret'
db = SQLAlchemy(app)

class User(db.Model):
    ID=db.Column(db.Integer, primary_key=True)
    Email=db.Column(db.String(200),unique=True)
@app.route('/api/user', methods=['GET'])
def get_all_users():
    Users=User.query.all()
    Data=[]
    for User1 in Users:
        UserData= {}
        UserData["Email"]=User1.Email
        Data.append(UserData)
    return jsonify({"Users":Data})

@app.route('/api/user', methods=['POST'])
def create_users():
    if request.method=='POST':
        data=request.get_json()
       
        try:
            new_user=User(Email=data['Email'])
            db.session.add(new_user)
            db.session.commit()
        except:
            return jsonify({"Message":"Couldnt Create"}),400
        return  ("Created")

def print_date_time():   
    url = 'https://www.fast2sms.com/dev/bulkV2'
    message="Oyee Lakshmi Devi, Message nod hog\nTime is "+time.asctime( time.localtime(time.time()) )
    myobj ={"route" : "v3","sender_id" : "TXTIND", "message" :message,"language" : "english","flash" : 0,"numbers" :"7483985695" }
    headers = {'Authorization':'mGQ2AkguCEiPnj81pRSDdwJrLoH40VahKXZ97YvqNOtWTFeyzbb7glzs0yLhTDXpjvrk8PYUd94oWiI2'}
    x =requests.post(url,data=myobj, headers=headers)
    return ("Success")

@app.route('/test', methods=['POST'])
def test():
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=print_date_time, trigger="interval", seconds=10)
    scheduler.start()
@app.route('/test1', methods=['GET'])
def test1():
    return ("Working")

if __name__=="__main__":
    app.run(debug=True)