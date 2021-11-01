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
import datetime
from functools import wraps

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

def get_all_users():
    Users=User.query.all()
    Data=[]
    for User1 in Users:
        UserData= {}
        UserData["Email"]=User1.Email
        Data.append(UserData)
    return jsonify({"Users":Data})

def create_users():
    if request.method=='POST':
        data=request.get_json()
        hashed_password=generate_password_hash(data['Password'],method='sha256')
        try:
            new_user=User(Email=data['Email'])
            db.session.add(new_user)
            db.session.commit()
        except:
            return jsonify({"Message":"Couldnt Create"}),400
        return  ("Created")