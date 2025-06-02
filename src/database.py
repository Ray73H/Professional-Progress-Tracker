import psycopg2
import os

def db():
    return psycopg2.connect(
        dbname=os.getenv("DATABASE_NAME"),
        user=os.getenv("USER_NAME"),
        password=os.getenv("PASSWORD"),
        host=os.getenv("HOST", "localhost"),
        port=os.getenv("PORT", 5432)
    )