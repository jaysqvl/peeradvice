import os

from flask import Flask, request, render_template, redirect
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

    return render_template('advisor.html', data=data)

@app.route('/editadvisor', methods=['POST'])
def modifyAdvisorDBEntry():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""UPDATE advisors SET name = %s, degree = %s, major = %s, minor = %s, 
                year_level = %s, calendly_link = %s, bio = %s, email = %s WHERE uid = %s""", 
                (request.form.get("name"), request.form.get("degree"), request.form.get("major"), 
                request.form.get("minor"), request.form.get("year_level", type=int), request.form.get("calendly_link"), 
                request.form.get("bio"), request.form.get("email"), request.form.get("uid")))

    cur.close()
    conn.commit()
    conn.close()

    return redirect(f'/advisor?uid={request.form.get("uid")}&name={request.form.get("name")}&email={request.form.get("email")}')

@app.route('/editstudent', methods=['POST'])
def modifyStudentDBEntry():
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("""UPDATE students SET name = %s, degree = %s, major = %s, minor = %s, 
                year_level = %s, email = %s WHERE uid = %s""", 
                (request.form.get("name"), request.form.get("degree"), request.form.get("major"),
                request.form.get("minor"), request.form.get("year_level", type=int),
                request.form.get("email"), request.form.get("uid")))

    cur.close()
    conn.commit()
    conn.close()

    return redirect(f'/student?uid={request.form.get("uid")}&name={request.form.get("name")}&email={request.form.get("email")}')

def getAllAdvisors():
    advisors = []

    conn = get_db_connection()
    cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)

    cur.execute('SELECT * FROM advisors')
    data = cur.fetchall() or []

    cur.close()
    conn.close()

    for advisor in data:
        advisors.append(advisor)

    return advisors

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

    return render_template('student.html', data=data)

@app.route('/connectAdvisor')
def connectAdvisor():
    return render_template('connectAdvisor.html')

@app.route('/connectStudent')
def connectStudent():
    advisors = getAllAdvisors()
    return render_template('connectStudent.html', advisors=advisors)

@app.route('/appointmentStudent')
def appointmentStudent():
    return render_template('appointmentStudent.html')

@app.route("/")
def home():
    return render_template('index.html')

def main():
    return "Hello World!"

if __name__ == '__main__':
    app.run(debug=True, host = "0.0.0.0", port = 8080)
