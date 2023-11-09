from datetime import datetime, timedelta
from bson import ObjectId
from pymongo import DESCENDING, MongoClient
import os
mongo_connect=os.getenv('M_CONNECTION_STRING')
db= MongoClient(mongo_connect)

def give_monster_to_player(game):
        monster= db.monsterdb.monsters.find_one({'id':int(game.game)})
        post_to_db={"monster_id":game.game,"poster_id":game.poster_id,'posted_date':game.posted_date,'active':True,'basepower':monster['power'],'hp':monster['hp'],'name':monster['name'],'atk':monster['atk'],"stage":1,"traning":0,"exp":0,"level":1,'hunger':0,"overfeed":1}
        db.playerMonster.monsters.insert_one(post_to_db)


def fetch_player_monster(id):      
        query = {"active": True, "poster_id": id} 
        monster=db.playerMonster.monsters.find_one(query)
 
        return(monster)

def feed_monster(id):
       query = {"active": True, "poster_id": id} 
       monster=db.playerMonster.monsters.find_one(query) 
       hunger= monster['hunger']  
       hunger += 1
       db.playerMonster.monsters.update_one(query,{'$set':{"hunger":hunger}})
       if hunger == 7:
              try:
                     of = monster['overfeed']
                     of += 1
                     db.playerMonster.monsters.update_one(query,{'$set':{"overfeed":of}})
              except KeyError:
                     db.playerMonster.monsters.update_one(query,{'$set':{"overfeed":1}})  

def remove_food_monster(id):
       query = {"active": True, "poster_id": id} 
       monster=db.playerMonster.monsters.find_one(query) 
       hunger= monster['hunger']  
       hunger -= 1
       db.playerMonster.monsters.update_one(query,{'$set':{"hunger":hunger}})

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
                    db.playerMonster.monsters.update_one(query,{'$set':{"monster_id":monsternew['id'],"name":monsternew['name'],"stage":2,"overfeed":0}})
       if monster['stage'] == 2:      
              print('stage 2')   
              time_difference = current_time - monster['posted_date']
              print(time_difference)
              if time_difference >= timedelta(hours=8):
                     print('ready')
                     print(monster['traning'])
                     if monster['traning'] >=4:
                            
                            monster=db.monsterdb.monsters.find_one({'id':int(monster['monster_id'])})
                            monsternew= db.monsterdb.monsters.find_one({'id':int(monster['evolvea'])})
                            db.playerMonster.monsters.update_one(query,{'$set':{"monster_id":monsternew['id'],"name":monsternew['name'],"stage":3,"hp":monsternew['hp'],'atk':monsternew['atk'],"basepower":monsternew['power'],"overfeed":0,'traning':0}})
                     else:
                            monster=db.monsterdb.monsters.find_one({'id':int(monster['monster_id'])})
                            print(monster)
                            monsternew= db.monsterdb.monsters.find_one({'id':int(monster['evolveb'])})
                            print(monsternew)
                            db.playerMonster.monsters.update_one(query,{'$set':{"monster_id":monsternew['id'],"name":monsternew['name'],"stage":3,"hp":monsternew['hp'],'atk':monsternew['atk'],"basepower":monsternew['power'],"overfeed":0,'traning':0}})
       if monster['stage'] ==3:
              time_difference = current_time - monster['posted_date']
              if time_difference >= timedelta(hours=36):
                     if monster['traning'] >=4 and monster['overfeed']>= 2:
                            
                            monster=db.monsterdb.monsters.find_one({'id':int(monster['monster_id'])})
                            monsternew= db.monsterdb.monsters.find_one({'id':int(monster['evolvec'])})
                            db.playerMonster.monsters.update_one(query,{'$set':{"monster_id":monsternew['id'],"name":monsternew['name'],"stage":4,"hp":monsternew['hp'],'atk':monsternew['atk'],"basepower":monsternew['power'],"overfeed":0,'traning':0}})
                     elif monster['traning'] >=4 :
                            monster=db.monsterdb.monsters.find_one({'id':int(monster['monster_id'])})
                            print(monster)
                            monsternew= db.monsterdb.monsters.find_one({'id':int(monster['evolvea'])})
                            print(monsternew)
                            db.playerMonster.monsters.update_one(query,{'$set':{"monster_id":monsternew['id'],"name":monsternew['name'],"stage":4,"hp":monsternew['hp'],'atk':monsternew['atk'],"basepower":monsternew['power'],"overfeed":0,'traning':0}})
                     elif monster['traning'] >=2:
                            monster=db.monsterdb.monsters.find_one({'id':int(monster['monster_id'])})
                            print(monster)
                            monsternew= db.monsterdb.monsters.find_one({'id':int(monster['evolvec'])})
                            print(monsternew)
                            db.playerMonster.monsters.update_one(query,{'$set':{"monster_id":monsternew['id'],"name":monsternew['name'],"stage":4,"hp":monsternew['hp'],'atk':monsternew['atk'],"basepower":monsternew['power'],"overfeed":0,'traning':0}})
                     else:
                            monster=db.monsterdb.monsters.find_one({'id':int(monster['monster_id'])})
                            print(monster)
                            monsternew= db.monsterdb.monsters.find_one({'id':int(monster['evolved'])})
                            print(monsternew)
                            db.playerMonster.monsters.update_one(query,{'$set':{"monster_id":monsternew['id'],"name":monsternew['name'],"stage":4,"hp":monsternew['hp'],'atk':monsternew['atk'],"basepower":monsternew['power'],"overfeed":0,'traning':0}})  



def expcheck(id,exp):
    query = {"active": True, "poster_id": id} 
    monster=db.playerMonster.monsters.find_one(query)
    xp=monster['exp']
    print(xp)   
    mlevel=monster['level']
    xp +=exp
    db.playerMonster.monsters.update_one(query,{'$set':{'exp':xp}})
    level = 1
    if xp >= 50:
           level = 2
    if xp >= 150:
           level = 3
    if xp >= 500:
           level = 4
    if xp >= 800:
           level =5
    if xp >= 1000 and monster['stage'] >=4:
           level =6
    if xp >= 1500 and monster['stage'] >=4:
           level =7 
    if xp >= 2000 and monster['stage'] >=4:
           level =8
    if xp >= 3000 and monster['stage'] >=4:
           level =9
    if xp >= 5000 and monster['stage'] >=4:
           level =10
           
    if mlevel != level:
           print("you have leveled up ")  
           db.playerMonster.monsters.update_one(query,{'$set':{'level':level}})     
    

#expcheck(ObjectId('6541107d9a2ed6e684a6552c'),1 )                  
           
    