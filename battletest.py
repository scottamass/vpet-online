import random
from time import sleep       

monster1 ={"name":"one","hp":3,"atk":1,"power":25}
monster2 ={"name":"Two","hp":3,"atk":1,"power":29}

def hitcalc(monster1,monster2):
    hitrate = ((monster1['power']*100)/(monster1['power']+monster2['power']))
    return (hitrate)


def player_turn():
    monster2['hp'] -= monster1['atk']

def opponent_turn():   
    monster1['hp'] -= monster2['atk']

def battle(monster1,monster2):    
    batteling =True
    p1 =monster1['name']
    p1hp =monster1['hp']
    p2 =monster2['name']
    p2hp =monster2['hp']
    print(f'{p1}/{p1hp} v.s. {p2}/{p2hp}')
    while batteling == True:
        hittate=hitcalc(monster1,monster2)
        dice = int(random.random() * 100)
        if dice <hittate:
            print(f"{p1} Hit")
            player_turn()
            print(monster2['hp'])
            sleep(5)
            if monster2['hp'] <=0:
                print('win')
                
                break

        else:
            print(f"{p2}Hit")
            opponent_turn()
            print(monster1['hp'])
            sleep(5)
            if monster1['hp'] <=0:
                
                print('loose')
                break    

battle(monster1,monster2)

# def battle(basepower,opponentTotal):
#     hitrate = ((basepower*100)/(basepower+opponentTotal))
#     return (hitrate)


# hittate=battle(33,25)
# dice = int(random.random() * 100)
# if dice <hittate:
#     print("Hit")
# else:
#     print("Miss")    
