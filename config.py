import os
from dotenv import load_dotenv

# Carga las variables de entorno del archivo .env
load_dotenv()

class Config:
    """Clase de configuración de la aplicación."""
    MYSQL_HOST = os.getenv('MYSQL_HOST')
    MYSQL_USER = os.getenv('MYSQL_USER')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
    MYSQL_DB = os.getenv('MYSQL_DB')
    SECRET_KEY = os.getenv('SECRET_KEY')