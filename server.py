import os
import traceback

from flask import Flask, jsonify, request
from model import calc, scrape
from flask_cors import CORS

import dotenv
import psycopg2

dotenv.load_dotenv()

app = Flask(__name__)
CORS(app)

def get_db_connection():
    conn = psycopg2.connect(os.environ('DATABASE_URL'))
    return conn


# immediately when you get to this domain
@app.route('/advisor')
def getAdvisor():
    uid = request.args.get('uid', '')

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute('SELECT * FROM advisors WHERE uid = %s', uid)
    try:
        data = cur.fetchone()
    except:
        # error
        pass

    cur.close()
    conn.close()

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
    try:
        data = cur.fetchall()
    except:
        # error
        pass

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

    cur.execute('SELECT * FROM students WHERE uid = %s', uid)
    try:
        data = cur.fetchone()
    except:
        # error
        pass

    cur.close()
    conn.close()

    response = jsonify({
        "uid": data[0],
        "name": data[1],
        "degree": data[2],
        "major": data[3],
        "minor": data[4],
        "year_level": data[5],
    })

    return response

@app.route('/submit')
def getCalc():
    try:
        calc_brand = request.args.get('brand')
        print(calc_brand)
        calc_cloth_type = request.args.get('cloth_type')
        print(calc_cloth_type)
        calc_material_one = request.args.get('materialone')
        print(calc_material_one)
        calc_material_two = request.args.get('materialtwo')
        print(calc_material_two)
        calc_num_washes = request.args.get('num_washes')
        print(calc_num_washes)

        calc_weight = request.args.get('weight')
        print(calc_weight)

        calc_data = calc.start_calc(calc_brand, calc_cloth_type, calc_material_one, calc_material_two, calc_num_washes, calc_weight)
        print(calc_data)

    except:
        print("Error processing, check data submitted")
        return "Error processing, check data submitted"

    response = jsonify({
        "sustainability_rating": calc_data[0],
        "fabric_quality": calc_data[1],
        "num_washes": calc_data[2],
    })
    return response

@app.route("/")
def homeRoute():
    return "Hello World!"


def main():
    return "Hello World!"

if __name__ == '__main__':
    app.run(debug=True, host = "0.0.0.0", port = 80)