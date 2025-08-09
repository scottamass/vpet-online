import random
      

monster1 ={"name":"one","hp":3,"atk":1,"power":25}
monster2 ={"name":"Two","hp":3,"atk":1,"power":29}

def hitcalc(monster1,monster2):
    power = monster1['basepower']+ monster1['power']
    powertwo = monster2['power']
    power = int(power)
    powertwo =int(powertwo)
    hitrate = ((power*100)/(power+powertwo))
    return (hitrate)





def opponent_turn():   
    monster1['hp'] -= monster2['atk']

def battle(monster1,monster2,loc):    
    print(loc)
    batteling =True
    p1 =monster1['name']
    p1hp =monster1['hp'] + monster1['basehp']
    p1atk=monster1['atk'] + monster1['baseatk']
    p1atk= int(p1atk)
    p1hp= int(p1hp)
    p2 =monster2['name']
    p2hp =monster2['hp']
    p2hp= int(p2hp)
    p2atk = int(monster2['atk'])
    print(f'{p1}/{p1hp} v.s. {p2}/{p2hp}')
    battlelog =[]
    turn=1
    while batteling == True:
        print(f'Turn {turn}')
        turn +=1
        hittate=hitcalc(monster1,monster2)
        dice = int(random.random() * 100)
        if dice <hittate:
            p2hp -= p1atk
            message = {'player':1,'dialog':f'{p1} struck {p2} for {p1atk} damage leaving them with {p2hp} hp','p1hp':str(p1hp),'p2hp':str(p2hp)}
            battlelog.append(message)
            if p2hp <=0:
                message = {'player':1,'dialog':"""<p>You were Victorious</p>
                 
              """}
                battlelog.append(message)
                
                return {'log':battlelog,'result':'win'}
        else:
            p1hp -= p2atk
            message = {'player':2,'dialog':f'{p2} struck {p1} for {p2atk} damage leaving you with {p1hp} hp','p1hp':str(p1hp),'p2hp':str(p2hp)}
            battlelog.append(message)
            if p1hp <=0:
                message = {'player':2,'dialog':"""<p>You Lost</p>
                            """}
                battlelog.append(message)
                
                
                return {'log':battlelog,'result':'loose'}
                    

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
