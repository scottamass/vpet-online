import json
from blueprints.mobile import new_feature_bp
from blueprints.auth_bp import auth_bp
from blueprints.gameplay import gameplay_bp
import datetime
import random
from flask import Flask, Response, flash, jsonify, redirect, request,session , render_template, url_for
from flask_login import LoginManager, UserMixin, login_required,login_user,current_user, logout_user
from flask_bcrypt import Bcrypt
import requests
from pymongo import DESCENDING, MongoClient
from bson import json_util,ObjectId
import os
from battletest import battle as btl
from dbjobs import dbjobsonerun
from explore import random_number
from functions.battletower import battleTower 
from functions.call_monster import call_monsters
from functions.dbfunct import evo_mon, evocheck, expcheck, fetch_player_monster, get_stage, give_monster_to_player
from functions.items import add_item_to_player, remove_item_from_player



mongo_connect=os.getenv('M_CONNECTION_STRING')
db= MongoClient(mongo_connect)

VERSION='0.5'
#db.playerMonster.monsters.update_many({},{'$set': {"seris": 1}})
class User(UserMixin):
    def __init__(self,id,username,pic,role):
        
        self.id = id
        self.username = username
        self.pic = pic
        self.roles=role

class Post():
    def __init__(self,monsterid,poster_id, posted_date):
        self.game = monsterid 
        self.poster_id=poster_id
        self.posted_date = posted_date

    


app = Flask(__name__)
bcrypt = Bcrypt(app)

app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)

login_manager = LoginManager()


@login_manager.unauthorized_handler
def unauthenticated():
        if request.path.startswith('/app/'):
        # Redirect to a different login page for /app/ routes
            return redirect(url_for('new_feature.app_login'))
        
        return redirect(url_for('login'))

@login_manager.user_loader
def load_user(user_id):
    u= db.userProfiles.userProfiles.find_one({'_id':ObjectId(user_id)})
    if u is not None:
        return User(id=u['_id'],username=u['username'],pic=u['profilePic'],role=u['role'])

login_manager.init_app(app)

def parse_json(data):
    return json.loads(json_util.dumps(data))

