import os
from flask import Flask
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

db_connection = mysql.connector.connect(
    database =  os.environ.get('DB_NAME'),
    host = os.environ.get('DB_HOST'),
    port = os.environ.get('DB_PORT'),
    user = os.environ.get('DB_USER'),
    password = os.environ.get('DB_PASSWORD')
)

print("connected to a database")

cursor = db_connection.cursor(dictionary = True)

cursor.execute("""
    DROP TABLE Test;
""")

cursor.execute("""
    CREATE TABLE Test(
        ime VARCHAR(255) NOT NULL
    );
""")

cursor.execute("""
    INSERT INTO Test(ime)
    VALUES ('darko');
""")




@app.route('/')
def home():
    cursor.execute("""
        SELECT * FROM Test;
    """)

    results = cursor.fetchall()

    print(results)

    return f"<h1>Zdravo, {results[0]['ime']}!</h1>"

@app.route('/about')
def about():
    return 'About'