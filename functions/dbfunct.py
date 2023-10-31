from datetime import datetime, timedelta
from bson import ObjectId
from pymongo import DESCENDING, MongoClient
import os
mongo_connect=os.getenv('M_CONNECTION_STRING')
db= MongoClient(mongo_connect)

def give_monster_to_player(game):
        monster= db.monsterdb.monsters.find_one({'id':int(game.game)})
        post_to_db={"monster_id":game.game,"poster_id":game.poster_id,'posted_date':game.posted_date,'active':True,'basepower':monster['power'],'hp':monster['hp'],'name':monster['name'],'atk':monster['atk'],"stage":1}
        db.playerMonster.monsters.insert_one(post_to_db)


def fetch_player_monster(id):      
        query = {"active": True, "poster_id": id} 
        monster=db.playerMonster.monsters.find_one(query)
 
        return(monster)


def evocheck(id):
        query = {"active": True, "poster_id": id} 
        monster=db.playerMonster.monsters.find_one(query)
        current_time = datetime.now()
        time_difference = current_time - monster['posted_date']
        if monster['stage'] == 1:
                time_difference = current_time - monster['posted_date']
                if time_difference >= timedelta(minutes=10):
                    monster=db.monsterdb.monsters.find_one({'id':int(monster['monster_id'])})
                    monsternew= db.monsterdb.monsters.find_one({'id':int(monster['evolve'])})
                    db.playerMonster.monsters.update_one(query,{'$set':{"monster_id":monsternew['id'],"name":monsternew['name'],"stage":2}})
        
