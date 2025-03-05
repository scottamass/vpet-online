from datetime import datetime, timedelta
from bson import ObjectId
from flask import flash
from pymongo import DESCENDING, MongoClient
import os

from functions.call_monster import call_monster
mongo_connect=os.getenv('M_CONNECTION_STRING')
db= MongoClient(mongo_connect)
import json



def give_monster_to_player(game):
        print(type(game.game))
        print(f"-------------------------Beginning function call ------------------------")
        monster= call_monster(int(game.game))
        print(f"-------------------------{monster}------------------------")
        post_to_db={"monster_id":monster['id'],"poster_id":game.poster_id,'posted_date':game.posted_date,'active':True,'power':0,'atk':0,'hp':0,"traning":0,"exp":0,"level":1,'wins':0,'losses':0,'evo':False}
        db.playerMonster.monsters.insert_one(post_to_db)


def fetch_player_monster(id):      
        query = {"active": True, "poster_id": id} 
        monster=db.playerMonster.monsters.find_one(query)
        if monster == None:
              # print(monster)
              return(monster)
        else :
              #  print(monster)
              i = call_monster(monster['monster_id'])
              monster_new ={'_id': monster['_id'], 'monster_id': monster['monster_id'], 'poster_id': monster['poster_id'], 'posted_date': monster['posted_date'], 'active': monster['active'], 'basepower': i['power'], 'basehp': i['hp'], 'power': monster['power'], 'atk': monster['atk'], 'hp': monster['hp'], 'name': i['name'], 'baseatk': i['atk'], 'stage': i['stage'], 'traning': monster['traning'], 'exp': monster['exp'], 'level': monster['level'], 'wins': monster['wins'] ,'losses': monster['losses'], 'type': i['type'],'evo':monster['evo']}
              return(monster_new)
        
def fetch_all_player_monster(id):      
       query = {"poster_id": id} 
       monster=db.playerMonster.monsters.find(query)
       monster_list=list(monster)
       if monster == None:
              # print(monster)
              return(monster)
       else :
              return_list = []
              for m in monster_list:
                     print(m)
                     monster = call_monster(m['monster_id'])
                     monster_new = {'_id': m['_id'], 'monster_id': m['monster_id'], 'poster_id': m['poster_id'], 'posted_date': m['posted_date'], 'active': m['active'], 'basepower': monster['power'], 'basehp': monster['hp'], 'power': m['power'], 'atk': m['atk'], 'hp': m['hp'], 'name': monster['name'], 'baseatk': monster['atk'], 'stage': monster['stage'], 'traning': m['traning'], 'exp': m['exp'], 'level': m['level'], 'wins': m['wins'] ,'losses': m['losses'], 'type': monster['type'],'evo':m['evo']}
                     return_list.append(monster_new)
              return(return_list)





# def evocheck(id):
#        query = {"active": True, "poster_id": id} 
#        monster=db.playerMonster.monsters.find_one(query)
#        current_time = datetime.now()
#        time_difference = current_time - monster['posted_date']
#        if monster['stage'] == 1:
#                 time_difference = current_time - monster['posted_date']
#                 if time_difference >= timedelta(minutes=10):
#                     monster=db.monsterdb.monsters.find_one({'id':int(monster['monster_id'])})
#                     monsternew= db.monsterdb.monsters.find_one({'id':int(monster['evolve'])})
#                     db.playerMonster.monsters.update_one(query,{'$set':{"monster_id":monsternew['id'],"name":monsternew['name'],"stage":2,"overfeed":0,'type':monsternew['type']}})
#        if monster['stage'] == 2:      
#               print('stage 2')   
#               time_difference = current_time - monster['posted_date']
#               print(time_difference)
#               if time_difference >= timedelta(minutes=30):
#                      print('ready')
#                      print(monster['traning'])
#                      if monster['traning'] >=4:
                            
#                             monster=db.monsterdb.monsters.find_one({'id':int(monster['monster_id'])})
#                             monsternew= db.monsterdb.monsters.find_one({'id':int(monster['evolvea'])})
#                             db.playerMonster.monsters.update_one(query,{'$set':{"monster_id":monsternew['id'],"name":monsternew['name'],"stage":3,"basehp":monsternew['hp'],'baseatk':monsternew['atk'],"basepower":monsternew['power'],"overfeed":0,'traning':0,'type':monsternew['type']}})
                     
