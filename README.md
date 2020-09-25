# Ranking-Project
W6 Project - The Ranking

![acceso-universal-a-internet-dstNtc](https://user-images.githubusercontent.com/61025562/94252247-92c7f800-ff1b-11ea-9574-5910f98e599e.jpg)

# Objetivo

Poner en práctica todo lo aprendido en el bootcamp de Data de Ironhack hasta el momento. Para ello, llevaremos a cabo lo siguiente:

- Creación de una API usando flask
- Análisis de los datos extraidos de las pull request del repositorio del bootcamp(datamad0820) mediante requests a la API de Github
- Usar pymongo para el almacenamiento de los datos en Mongodb
- Docker, Heroku and Cloud

# Metodología

- Los datos los obtendremos de las pull requests realizdas por los alumnos al repositorio del bootcamp mediante requests a la API pública de Github.
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
