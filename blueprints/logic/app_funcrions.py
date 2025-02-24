import os
from pymongo import MongoClient


mongo_connect=os.getenv('M_CONNECTION_STRING')
db= MongoClient(mongo_connect)


def process_win(player,prize,stage,monster,user_id):
    playerBank = int(player['money'])
    playerBank += int(prize)
    mwins = monster['wins'] 
    mwins += 1
    pwins = player['wins']
    pwins += 1
    if stage > player['battleTower']:
            db.userProfiles.userProfiles.update_one({"_id":user_id},{'$set':{"battleTower":stage,'money':playerBank,"wins":pwins,}})
            db.playerMonster.monsters.update_one({'_id':user_id},{'$set':{"wins":mwins}})
    else: 
            db.userProfiles.userProfiles.update_one({"_id":user_id},{'$set':{'money':playerBank,"wins":pwins}})
            db.playerMonster.monsters.update_one({'_id':user_id},{'$set':{"wins":mwins}})