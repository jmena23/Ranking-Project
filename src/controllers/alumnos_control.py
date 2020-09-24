from src.app import app
from flask import request, Response
from src.helpers.json_response import asJsonResponse
from src.database import db

@app.route('/student/create/<studentname>')
def insert_alumno(studentname):
    find_usuario = db["alumnos"].find_one({"usuario_github":studentname}, {"usuario_github":1})
    if not find_usuario:
        alum = {"usuario_github": studentname}
        a = db["alumnos"].insert_one(alum)
        return {"id_": str(a.inserted_id)} 
    else:
        return {
                "status": "not found",
                "message": f"User with name {studentname} already exists"
            }, 404


@app.route('/students/all')
@asJsonResponse
def search_alum():
    find_alumns = db["alumnos"].find()
    return find_alumns
