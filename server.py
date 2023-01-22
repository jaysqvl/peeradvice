import os
import traceback

from flask import Flask, jsonify, request
from flask_cors import CORS

import dotenv
import psycopg2

dotenv.load_dotenv()

app = Flask(__name__)
CORS(app)

def get_db_connection():
    conn = psycopg2.connect(os.environ.get('DATABASE_URL'))
    return conn

# immediately when you get to this domain
@app.route('/advisor')
def getAdvisor():
    uid = request.args.get('uid', '')

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute('SELECT * FROM advisors WHERE uid = %s', (uid,))
    data = cur.fetchone()

    cur.close()
    conn.close()

    if not data:
        return 'bad request!', 400

    response = jsonify({
        "uid": data[0],
        "name": data[1],
        "degree": data[2],
        "major": data[3],
        "minor": data[4],
        "year_level": data[5],
        "calendly_link": data[6],
        "bio": data[7]
    })

    return response

@app.route('/connectAdvisors')
def getAllAdvisors():
    advisors = []

    conn = get_db_connection()
    cur = conn.cursor()


    cur.execute('SELECT * FROM advisors')
    data = cur.fetchone() or []

    cur.close()
    conn.close()

    for advisor in data:
        advisors.append(advisor)

    response = jsonify(advisors)

    return response

@app.route('/student')
def getStudent():
    uid = request.args.get('uid', '')

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute('SELECT * FROM students WHERE uid = %s', (uid,))
    data = cur.fetchone()

    cur.close()
    conn.close()

    if not data:
        return 'bad request', 400

    response = jsonify({
        "uid": data[0],
        "name": data[1],
        "degree": data[2],
        "major": data[3],
        "minor": data[4],
        "year_level": data[5],
    })

    return response

@app.route("/")
def homeRoute():
    return "Hello World!"


def main():
    return "Hello World!"

if __name__ == '__main__':
    app.run(debug=True, host = "0.0.0.0", port = 80)
