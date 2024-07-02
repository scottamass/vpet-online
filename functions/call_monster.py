import json

def call_monster(data):
    with open('monsterdb.monsters2.json') as f:
                     d = json.load(f)
                     # print(d)
                     for i in d :
                            if i['id'] == data:
                                    return i 

