from src.app import app
from flask import request, Response
from src.helpers.json_response import asJsonResponse
from src.database import db
from flask import request, Response
import random
import datetime
import numpy as np
from collections import Counter

@app.route('/lab/create')
@asJsonResponse
def createlab():
    lab_name = request.args.get("lab")
    if not lab_name:
        return {
            "status": "error",
            "message": "Empty lab name, please specify one"
        }, 400

    lab_choice = db["pulls"].find_one({"lab": lab_name}, {"lab":1})

    if not lab_choice:
        return {
            "status": "not found",
            "message": f"No lab found with name {lab_name} in database"
        }, 404

    return {"lab_name": lab_choice}

@app.route('/lab/<lab_id>/search')
def analysis(lab_id):
    data = db["pulls"].find({'lab':lab_id}, {"alumnos":1, "estado":1, "last_commit_time":1, "pr_close_time":1, "meme":1})
    b = list(data)

    pr_open = 0
    for i in b:
        if i['estado'] == "open":
            pr_open += 1
            
    pr_closed = len(b) - pr_open

    percentage = 100 * pr_closed/(pr_open + pr_closed)
    percentage = str(percentage) + "%"

    estudiantes = []
    for i in b:
        for j in i["alumnos"]:
            estudiantes.append(j)

    dataalu = db["alumnos"].find({}, {"usuario_github":1})
    row_est = list(dataalu)
    students = []
    for i in row_est:
        students.append(i['usuario_github'])

    lista_est = list(set(students) - set(estudiantes))

    mememes = []
    for i in b:
        if i['meme'] != "Unknown":
            mememes.append(i["meme"])

    mememes = list(set(mememes))

    resta = []
    for i in b:
        cierre = datetime.datetime.strptime((i['pr_close_time'][:-1]).replace("T"," "), '%Y-%m-%d %H:%M:%S')
        ult_comm = datetime.datetime.strptime((i['last_commit_time'][:-1]).replace("T"," "), '%Y-%m-%d %H:%M:%S')
        resta.append(cierre - ult_comm)

    cierre_pull = np.mean(resta)
    days = cierre_pull.days
    sec = cierre_pull.seconds
    cierre_pull = f"{days} days, {days*24 + sec//3600} horas, {(sec%3600)//60} minutos, {sec%60} segundos"

    return {
        "pr_open": pr_open,
        "pr_closed": pr_closed,
        "percentage_completeness": percentage,
        "missing_pr": lista_est,
        "unique_memes": mememes,
        "time_pulls": cierre_pull
    }


@app.route('/lab/memeranking')
def rankingmeme():
    a = db["pulls"].distinct("lab")
    a = a[1:]

    mem = []
    for i in a:
        b = db["pulls"].find({'lab':i}, {"meme":1})
        mem.append(b)
    
    ret = []
    for i in range(len(mem)):
        data = list(mem[i])
        if data != []:
            m = []
            for j in data:
                if j['meme'] != "Unknown":
                    m.append(j["meme"])
            ordenados = sorted(Counter(m).items(), key=lambda x:x[1], reverse = True)
            h = []
            for k in ordenados:
                h.append(k[0]+ ":" + str(k[1]))
            reto = {"lab": a[i],"ranking": h}
            ret.append(reto)
    rank = {}
    for i in range(len(ret)):
        rank[i]=ret[i]
    return rank



@app.route('/lab/<lab_id>/meme')
def randommeme(lab_id):
    data = db["pulls"].find({'lab':lab_id}, {"meme":1})
    b = list(data)
    m = []
    for i in b:
        if i['meme'] != "Unknown":
            m.append(i["meme"])

    sol = random.choice(m)
    return {
        'meme' : sol
    }
