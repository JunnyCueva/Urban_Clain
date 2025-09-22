# mysql_connector.py
import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

def get_db_connection():
    """Establece una conexión a la base de datos MySQL."""
    try:
        conn = mysql.connector.connect(
            host=os.environ.get('DB_HOST', 'localhost'),
            user=os.environ.get('DB_USER', 'usuario_db'),
            password=os.environ.get('DB_PASSWORD', 'contrasena_db'),
            database=os.environ.get('DB_NAME', 'nombre_db')
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Error al conectar a la base de datos: {err}")
        return None

def close_db_connection(conn):
    """Cierra la conexión a la base de datos."""
    if conn:
        conn.close()

def get_cursor(conn):
    """Obtiene un cursor de la conexión."""
    if conn:
        return conn.cursor(dictionary=True) # dictionary=True para obtener resultados como diccionarios
    return None