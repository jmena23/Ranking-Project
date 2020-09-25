import requests
import math
import re
from pymongo import MongoClient
import os 
from dotenv import load_dotenv
load_dotenv()

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

#NO ME COGÍA BIEN LOS TÍTULOS CON UN DICCIONARIO Y TUVE QUE RECURRIR A LOS ELIF INFINITOS
#CUANDO TENGA MÁS TIEMPO LO CORREGIRÉ CON EL DICCIONARIO

#errores = {"mongo": '[lab-advance-querying-mongo]', "errhand": '[lab-errhand-listcomp]', "generat": '[lab-generator-functions]', 
#               "mysql":'[lab-mysql-select]', "parsing": '[lab-parsing-api]', "probability": '[lab-probability-distribution]', 
#               "resolving": '[lab-resolving-git-conflicts]', "storytelling": '[storytelling-project]', "tuple": '[lab-tuple-set-dict]', 
#               "web": '[lab-web-scraping]'}

titles = []
for i in titulos:
    if "mongo" in i:
        titles.append('[lab-advance-querying-mongo]')
    elif "errhand" in i:
        titles.append('[lab-errhand-listcomp]')
    elif "generat" in i:
        titles.append('[lab-generator-functions]')
    elif "mysql" in i:
        titles.append('[lab-mysql-select]')
    elif "parsing" in i:
        titles.append('[lab-parsing-api]')
    elif "probability" in i:
        titles.append('[lab-probability-distribution]')
    elif "resolving" in i:
        titles.append('[lab-resolving-git-conflicts]')
    elif "storytelling" in i:
        titles.append('[storytelling-project]')
    elif "tuple" in i:
        titles.append('[lab-tuple-set-dict]')
    elif "web" in i:
        titles.append('[lab-web-scraping]')
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
    if i == [] or "[image]" not in i[0]["body"]:
        memes.append("Unknown")
    else:
        memes.append(((i[0]["body"]).split("[image](")[1]).split(")")[0])

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
