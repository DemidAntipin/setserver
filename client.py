import requests

nickname=''
token=''
ip='http://158.160.144.217:5000'
gameId=0

def signup(nickname, password):
    data={'login':nickname, 'password':password}
    url=ip+'/user/signup'
    r=requests.post(url,json=data)
    print(r.status_code)
    print(r.text)

def login(nick, password):
    global nickname
    global token
    data={'login':nick, 'password':password}
    url=ip+'/user/login'
    r=requests.post(url,json=data)
    print(r.status_code)
    print(r.text)
    data = r.json()
    if (data['success']):
        nickname = data['login']
        token = data['accessToken']

def logout(login):
    global token
    global nickname
    data={'login':login, 'accessToken':token}
    url=ip+'/user/logout'
    r=requests.post(url,json=data)
    print(r.status_code)
    print(r.text)
    if (r.json()['success']):
        token = ''
        nickname = ''

def create():
    global token
    data={'accessToken':token}
    url=ip+'/set/room/create'
    r=requests.post(url,json=data)
    print(r.status_code)
    print(r.text)

def enter(game):
    global token
    global gameId
    data={'accessToken':token,'gameId':game}
    url=ip+'/set/enter'
    r=requests.post(url,json=data)
    print(r.status_code)
    print(r.text)
    data=r.json()
    if (data['success']):
        gameId = data['gameId']

def field():
    global token
    data={'accessToken':token}
    url=ip+'/set/field'
    r=requests.post(url,json=data)
    print(r.status_code)
    text=r.json()
    for i in text["cards"]:
        print(i)
    
def add():
    global token
    data={'accessToken':token}
    url=ip+'/set/add'
    r=requests.post(url,json=data)
    print(r.status_code)
    print(r.text)

def score():
    global token
    data={'accessToken':token}
    url=ip+'/set/score'
    r=requests.post(url,json=data)
    print(r.status_code)
    print(r.text)

def pick(l):
    global token
    data={'accessToken':token,'cards':l}
    url=ip+'/set/pick'
    r=requests.post(url,json=data)
    print(r.status_code)
    print(r.text)

def interface():
    command_list=['signup','login','logout','create','enter','field','add','score','pick','exit']
    while True:
        print('Список доступных команд: ', *command_list)
        command=input('Введите команду из списка:')
        if command=='signup':
            nickname=input('Введите ник: ')
            password=input('Введите пароль: ')
            signup(nickname,password)
        elif command=='login':
            nickname=input('Введите ник: ')
            password=input('Введите пароль: ')
            login(nickname,password)
        elif command=='logout':
            nickname=input('Введите ник: ')
            logout(nickname)
        elif command=='create':
            create()
        elif command=='enter':
            i=int(input('Введите id комнаты: '))
            enter(i)
        elif command=='field':
            field()
        elif command=='add':
            add()
        elif command=='score':
            score()
        elif command=='pick':
            l=list(map(int, input('Введите через пробел id 3-ех карт. Чтобы посмотреть карты используйте комманду `field`.').split()))
            pick(l)
        elif command=='exit':
            print('Ждем вашего возвращения.')
            break

interface()
