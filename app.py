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
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['SECRET_KEY'] = 'thisissecret'
db = SQLAlchemy(app)

class User(db.Model):
    ID=db.Column(db.Integer, primary_key=True)
    Public_ID=db.Column(db.String(200), unique=True)
    Name=db.Column(db.String(200))
    Password=db.Column(db.String(200))
    Admin=db.Column(db.Boolean)
    Email=db.Column(db.String(200),unique=True)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    Description = db.Column(db.String(200), nullable=True)
    Date=db.Column(db.String(500), nullable=True)
    StartTime = db.Column(db.String(500), nullable=True)
    EndTime=db.Column(db.String(500), nullable=True)
    EventCalendar=db.Column(db.String(500), nullable=True)
    Status = db.Column(db.String(500), nullable=True)
    USER_ID=db.Column(db.String(500))

def token_required(f):
    
    @wraps(f)
    def decorated(*args,**kwargs):
        token=None
        if 'x-access-token' in request.headers:
            token=request.headers['x-access-token']
        if not token:
            return jsonify({'Message':'Token is missing!'}),401
        Users=User.query.all()
        Data1=[]
        CurrentUser=None
        for User1 in Users:
            UserData= {}
            UserData['Public_ID']=User1.Public_ID
            UserData["Email"]=User1.Name
            Data1.append(UserData)
        try:
            data=jwt.decode(token,app.config['SECRET_KEY'],algorithms="HS256")
            CurrentUser=User.query.filter_by(Public_ID=data['Public_ID']).first()
             
        except:
            return jsonify({'message':'Token is invalid'}),401

        return f(CurrentUser,*args,**kwargs)

    return decorated


@app.route('/user', methods=['GET'])
@token_required
def get_all_users(CurrentUser):
    Users=User.query.all()
    Data=[]
    for User1 in Users:
        UserData= {}
        UserData['Public_ID']=User1.Public_ID
        UserData["Name"]=User1.Name
        UserData["Email"]=User1.Email
        Data.append(UserData)
    return jsonify({"Users":Data})

@app.route('/api/user', methods=['POST'])
def create_users():
    data=request.get_json()
    hashed_password=generate_password_hash(data['Password'],method='sha256')
    try:
      new_user=User(Public_ID=str(uuid.uuid4()),Email=data['Email'],Name=data['Name'],Password=hashed_password,Admin=False)
      db.session.add(new_user)
      db.session.commit()
    except:
        return jsonify({"Message":"Couldnt Create"}),400
    return  ("Created")

@app.route('/api/user',methods=['GET'])
@token_required
def get_one_user(CurrentUser):
    User1=User.query.filter_by(Public_ID=CurrentUser.Public_ID).first()
    if not User1:
        return jsonify({'Message':'No user Data'})
    UserData={}
    UserData["Email"]=User1.Email
    UserData['Public_ID']=User1.Public_ID
    UserData["Name"]=User1.Name
    
    return jsonify(UserData)

# @app.route('/user/<Public_ID)>',methods=['PUT'])
# def promote_user(Public_ID):
#     User1=User.query.filter_by(Public_ID=Public_ID).first()
#     if not User1:
#         return jsonify({'Message':'No user Data'})
#     return ''

@app.route('/user/<user_id>',methods=['DELETE'])
@token_required
def delete_user(CurrentUser):
    if not CurrentUser.admin:
        return jsonify({'Message':'You cant Perform it'})
    User1=User.query.filter_by(Public_ID=CurrentUser.ID).first()
    if not User1:
        return jsonify({'Message':'No user Data'})
    db.session.delete(User1)
    db.session.commit()
    return jsonify({'Message':'The user has been deleted'})

@app.route('/api/login')
def login():
    auth=request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify',401)
    
    user=User.query.filter_by(Email=auth.username).first()
    if not user:
        return make_response('Could not verify',401)
    
    if check_password_hash(user.Password,auth.password):
        token=jwt.encode({'Public_ID':user.Public_ID,'exp':datetime.datetime.utcnow()+datetime.timedelta(minutes=1000)},app.config['SECRET_KEY'])
        return jsonify({"Token": token})
    return make_response('Could not verify',401)

resource_fields={
    'sno':fields.Integer,
    'Description':fields.String,
    'Date':fields.String,
    'StartTime':fields.String,
    'EndTime':fields.String,
    'EventCalendar':fields.String,
    'Status':fields.String
}

info_put_args = reqparse.RequestParser()
info_put_args.add_argument("Description", type=str, required=True)
info_put_args.add_argument("Date", type=str, required=True)
info_put_args.add_argument("StartTime", type=str, required=True)
info_put_args.add_argument("EndTime", type=str, required=True)
info_put_args.add_argument("EventCalendar", type=str, required=True)
info_put_args.add_argument("Status", type=str,  required=True)

@app.route('/api/info',methods=['GET'])
@token_required
def get(CurrentUser):
    result=Todo.query.filter_by(USER_ID=CurrentUser.ID).all()
    jsonobj=[]
    for itr in result:
        jsonitr={
            "sno":itr.sno,
            "Description":itr.Description,
            "Date":itr.Date,
            "StartTime":itr.StartTime,
            "EndTime":itr.EndTime,
            "EventCalendar":itr.EventCalendar,
            "Status":itr.Status
                }
        jsonobj.append(jsonitr)
    
    return jsonify(jsonobj)
    
@app.route('/api/info',methods=['POST'])
@token_required
def post(CurrentUser):
    args = request.get_json()
    USER_ID=CurrentUser.ID
    Description=args["Description"]
    Date=args["Date"]
    StartTime=args["StartTime"]
    EndTime=args["EndTime"]
    EventCalendar=args["EventCalendar"]
    Status=args["Status"]    
    todo=Todo(Description=Description,Date=Date,StartTime=StartTime,EndTime=EndTime,EventCalendar=EventCalendar,Status=Status,USER_ID=USER_ID)
    db.session.add(todo)
    db.session.commit()
    return {"ID":"hjey","Description" :Description,"Date":Date,"StartTime":StartTime,"EndTime":EndTime,"EventCalendar":EventCalendar,"Status":Status}

@app.route('/api/calendar/<int:sno>',methods=['GET'])
@token_required
def put(self,sno):
    todo = Todo.query.filter_by(sno=sno).first()
    if not todo:
        return{"MessTime":"Data Doesnt exist"} ,401
    todo.EventCalendar=True
    db.session.commit()
    return{"Message":"Updated Successfully"},200
class EditTable(Resource):
    def get(self,sno):
        todo = Todo.query.filter_by(sno=sno).first()
        return {"Description" :todo.Description,"Date":todo.Date,"StartTime":todo.StartTime,"EndTime":todo.EndTime,"EventCalendar":todo.EventCalendar,"Status":todo.Status}

    def put(self,sno):
        todo = Todo.query.filter_by(sno=sno).first()
        if not todo:
            return{"MessTime":"Data Doesnt exist"}
        args = info_put_args.parse_args()
        Status=args["Status"]
        todo.Status=Status
        db.session.commit()
        return{"Message":"Updated Successfully"}

    def delete(self,sno):
        todo = Todo.query.filter_by(sno=sno).first()
        if not todo:
            return{"Message":"Data Doesnt exist"}
        db.session.delete(todo)
        db.session.commit()
        return{"Message":"Deleted Successfull"}


api.add_resource(EditTable,"/api/edit/<int:sno>")

if __name__=="__main__":
    app.run(debug=True)