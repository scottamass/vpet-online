
import bcrypt
from pymongo import MongoClient
import os


# Connect to MongoDB (replace 'your_mongo_uri' with your actual MongoDB connection string)
mongo_uri = os.getenv('M_CONNECTION_STRING')
client = MongoClient(mongo_uri)

# Access the 'monsterdb' database
db = client.monsterdb



# Create the 'monsters' collection and insert data
monsters_collection = db.monsters
def init_monsterdb():
    monsters_collection.insert_many([{
    
    "id": 1,
    "name": "botamon",
    "slot": "a",
    "power": 4,
    "hp": 0,
    "atk": 0,
    "evolve": 2,
    "stage": 1
    },
    {

    "id": 2,
    "name": "koromon",
    "slot": "b",
    "power": 4,
    "hp": 0,
    "atk": 0,
    "evolvea": 3,
    "evolveb": 4,
    "stage": 2
    },
    {
    
    "id": 999,
    "name": "MissingNo",
    "slot": "j",
    "power": 220,
    "hp": 20,
    "atk": 5,
    "evolvea": None,
    "evolveb": None,
    "stage": 5
    },
    {
    
    "id": 3,
    "name": "agumon",
    "slot": "b",
    "power": 15,
    "hp": 5,
    "atk": 1,
    "evolvea": 6,
    "evolveb": 7,
    "evolvec": 8,
    "stage": 3
    },
    {
    
    "id": 4,
    "name": "agumon(black)",
    "slot": "b",
    "power": 15,
    "hp": 5,
    "atk": 1,
    "evolvea": 6,
    "evolveb": 7,
    "evolvec": 8,
    "stage": 3
    }])


def initTestProfile():


    email= "scott@scott.com"
    user = "scott"
    pw= "1"
    if db.authDb.users.find_one({"email":email}):
        print ("user in db")
    elif db.authDb.users.find_one({"username":user}):    
        print( "username exists")
    else: 
                hashed_pw = pw
                db.authDb.users.insert_one({"email":email,"password":hashed_pw,'username':user})
                requested_user = db.authDb.users.find_one({"email":email})
                print(requested_user)
                user_uid = requested_user["_id"]
                #add user to profile db
                db.userProfiles.userProfiles.insert_one({'auth_id':user_uid,'username':user,"profilePic":None,"role":"player",'battleTower':0,"money":100})

    client.close()

init_monsterdb()
#initTestProfile()