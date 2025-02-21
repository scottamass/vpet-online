import datetime
from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import current_user, login_required


from functions.dbfunct import evo_mon, evocheck, fetch_player_monster, give_monster_to_player
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
    return render_template('app/partials/screens/monsters.html')
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