import requests
import math
import re
from pymongo import MongoClient
import os 
from dotenv import load_dotenv
load_dotenv()
from helpers.limpia_titulos import contains as lt

def get_gh_v3(endpoint, apiKey=os.getenv("GITHUB_APIKEY"), query_params={}): 
    """
    Get data from github using query parameters and passing a custom apikey header
    """
    
    # Compose the endpoint url
    baseUrl = "https://api.github.com"
    url = f"{baseUrl}{endpoint}"

    # Create the headers
    headers = {
        "Authorization": f"Bearer {apiKey}"
    }
    # make the request and get the response using HTTP GET verb 
    res = requests.get(url, params=query_params, headers=headers)
    print(f"Request data to {res.url} status_code:{res.status_code}")
    
    data = res.json()
    return data

# Obtengo todas las pulls de la API
number = get_gh_v3("/repos/ironhack-datalabs/datamad0820/pulls", apiKey=os.getenv("GITHUB_APIKEY"), query_params={'state': 'all', 'page' : 1, "per_page":100})[0]['number']

pulls = []
for i in range(1, math.ceil(number/100) + 1):
    pulls.append(get_gh_v3("/repos/ironhack-datalabs/datamad0820/pulls",query_params={'state': 'all', 'page' : i, "per_page":100}))

# Obtengo las url de los comments
comments = []
for i in pulls:
    for j in i: 
        comments.append(j['comments_url'])

# Obtengo los comments de la API con las URL del paso anterior
com = []
for i in comments:
    data = get_gh_v3(i.split(".com")[1], apiKey=os.getenv("GITHUB_APIKEY"), query_params={'page' : 1})
    com.append(data)

# Obtengo las url de los commits
commits = []
for i in pulls:
    for j in i: 
        commits.append(j['commits_url'])

# Obtengo los commits de la API con las URL del paso anterior
comit = []
for i in commits:
    data = get_gh_v3(i.split(".com")[1], apiKey=os.getenv("GITHUB_APIKEY"), query_params={'page' : 1})
    comit.append(data)

#Obtengo la fecha del último commit de cada pull request
lastcom = []
for i in comit:
    lastcom.append(i[-1]['commit']['author']['date'])

#Obtengo los títulos de las pull request
titulo = []
for i in pulls:
    for j in i:
        if "]" in j['title']: 
            nombre = ((j['title']).split("]")[0]).strip()
            nombre = (nombre + "]").replace(" ", "-")
            titulo.append(nombre)
        else:
            titulo.append(" ")

titulos = []
for i in titulo:
    if "]" in i and i[0] != "[":
        titulos.append("[" + i.lower())
    else:
        titulos.append(i.lower())

errores = {"mongo": '[lab-advance-querying-mongo]', "errhand": '[lab-errhand-listcomp]', "generat": '[lab-generator-functions]', 
           "parsing": '[lab-parsing-api]', "probability": '[lab-probability-distribution]', 
           "resolving": '[lab-resolving-git-conflicts]', "storytelling": '[storytelling-project]', "tuple": '[lab-tuple-set-dict]', 
           "web": '[lab-web-scraping]'}
ttts = []
for i in titulos:
    abc = lt.contains(i,errores)
    ttts.append(abc)

titles = []

for i in ttts:
    if "select" in i:
        titles.append('[lab-mysql-select]')
    elif "mysql" in i and "select" not in i:
        titles.append('[lab-mysql]')
    else:
        titles.append(i)

#Obtengo los alumnos de cada pull request(Creador, con @, join)
autor = ["@" + j['user']['login'] for i in pulls for j in i]

joins = []
for i in com:
    if i == [] or 'join' not in i[0]["body"] or i[0]["user"]["login"] in ['ferrero-felipe', 'agalvezcorell', 'WHYTEWYLL']:
        joins.append("Unknown")
    else:
        joins.append("@" + i[0]["user"]["login"])

al = []
for i in range(len(joins)):
    if joins[i] != 'Unknown' and joins[i] not in al:
        al.append([autor[i],joins[i]])
    elif joins[i] == 'Unknown':
        al.append([autor[i]])

intrusos = []
for i in pulls:
    for j in i:
        res = re.findall(r'@[\w-]+', j["body"])
        if res:    
            intrusos.append(res)
        else:
            intrusos.append("Unknown")

alu = []
for i in range(len(al)):
    if intrusos[i] != 'Unknown':
        alu.append(intrusos[i] + al[i])
    elif intrusos[i] == 'Unknown':
        alu.append(al[i])

duplicados = []
for i in alu:
    duplicados.append(list(set(i)))

definitivo = []
for i in range(len(duplicados)):
    inter = []
    for j in duplicados[i]:
        inter.append(j[1:])
    definitivo.append(inter)

#Obtengo los memes del body de los comments
memes = []
for i in com:
    if i == []:
        memes.append("Unknown")
    else:
        search = re.findall(r"https://.*", i[-1]["body"])
        if search:
            if ".jpeg" in search[0] or ".png" in search[0] or "jpg" in search[0]:
                memes.append((search[0]).split(")")[0])
            else:
                memes.append("Unknown")
        else:
            memes.append("Unknown")

#Creo los que serán los documentos de las pull request y los almaceno en una lista
pullrq = []
for i in range(len(memes)):
    pr = {
        "numero" : [j['number'] for i in pulls for j in i][i],
        "lab": titles[i],
        "alumnos" :definitivo[i],
        "estado" : [j['state'] for i in pulls for j in i][i],
        "last_commit_time": lastcom[i],
        "pr_close_time": [j["closed_at"] for i in pulls for j in i][i],
        "meme": memes[i]
    }
    pullrq.append(pr)

#Cargo en Mongo los documentos de la colección de las pull request
client2 = MongoClient("mongodb://localhost/")
mydb2 = client2["ranking"]
mycol2 = mydb2["pulls"]

mycol2.insert_many(pullrq)
