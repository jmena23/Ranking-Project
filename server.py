from src.app import app
import src.controllers.alumnos_control
from config import PORT

app.run("0.0.0.0", PORT, debug = True)