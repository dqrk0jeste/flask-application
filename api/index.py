import os
from flask import Flask
import mysql.connector
from dotenv import load_dotenv

#load enviroment variables
load_dotenv()

#create app
app = Flask(__name__)

@app.route('/')
def home():
    #connect to a database, should do this in every serverless function
    #remember to close the connection before returning
    connection = connectDatabase()
    if(connection):
        cursor = createCursor(connection)
    else:
        return "there has been an error connecting to a database"

    #drop existing table
    cursor.execute("""
        DROP TABLE Test;
    """)

    #create mock table
    cursor.execute("""
        CREATE TABLE Test(
            ime VARCHAR(255) NOT NULL
        );
    """)

    #insert mock value
    cursor.execute("""
        INSERT INTO Test(ime)
        VALUES ('darko');
    """)

    #retrieve data from a database
    cursor.execute("""
        SELECT * FROM Test;
    """)

    results = cursor.fetchall()

    closeCursor(cursor)
    dissconnectDatabase(connection)

    return f"<h1>Zdravo, {results[0]['ime']}!</h1>"

@app.route('/about')
def about():
    return 'About'

#utils, I don't know how to make Vercel not pick them up as serverless functions, should probably be in the documentation.
def connectDatabase():
    try:
        connection = mysql.connector.connect(
            database =  os.environ.get('DB_NAME'),
            host = os.environ.get('DB_HOST'),
            port = os.environ.get('DB_PORT'),
            user = os.environ.get('DB_USER'),
            password = os.environ.get('DB_PASSWORD')
            #ssl_ca = os.environ.get('MYSQL_ATTR_SSL_CA') #uncomment in production to enable secured connection
        )
        print("connected to a database")
        return connection
    except:
        print("there has been an error")
        return None

def dissconnectDatabase(connection):
    connection.close()

def createCursor(connection):
    return connection.cursor(dictionary = True)

def closeCursor(cursor):
    cursor.close()