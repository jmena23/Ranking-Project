import requests
import math
from pymongo import MongoClient

def get_github(endpoint, query_params={}): 
    """
    Get data from github using query parameters and passing a custom apikey header
    """
    
    # Compose the endpoint url
    baseUrl = "https://api.github.com"
    url = f"{baseUrl}{endpoint}"

    # make the request and get the response using HTTP GET verb 
    res = requests.get(url, params=query_params)
   
    print(f"Request data to {res.url} status_code:{res.status_code}")
    data = res.json()
    
    if res.status_code != 200:
        raise ValueError(f'Invalid github api call: {data["message"]}')

    return data

number = get_github("/repos/ironhack-datalabs/datamad0820/pulls",query_params={'state': 'all', 'page' : 1, "per_page":100})[0]['number']

#Obtengo las pull requests de la API
pulls = []
for i in range(1, math.ceil(number/100) + 1):
    pulls.append(get_github("/repos/ironhack-datalabs/datamad0820/pulls",query_params={'state': 'all', 'page' : i, "per_page":100}))

#Obtengo los nombres de login de los alumnos y los almaceno en una lista
alumnos = []
fin = []
for i in pulls:
    for j in i: 
        alumnos.append(j['user']['login'])
for i in alumnos:
    if i not in fin:
        fin.append(i)

#Cargo en Mongo la colección de los alumnos
client = MongoClient("mongodb://localhost/")
mydb = client["ranking"]
mycol = mydb["alumnos"]

mycol.insert_many(fin)