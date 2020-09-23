import requests
import math
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

#Obtengo los títulos de las pull request
titulos = []
for i in pulls:
    for j in i:
        if "]" in j['title']: 
            nombre = ((j['title']).split("]")[0]).strip()
            nombre = (nombre + "]").replace(" ", "-")
            titulos.append(nombre)
        else:
            titulos.append(" ")

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
        "prq": titulos[i],
        "alumni" :{f"0":[j['user']['login'] for i in pulls for j in i][i]},
        "estado" : [j['state'] for i in pulls for j in i][i],
        "update": [j['updated_at'] for i in pulls for j in i][i],
        "cierre": [j["closed_at"] for i in pulls for j in i][i],
        "meme": {"0": memes[i]}
    }
    pullrq.append(pr)

#Cargo en Mongo los documentos
client2 = MongoClient("mongodb://localhost/")
mydb2 = client2["ranking"]
mycol2 = mydb2["pullrequest"]

mycol2.insert_many(pullrq)

##FALTA INCLUIR LOS QUE TIENEN MAS DE UN MEME O MAS DE UNA ALUMNO
