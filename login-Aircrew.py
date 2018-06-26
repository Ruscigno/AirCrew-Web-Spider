import requests
from bs4 import BeautifulSoup

url_base = 'https://pilotobrasil.com.br'

def login(event, context):
    # TODO implement
    return doLogin(**event)

def doLogin(username,password):  
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