#        if monster['stage'] ==3:
#               time_difference = current_time - monster['posted_date']
#               if time_difference >= timedelta(hours=36):
#                      if monster['traning'] >=4 and monster['overfeed']>= 2:
                            
#                             monster=db.monsterdb.monsters.find_one({'id':int(monster['monster_id'])})
#                             monsternew= db.monsterdb.monsters.find_one({'id':int(monster['evolvec'])})
#                             db.playerMonster.monsters.update_one(query,{'$set':{"monster_id":monsternew['id'],"name":monsternew['name'],"stage":4,"basehp":monsternew['hp'],'baseatk':monsternew['atk'],"basepower":monsternew['power'],"overfeed":0,'traning':0,'type':monsternew['type']}})
#                      elif monster['traning'] >=4 :
#                             monster=db.monsterdb.monsters.find_one({'id':int(monster['monster_id'])})
#                             print(monster)
#                             monsternew= db.monsterdb.monsters.find_one({'id':int(monster['evolvea'])})
#                             print(monsternew)
#                             db.playerMonster.monsters.update_one(query,{'$set':{"monster_id":monsternew['id'],"name":monsternew['name'],"stage":4,"basehp":monsternew['hp'],'baseatk':monsternew['atk'],"basepower":monsternew['power'],"overfeed":0,'traning':0,'type':monsternew['type']}})
#                      elif monster['traning'] >=2:
#                             monster=db.monsterdb.monsters.find_one({'id':int(monster['monster_id'])})
#                             print(monster)
#                             monsternew= db.monsterdb.monsters.find_one({'id':int(monster['evolveb'])})
#                             print(monsternew)
#                             db.playerMonster.monsters.update_one(query,{'$set':{"monster_id":monsternew['id'],"name":monsternew['name'],"stage":4,"basehp":monsternew['hp'],'baseatk':monsternew['atk'],"basepower":monsternew['power'],"overfeed":0,'traning':0,'type':monsternew['type']}})
#                      else:
#                             monster=db.monsterdb.monsters.find_one({'id':int(monster['monster_id'])})
#                             print(monster)
#                             monsternew= db.monsterdb.monsters.find_one({'id':int(monster['evolved'])})
#                             print(monsternew)
#                             db.playerMonster.monsters.update_one(query,{'$set':{"monster_id":monsternew['id'],"name":monsternew['name'],"stage":4,"basehp":monsternew['hp'],'baseatk':monsternew['atk'],"basepower":monsternew['power'],"overfeed":0,'traning':0,'type':monsternew['type']}})  
#        if monster['stage'] == 4:
#               print(monster)
#               if monster['monster_id'] != 9:
# #              if monster['monster_id'] != 9 and monster['monster_id'] != 10 and monster['monster_id'] != 12:
#                      time_difference = current_time - monster['posted_date']
#                      if time_difference >= timedelta(hours=72):
#                             if monster['wins'] >= 5 and monster['wins'] >= monster['losses']:
#                                    monster=db.monsterdb.monsters.find_one({'id':int(monster['monster_id'])})
#                                    print(monster)
#                                    monsternew= db.monsterdb.monsters.find_one({'id':int(monster['evolvea'])})
#                                    print(monsternew)
#                                    db.playerMonster.monsters.update_one(query,{'$set':{"monster_id":monsternew['id'],"name":monsternew['name'],"stage":5,"basehp":monsternew['hp'],'baseatk':monsternew['atk'],"basepower":monsternew['power'],"overfeed":0,'traning':0,'type':monsternew['type']}})  
#                             elif monster['wins'] >= monster['losses'] :
#                                    monster=db.monsterdb.monsters.find_one({'id':int(monster['monster_id'])})
#                                    print(monster)
#                                    monsternew= db.monsterdb.monsters.find_one({'id':int(monster['evolveb'])})
#                                    print(monsternew)
#                                    db.playerMonster.monsters.update_one(query,{'$set':{"monster_id":monsternew['id'],"name":monsternew['name'],"stage":5,"basehp":monsternew['hp'],'baseatk':monsternew['atk'],"basepower":monsternew['power'],"overfeed":0,'traning':0,'type':monsternew['type']}})  

