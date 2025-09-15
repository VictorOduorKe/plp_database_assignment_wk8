import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()
if not os.getenv("HOST"):
    raise ValueError("Environment variables not set. Please check your .env file.")
# ----------------- DATABASE CONNECTION HELPERS -----------------
def create_db_connection():
    try:
        connection = mysql.connector.connect(
            host=os.getenv("HOST"),
            user=os.getenv("USER"),
            database=os.getenv("DATABASE"),
            password=os.getenv("PASSWORD"),
            port=int(os.getenv("PORT"))
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error: '{e}'")
        return None

def close_db_connection(connection):
    if connection and connection.is_connected():
        connection.close()