# Ranking-Project
W6 Project - The Ranking

![91af7af540ac583d9f76b1ca920e962a](https://user-images.githubusercontent.com/61025562/94283775-590de600-ff49-11ea-84fd-96432e60d690.png)

# Objetivo

Poner en práctica todo lo aprendido en el bootcamp de Data de Ironhack hasta el momento. Para ello, llevaremos a cabo lo siguiente:

- Creación de una API usando flask
- Análisis de los datos extraidos de las pull request del repositorio del bootcamp(datamad0820) mediante requests a la API de Github
- Usar pymongo para el almacenamiento de los datos en Mongodb
- Docker, Heroku and Cloud

# Metodología

- Los datos los obtendremos de las pull requests realizadas por los alumnos al repositorio del bootcamp mediante requests a la API pública de Github.
- Limpiaremos los datos con la ayuda de python, bs4, regex o cualquier otra herramienta que nos sea útil.
- Los datos depurados los almacenaremos en Mongodb utilizando pymongo.
- Configuraremos una API con flask.
- Crearemos los siguientes endpoints para interactuar desde el navegador con los datos que están en la base de datos en Mongodb:
    - L1. Student endpoints
        - (GET) /student/create/<studentname>

            Propósito: Crear un estudiante y guardarlo en la base de datos

            Parámetro: nombre del estudiante en Github

            Returns: student_id

        - (GET) /student/all

            Propósito: Listar a los estudiantes en la base de datos

            Returns: Un array con los estudiantes

    - L2. Lab endpoints

        - (POST) /lab/create

            Propósito: Crear un lab para analizar.

            Params: Prefijo del lab a analizar. Ejemplo: [lab-scavengers]

            Returns: lab_id

        - (GET) /lab/<lab_id>/search

            Propósito: Realizar el análisis de un lab concreto

            Parámetro: lab_id

            Returns: Ver Lab analysis section

        - (GET) /lab/memeranking

            Propósito: Ranking de los memes más usados en datamad0820 dividido por labs

        - (GET) /lab/<lab_id>/meme

            Propósito: Obtener un meme random del lab que indicamos en la url.

    - LAB ANALYSIS SECTION

        Por cada lab analizar lo siguiente:

            Número de PR abiertas

            Número de PR cerradas

            Porcentaje (cerradas vs abiertas)

            Lista de estudiantes que no enviaron la PR

            Lista de memes únicos en el lab

            Tiempo medio de cierra del lab: (fecha de cierre-último commit)

# Organización

- Carpeta mongo donde están los scripts para cargar en la base de datos los alumnos y las pull request

- Carpeta scr donde están:
 
    - Los controladores de la API

    - Archivo helpers que contiene un decorador para resolver el object_id en el return ya que no es serializable

    - Archivo app con la API

    - Archivo database con la conexión a la base de datos de Mongodb

- Archivo config con los parámetros de configuración de API y base de datos

- Archivo server ejecutable para arrancar la API desde la terminal

# Enlaces de interés

- https://flask.palletsprojects.com/

- https://www.getpostman.com/

- https://api.mongodb.com/python/current/api/pymongo/collection.html#pymongo.collection.Collection.insert_one

- https://api.mongodb.com/python/current/tutorial.html

Cloud:

- https://docs.docker.com/engine/reference/builder/

- https://runnable.com/docker/python/dockerize-your-python-application

- https://devcenter.heroku.com/articles/container-registry-and-runtime

- https://devcenter.heroku.com/categories/deploying-with-docker

- https://www.mongodb.com/cloud/atlas
