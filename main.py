import requests
import yaml
import io
import db_persistence as dbp
from bs4 import BeautifulSoup

url_base = 'https://pilotobrasil.com.br'

def login(username,password):  
  url_login = url_base + '/login'
  url_check_logged = url_base + '/usuario/dashboard'
  txt_check = url_base + '/usuario/meus-dados'

  #preparing login data
  user = username
  pws = password
  page = c.get(url_login)
  soup = BeautifulSoup(page.content, "html.parser")
  token = soup.find_all("input", {"name": "_token"})  
  token = token[0].get('value')
  login = dict(_token=token, email=user, password=pws, remember='on')

  #log into web site
  c.post(url_login, data=login, headers={"Refers":url_base})
  page = c.get(url_check_logged)

  #checking success
  soup = BeautifulSoup(page.content, "html.parser")
  soup = soup.find(href=txt_check)
  if soup != None:
    return True
  else:
    return False

def get_Pretest_Question_FormData(form, data):
  #token
  token = form.find_all("input", {"name": "_token"})
  data['token'] = token[0].get('value')
  #course
  course = form.find_all("input", {"name": "course"})  
  data['course'] = course[0].get('value')
  #group
  group = form.find_all("input", {"name": "group"})  
  data['group'] = group[0].get('value')
  #time
  #time = form.find_all("input", {"name": "time"})  
  #time = token[0].get('value')
  #data['time'] = ''

def get_Quantidade_Questao(form):
  lis = form.find_all("li")
  if len(lis) > 0:
    return len(lis)
  else:
    return 0

def getQuestoes(qtd, form, data):
  result = []
  for i in range(0, qtd):
    div = form.find("div", {"id": "tabs-" + str(i)})
    cdQuestao = div.find("input", {"name":"q" + str(i)}).get("value")
    deQuestao = div.find("div", {"class":"question"}).find("p").text
    op1 = div.find("label",{"id":"label-"+str(i)+"-a"}).text[1:].strip()
    op2 = div.find("label",{"id":"label-"+str(i)+"-b"}).text[1:].strip()
    op3 = div.find("label",{"id":"label-"+str(i)+"-c"}).text[1:].strip()
    op4 = div.find("label",{"id":"label-"+str(i)+"-d"}).text[1:].strip()
    #result['questao-'+str(data['course'])+'-'+str(data['group'])+'-'+str(cdQuestao)] = {
    questao = {
      "course":data['course'],
      'group':data['group'],
      'questao':cdQuestao,
      'descricao':deQuestao,
      'alternativas': [op1,op2,op3,op4]
    }
    result.append(questao)
    #dbp.inserirQuestao(questao)
  return result

def get_PCA_Hot_Questions(data):
  # hot questions
  hot_ct = '/simulados/realizar/5/17'
  hot_met = '/simulados/realizar/5/19'
  hot_nav = '/simulados/realizar/5/55'
  hot_reg = '/simulados/realizar/5/23'
  hot_tv = '/simulados/realizar/5/18'

  form = BeautifulSoup(c.get(url_base + hot_ct).content, "html.parser").find('form')
  get_Pretest_Question_FormData(form, data)
  qtd = get_Quantidade_Questao(form)
  questoes = getQuestoes(qtd, form, data)
  dbp.inserirQuestoes(questoes)

def get_PCA_Fav_Questions():
  # favorite questions
  fav_ct = '/simulados/questoes-favoritas/5/17'
  fav_met = '/simulados/questoes-favoritas/5/19'
  #fav_nav = '/simulados/realizar/5/55'
  fav_reg = '/simulados/questoes-favoritas/5/23'
  fav_tv = '/simulados/questoes-favoritas/5/18'



data = {}
# Read YAML file
with open("config.yaml", 'r') as stream:
    data_loaded = yaml.load(stream)

with requests.Session() as c:
  if login(**data_loaded):
    for x in range(100):
      get_PCA_Hot_Questions(data)
  else:
    print('Ops! Deu zica!!!')