# @app.errorhandler(404)
# def error(error):
#     return 'sometimes server had died'
app.register_blueprint(new_feature_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(gameplay_bp)
@app.route('/')
def index():
 
    return render_template('home.html')
    
############# monster screen #############
@app.route('/player')
@login_required
def player():
    monster=fetch_player_monster(current_user.id)
    if monster != None:
        # evocheck(current_user.id)
        monster=fetch_player_monster(current_user.id)
        print(monster)
    backgroundUrl='/static/bg/1.jpeg'
    
    return render_template('playersummary.html' ,monster=monster ,backgroundUrl=backgroundUrl) 

@app.route('/part/monster')
@login_required
def monster():
    monster=fetch_player_monster(current_user.id)
    if monster != None:
        evocheck(current_user.id)
        monster=fetch_player_monster(current_user.id)
    backgroundUrl='/static/bg/1.jpeg'
    return render_template('/partials/monster.html',monster=monster ,backgroundUrl=backgroundUrl)
########### monster management screen #########
@app.route('/train',methods=['POST','GET'])
def train():
    if request.method == 'POST':       
        monster=fetch_player_monster(current_user.id)
        args=request.args
        train = args.get('training')
        
        expcheck(current_user.id,5)
        newtrain = monster['traning'] 
        newtrain += 1
        query = {"active": True, "poster_id": current_user.id} 
        db.playerMonster.monsters.update_one(query,{'$set':{"traning":newtrain}})
        return redirect(url_for('monster'))
    
    return render_template('/partials/traning.html')


@app.route('/evolve')
def evolve():
    # print('evolve')
    evo_mon(current_user.id)
    return redirect(url_for('monster'))

@app.route('/directory')
def directory():
    monsters = call_monsters()
    return render_template('directory.html',monsters=monsters)

@app.route('/explore',methods=["GET","POST"])
def explore():
    print(get_stage(current_user.id))
    
    val1=random_number()
    val2=random_number()
    val3=random_number()
    monsters = [val1,val2,val3]
    stage = get_stage(current_user.id)
    return render_template('explore.html',stage=stage,monster=monsters)


@app.route('/explore/monster/<mon>',methods=["GET","POST"])
def explore_monster(mon):
    
    monId = int(mon)
    val=random.randint(5,75)
    monster = battleTower
    print(monster[monId])
    player = db.userProfiles.userProfiles.find_one({"_id":current_user.id})
    if request.method == 'POST':
            monster=fetch_player_monster(current_user.id)
            args = request.args
            stage= int(args['stage'])
            prize = args['prize']
            name = args['name']
            hp = args['hp']
            pow = args['power']
            atk = args['atk']
            xp =int(args['xp'])
            opponent = {'name':name,'atk':atk,"hp":hp,"power":pow}
            result=btl(monster,opponent,1)
            if result['result'] == "win":
                playerBank = int(player['money'])
                playerBank += int(prize)
                mwins = monster['wins'] 
                mwins += 1
                pwins = player['wins']
                pwins += 1
                if stage > player['battleTower']:
                    db.userProfiles.userProfiles.update_one({"_id":current_user.id},{'$set':{"battleTower":stage,'money':playerBank,"wins":pwins,}})
                    db.playerMonster.monsters.update_one({'_id':monster['_id']},{'$set':{"wins":mwins}})
                else: 
                    db.userProfiles.userProfiles.update_one({"_id":current_user.id},{'$set':{'money':playerBank,"wins":pwins}})
                    db.playerMonster.monsters.update_one({'_id':monster['_id']},{'$set':{"wins":mwins}})


                expcheck(current_user.id,xp)
                return render_template('/partials/battleScreen.html',result=result ,monster=monster,opponent=opponent,loc=1)
            else: 
                losses = monster['losses'] 
                losses += 1
                db.userProfiles.userProfiles.update_one({"_id":current_user.id},{'$set':{'losses':losses}})
                
                return render_template('/partials/battleScreen.html',result=result,monster=monster,opponent=opponent)
    response = Response(render_template('partials/mon.html', monster=monster[monId], id=monId ,val=val))
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    return response

@app.route('/battle',methods=["GET"])
def battle():
    return render_template('/partials/battlemenu.html')

@app.route('/battle/battletower',methods=["GET","POST"])
def battle_tower():
    fetch_player_monster(current_user.id)
    bt = battleTower
    player = db.userProfiles.userProfiles.find_one({"_id":current_user.id})
    if request.method == 'POST':
            monster=fetch_player_monster(current_user.id)
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
                playerBank = int(player['money'])
                playerBank += int(prize)
                mwins = monster['wins'] 
                mwins += 1
                pwins = player['wins']
                pwins += 1
                if stage > player['battleTower']:
                    db.userProfiles.userProfiles.update_one({"_id":current_user.id},{'$set':{"battleTower":stage,'money':playerBank,"wins":pwins,}})
                    db.playerMonster.monsters.update_one({'_id':monster['_id']},{'$set':{"wins":mwins}})
                else: 
                    db.userProfiles.userProfiles.update_one({"_id":current_user.id},{'$set':{'money':playerBank,"wins":pwins}})
                    db.playerMonster.monsters.update_one({'_id':monster['_id']},{'$set':{"wins":mwins}})


                expcheck(current_user.id,xp)
                return render_template('/partials/battleScreen.html',result=result ,monster=monster,opponent=opponent,loc=0)
            else: 
                losses = monster['losses'] 
                losses += 1
                db.userProfiles.userProfiles.update_one({"_id":current_user.id},{'$set':{'losses':losses}})
                
                return render_template('/partials/battleScreen.html',result=result,monster=monster,opponent=opponent)
    return render_template('/partials/battletower.html', bt=bt, player=player)


####### new monster management ###########
@app.route('/api/createmonster', methods=['POST'])
@login_required
def post_game():
    
    game = request.form.get('options')
    poster_id = current_user.id
    posted_date = datetime.datetime.now()
    newmonster = Post(game,poster_id,posted_date)
    print(newmonster)
    give_monster_to_player(newmonster)
    return redirect(url_for('index'))


    






################ USER MANAGEMENT AND AUTH ##################
@app.route('/dbjobs')
@login_required
def dbjobsadmin():
    status = dbjobsonerun()
    return status 

@app.route('/item_test')
@login_required
def item_test():
    print(current_user)
    item=add_item_to_player(1,current_user.id)
    return item

@app.route('/item_test-remove')
@login_required
def item_remove():
    item = remove_item_from_player(1, current_user.id)
    return item
@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        email= request.form ['email']
        user = request.form ['username']
        pw= request.form ['pwd']
        if db.authDb.users.find_one({"email":email}):
            return "user in db"
        elif db.authDb.users.find_one({"username":user}):    
            return "username exists"
        else: 
            hashed_pw = bcrypt.generate_password_hash(pw)
            db.authDb.users.insert_one({"email":email,"password":hashed_pw,'username':user})
            requested_user = db.authDb.users.find_one({"email":email})
            print(requested_user)
            user_uid = requested_user["_id"]
            #add user to profile db
            db.userProfiles.userProfiles.insert_one({'auth_id':user_uid,'username':user,"profilePic":None,"role":"player",'battleTower':0,"money":100,'wins':0,'losses':0})
            return redirect(url_for('login'))
    else: return render_template("register.html")            

@app.route('/login',methods=['POST','GET'] )
def login():
    if request.method == 'POST':
        user = request.form ['username']
        pw= request.form ['pwd']
        query= db.authDb.users.find_one({"username":user})
        if db.authDb.users.find_one({"username":user}):
            if bcrypt.check_password_hash(query['password'],pw):                
                user_name=db.userProfiles.userProfiles.find_one({"auth_id":ObjectId(query['_id'])})
                user_id = user_name['_id']
                user = User(user_id,user_name['username'],None,user_name['role'])                
                login_user(user, remember=True)
                return redirect('/')
            else: 
                flash('Incorrect email or password please try again ')
                return redirect('/login')
        else: 
            flash('Incorrect email or password please try again ')
            return redirect('/login')
    else: return render_template("login.html")

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')

@app.route('/api/register', methods=['GET','POST'])
def api_register():
    if request.method == 'POST':
        user=request.json["email"]
        pw=request.json["password"]
        print(user)
        if db.loginUsers.created_users.find_one({"email":user}):
            return "user in db"
        else: 
            hashed_pw = bcrypt.generate_password_hash(pw)
            db.loginUsers.created_users.insert_one({"email":user,"password":hashed_pw})
            requested_user = db.loginUsers.created_users.find_one({"email":user})
            user_uid = requested_user["_id"]
            print(user_uid)
            return redirect(url_for('login'))
    else: return render_template("register.html")       

@app.route('/admin')
@login_required
def admin_screen():
    if current_user.roles == 'admin':
        itemsarray = db.userProfiles.userItems.find_one({'player_id':current_user.id})
        return render_template('adminscreen.html',items=itemsarray)
    else: return 'access denined'

@app.route('/api/login',methods=['POST','GET'] )
def api_login():
    if request.method == 'POST':
        user=request.json["email"]
        pw=request.json["password"]
        query= db.loginUsers.created_users.find_one({"email":user})
        if db.loginUsers.created_users.find_one({"email":user}):
            print('user in db')                        
            if bcrypt.check_password_hash(query['password'],pw):               
                user_name=db.loginUsers.created_users.find_one({"email":user})
                user_id = user_name['_id']
                print(user_id)
                user = User(user_id,user_name['email'],None)              
                login_user(user)
                return "200"
            else: return jsonify({"error":"unauthorized"}),401
        else: return jsonify({"error":"unauthorized"}),401
    else: return render_template("login.html")    


@app.route('/healthcheck')
def healthcheck():
    return jsonify({'status': 'ok', 'message': 'Health check passed'})


@app.route('/login/discord')
def login_discord():

    url_discord = os.getenv('DISCORD_URL')
    return redirect(url_discord)

@app.route('/login/discord/callback')
def login_discord_callback():
    code = request.args['code']
    secret =os.getenv('DISCORD_SECRET')
    client_id = os.getenv('DISCORD_CLIENT')
    uri_redirect = os.getenv('URL_REDIRECT')
    
    token_params = {
            'client_id': client_id,
            'client_secret': secret,
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': f'{uri_redirect}/login/discord/callback',
            'scope': 'identify',
            'prompt':'none'
        }
    res= requests.post('https://discord.com/api/oauth2/token',data=token_params)
    data = res.json()
    if 'access_token' in data:
            # Fetch user information using the access token
            user_url = 'https://discord.com/api/users/@me'
            headers = {'Authorization': f'Bearer {data["access_token"]}'}
            user_response = requests.get(user_url, headers=headers)
            user_data = user_response.json()
            #print(user_data)
            did=user_data['id']
            dun=user_data['username']
            print(did)
            query= db.userProfiles.userProfiles.find_one({"auth_id":did})
            if query == None:
                db.userProfiles.userProfiles.insert_one({'auth_id':did,'username':dun,"profilePic":None,"role":"player",'battleTower':0,"money":100,'wins':0,'losses':0})
                query= db.userProfiles.userProfiles.find_one({"auth_id":did})
                user_id = query
                user_id = query['_id']
                user = User(user_id,query['username'],None,query['role'])                
                login_user(user, remember=True)
            else: 
                print('user Exists')
                query= db.userProfiles.userProfiles.find_one({"auth_id":did})
                print(query)
                user_id = query['_id']
                user = User(user_id,query['username'],None,query['role'])                
                login_user(user, remember=True)
    return redirect('/player')

if __name__=="__main__":
    app.run(debug=True ,host='0.0.0.0' ,port='80')