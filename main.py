import requests
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

def get_Pretest_Question(url, data):
  quest = c.get(url)
  soup = BeautifulSoup(quest.content, "html.parser")
  form = soup.find('form')
  #token
  token = form.find_all("input", {"name": "_token"})  
  data['token'] = token[0].get('value')
  #course
  course = form.find_all("input", {"name": "course"})  
  data['course'] = token[0].get('value')
  #group
  group = form.find_all("input", {"name": "group"})  
  data['group'] = token[0].get('value')
  #time
  #time = form.find_all("input", {"name": "time"})  
  #time = token[0].get('value')
  data['time'] = ''



def get_PCA_Hot_Questions(data):
  # hot questions
  hot_ct = '/simulados/realizar/5/17'
  hot_met = '/simulados/realizar/5/19'
  hot_nav = '/simulados/realizar/5/55'
  hot_reg = '/simulados/realizar/5/23'
  hot_tv = '/simulados/realizar/5/18'

  get_Pretest_Question(url_base + hot_ct, data)

def get_PCA_Fav_Questions():
  # favorite questions
  fav_ct = '/simulados/questoes-favoritas/5/17'
  fav_met = '/simulados/questoes-favoritas/5/19'
  #fav_nav = '/simulados/realizar/5/55'
  fav_reg = '/simulados/questoes-favoritas/5/23'
  fav_tv = '/simulados/questoes-favoritas/5/18'



data = {}
with requests.Session() as c:
  if login('teste@gmail.com','teste'):
    get_PCA_Hot_Questions(data)
    print(data)
  else:
    print('Ops! Deu zica!!!')