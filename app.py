from flask import Flask, render_template, request
from db_model import DB #, Client
import selfcare
from selfcare import connection, cursor
from dotenv import load_dotenv
from os import getenv
import copy
import json

load_dotenv()

# Internal Links
CSTLink = '<a href="/CranioSacralTherapy">CranioSacral Therapy</a>'
TPTLink = '<a href="/TriggerPointTherapy">Trigger Point Therapy</a>'
HoldingLink = '<a href="/ChronicHoldingPatterns">Chronic Holding Patterns</a>'
ContrastLink = '<a href="/ContrastTreatment">Contrast Treatment</a>'
GlutesLink = '<a href="/Glutes">Glutes</a>'
StretchingLink = '<a href=/Stretching>Stretching</a>'
PainScaleLink = '<a href=/PainScale>Pain Scale</a>'
MoodCureBookLink = '<a href=https://www.juliarosscures.com/mood-cure/>This book</a>'

# Create App
def create_app():
    '''Create and configure an instance of our Flask application'''
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:\\Users\\iambr\\Desktop\\Massage\\selfcare101\\selfcare.sqlite3'  # for absolute path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['FLASK_ENV'] = 'development' # Turns debug mode ON
    DB.init_app(app)  # Connect Flask app to SQLAlchemy DB
    #with app.app_context():#to create app for DB
        #DB.create_all()

    @app.route('/')
    @app.route('/intake')
    def intake():
        return render_template('intake.html', title='Intake')

    @app.route('/survey', methods=['POST'])
    def survey():
        #return request.form['Over18']
        Over18 = request.form['Over18']
        CurrentlyPregnant = request.form['CurrentlyPregnant']
        DrsCare = request.form['DrsCare']
        InjuryStatus = request.form['InjuryStatus']
        #FullIntake = request.form

        if Over18=='Child':
            return 'Please ask an adult to help you use this app. :-)'
        if CurrentlyPregnant=='Pregnant':
            return 'Please consult your medical provider to ask whether you should use this app while pregnant. :-)'
        if DrsCare=='UnderDr':
            return 'Please consult your medical provider to ask whether you should use this app while under their care. :-)'
        if InjuryStatus=='Major':
            return 'Please consult your medical provider to ask whether you should use this app while injured. :-)'

        else:
            return render_template('survey.html', title='Health Screening') 


    @app.route('/results', methods=['POST']) #from survey.html
    def results():
        Age = int(request.form['Age'])
        Weight = int(request.form['Weight'])
        Water = int(request.form['Water'])
        PhoneTime = int(request.form['PhoneTime'])
        CompTime = int(request.form['CompTime'])
        DriveTime = int(request.form['DriveTime'])
        SittingTime = int(request.form['SittingTime'])
        StandingTime = int(request.form['StandingTime'])
        WalkingTime = int(request.form['WalkingTime'])
        RunningTime = int(request.form['RunningTime'])
        BikingTime = int(request.form['BikingTime'])
        ExerciseTime = int(request.form['ExerciseTime'])
        StretchingTime = int(request.form['StretchingTime'])
        SleepingTime = int(request.form['SleepingTime'])
        WorkingTime = int(request.form['WorkingTime'])
        Digestion = request.form['Digestion']
        Stamina = request.form['Stamina']
        Mood = request.form['Mood']
        Headaches = request.form['Headaches']
        Fallen = request.form['Fallen']
        HeadTrauma = request.form['HeadTrauma']
        PainLevel = int(request.form['PainLevel'])
        SleepPose = request.form['SleepPose']
        DrivePose = request.form['DrivePose']
        WorkPose = request.form['WorkPose']

        FullForm = request.form
        FullForm = FullForm.copy()
        #print(FullForm)
        data  = json.dumps(FullForm, skipkeys=True)

        MSGProblem = 'Based off your answers, here are a few things that might be affecting your day: <br/><br/><br/>'
        MSGSolution = '<br/><br/><br/>And here are some suggestions as to what you can do to improve the quality of your life: <br/><br/><br/>'
        VeryActive = False
        ###########################################PROBLEM LISTINGS##################################
        # Suggested Water Intake vs Actual
        suggWaterMIN = 0.75*(Weight/2)
        suggWater = round(Weight/2)
        suggWaterGlass = round(suggWater/12)
        if Water>=suggWaterMIN:
            MSGWater = "Great job on drinking plenty of water!<br/><br/>"
        else:
            MSGWater = f'Try to drink at least {suggWater} ounces, which is just {suggWaterGlass} "12-ounce glasses" of water every day.<br/><br/>'
        #return MSGWater

        # Suggested Phone Time
        if PhoneTime>=60:
            tense = True
            MSGPhone = f"Spending a lot of time looking DOWN at our phones can cause extra strain on our neck and skull.<br/><br/>"
        else:
            MSGPhone = ""
        #return MSGPhone

       # Suggested Computer Time
        if CompTime>=120:
            tense = True
            spasm = True
            MSGComp = f"Computer work, or any work with our hands can cause spasms in the rotator cuff.<br/><br/>"
        else:
            MSGComp = ""
        #return MSGPhone
        
        # Suggested Drive Time
        if DriveTime>=90:
            tense = True
            spasm = True
            MSGDrive = f"Driving long hours can cause {HoldingLink} which lead to chonic pain.<br/><br/>"
        else:
            MSGDrive = ""
        #return MSGDrive

        # Suggested Sitting Time
        if SittingTime>=120:
            stiff = True
            MSGSitting = f"Sitting for long periods decreases blood flow to the {GlutesLink} and legs.<br/><br/>"
        else:
            MSGSitting = ""
        #return MSGSitting
        
        # Suggested Standing Time
        if StandingTime>=120:
            tense = True
            stiff = True
            MSGStanding = f"Standing still for long periods is hard on the knees and ankles. To maintain circulation and avoid {HoldingLink}, keep your knees slightly bent, rather than locking them in place. {StretchingLink} can help prevent low back pain.<br/><br/>"
        else:
            MSGStanding = ""
        #return MSGStanding
        
        # Suggested Walking Time
        if WalkingTime>=60:
            tense = True
            stiff = True
            MSGWalking = f"Walking long distances can cause your IT Band to stiffen up, which can lead to pain the knees or low back.<br/><br/>"
        elif WalkingTime<=10:
            stiff = True
            MSGWalking = ""
        else:
            MSGWalking = ""
        #return MSGWalking
        
        # Suggested Running Time
        if RunningTime>=30 and WalkingTime<60:
            tense = True
            VeryActive = True
            MSGRunning = f"Running long distances can cause your IT Band to stiffen up, which can lead to pain the knees or low back.<br/><br/>"
        elif RunningTime>=30 and WalkingTime>=60:
            MSGRunning = f"Running is great cardio but it's even harder on your knees than walking. Consider riding a Bicycle or Roller Skating for less impact."
        else:
            MSGRunning = ""
        #return MSGRunning
        
        # Suggested Biking Time
        if BikingTime>=30 and RunningTime<30 and WalkingTime<60:
            tense = True
            MSGBiking = f"Biking long distances can cause your IT Band to stiffen up, which can lead to pain the knees or low back.<br/><br/>"
        else:
            MSGBiking = ""
        #return MSGBiking

        # Suggested Exercise Time
        if (ExerciseTime+BikingTime+RunningTime+WalkingTime)>=60:
            VeryActive = True
            MSGExercise = f"Exercise is wonderful but don't forget to take a day off each week to let your body recover.<br/><br/>"
        else:
            MSGExercise = ""
        #return MSGExercise
        
        # Suggested Stretching Time
        if StretchingTime<+10:
            tense = True
            stiff = True
            MSGStretching = f"{StretchingLink} for even a few minutes per day increases range of motion, joint mobility, and circulation throughout your body. It can help to improve energy, mood, and pain tolerance.<br/><br/>"
        else:
            MSGStretching = ""
        #return MSGStretching

        # Suggested Sleeping Time
        if SleepingTime<6 or SleepingTime>9:
            tense = True
            MSGSleeping = f"Sleep helps our bodies repair damaged tissue and regulate systems throughout our body. Too little OR too much can affect mood, appetite, energy levels, and immunity.<br/><br/>"
        else:
            MSGSleeping = ""
        #return MSGSleeping
        
        # Suggested Working Time
        if WorkingTime>9:
            tense = True
            MSGWorking = f"You work hard. Make sure your body works with you, not against you.<br/><br/>"
        else:
            MSGWorking = ""
        #return MSGWorking

        # Suggested Pain Level
        if PainLevel>=7:
            tense = True
            MSGHighPain = f"Severe pain can affect your central nervous system. Consult a doctor about your pain as soon as possible.<br/><br/>"
        elif PainLevel>=3:
            MSGHighPain = f"Over time, even moderate pain can affect your central nervous system and lead to {HoldingLink}.<br/><br/>"
        else:
            MSGHighPain = ""
        #return MSGHighPain

        # Digestion Relief
        if Digestion=="SlowDigest":
            MSGDigestion = f'Digestion can be affected by many factors. I find the most commonly overlooked treatments are {StretchingLink} your abdominal area or performing {TPTLink} on your Psoas Muscle.<br/><br/>'
        else:
            MSGDigestion = ""

        # Improve Stamina 
        if Stamina=="LowStamina":
            MSGStamina = f'Along with improving your diet, massage can help improve stamina for sports or academics.<br/><br/>'
        else:
            MSGStamina = ""

        # Improve Mood
        if Mood=="BadMood":
            MSGMood = 'MOOOODY'#f'{MoodCureBookLink} helped me undertand how my diet affects my moods.<br/><br/>'
        else:
            MSGMood = 'MOOOODY2'#""

        # Decrease Headaches
        if Headaches=="Headaches":
            MSGHeadaces = f"If you already improved your diet and water intake and don't smoke cigarettes, consider {CSTLink} to help treat your chronic headaches or migraines.<br/><br/>"
        else:
            MSGHeadaces = ""

        # Spinal Compression
        if Fallen=="ManyTailFalls" or Fallen=="OneTailFall":
            MSGFallen = f'Falling can compress the spine and pinch nerves, leading to chronic pain. {CSTLink} can help with this.<br/><br/>'
        else:
            MSGFallen = ""

        # Treat Head Trauma
        if HeadTrauma=='ManyHeadTraumas' or HeadTrauma=='OneHeadTrauma':
            MSGHeadTrauma = f'Any traumatic injury to the head, neck, or spine can affect the central nervous system. Many people have experienced relief from their symptoms after {CSTLink}<br/><br/>'
        else:
            MSGHeadTrauma = ""

        # Sleep Pose
        if SleepPose=="TossTurn":
            MSGSleepPose = f"Tossing and turing can affect the quality of your sleep and your body's ability to heal. If you have trouble relaxing, consider {CSTLink} to help your body activate the 'Rest and Digest' functions of your parasympathetic nervous system.<br/><br/>"
        elif SleepPose=="SideSleeper":
            MSGSleepPose = f"When sleeping on your side it's important to keep your spine straight. Using a pillow between your knees reduced rotaion in the thigh, relieving tension in the hip and low back. Properly supporting your head helps maintain circulation through the neck and chest.<br/><br/>"
        elif SleepPose=="SupineSleeper":
            MSGSleepPose = f"It's important to keep your spine straight while sleeping. A pillow under your feet can help relieve stiffness in the low back. Keeping your arms down to your sides will maintain circulation your shoulders and neck.<br/><br/>"
        else: #Prone Sleeper
            MSGSleepPose = f"Turning your neck while sleeping lead to headaches and tension in the neck and shoulders. Keeping your arms down to your sides will help but you would likely benefit from massage or {TPTLink} on your neck.<br/><br/>"

        # Drive Pose
        if DrivePose=="OneHandDriver":
            MSGDrivePose = f"Driving with only one hand on the wheel causes poor posture, leading to {HoldingLink}<br/><br/>"
        elif DrivePose=="StickShift":
            spasm=True
            MSGDrivePose = f"Driving stick shifts can lead to spasms in the rotator cuff.<br/><br/>"
        else:
            MSGDrivePose = ""

        # Work Pose
        if WorkPose=="HeavyLifting":
            MSGWorkPose = f"Heavy lifting can strain the knees and back. {ContrastLink} and {StretchingLink} can help prevent injuries.<br/><br/>"
        elif WorkPose=="LongStander" and StandingTime<120:
            stiff = True
            MSGWorkPose = f"Standing still for long periods is hard on the knees and ankles. To maintain circulation and avoid {HoldingLink}, keep your knees slightly bent, rather than locking them in place. {StretchingLink} can help prevent low back pain.<br/><br/>"
        elif WorkPose=="LongSitter" and SittingTime<120:
            stiff = True
            MSGWorkPose = f"Sitting for long periods decreases blood flow to the {GlutesLink} and legs.<br/><br/>"
        elif WorkPose=="LongDriver" and DriveTime<90:
            stiff = True
            MSGWorkPose = f"Sitting for long periods decreases blood flow to the {GlutesLink} and legs. Driving long hours can cause {HoldingLink} which lead to chonic pain.<br/><br/>"
        elif WorkPose=="AkwardPosture":
            tense = True
            MSGWorkPose = ""
        else:
            MSGWorkPose = ""



        MSG_Problem = MSGProblem + MSGHighPain + MSGWater + MSGPhone + MSGComp + MSGDrive + MSGSitting + MSGStanding + MSGWalking + MSGRunning + MSGBiking + MSGExercise + MSGStretching + MSGSleeping + MSGWorking + MSGDigestion + MSGStamina + MSGMood + MSGHeadaces + MSGFallen + MSGHeadTrauma + MSGSleepPose + MSGDrivePose + MSGWorkPose

        #################################SOLUTIONS################################# 
        # TENSE?
        if tense==True:
            MSGtense = f'RELIEVE YOUR SORE MUSCLES: {StretchingLink}, {ContrastLink}, and {TPTLink} can help ease that tension.<br/><br/>'
        else:
            MSGtense = ''
        
        # SPASM?
        if spasm==True:
            MSGspasm = f'PIN AND {StretchingLink}: The best way to treast spasms is to PUSH on the area that is spasming and then stretch the muslce that is spasming. <br/><br/>'
        else:
            MSGspasm = ''
        
        # STIFF?
        if stiff==True:
            MSGstiff = f'{ContrastLink} is expecially helpful for stiff joints and muscles.<br/><br/>'
        else:
            MSGstiff = ''
        
        # VERY ACTIVE?
        if VeryActive==True:
            MSGVeryActive = f'Remember to incorporate {StretchingLink} both BEFORE AND AFTER a workout.'
        else:
            MSGVeryActive = ''

        MSG_Solution = MSGSolution + MSGtense + MSGspasm + MSGstiff + MSGVeryActive
        
        #Add client to Database
        '''
        client = (Over18, CurrentlyPregnant, DrsCare, InjuryStatus, Age, Weight, Water, PhoneTime, CompTime, DriveTime, SittingTime, StandingTime, WalkingTime, RunningTime, BikingTime, ExerciseTime, StretchingTime, SleepingTime, WorkingTime, Digestion, Stamina, Mood, Headaches, Fallen, HeadTrauma, PainLevel, SleepPose, DrivePose, WorkPose)
        DB.session.add(client)
        DB.session.commit()
        '''


        ###selfcare.py

        import os
        import sqlite3
        import pandas as pd


        DB_FILEPATH = os.path.join(os.path.dirname(__file__),
                                   "selfcare.sqlite3")

        connection = sqlite3.connect(DB_FILEPATH)
        print("CONNECTION:", connection)

        cursor = connection.cursor()
        print("CURSOR:", cursor)
        print(" ")

        # ##Create SelfCare Table with SQLite ####
        # cursor.execute('''DROP TABLE IF EXISTS selfcare_table''')
        # create_selfcare_table_query = '''
        # CREATE TABLE selfcare_table (
        #     id                      INTEGER PRIMARY KEY AUTOINCREMENT,
        #     Age                     INTEGER  NOT NULL,
        #     Weight                  INTEGER  NOT NULL,
        #     Water                   INTEGER  NOT NULL,
        #     PhoneTime               INTEGER  NOT NULL,
        #     CompTime                INTEGER  NOT NULL,
        #     DriveTime               INTEGER  NOT NULL,
        #     SittingTime             INTEGER  NOT NULL,
        #     StandingTime            INTEGER  NOT NULL,
        #     WalkingTime             INTEGER  NOT NULL,
        #     RunningTime             INTEGER  NOT NULL,
        #     BikingTime              INTEGER  NOT NULL,
        #     ExerciseTime            INTEGER  NOT NULL,
        #     StretchingTime          INTEGER  NOT NULL,
        #     SleepingTime            INTEGER  NOT NULL,
        #     WorkingTime             INTEGER  NOT NULL,
        #     Digestion               STRING  NOT NULL,
        #     Stamina                 STRING  NOT NULL,
        #     Mood                    STRING  NOT NULL,
        #     Headaches               STRING  NOT NULL,
        #     Fallen                  STRING  NOT NULL,
        #     HeadTrauma              STRING  NOT NULL,
        #     PainLevel               INTEGER  NOT NULL,
        #     SleepPose               STRING  NOT NULL,
        #     DrivePose               STRING  NOT NULL,
        #     WorkPose                STRING  NOT NULL
        #     )

        #     '''
        # cursor.execute(create_selfcare_table_query)
        # connection.commit()


        # # Add sample data for app creation
        # sample_data = [
        #     (50, 200, 40, 60, 60, 60, 60, 60, 15, 15, 15, 15, 15, 8, 8, 'True', 'True', 'True', 'True', 'True', 'True', 3, 3, 3, 3),
        #     (10, 150, 80, 10, 10, 10, 10, 10, 45, 45, 45, 45, 45, 4, 13, 'False', 'False', 'False', 'False', 'False', 'False', 6, 6, 6, 6),
        #     (17, 200, 40, 60, 60, 60, 60, 60, 15, 15, 15, 15, 15, 8, 8, 'True', 'True', 'True', 'True', 'True', 'True', 3, 3, 3, 3)
        # ]

        # for sample in sample_data:
        #     insert_data_query = f'''
        #     INSERT INTO selfcare_table
        #     (Age, Weight, Water, PhoneTime, CompTime, DriveTime, SittingTime, StandingTime, WalkingTime, RunningTime, BikingTime, ExerciseTime, StretchingTime, SleepingTime, WorkingTime, Digestion, Stamina, Mood, Headaches, Fallen, HeadTrauma, PainLevel, SleepPose, DrivePose, WorkPose)
        #     VALUES {sample}
        #     '''
        #     # print(insert_data_query)
        #     cursor.execute(insert_data_query)

        # connection.commit()
        ##### insert form data

        vals = (Age, Weight, Water, PhoneTime, CompTime, DriveTime, SittingTime, StandingTime, WalkingTime, RunningTime, BikingTime, ExerciseTime, StretchingTime, SleepingTime, WorkingTime, Digestion, Stamina, Mood, Headaches, Fallen, HeadTrauma, PainLevel, SleepPose, DrivePose, WorkPose)
        insert_client_query = f'''INSERT INTO selfcare_table
            (Age, Weight, Water, PhoneTime, CompTime, DriveTime, SittingTime, StandingTime, WalkingTime, RunningTime, BikingTime, ExerciseTime, StretchingTime, SleepingTime, WorkingTime, Digestion, Stamina, Mood, Headaches, Fallen, HeadTrauma, PainLevel, SleepPose, DrivePose, WorkPose)
            VALUES {vals}
            '''
        #print('query:: ', insert_client_query)
        cursor.execute(insert_client_query)
        connection.commit()


        # # Print dataframe
        # allresults_query = """
        # SELECT *
        # FROM selfcare_table
        # """
        # allresults = cursor.execute(allresults_query).fetchall()
        # # print("All Results: ", allresults)
        # last = allresults[-1]
        # print("Last Results: ", last) # prints last line only

        # # Average Age
        # avgage_query = """
        # SELECT AVG(Age)
        # FROM selfcare_table
        # WHERE Age>17
        # """
        # avgage = cursor.execute(avgage_query).fetchall()
        # print("Average Age : ", round(avgage[0][0]))


        return MSG_Problem + MSG_Solution


    @app.route('/TriggerPointTherapy')
    def triggerpointtherapy():
        return 'Trigger Point Therapy'

    @app.route('/ChronicHoldingPatterns')
    def chronicholdignpatterns():
        return 'Chronic Holding Patterns'

    @app.route('/ContrastTreatment')
    def contrasttreatment():
        return 'Contrast Treatment'

    @app.route('/Glutes')
    def glutes():
        return 'Glutes'

    @app.route('/Stretching')
    def stretching():
        return 'Stretching'

    @app.route('/PainScale')
    def painscale():
        return 'Pain Scale'



    return app

