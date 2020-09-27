from src.app import app
from flask import request, Response
from src.helpers.json_response import asJsonResponse
from src.database import db

@app.route('/student/create/<studentname>')
def insert_alumno(studentname):
    """
    Mediante este endpoint se puede crear y agregar un nuevo alumno a la base de datos, si éste no existe ya. 
    Para ello, se debe especificar el nombre de usuario de Github en el campo <studentname> de la url. 
    """

    find_usuario = db["alumnos"].find_one({"usuario_github":studentname}, {"usuario_github":1})
    if not find_usuario:
        alum = {"usuario_github": studentname}
        a = db["alumnos"].insert_one(alum)
        return {
            "id_": str(a.inserted_id),
            "msg": f"El alumno con usuario de Github {studentname} se ha introducido correctamente en la base de datos",
            "status": "OK"
        } 
    else:
        return {
                "status": "not found",
                "message": f"User with name {studentname} already exists"
            }, 404


@app.route('/students/all')
@asJsonResponse
def search_alum():
    """
    Mediante este endpoint, la función devuelve una lista con los alumnos que se encuentran en 
    la base de datos.
    """

    find_alumns = db["alumnos"].find()
    alumns = []
    for i in find_alumns:
        alumns.append(i["usuario_github"])

    return {
        "lista de alumnos": alumns
        }
