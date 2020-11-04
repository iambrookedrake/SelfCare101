from flask_sqlalchemy import SQLAlchemy
#import selfcare
#from selfcare import connection, cursor
import app


DB = SQLAlchemy()


class Client(DB.Model):
    id = DB.Column(DB.BigInteger, primary_key=True)  
    Age = DB.Column(DB.Integer, nullable=False)
    Weight = DB.Column(DB.Integer, nullable=False)
    Water = DB.Column(DB.Integer, nullable=False)
    PhoneTime = DB.Column(DB.Integer, nullable=False)
    CompTime = DB.Column(DB.Integer, nullable=False)
    DriveTime = DB.Column(DB.Integer, nullable=False)
    SittingTime = DB.Column(DB.Integer, nullable=False)
    StandingTime = DB.Column(DB.Integer, nullable=False)
    WalkingTime = DB.Column(DB.Integer, nullable=False)
    RunningTime = DB.Column(DB.Integer, nullable=False)
    BikingTime = DB.Column(DB.Integer, nullable=False)
    ExerciseTime = DB.Column(DB.Integer, nullable=False)
    StretchingTime = DB.Column(DB.Integer, nullable=False)
    SleepingTime = DB.Column(DB.Integer, nullable=False)
    WorkingTime = DB.Column(DB.Integer, nullable=False)
    Digestion = DB.Column(DB.Text, nullable=False)
    Stamina = DB.Column(DB.Text, nullable=False)
    Mood = DB.Column(DB.Text, nullable=False)
    Headaches = DB.Column(DB.Text, nullable=False)
    Fallen = DB.Column(DB.Text, nullable=False)
    HeadTrauma = DB.Column(DB.Text, nullable=False)
    PainLevel = DB.Column(DB.Integer, nullable=False)
    SleepPose = DB.Column(DB.Text, nullable=False)
    DrivePose = DB.Column(DB.Text, nullable=False)
    WorkPose = DB.Column(DB.Text, nullable=False)

    def __repr__(self):
        return '<Client %r>' % self.Age


# To create the database:
# python
# from SelfCare101.db_model import DB, Client
# DB.create_all()
# to reset
# DB.drop_all()
