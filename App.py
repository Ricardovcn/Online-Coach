#coding utf-8

import json
from flask import Flask, Response, render_template
from flask import request
import requests
import hashlib
import datetime

#Id do desenvolvedsor, servira como um 'usuario' para utilizar a api
devId = '2884'

#Chave de autenticação do usuario, usada para gerar uma assinatura
authKey = '555796E8AFC1466EAD08B6B325BD6D1B'

urlPrefixo = 'http://api.smitegame.com/smiteapi.svc/'

#Id da sessãoq ue será utilizado em todas as requisições
#Vale lembrar que cada sessão possui apenas 15 min
# para crfiar uma sessao usaremos a seguinte sintaxe '/createsession​[ResponseFormat]/{developerId}/{signature}/{timestamp}'
session = ''

nickname = ''

player = ''
linguas = {'portugues':10,'english':1}

partidas = {'Arena':435, 'Assalto':445, 'Conquista':426, 'Justa':448}

#A assinatura é um hash md5 de um combinado de itens (devId, metodo_da_api, authKey, timestamp)
def assinatura(devId, metodo, authKey, timestamp):
    h = hashlib.md5()
    h.update((devId+metodo+authKey+timestamp).encode('utf-8'))
    return h.hexdigest()

def criaSessao(url, metodo, tipoRetorno, devId, authKey):
  timestamp = datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S')
  r = requests.get(urlPrefixo+metodo+tipoRetorno+'/'+devId+'/'+assinatura(devId, metodo, authKey, timestamp)+'/'+timestamp)
  dados = json.loads(r.text)
  return dados['session_id']

#/getplayer​[ResponseFormat]/{developerId}/{signature}/{session}/{timestamp}/{playerName}
def requisicaoPlayer(url, metodo, tipoResposta, devId, authKey, session, nick):
    timestamp = datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S')
    r = requests.get(urlPrefixo+metodo+tipoResposta+'/'+devId+'/'+assinatura(devId, metodo, authKey, timestamp)+'/'+session+'/'+timestamp+'/'+nick)
    return r.text

#/getgods​[ResponseFormat]/{developerId}/{signature}/{session}/{timestamp}/{languageCode}
def requisicaoDeuses(url, metodo, tipoResposta, devId, authKey, session, lingua):
    timestamp = datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S')
    r = requests.get(urlPrefixo+metodo+tipoResposta+'/'+devId+'/'+assinatura(devId, metodo, authKey, timestamp)+'/'+session+'/'+timestamp+'/'+str(lingua))
    return r.text



 
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST', 'PUT', 'DELETE'])
def api():
  if request.method == 'GET':
    global session 
    #if session == '':
      #session = criaSessao(urlPrefixo, 'createsession', 'json', devId, authKey)
    return render_template('index.html')  
  else:
    return json.dumps({'erro': 'Utilize o metodo GET para acessar essa API.'})

@app.route('/deuses/<nick>', methods=['GET', 'POST'])
def deuses(nick):
  global player
  global nickname
  nickname = nick
  #gods =  requisicaoDeuses(urlPrefixo, 'getgods', 'json', devId, authKey, session,linguas['portugues'])
  #player = requisicaoPlayer(urlPrefixo, 'getplayer', 'json', devId, authKey, session, nick)
  arq = open('gods.json', 'r')
  gods = arq.read()

  if player =='[]':
    return json.dumps({'erro':'Jogador inexistente'})
  else:
    
    gods = json.loads(gods)
   # gods = gods
  #  print(gods)
    nickname=nick
    return render_template('deuses.html', deuses = gods, nick=nick)



@app.route('/player/deus/<id>', methods=['GET', 'POST'])
def playerGod(id):
  return 'asd'
if __name__ == "__main__":
 app.run(debug=True, host='10.3.1.19')
