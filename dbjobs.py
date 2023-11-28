from datetime import datetime, timedelta
from bson import ObjectId
from pymongo import DESCENDING, MongoClient
import os
mongo_connect=os.getenv('M_CONNECTION_STRING')
db= MongoClient(mongo_connect)

#db.playerMonster.monsters.update_many({},{'$set':{'lastfed':0}})
def dbjobsonerun():
    #db.monsterdb.monsters.update_many({},{'$set': {"seris": 1}})
    #db.playerMonster.monsters.update_many({},{'$set': {"seris": 1}})
    #db.playerMonster.monsters.update_many({},{'$set': {"wins": 0}})
    #db.playerMonster.monsters.update_many({},{'$set': {"losses": 0}})    
    #db.userProfiles.userProfiles.update_many({},{'$set': {"wins": 0}})
    #db.userProfiles.userProfiles.update_many({},{'$set': {"losses": 0}})
    for monsters in db.playerMonster.monsters.find({}):
        print(monsters['monster_id'])
        m = monsters['monster_id']
        mid = monsters['_id']
        monsterdb= db.monsterdb.monsters.find_one({'id':m})
        print(monsterdb)
        mtype=monsterdb['type']
        db.playerMonster.monsters.update_one({"_id":mid},{'$set':{'type':mtype}})
        #db.playerMonster.monster.update_one{}


    return 'ok'
