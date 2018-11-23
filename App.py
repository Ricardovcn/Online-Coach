#coding: utf-8

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
urlPrefixoYtb = 'https://www.youtube.com/embed/'

#Id da sessãoq ue será utilizado em todas as requisições
#Vale lembrar que cada sessão possui apenas 15 min
# para crfiar uma sessao usaremos a seguinte sintaxe '/createsession​[ResponseFormat]/{developerId}/{signature}/{timestamp}'
session = ''

nickname = ''

player = ''

deuses = '' 

linguas = {'portugues':10,'english':1}

partidas = {'Arena':435, 'Assalto':445, 'Conquista':426, 'Justa':448, 'Colisão':466 }

elos = {'0' : 'Não classificado.',
        '1' : 'Bronze V', '2' : 'Bronze IV', '3' : 'Bronze III', '4': 'Bronze II', '5' : 'Bronze I',
        '6': 'Prata V', '7': 'Prata IV', '8': 'Prata III', '9': 'Prata II', '10': 'Prata I',
        '11': 'Ouro V', '12': 'Ouro IV', '13': 'Ouro III', '14': 'Ouro II', '15': 'Ouro I', 
        '16': 'Platina V', '17': 'Platina IV', '18': 'Platina III', '19': 'Platina II', '20': 'Platina I', 
        '21': 'Diamante V', '22': 'Diamante IV', '23': 'Diamante III', '24': 'Diamante II', '25': 'Diamante I', '26': 'Masters I',}

partidas = [ 426, 451, 448, 466 ]

#A assinatura é um hash md5 de um combinado de itens (devId, metodo_da_api, authKey, timestamp)
def assinatura(devId, metodo, authKey, timestamp):
    h = hashlib.md5()
    h.update((devId+metodo+authKey+timestamp).encode('utf-8'))
    return h.hexdigest()

def criaSessao(url, metodo, tipoRetorno, devId, authKey):
  timestamp = datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S')
  r = requests.get(url+metodo+tipoRetorno+'/'+devId+'/'+assinatura(devId, metodo, authKey, timestamp)+'/'+timestamp)
  dados = json.loads(r.text)
  return dados['session_id']

#/getplayer​[ResponseFormat]/{developerId}/{signature}/{session}/{timestamp}/{playerName}
def requisicaoPlayer(url, metodo, tipoResposta, devId, authKey, session, nick):
    timestamp = datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S')
    r = requests.get(url+metodo+tipoResposta+'/'+devId+'/'+assinatura(devId, metodo, authKey, timestamp)+'/'+session+'/'+timestamp+'/'+nick)
    return r.text

#/getgods​[ResponseFormat]/{developerId}/{signature}/{session}/{timestamp}/{languageCode}
def requisicaoDeuses(url, metodo, tipoResposta, devId, authKey, session, lingua):
    timestamp = datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S')
    r = requests.get(url+metodo+tipoResposta+'/'+devId+'/'+assinatura(devId, metodo, authKey, timestamp)+'/'+session+'/'+timestamp+'/'+str(lingua))
    return r.text


#/getqueuestats​[ResponseFormat]/{developerId}/{signature}/{session}/{timestamp}/{player}/{queue}
def requisicaoPartidas(url, metodo, tipoResposta, devId, authKey, session, nick, queue):
    timestamp = datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S')
    r = requests.get(url+metodo+tipoResposta+'/'+devId+'/'+assinatura(devId, metodo, authKey, timestamp)+'/'+session+'/'+timestamp+'/'+nick+"/"+str(queue))
    return r.text
 
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST', 'PUT', 'DELETE'])
def api():
  if request.method == 'GET':
    global session 
    if session == '':
      session = criaSessao(urlPrefixo, 'createsession', 'json', devId, authKey)
    return render_template('index.html')  
  else:
    return json.dumps({'erro': 'Utilize o metodo GET para acessar essa API.'})

@app.route('/deuses', methods=['GET', 'POST'])
def deusesPagina():
  global deuses
  try:
    with open('/cache/gods.json', 'r') as f:
      gods = f.read()
  except IOError:
    gods =  requisicaoDeuses(urlPrefixo, 'getgods', 'json', devId, authKey, session,linguas['portugues'])
    f = open('./cache/gods.json', 'w')
    f.write(gods)
  gods = json.loads(gods)
  deuses = gods
  return render_template('deuses.html', deuses = gods, nick=nickname)