#                             else: 
#                                    monster=db.monsterdb.monsters.find_one({'id':int(monster['monster_id'])})
#                                    print(monster)
#                                    monsternew= db.monsterdb.monsters.find_one({'id':int(monster['evolveb'])})
#                                    print(monsternew)
#                                    db.playerMonster.monsters.update_one(query,{'$set':{"monster_id":monsternew['id'],"name":monsternew['name'],"stage":5,"basehp":monsternew['hp'],'baseatk':monsternew['atk'],"basepower":monsternew['power'],"overfeed":0,'traning':0,'type':monsternew['type']}})  

                     
#               else: print('you cant ')     
def evocheck(id):
       query = {"active": True, "poster_id": id} 
       monster=db.playerMonster.monsters.find_one(query)
       pre_mon = monster['monster_id']
       print(pre_mon)
       current_time = datetime.now()
       time_difference = current_time - monster['posted_date']
       mon_data = call_monster(monster['monster_id'])
       if mon_data['stage'] == 1:
                time_difference = current_time - monster['posted_date']
                if time_difference >= timedelta(minutes=2):
                    monster=call_monster(monster['monster_id'])
                    monsternew= call_monster(monster['evolve'])
                    db.playerMonster.monsters.update_one(query,{'$set':{"monster_id":monsternew['id'],'evo':False,'prev_evo':pre_mon}})
      
       if mon_data['stage'] == 2:      
              print('stage 2')   
              time_difference = current_time - monster['posted_date']
              print(time_difference)
              if time_difference >= timedelta(minutes=10):
                     print('ready')
                     print(monster['traning'])
                     if monster['traning'] >=4:
                            
                            monster=monster=call_monster(monster['monster_id'])
                            monsternew= call_monster(monster['evolvea'])
                            db.playerMonster.monsters.update_one(query,{'$set':{"monster_id":monsternew['id'],'evo':False,'prev_evo':pre_mon}})
                     else:
                            monster=monster=call_monster(monster['monster_id'])
                            monsternew= call_monster(monster['evolveb'])
                            db.playerMonster.monsters.update_one(query,{'$set':{"monster_id":monsternew['id'],'evo':False,'prev_evo':pre_mon}})

def evo_mon(id):
       query = {"active": True, "poster_id": id} 
       player_monster=db.playerMonster.monsters.find_one(query)
       print(player_monster)    
       if player_monster['evo'] == True:
              print('time for evo ')  
              monster=call_monster(player_monster['monster_id'])
              print(monster)
              if monster['stage'] ==3:      
                     monster=call_monster(monster['id'])
                     monsternew= call_monster(monster['evolve'][0])
                     print(monsternew)
                     db.playerMonster.monsters.update_one(query,{'$set':{"monster_id":monsternew['id'],'evo':False, 'prev_evo':player_monster['monster_id']}})     


def update_stat(id,stat,ammount):
       query = {"active": True, "poster_id": id} 
       stats= db.playerMonster.monsters.find_one(query)
       stat_single=stats[stat]
       stat_single += ammount
       db.playerMonster.monsters.update_one(query,{'$set':{stat:ammount}})   
       
def get_stage(id):
       query = {"_id":id}
       res = db.userProfiles.userProfiles.find_one(query)
       if 'stage' not in res or res['stage'] is None:
              db.userProfiles.userProfiles.update_one(query,{'$set':{'stage':0}})
              res = db.userProfiles.userProfiles.find_one(query)
       return res['stage']


def expcheck(id,exp):
    query = {"active": True, "poster_id": id} 
    monster=db.playerMonster.monsters.find_one(query)
    xp=monster['exp']  
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
              flash('Ding')
              db.playerMonster.monsters.update_one(query,{'$set':{'level':level}})  
              if level == 3:
                     print('update stat')
                     update_stat(id,"atk",1) 
              if level ==4:
                     update_stat(id,'hp',1)
                     update_stat(id,"atk",1) 
              if level ==5:
                     update_stat(id,"power",2)
              if level ==6:  
                     update_stat(id,"hp",2)   
                     update_stat(id,"power",2)
              if level ==7:  
                     update_stat(id,"atk",2)  
              if level ==8:  
                     update_stat(id,"hp",2)
              if level ==9:  
                     update_stat(id,"hp",2)
              if level ==10:  
                     update_stat(id,"hp",3)
                     update_stat(id,"power",3)
                     update_stat(id,"atk",2)

                     
         
    

#expcheck(ObjectId('6541107d9a2ed6e684a6552c'),1 )                  
           
    