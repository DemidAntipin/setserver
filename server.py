from flask import Flask, request, json
from random import randint
import requests
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)

logins=[]
passwords={}
tokens={}
games={}
running_games={}
max_id=0

@app.post('/user/login')
def login_post():
    data = json.loads(request.data)
    if 'login' not in data or 'password' not in data:
        response={'success':False, 'exception':{'message':'Couldn`t find login or password in request.'}}
        return response
    login = data.get('login')
    password=data.get('password')
    if login not in logins or not(check_password_hash(passwords[login], password)):
        response={'success':False, 'exception':{'message': 'Incorrect login or password.'}}
        return response
    if login in tokens.keys():
        response={'success':False, 'exception':{'message': 'You have already logged in.'}}
        return response
    response={'success':True,'exception':None,'login':login, 'accessToken': os.urandom(8).hex()}
    tokens[login]=response['accessToken']
    return response

@app.route('/user/signup', methods=['POST'])
def signup_post():
    data = json.loads(request.data)
    if 'login' not in data or 'password' not in data:
        response={'success':False, 'exception':{'message':'Couldn`t find login or password in request.'}}
        return response    
    login = data.get('login')
    password=generate_password_hash(data.get('password'))
    if login in logins:
        response={'success':False, 'exception':{'message':'Login is already exist.'}}
        return response
    logins.append(login)
    passwords[login]=password
    print(logins, passwords)
    response={'success':True,'exception':None}
    return response

@app.post('/user/logout')
def logout_post():
    data = json.loads(request.data)
    if 'login' not in data or 'accessToken' not in data:
        response={'success':False, 'exception':{'message': 'Couldn`t find login or accessToken in request.'}}
        return response
    login = data.get('login')
    token = data.get('accessToken')
    if login not in logins or login not in tokens.keys():
        response={'success':False, 'exception':{'message': 'Unknown user. Check your login.'}}
        return response
    if tokens[login]!=token:
        response={'success':False, 'exception':{'message': 'Invalid accessToken for this user.'}}
        return response
    del tokens[login]
    response={'success':True,'exception':None}
    return response

@app.post('/set/room/create')
def create_set():
    global max_id
    data = json.loads(request.data)
    if 'accessToken' not in data:
        response={'success':False, 'exception':{'message':'Couldn`t find accessToken.'}}
        return response
    token = data.get('accessToken')
    if token not in tokens.values():
        response={'success':False, 'exception':{'message':'Invalid accessToken'}}
        return response
    deck=[]
    cards=[]
    for i in range(81):
        card={}
        card['id']=i+1
        card['color']=i//27+1
        card['shape']=i%27//9+1
        card['fill']=i%27%9//3+1
        card['count']=i%27%9%3+1
        deck.append(card)
    for i in range(12):
        j=randint(0,len(deck)-1)
        card=deck.pop(j)
        cards.append(card)
    game={}
    max_id+=1
    game['id']=max_id
    game['deck']=deck
    game['cards']=cards
    game['score']=0
    game['status']='ongoing'
    game['scores']=[]
    games[max_id]=game
    response={'success':True, 'exception': None,'gameId':max_id}
    return response

@app.post('/set/enter')
def enter():
    data = json.loads(request.data)
    if 'accessToken' not in data or 'gameId' not in data:
        response={'success':False, 'exception':{'message':'Couldn`t find accessToken or gameId.'}}
        return response
    id=data.get('gameId')
    token=data.get('accessToken')
    if token not in tokens.values() or id>max_id:
        response={'success':False, 'exception':{'message':'Invalid accessToken or game doesn`t exist.'}}
        return response
    if token in running_games.keys():
        response={'success':False, 'exception':{'message':'You are already in game.'}}
        return response
    if id in running_games.values():
        response={'success':False, 'exception':{'message':'Access denied. Somebody already joined this game.'}}
        return response
    running_games[token]=id
    response={'success':True, 'exception': None, 'gameId':id}
    return response

