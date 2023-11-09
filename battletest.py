import random
      

monster1 ={"name":"one","hp":3,"atk":1,"power":25}
monster2 ={"name":"Two","hp":3,"atk":1,"power":29}

def hitcalc(monster1,monster2):
    power = monster1['basepower']
    powertwo = monster2['power']
    power = int(power)
    
    powertwo =int(powertwo)

    hitrate = ((power*100)/(power+powertwo))
    return (hitrate)


def player_turn():
    monster2['hp'] -= monster1['atk']

def opponent_turn():   
    monster1['hp'] -= monster2['atk']

def battle(monster1,monster2):    
    batteling =True
    p1 =monster1['name']
    p1hp =monster1['hp']
    p1atk=monster1['atk']
    p1atk= int(p1atk)
    p1hp= int(p1hp)
    p2 =monster2['name']
    p2hp =monster2['hp']
    p2hp= int(p2hp)
    p2atk = int(monster2['atk'])
    print(f'{p1}/{p1hp} v.s. {p2}/{p2hp}')
    while batteling == True:
        hittate=hitcalc(monster1,monster2)
        dice = int(random.random() * 100)
        if dice <hittate:
            print(f"{p1} Hit")
            p2hp -= p1atk
            print(p2hp)
            if p2hp <=0:
                return 'win'
        else:
            print(f"{p2}Hit")
            p1hp -= p2atk
            print(monster1['hp'])
            if p1hp <=0:
                return 'loose'
                    

#battle(monster1,monster2)

# def battle(basepower,opponentTotal):
#     hitrate = ((basepower*100)/(basepower+opponentTotal))
#     return (hitrate)


# hittate=battle(33,25)
# dice = int(random.random() * 100)
# if dice <hittate:
#     print("Hit")
# else:
#     print("Miss")    
