from flask import Flask, render_template, request
from .db_model import DB , Client
from dotenv import load_dotenv
from os import getenv
import copy
import json
import os
import sqlite3
import pandas as pd


load_dotenv()

# Internal Links
CSTLink = '<a href="https://my.clevelandclinic.org/health/treatments/17677-craniosacral-therapy#:~:text=Craniosacral%20therapy%20(CST)%20is%20a,and%20boosting%20health%20and%20immunity.">CranioSacral Therapy</a>'#'<a href="/CranioSacralTherapy">CranioSacral Therapy</a>'
TPTLink = '<a href="/TriggerPointTherapy">Trigger Point</a>'
HoldingLink = '<a href="https://www.romphysiotherapy.com/single-post/2016/11/01/Whats-Your-Holding-Pattern">Chronic Holding Patterns</a>'#'<a href="/ChronicHoldingPatterns">Chronic Holding Patterns</a>'
ContrastLink = '<a href="https://en.wikipedia.org/wiki/Contrast_bath_therapy#:~:text=Contrast%20bath%20therapy%2C%20is%20a,times%2C%20alternating%20hot%20and%20cold.">Contrast Therapy</a>'#'<a href="/ContrastTreatment">Contrast Treatment</a>'
GlutesLink = '<a href="https://www.healthline.com/health/exercise-fitness/how-to-stretch-glutes#downward-facing-dog">Glutes</a>'#'<a href="/Glutes">Glutes</a>'
StretchingLink = '<a href="https://en.wikipedia.org/wiki/Contrast_bath_therapy#:~:text=Contrast%20bath%20therapy%2C%20is%20a,times%2C%20alternating%20hot%20and%20cold.">Stretching</a>'#'<a href=/Stretching>Stretching</a>'
SpasmsLink = '<a href="https://learnmuscles.com/blog/2017/08/06/pin-stretch-technique/">spasms</a>'#'<a href=/Stretching>spasms</a>' # goes to StretchingLink for Pin and Stretch but hyperlink will show "spasms"
PainScaleLink = '<a href="https://realtalkablog.wordpress.com/2018/05/07/no-pain-no-gain-has-its-limitations/">Pain Scale</a>'#'<a href=/PainScale>Pain Scale</a>'
MoodCureBookLink = '<a href=https://www.juliarosscures.com/mood-cure/>this book</a>'
YogaBookLink = '<a href=https://www.google.com/search?q=light+on+yoga+by+b.k.s.+iyengar>Yoga</a>'
BreakLine = '------------------------------------------------------------------------------------------------------------------------------------<br/>'
TAKLink = '<a href=https://takeaskneaded.massagetherapy.com/>Take As Kneaded, LLC</a>'