@app.post('/set/field')
def field():
    data = json.loads(request.data)
    if 'accessToken' not in data:
        response={'success':False, 'exception':{'message':'Couldn`t find accessToken.'}}
        return response
    token = data.get('accessToken')
    if token not in running_games.keys():
        response={'success':False, 'exception':{'message':'You didn`t joined any games.'}}
    id = running_games[token]
    game=games[id]
    response = {}
    response['cards']=game['cards']
    response['status']=game['status']
    response['status']=game['status']
    return response

@app.post('/set/add')
def add():
    data = json.loads(request.data)
    if 'accessToken' not in data:
        response={'success':False, 'exception':{'message':'Couldn`t find accessToken.'}}
        return response
    token = data.get('accessToken')
    if token not in running_games.keys():
        response={'success':False, 'exception':{'message':'You didn`t joined any games.'}}
    id = running_games[token]
    game=games[id]
    if len(game['deck'])<3:
        response={'success':False, 'exception':{'message':'Not enough card. All cards already in play.'}}
        return response
    for i in range(3):
        j=randint(0,len(game['deck'])-1)
        card=game['deck'].pop(j)
        game['cards'].append(card)
    response = {'success':True, 'exception': None}
    return response

@app.post('/set/score')
def score():
    data = json.loads(request.data)
    if 'accessToken' not in data:
        response={'success':False, 'exception':{'message':'Couldn`t find accessToken.'}}
        return response
    token = data.get('accessToken')
    if token not in running_games.keys():
        response={'success':False, 'exception':{'message':'You didn`t joined any games.'}}
    id = running_games[token]
    game=games[id]
    response={'success':True, 'exception': None, 'users':game['scores']}
    return response

@app.post('/set/pick')
def pick():
    data = json.loads(request.data)
    if 'accessToken' not in data or 'cards' not in data:
        response={'success':False, 'exception':{'message':'Couldn`t find accessToken or cards.'}}
        return response
    token = data.get('accessToken')
    if token not in running_games.keys():
        response={'success':False, 'exception':{'message':'You didn`t joined any games.'}}
    id = running_games[token]
    game=games[id]
    cards=data.get('cards')
    hand_id=[card['id'] for card in game['cards']]
    if not isinstance(cards,list) or len(cards)!=3:
        response={'success':False, 'exception':{'message':'Cards must be a list with lenght 3!'}}
        return response
    if game['status']=='ended':
        response={'success':False, 'exception':{'message':'Game ended.'}}
        return response
    for i in cards:
        if not isinstance(i,int) or i<=0 or i>81 or i not in hand_id:
            response={'success':False, 'exception':{'message':'Invalid card_id or card not in play.'}}
            return response
    card_1=game['cards'][hand_id.index(cards[0])]
    card_2=game['cards'][hand_id.index(cards[1])]
    last_card={}
    for quality in ['color','shape','fill','count']:
        if card_1[quality]==card_2[quality]:
            last_card[quality]=card_1[quality]
        else:
            last_card[quality]=6-card_1[quality]-card_2[quality]
    last_card['id']=(last_card['color']-1)*27+(last_card['shape']-1)*9+(last_card['fill']-1)*3+last_card['count']
    if last_card['id']!=cards[2]:
        response={'isSet':False,'score':game['score']}
        return response
    else:
        game['cards'].pop(hand_id.index(cards[0]))
        game['cards'].pop(hand_id.index(cards[1]))
        game['cards'].pop(hand_id.index(cards[2]))
        if len(game['deck']) and len(game['cards'])<12:
            data={'accessToken':token}
            url="http://158.160.144.217:5000/set/add"
            r=requests.post(url,json=data)
        game['score']+=100
        if len(game['cards'])<3:
            game['status']='ended'
            name=[n for n in tokens.keys() if tokens[n]==token][0]
            game['scores'].append({'name':name,'score':game['score']})
        response={'isSet':True, 'score': game['score'] }
        return response


if __name__ == "__main__":
    app.run(host='0.0.0.0')
