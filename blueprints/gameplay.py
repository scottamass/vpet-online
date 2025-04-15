import datetime
from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from battletest import battle as btl
from blueprints.logic.app_funcrions import process_win
from functions.battletower import battleTower 
from functions.dbfunct import evo_mon, evocheck, expcheck, fetch_all_player_monster, fetch_player_monster, give_monster_to_player, db
from bson import json_util
import json

class Post():
    def __init__(self,monsterid,poster_id, posted_date):
        self.game = monsterid 
        self.poster_id=poster_id
        self.posted_date = posted_date
gameplay_bp = Blueprint('gameplay', __name__ ,template_folder='templates')

#Screens 

#main game loop
@gameplay_bp.route('/app/monster') 
def monster():
    monster=fetch_player_monster(current_user.id)
    if monster != None:
        evocheck(current_user.id)
        monster=fetch_player_monster(current_user.id)
    backgroundUrl='/static/bg/1.jpeg'
    return render_template('/app/partials/screens/gameSreen.html',monster=monster)

@gameplay_bp.route('/app/shop')
def shop():
    return render_template('app/partials/screens/shop.html')

@gameplay_bp.route('/app/monsters')
def monsters():
    monsters_cursor = fetch_all_player_monster(current_user.id)
    # Convert cursor to list and serialize MongoDB-specific types
    monsters = json.loads(json_util.dumps(list(monsters_cursor)))
    return render_template('app/partials/screens/monsters.html', monsters=monsters)
    # return render_template('directory.html',monsters=monsters)
    #return 'TEST'

@gameplay_bp.route('/app/evolve')
def evolve():
    # print('evolve')
    evo_mon(current_user.id)
    return redirect(url_for('gameplay.monster'))


@gameplay_bp.route('/app/battle')
def battle():
    return render_template('app/partials/battlemenu.html')

@gameplay_bp.route('/app/api/createmonster', methods=['POST'])
@login_required
def post_game():
    
    game = request.form.get('options')
    poster_id = current_user.id
    posted_date = datetime.datetime.now()
    newmonster = Post(game,poster_id,posted_date)
    
    give_monster_to_player(newmonster)
    return redirect('/app/new-feature')

@gameplay_bp.route('/app/utils/switch',methods=["POST"])
def switch_monster():
    pass
@gameplay_bp.route('/app/battle/battletower',methods=["GET","POST"])
def battle_tower():
    fetch_player_monster(current_user.id)
    bt = battleTower
    print(bt)
    player = db.userProfiles.userProfiles.find_one({"_id":current_user.id})
    if request.method == 'POST':
            monster=fetch_player_monster(current_user.id)
            user_id=current_user.id
            args = request.args
            stage= int(args['stage'])
            prize = args['prize']
            name = args['name']
            hp = args['hp']
            pow = args['power']
            atk = args['atk']
            xp =int(args['xp'])
            opponent = {'name':name,'atk':atk,"hp":hp,"power":pow}
            result=btl(monster,opponent,0)
            if result['result'] == "win":
                process_win(player,prize,stage,monster,user_id)
                expcheck(current_user.id,xp)
                return render_template('/app/partials/battleScreen.html',result=result ,monster=monster,opponent=opponent,loc=0)
            else: 
                losses = monster['losses'] 
                losses += 1
                db.userProfiles.userProfiles.update_one({"_id":current_user.id},{'$set':{'losses':losses}})
                
                return render_template('/app/partials/battleScreen.html',result=result,monster=monster,opponent=opponent)
    return render_template('/app/partials/battletower.html', bt=bt, player=player)