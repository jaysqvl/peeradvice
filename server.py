import os

from flask import Flask, jsonify, request, render_template
from flask_cors import CORS

import dotenv
import psycopg2
import psycopg2.extras

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
    name = request.args.get('name', '')
    email = request.args.get('email', '')

    conn = get_db_connection()
    cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)

    cur.execute('SELECT * FROM advisors WHERE uid = %s', (uid,))
    data = cur.fetchone()

    if not data:
        cur.execute('INSERT INTO advisors (uid, name, email) VALUES (%s, %s, %s)', (uid, name, email))
        data = {
            "uid": uid,
            "name": name,
            "degree": None,
            "major": None,
            "minor": None,
            "year_level": None,
            "calendly_link": None,
            "bio": None,
            "email": email,
        }

    cur.close()
    conn.commit()
    conn.close()
    print(data)

    data = {
        "uid": data['uid'],
        "name": data['name'],
        "degree": data['degree'],
        "major": data['major'],
        "minor": data['minor'],
        "year_level": data['year_level'],
        "calendly_link": data['calendly_link'],
        "bio": data['bio'],
        "email": data['email'],
    }

    return render_template('advisor.html', data=data)

@app.route('/connectAdvisors')
def getAllAdvisors():
    advisors = []

    conn = get_db_connection()
    cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)

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
    name = request.args.get('name', '')
    email = request.args.get('email', '')

    conn = get_db_connection()
    cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)

    cur.execute('SELECT * FROM students WHERE uid = %s', (uid,))
    data = cur.fetchone()

    if not data:
        cur.execute('INSERT INTO students (uid, name, email) VALUES (%s, %s, %s)', (uid, name, email))
        data = {
            "uid": uid,
            "name": name,
            "degree": None,
            "major": None,
            "minor": None,
            "year_level": None,
            "email": email,
        }

    cur.close()
    conn.commit()
    conn.close()

    data = {
        "uid": data['uid'],
        "name": data['name'],
        "degree": data['degree'],
        "major": data['major'],
        "minor": data['minor'],
        "year_level": data['year_level'],
        "email": data['email'],
    }


    return render_template('student.html', data=data)

@app.route('/connectAdvisor')
def connectAdvisor():
    return render_template('connectAdvisor.html')

@app.route('/connectStudent')
def connectStudent():
    return render_template('connectStudent.html')

@app.route('/appointmentStudent')
def appointmentStudent():
    return render_template('appointmentStudent.html')


@app.route("/")
def home():
    return render_template('index.html')


def main():
    return "Hello World!"

if __name__ == '__main__':
    app.run(debug=True, host = "0.0.0.0", port = 80)
