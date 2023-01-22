import traceback
from flask import Flask, jsonify, request
from model import calc, scrape
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

class Calc():
    BLAH = "test"

class Scraped():
    BLAHH = "test"

# immediately when you get to this domain
@app.route('/webscrape')
def getScrape():
    try:
        print("inside /webscrape")
        url_to_scrape = request.args.get('url')
        print("grabbed url_to_scrape", url_to_scrape)
        data = scrape.start_scrape(url_to_scrape)
        print("got data", data)
    except:
        traceback.print_exc()
        print("Error processing, are you sure this is a valid url?")
        return "Error processing, are you sure this is a valid url?"
    
    response = jsonify({
        "cloth_type": data[0],
        "brand": data[1],
        "materials": data[2],
        "num_washes": data[3],
        "weight_grams": data[4]
    })

    response.headers.add('Access-Control-Allow-Origin', '*')
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

    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route("/")
def homeRoute():
    return "Hello World!"


def main():
    return "Hello World!"

if __name__ == '__main__':
    app.run(debug=True, host = "0.0.0.0", port = 80)