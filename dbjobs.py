from datetime import datetime, timedelta
from bson import ObjectId
from pymongo import DESCENDING, MongoClient
import os
mongo_connect=os.getenv('M_CONNECTION_STRING')
db= MongoClient(mongo_connect)

#db.playerMonster.monsters.update_many({},{'$set':{'lastfed':0}})
#db.monsterdb.monsters.update_many({},{'$set': {"seris": 1}})
#db.playerMonster.monsters.update_many({},{'$set': {"seris": 1}})
