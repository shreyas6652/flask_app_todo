from flask import Flask,jsonify
from flask_restful import Api,Resource,fields, marshal_with,reqparse
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
app=Flask(__name__)
api=Api(app)
CORS(app,resources=r'/api/*')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    Description = db.Column(db.String(200), nullable=True)
    Date=db.Column(db.String(500), nullable=True)
    StartTime = db.Column(db.String(500), nullable=True)
    EndTime=db.Column(db.String(500), nullable=True)
    EventCalendar=db.Column(db.String(500), nullable=True)
    Status = db.Column(db.String(500), nullable=True)

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

class GetTable(Resource):
    @marshal_with(resource_fields)
    def get(self):
        result=Todo.query.all()
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
        return(jsonobj)
    def post(self):
        args = info_put_args.parse_args()
        Description=args["Description"]
        Date=args["Date"]
        StartTime=args["StartTime"]
        EndTime=args["EndTime"]
        EventCalendar=args["EventCalendar"]
        Status=args["Status"]
        todo=Todo(Description=Description,Date=Date,StartTime=StartTime,EndTime=EndTime,EventCalendar=EventCalendar,Status=Status)
        db.session.add(todo)
        db.session.commit()
        return {"Description" :Description,"Date":Date,"StartTime":StartTime,"EndTime":EndTime,"EventCalendar":EventCalendar,"Status":Status}

class EditTable(Resource):
    def get(self,sno):
        todo = Todo.query.filter_by(sno=sno).first()
        return {"Description" :todo.Description,"Date":todo.Date,"StartTime":todo.StartTime,"EndTime":todo.EndTime,"EventCalendar":todo.EventCalendar,"Status":todo.Status}

    def put(self,sno):
        todo = Todo.query.filter_by(sno=sno).first()
        if not todo:
            return{"MessTime":"Data Doesnt exist"}
        args = info_put_args.parse_args()
        Description=args["Description"]
        Date=args["Date"]
        StartTime=args["StartTime"]
        EndTime=args["EndTime"]
        EventCalendar=args["EventCalendar"]
        Status=args["Status"]
        todo=Todo(Description=Description,Date=Date,StartTime=StartTime,EndTime=EndTime,EventCalendar=EventCalendar,Status=Status)
        db.session.add(todo)
        db.session.commit()
        return{"Message":"Updated Successfully"}

    def delete(self,sno):
        todo = Todo.query.filter_by(sno=sno).first()
        if not todo:
            return{"Message":"Data Doesnt exist"}
        db.session.delete(todo)
        db.session.commit()
        return{"Message":"Deleted Successfull"}

api.add_resource(GetTable,"/api/info")
api.add_resource(EditTable,"/api/edit/<int:sno>")

if __name__=="__main__":
    app.run(debug=True)