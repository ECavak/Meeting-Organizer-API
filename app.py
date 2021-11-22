from flask import Flask,request,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app=Flask(__name__)

basedir=os.path.abspath(os.path.dirname(__file__))

#Database
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+os.path.join(basedir,'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
#Inıt db
db = SQLAlchemy(app)
#Init marsh
ma=Marshmallow(app)

#Meeting Class/Model
class Meeting(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    subject=db.Column(db.String)
    startDate=db.Column(db.String)
    startTime=db.Column(db.String)
    endTime=db.Column(db.String)
    participants=db.Column(db.String(200))

    def __init__(self,subject,startDate,startTime,endTime,participants):
        self.subject=subject
        self.startDate=startDate
        self.startTime=startTime
        self.endTime=endTime
        self.participants=participants
    
#Meeting Schema
class MeetingSchema(ma.Schema):
    class Meta:
        fields=('id','subject',"startDate",'startTime','endTime','participants')       

#Init Schema
meeting_schema=MeetingSchema()
meetings_schema=MeetingSchema(many=True)


#Create Meeting
@app.route('/meeting',methods=['POST'])
def add_meeting():
    subject=request.json['subject']
    startDate=request.json['startDate']
    startTime=request.json['startTime']
    endTime=request.json['endTime']
    participants=request.json['participants']

    new_meeting=Meeting(subject,startDate,startTime,endTime,participants)
    db.session.add(new_meeting)
    db.session.commit()

    return meeting_schema.jsonify(new_meeting)
#Get All Meeting
@app.route('/meeting',methods=['GET'])
def get_meetings():
    all_meetings=Meeting.query.all()
    result=meetings_schema.dump(all_meetings)
    return jsonify(result)

#Get Single Meeting
@app.route('/meeting/<id>',methods=['GET'])
def get_meeting(id):
    meeting=Meeting.query.get(id)
    return meeting_schema.jsonify(meeting)

#Update Meeting
@app.route('/meeting/<id>',methods=['PUT'])
def update_meeting(id):
    meeting=Meeting.query.get(id)

    subject=request.json['subject']
    startDate=request.json['startDate']
    startTime=request.json['startTime']
    endTime=request.json['endTime']
    participants=request.json['participants']

    meeting.subject=subject
    meeting.startDate=startDate
    meeting.startTime=startTime
    meeting.endTime=endTime
    meeting.participants=participants

    db.session.commit()

    return meeting_schema.jsonify(meeting)

#Delete  Meeting
@app.route('/meeting/<id>',methods=['DELETE'])
def delete_meeting(id):
    meeting=Meeting.query.get(id)
    db.session.delete(meeting)
    db.session.commit()
    return meeting_schema.jsonify(meeting)

if __name__ == '__main__':
    app.run(debug=True)