@app.route('/perfil/<nick>', methods=['GET', 'POST'])
def perfil(nick):
  global player
  global nickname
  global dadosPLayer
  nickname = nick
  player = requisicaoPlayer(urlPrefixo, 'getplayer', 'json', devId, authKey, session, nick)
  dadosPLayer = json.loads(player)
  if player =='[]':
    return render_template('error.html', mensagem="Esse nick corresponde a um jogador inexistente ou com perfil privado.")
  else:
    dicas = []
    dadoPLayer = dadosPLayer[0]
    d = open('./dicas/dicas.json', 'r', encoding='utf-8')
    jsond = json.loads(d.read())
    d.close()
    if dadoPLayer['MasteryLevel'] < 75:
      r = requests.get('https://www.googleapis.com/youtube/v3/search?part=id&order=relevance&q=SMITE - EXPLICANDO SOBRE MAESTRIA DE DEUSES&key=AIzaSyDrcUdUEc-7E_QqCh9GTBry4zfh3An5SWg') 
      ytbResp = json.loads(r.text)
      dicas.append({'titulo': 'Maestrias', 'texto': jsond['dicaMaestrias'], 'video': urlPrefixoYtb+ytbResp['items'][0]['id']['videoId']})

    if dadoPLayer['Wins'] * 100 / (dadoPLayer['Wins'] + dadoPLayer['Losses']) < 60:
      dicas.append({'titulo': 'Taxa de Vitórias', 'texto': jsond['dicaVitoria'], 'video': ''})
    
    if dadoPLayer['Tier_Conquest'] < 14:
      r = requests.get('https://www.googleapis.com/youtube/v3/search?part=id&order=relevance&q=SMITE LIGA CONQUISTA - INFORMAÇOES BÁSICAS SOBRE ELO E ORDEM DE PICK&key=AIzaSyDrcUdUEc-7E_QqCh9GTBry4zfh3An5SWg') 
      ytbResp = json.loads(r.text)
      dicas.append({'titulo': 'Conquista Rankeada', 'texto': jsond['dicaConquista'], 'video': urlPrefixoYtb+ytbResp['items'][0]['id']['videoId']})
    
    if dadoPLayer['Tier_Joust'] < 14:
      r = requests.get('https://www.googleapis.com/youtube/v3/search?part=id&order=relevance&q=SMITE - DICAS PARA SUBIR DE ELO NA JUSTA 3X3&key=AIzaSyDrcUdUEc-7E_QqCh9GTBry4zfh3An5SWg') 
      ytbResp = json.loads(r.text)
      dicas.append({'titulo': 'Justa Rankeada', 'texto': jsond['dicaJusta'], 'video': urlPrefixoYtb+ytbResp['items'][0]['id']['videoId']})
    
    if dadoPLayer['Tier_Duel'] < 14: 
      r = requests.get('https://www.googleapis.com/youtube/v3/search?part=id&order=relevance&q=SMITE - DICAS PARA SE DAR BEM NO DUELO&key=AIzaSyDrcUdUEc-7E_QqCh9GTBry4zfh3An5SWg') 
      ytbResp = json.loads(r.text)
      dicas.append({'titulo': 'Duelo', 'texto': jsond['dicaDuelo'], 'video': urlPrefixoYtb+ytbResp['items'][0]['id']['videoId']})
    return render_template('perfil.html', players=dadosPLayer , elo=elos, dica=dicas)


def retornaEficiencia(mediaKills,  mediaMortes, mediaAssists):
  return float(mediaKills)*1.1+float(mediaAssists)*0.9-float(mediaMortes);


@app.route('/player/deus/<id>', methods=['GET', 'POST'])
def playerGod(id):
  global deuses
  god=''
  for i in deuses:
    if str(i['id']) == str(id):
      god = i
    
  #def requisicaoPartidas(url, metodo, tipoResposta, devId, authKey, session, nick, queue):
  resultados = []
  for i in partidas:
    partida =   requisicaoPartidas(urlPrefixo, "getqueuestats", "Json", devId, authKey, session, nickname, i)
    partida = json.loads(partida)
    for j in partida:
     if str(j['GodId']) == str(god['id']):
       resultados.append(j)
  resultadoFinal = {'Assists' : 0, 'Deaths': 0, 'Gold': 0, 'Kills': 0, 'Losses': 0, 'Wins': 0}
  for i in resultados:
    resultadoFinal['Assists'] += i['Assists']
    resultadoFinal['Deaths'] += i['Deaths']
    resultadoFinal['Gold'] += i['Gold']
    resultadoFinal['Kills'] += i['Kills']
    resultadoFinal['Losses'] += i['Losses']
    resultadoFinal['Wins'] += i['Wins']
  d = open('./dicas/dicas.json', 'r', encoding='utf-8')
  jsond = json.loads(d.read())
  d.close()
  dica=""
  numPartidas = resultadoFinal['Losses']+resultadoFinal['Wins']
  videos = []
  if numPartidas != 0:
    if retornaEficiencia(resultadoFinal['Kills']/numPartidas,resultadoFinal['Deaths']/numPartidas,resultadoFinal['Assists']/numPartidas)<6.8:
      if god['Roles']==' Assassino':
        dica = jsond['dicaAssassino']
      elif god['Roles']==' Guerreiro':
        dica = jsond['dicaGuerreiro']
      elif god['Roles']==' Mago':
        dica = jsond['dicaMago']
      elif god['Roles']==' Caçador':
        dica = jsond['dicaCacador']
      else:
        dica = jsond['dicaGuardiao']
      r = requests.get('https://www.googleapis.com/youtube/v3/search?part=id&order=relevance&q=SMITE Como jogar '+god['Name']+'&key=AIzaSyDrcUdUEc-7E_QqCh9GTBry4zfh3An5SWg') 
      ytbResp = json.loads(r.text)
      for i in range(3):
        videos.append(urlPrefixoYtb+ytbResp['items'][i]['id']['videoId'])
  return render_template('deus.html', god = god, resultado = resultadoFinal, dica=dica, videos=videos)



if __name__ == "__main__":
 app.run(debug=True)