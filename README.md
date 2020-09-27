# Ranking-Project

![91af7af540ac583d9f76b1ca920e962a](https://user-images.githubusercontent.com/61025562/94283775-590de600-ff49-11ea-84fd-96432e60d690.png)


# Link despliegue en Heroku

https://ranking2020.herokuapp.com

# Objetivo

Poner en práctica todo lo aprendido en el bootcamp de Data de Ironhack hasta el momento. Para ello, llevaremos a cabo lo siguiente:

- Creación de una API usando flask
- Análisis de los datos extraidos de las pull request del repositorio del bootcamp(datamad0820) mediante requests a la API de Github
- Usar pymongo para el almacenamiento de los datos en Mongodb
- Despliegue de la API en producción mediante Docker, Heroku y Mongo Atlas

# Metodología

- Los datos los obtendremos de las pull requests realizadas por los alumnos al repositorio del bootcamp mediante requests a la API pública de Github.
- Limpiaremos los datos con la ayuda de python, bs4, regex o cualquier otra herramienta que nos sea útil.
- Los datos depurados los almacenaremos en Mongodb utilizando pymongo.
- Configuraremos una API con flask.
- Crearemos los siguientes endpoints para interactuar desde el navegador con los datos que están en la base de datos en Mongodb:
    - L1. Student endpoints
        - (GET) **/student/create/<studentname>**    -->  Ejemplo de uso: ```/student/create/thecoder```

            Propósito: Crear un estudiante nuevo e insertarlo en la base de datos
            ```
            {
             "id_": "5f70cec2a6a8b145c33f628e", 
            "msg": "El alumno con usuario de Github thecoder se ha introducido correctamente en la base de datos", 
            "status": "OK"
            }
            ```

        - (GET) **/student/all**    -->  Ejemplo de uso: ```/student/all```

            Propósito: Listar a los estudiantes en la base de datos

            ```
            {"lista de alumnos": ["Diegon8", "gontzalm", "IreneLopezLujan", "PaulaNuno", "rfminguez", "Jav1-Mart1nez", "Daniel-GarciaGarcia", "DiegoCaulonga", "jmena23", "grundius1", "marta-zavala", "Joycelili", "charliesket", "KevsDe", "bmedm", "VanessaMacC", "miguelgimenezgimenez", "AnaMA96", "FDELTA", "jorge-alamillos", "laura290", "silviaherf", "Davidlazarog", "CarlosSanzDGP"]}
            ```

    - L2. Lab endpoints

        - (POST) **/lab/create**    -->  Ejemplo de uso: ```/lab/create?lab=[lab-numpy]```

            Propósito: Obtener un lab de la base de datos para analizar.

            ```
            {"Lab_selected": "El lab elegido para su analisis es el siguiente: {'_id': ObjectId('5f6dd98109fbebc92e9b3c62'), 'lab': '[lab-numpy]'}"}
            ```

        - (GET) **/lab/<lab_id>/search**    -->  Ejemplo de uso: ```/lab/[lab-numpy]/search```

            Propósito: Realizar el análisis de un lab concreto

            ```
            {
            "missing_pr": [
                "marta"
            ], 
            "percentage_completeness": "100.0%", 
            "pr_closed": 24, 
            "pr_open": 0, 
            "time_pulls": "0 days, 20 horas, 45 minutos, 15 segundos", 
            "unique_memes": [
                "https://user-images.githubusercontent.com/57899051/91285936-18764d80-e78e-11ea-898d-726724084d72.png", 
                "https://user-images.githubusercontent.com/57899051/91280561-2f657180-e787-11ea-9be7-96aba50b9874.png\">\r", 
                "https://user-images.githubusercontent.com/57899051/91167725-bc9bbe00-e6d4-11ea-85f2-97770cd71402.png", 
                "https://user-images.githubusercontent.com/57899051/91165875-c112a780-e6d1-11ea-95e0-8d4878807b9e.png", 
                "https://user-images.githubusercontent.com/52798316/91197561-c258ca00-e6fb-11ea-990d-c311cd13131a.png", 
                "https://user-images.githubusercontent.com/52798316/91156967-067ca800-e6c5-11ea-9d89-689bcd0778aa.png>", 
                "https://user-images.githubusercontent.com/57899051/91279433-c3ced480-e785-11ea-90f8-45f77663edfe.jpg", 
                "https://user-images.githubusercontent.com/57899051/91171286-83fee300-e6da-11ea-8aa5-20d4008a80b7.png", 
                "https://user-images.githubusercontent.com/57899051/91282531-c29fa680-e789-11ea-81ef-0d39c0bc16fe.png", 
                "https://user-images.githubusercontent.com/52798316/91156967-067ca800-e6c5-11ea-9d89-689bcd0778aa.png", 
                "https://user-images.githubusercontent.com/57899051/91280379-f2997a80-e786-11ea-9817-1d842ebaf596.png", 
                "https://user-images.githubusercontent.com/52798316/91313577-d6610200-e7b5-11ea-963c-d96cc7f0060f.png", 
                "https://user-images.githubusercontent.com/57899051/91170124-af80ce00-e6d8-11ea-90eb-bd6e8478674f.png", 
                "https://user-images.githubusercontent.com/57899051/91295660-b4f31c80-e79b-11ea-9d9a-b4dd95a735bd.png"
                ]
            }
            ```

        - (GET) **/lab/memeranking**    -->  Ejemplo de uso: ```/lab/memeranking```

            Propósito: Ranking de los memes más usados en datamad0820 dividido por labs

            ```{
            "0": {
                "lab": "[lab-advance-querying-mongo]", 
                "ranking": [
                "https://user-images.githubusercontent.com/52798316/93356303-4e639a80-f83f-11ea-8d61-65fe94209815.png:12", 
                "https://user-images.githubusercontent.com/57899051/93536225-cff31f80-f948-11ea-9e32-e4b29dca17e2.jpg:1", 
                "https://user-images.githubusercontent.com/57899051/93535836-185e0d80-f948-11ea-99a1-b7f4cf461c1e.png\">\r:1", 
                "https://user-images.githubusercontent.com/57899051/93535708-d3d27200-f947-11ea-852e-d832ec1c9bb3.jpg:1", 
                "https://user-images.githubusercontent.com/57899051/93535595-8e15a980-f947-11ea-9af6-03148d4e154e.jpg>:1", 
                "https://user-images.githubusercontent.com/57899051/93535510-658daf80-f947-11ea-9014-9d7100c37aea.jpg:1", 
                "https://user-images.githubusercontent.com/57899051/93535363-18114280-f947-11ea-9070-431ed6186d23.jpg:1", 
                "https://user-images.githubusercontent.com/57899051/93535270-e8fad100-f946-11ea-800d-a55ea823eaaf.jpg:1", 
                "https://user-images.githubusercontent.com/57899051/93535156-b18c2480-f946-11ea-9530-cef9478c97b0.jpg:1", 
                "https://user-images.githubusercontent.com/57899051/93534770-ffecf380-f945-11ea-9510-1051156448d2.jpg:1", 
                "https://user-images.githubusercontent.com/57899051/93534422-573e9400-f945-11ea-9aed-9fe4ee574dd3.jpg:1", 
                "https://user-images.githubusercontent.com/57899051/93534004-80125980-f944-11ea-8d1f-9e6782f713e0.png\">\r:1"
                ]
            }, 
            "1": {
                "lab": "[lab-advanced-pandas]", 
                "ranking": [
                "https://user-images.githubusercontent.com/52798316/93324278-f3697d80-f815-11ea-93a4-ec9760c90fba.png:9", 
                "https://user-images.githubusercontent.com/57899051/93533275-dc747980-f942-11ea-984c-c1c01f24ea92.png\">\r:1", 
                "https://user-images.githubusercontent.com/52798316/93328615-3e868f00-f81c-11ea-82ae-066cdf84f383.png:1", 
                "https://user-images.githubusercontent.com/57899051/93532881-2315a400-f942-11ea-885a-b9d7bef1cbe2.jpg:1", 
                "https://user-images.githubusercontent.com/57899051/93526194-6585b380-f937-11ea-8505-200ee814ae7b.jpg:1", 
                "https://user-images.githubusercontent.com/52798316/93326252-cd91a800-f818-11ea-901b-ed49c2208aa1.png:1", 
                "https://user-images.githubusercontent.com/57899051/93532727-dc27ae80-f941-11ea-84cd-ec99e83c2c5e.jpg:1", 
                "https://user-images.githubusercontent.com/57899051/93532431-4db32d00-f941-11ea-9300-e9e393cd174e.jpg:1", 
                "https://user-images.githubusercontent.com/52798316/93325648-e64d8e00-f817-11ea-988f-258c75bd3409.png:1", 
                "https://user-images.githubusercontent.com/57899051/93522409-b4c8e580-f931-11ea-9c62-cfaa35bd5db6.png\">\r:1", 
                "https://user-images.githubusercontent.com/57899051/93526567-efce1780-f937-11ea-9d49-2b22195589f9.png\">\r:1", 
                "https://user-images.githubusercontent.com/57899051/93522281-83e8b080-f931-11ea-8bc3-5eeb3cd674e1.jpg:1", 
                "https://user-images.githubusercontent.com/57899051/93494993-efb92200-f90d-11ea-872a-448a358f600a.png\">\r:1", 
                "https://user-images.githubusercontent.com/57899051/93494499-60ac0a00-f90d-11ea-9d28-a414a2971679.jpg:1"
                ]
            },
            [...]
            ```

        - (GET) **/lab/<lab_id>/meme**    -->  Ejemplo de uso: ```/lab/[lab-numpy]/meme```

            Propósito: Obtener un meme random del lab que indicamos en la url.
            ```
            {
            "meme": "El meme random seleccionado del lab [lab-numpy] es: https://user-images.githubusercontent.com/52798316/91156967-067ca800-e6c5-11ea-9d89-689bcd0778aa.png"
            }
            ```

# Organización

- Carpeta mongo donde están los scripts para cargar en la base de datos los alumnos y las pull request

- Carpeta scr donde están:
 
    - Los controladores de la API

    - Archivo helpers que contiene un decorador para resolver el problema con el object_id en el return ya que no es serializable

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