# Create App
def create_app():
    '''Create and configure an instance of our Flask application'''
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    DB.init_app(app)  # Connect Flask app to SQLAlchemy DB

    @app.route('/')
    @app.route('/intake')
    def intake():
        return render_template('intake.html', title='Intake')

    @app.route('/survey', methods=['POST']) # from intake.html
    def survey():
        # Form-Intake Results as variables
        Over18 = request.form['Over18']
        CurrentlyPregnant = request.form['CurrentlyPregnant']
        DrsCare = request.form['DrsCare']
        InjuryStatus = request.form['InjuryStatus']

        # Analyze Inputs for as intake for survey
        # DECLINE access to Survey if:
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
        #Connect to database
        DB_FILEPATH = os.path.join(os.path.dirname(__file__),
                                   "selfcare.sqlite3")
        connection = sqlite3.connect(DB_FILEPATH)
        #print("CONNECTION:", connection)
        cursor = connection.cursor()
        #print("CURSOR:", cursor)
        #print(" ")

        # Form-Survey Results as variables
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

        MSGProblem = 'Based off your answers, here are a few things that might be affecting your day:<br/>'
        MSGSolution = 'And here are some suggestions as to what you can do to improve the quality of your life:<br/>'
        
        ###########################################PROBLEM LISTINGS##################################
        
        # Base Results
        VeryActive = False
        cuff = False
        CST = False
        Yoga = False
        stiff = False
        spasm = False    
        PNS = False    

        # Suggested Pain Level
        if PainLevel>=7:
            tense = True
            MSGHighPain = f"Severe pain can affect your central nervous system. Consult a doctor about your pain as soon as possible.<br/><br/>"
        elif PainLevel>=3:
            MSGHighPain = f"Over time, even moderate pain can affect your central nervous system and lead to {HoldingLink}.<br/><br/>"
        else:
            MSGHighPain = ""
        #return MSGHighPain

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
            cuff = True
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
            MSGStanding = f"Standing still for long periods is hard on the knees and ankles.<br/><br/>To maintain circulation and avoid {HoldingLink}, keep your knees slightly bent, rather than locking them in place.<br/><br/>"
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
            MSGRunning = f"Running even short distances can cause your IT Band to stiffen up, which can lead to pain the knees or low back.<br/><br/>"
        elif RunningTime>=30 and WalkingTime>=60:
            SkateCityLink = '<a href=https://www.skatecitycolorado.com/>roller skating</a>'
            tense = True
            VeryActive = True
            MSGRunning = f"Running is great for cardio but it's very hard on your knees.<br/><br/>Both running and walking can cause your IT Band to stiffen up, which can lead to pain the knees or low back.<br/<br/>Consider riding a bicycle or {SkateCityLink} for less impact.<br/><br/>"
        else:
            MSGRunning = ""
        #return MSGRunning
        
        # Suggested Biking Time
        if BikingTime>=30 and RunningTime<30 and WalkingTime<60:
            tense = True
            VeryActive = True
            MSGBiking = f"Biking can cause your IT Band to stiffen up, which can lead to pain the knees or low back.<br/><br/>Consider riding a bicycle or {SkateCityLink} for less impact.<br/><br/>"
        else:
            MSGBiking = ""
        #return MSGBiking
        
        # Suggested Stretching Time
        if StretchingTime<10:
            tense = True
            stiff = True
            #MSGStretching = f"{StretchingLink} for even a few minutes per day increases range of motion, joint mobility, and circulation throughout your body. It can help to improve energy, mood, and pain tolerance.<br/><br/>"
        #else:
            #MSGStretching = ""
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

        # Decrease Headaches
        if Headaches=="Headaches":
            CST = True
        #     MSGHeadaces = f"If you already improved your diet and water intake and don't smoke cigarettes, consider {CSTLink} to help treat your chronic headaches or migraines.<br/><br/>"
        # else:
        #     MSGHeadaces = ""

        # Spinal Compression
        if Fallen=="ManyTailFalls" or Fallen=="OneTailFall":
            Yoga = True
            CST = True
            MSGFallen = f'Falling can compress the spine and pinch nerves, leading to chronic pain.<br/><br/>'# {CSTLink} can help with this.<br/><br/>'
        else:
            MSGFallen = ""

        # Treat Head Trauma
        if HeadTrauma=='ManyHeadTraumas' or HeadTrauma=='OneHeadTrauma':
            CST = True
            MSGHeadTrauma = f'Any traumatic injury to the head, neck, or spine can affect the central nervous system.<br/><br/>'# Many people have experienced relief from their symptoms after {CSTLink}<br/><br/>'
        else:
            MSGHeadTrauma = ""

        # Sleep Pose
        if SleepPose=="TossTurn":
            PNS=True
            MSGSleepPose = f"Tossing and turing can affect the quality of your sleep and your body's ability to heal.<br/><br/>"
        elif SleepPose=="SideSleeper":
            MSGSleepPose = f"When sleeping on your side it's important to keep your spine straight.<br/><br/>Using a pillow between your knees reduced rotaion in the thigh, relieving tension in the hip and low back.<br/><br/>Properly supporting your head helps maintain circulation through the neck and chest.<br/><br/>"
        elif SleepPose=="SupineSleeper":
            MSGSleepPose = f"It's important to keep your spine straight while sleeping. A pillow under your feet can help relieve stiffness in the low back. Keeping your arms down to your sides will maintain circulation your shoulders and neck.<br/><br/>"
        else: #Prone Sleeper
            MSGSleepPose = f"Turning your neck while sleeping can lead to headaches, tension, and {TPTLink}s in the neck and shoulders.<br/><br/>"

        # Drive Pose
        if DrivePose=="OneHandDriver":
            MSGDrivePose = f"Driving with only one hand on the wheel causes poor posture, leading to {HoldingLink}<br/><br/>"
        elif DrivePose=="StickShift":
            spasm=True
            cuff=True
            MSGDrivePose = f"Using a stick shift can lead to spasms in the rotator cuff.<br/><br/>"
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

        MSG_Problem = BreakLine + MSGProblem + BreakLine + MSGHighPain + MSGPhone + MSGComp + MSGDrive + MSGSitting + MSGStanding + MSGWalking + MSGRunning + MSGBiking + MSGSleeping + MSGWorking + MSGFallen + MSGHeadTrauma + MSGSleepPose + MSGDrivePose + MSGWorkPose

        #################################SOLUTIONS################################# 
        # TENSE?
        if tense==True:
            Yoga = True
            MSGtense = f'Relieve your sore muscles: {StretchingLink}, {ContrastLink}, and {TPTLink} Therapy can help ease that tension.<br/><br/>'
        else:
            MSGtense = ''
        
        # SPASM?
        if spasm==True:
            MSGspasm = f'Pinning AND {StretchingLink}: The best way to treast spasms is to PUSH on the area that is spasming and then stretch the muslce that is spasming. <br/><br/>'
        else:
            MSGspasm = ''
        
        # STIFF?
        if stiff==True:
            Yoga = True
            MSGstiff = f'{ContrastLink} is expecially helpful for stiff joints and muscles.<br/><br/>'
        else:
            MSGstiff = ''
        
        # VERY ACTIVE?
        if VeryActive==True:
            MSGVeryActive = f'Remember to incorporate {StretchingLink} both BEFORE AND AFTER a workout.<br/><br/>'
        else:
            MSGVeryActive = ''

        # NEED YOGA?
        if Yoga==True:
            MSGYoga = f'This book helped me begin {YogaBookLink} at my own pace without feeling self conscious in a class.<br/><br/>'
        else:
            MSGYoga = ''

        # Rotator Cuff Issues?
        RotatorCuffLink = '<a href=https://www.yorkvillesportsmed.com/blog/top-rotator-cuff-exercises-for-stretches-strengthening>rotator cuff</a>'
        if cuff==True:
            MSGCuff = f"{RotatorCuffLink} issues are unique because soft tissue damage won't always appear in medical testing. If your range of motion is affected consult your healthcare provider to ensure there is no acute injury.<br/><br/>Otherwise, even extreme pain often turns out to be linked to a {TPTLink} that is difficult to access."
        else:
            MSGCuff = ""

        # Need CST Assessment?
        SuturesLink = '<a href=https://www.realbodywork.com/articles/cranial-sacral-therapy/>sutures</a>'
        if CST==True:
            MSGCST = f"Did you know the bones of the skull DO NOT fuse, but rather, form comparitively malleable {SuturesLink}?<br/>Like dripping water slowly etching its way through a rock, {CSTLink} uses extremely light touch to connect directly with the tissue surrounding your brain and spinal fluid.<br/>This treatment can improve a variety of issues with the central nervous system.<br/><br/>"

        # Digestion Issues?
        if Digestion=="SlowDigest":
            Yoga = True
            MSGDigestion = f'Digestion can be affected by many factors. I find the most commonly overlooked treatments are {StretchingLink} your abdominal area or performing {TPTLink} Therapy on your Psoas Muscle.<br/><br/>'
        else:
            MSGDigestion = ""

        # Weak PNS/Parasympathetic Nervous System?
        if PNS==True:
            MSGPNS = f"If you have trouble relaxing, consider {CSTLink} to help your body activate the 'Rest and Digest' functions of your parasympathetic nervous system.<br/><br/>"

        # Improve Stamina 
        if Stamina=="LowStamina":
            Yoga = True
            MSGStamina = f'Along with improving your diet, massage can help improve stamina for sports or academics.<br/><br/>'
        else:
            MSGStamina = ""

        # Improve Mood
        if Mood=="BadMood":
            MSGMood = f'Speak to your healthcare providers about how to improve your moods. I am not a nutritionist but I can tell you that {MoodCureBookLink} helped me undertand how my diet affects my moods.<br/><br/>'
        else:
            MSGMood = ""

        # Suggested Exercise Time
        if (ExerciseTime+BikingTime+RunningTime+WalkingTime)>=60:
            VeryActive = True
            MSGExercise = f"Exercise is wonderful but don't forget to take a day off each week to let your body recover.<br/><br/>"
        else:
            MSGExercise = ""
        #return MSGExercise

        # Suggested Water Intake vs Actual
        suggWaterMIN = 0.75*(Weight/2)
        suggWater = round(Weight/2)
        suggWaterGlass = round(suggWater/12)
        if Water>=suggWaterMIN:
            MSGWater = "Great job on drinking plenty of water!<br/><br/>"
        else:
            MSGWater = f'Try to drink at least {suggWater} ounces, which is just {suggWaterGlass} "12-ounce glasses" of water every day.<br/><br/>'
        #return MSGWater

        MSG_Solution = BreakLine + MSGSolution + BreakLine + MSGtense + MSGspasm + MSGstiff + MSGCuff + MSGCST + MSGDigestion + MSGPNS + MSGStamina + MSGMood + MSGVeryActive + MSGExercise + MSGYoga + MSGWater
 
        ##### insert form data
        client = Client(Age=Age, Weight=Weight, Water=Water, PhoneTime=PhoneTime, CompTime=CompTime, DriveTime=DriveTime, SittingTime=SittingTime, StandingTime=StandingTime, WalkingTime=WalkingTime, RunningTime=RunningTime, BikingTime=BikingTime, ExerciseTime=ExerciseTime, StretchingTime=StretchingTime, SleepingTime=SleepingTime, WorkingTime=WorkingTime, Digestion=Digestion, Stamina=Stamina, Mood=Mood, Headaches=Headaches, Fallen=Fallen, HeadTrauma=HeadTrauma, PainLevel=PainLevel, SleepPose=SleepPose, DrivePose=DrivePose, WorkPose=WorkPose)
        DB.session.add(client)
        DB.session.commit()

        # vals = (Age, Weight, Water, PhoneTime, CompTime, DriveTime, SittingTime, StandingTime, WalkingTime, RunningTime, BikingTime, ExerciseTime, StretchingTime, SleepingTime, WorkingTime, Digestion, Stamina, Mood, Headaches, Fallen, HeadTrauma, PainLevel, SleepPose, DrivePose, WorkPose)
        # insert_client_query = f'''INSERT INTO selfcare_table
        #     (Age, Weight, Water, PhoneTime, CompTime, DriveTime, SittingTime, StandingTime, WalkingTime, RunningTime, BikingTime, ExerciseTime, StretchingTime, SleepingTime, WorkingTime, Digestion, Stamina, Mood, Headaches, Fallen, HeadTrauma, PainLevel, SleepPose, DrivePose, WorkPose)
        #     VALUES {vals}
        #     '''
        # #print('query:: ', insert_client_query)
        # cursor.execute(insert_client_query)
        # connection.commit()'''

        return render_template('results.html') + MSG_Problem + MSG_Solution + BreakLine

    
    @app.route(getenv('database_reset_key'))
    def reset():
        # Connect to database
        DB_FILEPATH = os.path.join(os.path.dirname(__file__),
                                   "selfcare.sqlite3")
        connection = sqlite3.connect(DB_FILEPATH)
        #print("CONNECTION:", connection)
        cursor = connection.cursor()
        #print("CURSOR:", cursor)
        #print(" ")

        DB.drop_all()
        DB.create_all()
        return 'Database Reset'

    @app.route('/database')
    def database():
        DB_FILEPATH = os.path.join(os.path.dirname(__file__),
                                   "selfcare.sqlite3")

        connection = sqlite3.connect(DB_FILEPATH)
        #print("CONNECTION:", connection)

        cursor = connection.cursor()
        #print("CURSOR:", cursor)

        # Print dataframe
        allresults_query = """
        SELECT *
        FROM Client
        """
        allresults = cursor.execute(allresults_query).fetchall()
        #print("All Results: ", allresults)


        last = allresults[-1]
        #print("Last Results: ", last) # PYTHON prints last line only

        # Average Age
        avgage_query = """
        SELECT AVG(Age)
        FROM Client
        """
        avgage = cursor.execute(avgage_query).fetchall()
        avgage = round(avgage[0][0])
        print("Average Age : ", avgage) #PYTHON prints

        # message = f'Average age of users is {avgage}<br/><br/>'
        # headers = 'Age, Weight, Water, PhoneTime, CompTime, DriveTime, SittingTime, StandingTime, WalkingTime, RunningTime, BikingTime, ExerciseTime, StretchingTime, SleepingTime, WorkingTime, Digestion, Stamina, Mood, Headaches, Fallen, HeadTrauma, PainLevel, SleepPose, DrivePose, WorkPose'
        
        # for c in allresults:
        #     clients = dict(headers,c)
        
        clients = str(allresults)
        
        print("clients: ", clients)
        return clients

    @app.route('/TriggerPointTherapy')
    def triggerpointtherapy():
        TPTHistoryLink = '<a href=https://www.dgs-academy.com/en/trigger-point-therapy/trigger-point-therapy/#:~:text=Myofascial%20Trigger%20Point%20Therapy%2C%20also,MTrPs%20affect%20muscles%20and%20fascia.>technical description</a>'
        FoamRollerLink = '<a href=https://www.amazon.com/Gimme-10-Massager-Myofascial-Trigger/dp/B07G2ZWLD2/ref=asc_df_B07G2ZWLD2/?tag=hyprod-20&linkCode=df0&hvadid=312130834541&hvpos=&hvnetw=g&hvrand=6281305891803666593&hvpone=&hvptwo=&hvqmt=&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=9029017&hvtargid=pla-583753266400&psc=1>Foam Roller</a>'
        TheraCaneLink = '<a href=http://www.theracane.com/>TheraCane</a>'
        GenericCaneLink = '<a href=https://www.google.com/search?q=generic+theracane>generics</a>'
        TPT_History_MSG = f'This webstite provides a very {TPTHistoryLink} of Trigger Point Therapy if you would like more information.<br/><br/>'
        TPT_MyDesc_MSG = 'Trigger Points are more than just sore muscles. Over time, tissue that is chronically shortened will collect excess lymph, lactic acid, and other bodily fluids. This can cause multiple anatomical regions to bind on a molecular level, leading to referral pains throughout the body.<br/><br/>'
        TPT_Treatment_MSG = f'A Licensed Massage Therapist or a Chiropractor can help you treat trigger points.<br/><br/>For at-home remedies, there are several options. I do not sell any version or brand of these items but have included links as a visual so you find the best item for your needs.<br/><br/>My Personal Favorite: Just a simple Tennis Ball<br/><br/>Another Common Tool: {FoamRollerLink}<br/><br/>This {TheraCaneLink} is the original but the {GenericCaneLink} work well and cost ~$10 less.<br/><br/>'
        
        return render_template('results.html') + TPT_MyDesc_MSG + TPT_History_MSG + TPT_Treatment_MSG


    # @app.route('/ChronicHoldingPatterns')
    # def chronicholdignpatterns():
    #     return 'Chronic Holding Patterns'

    # @app.route('/ContrastTreatment')
    # def contrasttreatment():
    #     return 'Contrast Treatment'

    # @app.route('/Glutes')
    # def glutes():
    #     return 'Glutes'

    # @app.route('/Stretching')
    # def stretching():
    #     return 'Stretching'

    # @app.route('/PainScale')
    # def painscale():
    #     return 'Pain Scale'

    # @app.route('/CranioSacralTherapy')
    # def CST():
    #     return 'CranioSacralTherapy'



    return app

