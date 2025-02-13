from flask import Blueprint, render_template
from flask_login import current_user

from functions.dbfunct import evocheck, fetch_player_monster

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
    #return 'TEST'