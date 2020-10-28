'''
import pandas as pd
import os
import psycopg2
from psycopg2.extras import execute_values
from dotenv import load_dotenv

load_dotenv()

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST")


# Connect to ElephantSQL-hosted PostgreSQL
connection = psycopg2.connect(
    dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)

print("CONNECTION:", connection)

# A "cursor", a structure to iterate over db records to perform queries
cursor = connection.cursor()
print("CURSOR:", cursor)

connection.commit()
'''
###selfcare.py
import os
import sqlite3
import pandas as pd
#from app import vals

DB_FILEPATH = os.path.join(os.path.dirname(__file__),
                           "selfcare.sqlite3")

connection = sqlite3.connect(DB_FILEPATH)
print("CONNECTION:", connection)

cursor = connection.cursor()
print("CURSOR:", cursor)
print(" ")

##Create SelfCare Table with SQLite ####
# cursor.execute('''DROP TABLE IF EXISTS selfcare_table''')
# create_selfcare_table_query = '''
# CREATE TABLE selfcare_table (
#    id                      INTEGER PRIMARY KEY AUTOINCREMENT,   
#    Over18                  STRING  NOT NULL,
#    CurrentlyPregnant       STRING  NOT NULL,
#    DrsCare                 STRING  NOT NULL,
#    InjuryStatus            STRING  NOT NULL,
#    Age                     INTEGER  NOT NULL,
#    Weight                  INTEGER  NOT NULL,
#    Water                   INTEGER  NOT NULL,
#    PhoneTime               INTEGER  NOT NULL,
#    CompTime                INTEGER  NOT NULL,
#    DriveTime               INTEGER  NOT NULL,
#    SittingTime             INTEGER  NOT NULL,
#    StandingTime            INTEGER  NOT NULL,
#    WalkingTime             INTEGER  NOT NULL,
#    RunningTime             INTEGER  NOT NULL,
#    BikingTime              INTEGER  NOT NULL,
#    ExerciseTime            INTEGER  NOT NULL,
#    StretchingTime          INTEGER  NOT NULL,
#    SleepingTime            INTEGER  NOT NULL,
#    WorkingTime             INTEGER  NOT NULL,
#    Digestion               STRING  NOT NULL,
#    Stamina                 STRING  NOT NULL,
#    Mood                    STRING  NOT NULL,
#    Headaches               STRING  NOT NULL,
#    Fallen                  STRING  NOT NULL,
#    HeadTrauma              STRING  NOT NULL,
#    PainLevel               INTEGER  NOT NULL,
#    SleepPose               STRING  NOT NULL,
#    DrivePose               STRING  NOT NULL,
#    WorkPose                STRING  NOT NULL
# )

# '''
# cursor.execute(create_selfcare_table_query)
# connection.commit()


# # Add sample data for app creation
# sample_data = [
#     ('True', 'False', 'False', 'False', 50, 200, 40, 60, 60, 60, 60, 60, 15, 15, 15, 15, 15, 8, 8, 'True', 'True', 'True', 'True', 'True', 'True', 3, 3, 3, 3),
#     ('True', 'False', 'False', 'False', 10, 150, 80, 10, 10, 10, 10, 10, 45, 45, 45, 45, 45, 4, 13, 'False', 'False', 'False', 'False', 'False', 'False', 6, 6, 6, 6),
#     ('False', 'True', 'True', 'True', 17, 200, 40, 60, 60, 60, 60, 60, 15, 15, 15, 15, 15, 8, 8, 'True', 'True', 'True', 'True', 'True', 'True', 3, 3, 3, 3)
# ]

# for sample in sample_data:
#     insert_data_query = f'''
#     INSERT INTO selfcare_table
#     (Over18, CurrentlyPregnant, DrsCare, InjuryStatus, Age, Weight, Water, PhoneTime, CompTime, DriveTime, SittingTime, StandingTime, WalkingTime, RunningTime, BikingTime, ExerciseTime, StretchingTime, SleepingTime, WorkingTime, Digestion, Stamina, Mood, Headaches, Fallen, HeadTrauma, PainLevel, SleepPose, DrivePose, WorkPose)
#     VALUES {sample}
#     '''
#     # print(insert_data_query)
#     cursor.execute(insert_data_query)

# connection.commit()
##### insert form data
# vals = (Age, Weight, Water, PhoneTime, CompTime, DriveTime, SittingTime, StandingTime, WalkingTime, RunningTime, BikingTime, ExerciseTime, StretchingTime, SleepingTime, WorkingTime, Digestion, Stamina, Mood, Headaches, Fallen, HeadTrauma, PainLevel, SleepPose, DrivePose, WorkPose)
# insert_client_query = f'''INSERT INTO selfcare_table
#     (Age, Weight, Water, PhoneTime, CompTime, DriveTime, SittingTime, StandingTime, WalkingTime, RunningTime, BikingTime, ExerciseTime, StretchingTime, SleepingTime, WorkingTime, Digestion, Stamina, Mood, Headaches, Fallen, HeadTrauma, PainLevel, SleepPose, DrivePose, WorkPose)
#     VALUES {vals}
#     '''
# #print('query:: ', insert_client_query)
# cursor.execute(insert_client_query)
# connection.commit()

# Print dataframe
allresults_query = """
SELECT *
FROM selfcare_table
"""
allresults = cursor.execute(allresults_query).fetchall()
# print("All Results: ", allresults)
last = allresults[-1]
print("Last Results: ", last) # prints last line only

# Average Age
avgage_query = """
SELECT AVG(Age)
FROM selfcare_table
WHERE Age>17
"""
avgage = cursor.execute(avgage_query).fetchall()
print("Average Age : ", round(avgage[0][0]))



####
'''
for sample in sample_data:
    insert_user_data_query = f'''   '''
    INSERT INTO selfcare_table
    (Over18, CurrentlyPregnant, DrsCare, InjuryStatus, Age, Weight, Water, PhoneTime, CompTime, DriveTime, SittingTime, StandingTime, WalkingTime, RunningTime, BikingTime, ExerciseTime, StretchingTime, SleepingTime, WorkingTime, Digestion, Stamina, Mood, Headaches, Fallen, HeadTrauma, PainLevel, SleepPose, DrivePose, WorkPose)
    VALUES {sample}
    '''   '''
    # print(insert_user_data_query)
    cursor.execute(insert_user_data_query)

connection.commit()

'''