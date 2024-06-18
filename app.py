from flask import Flask, jsonify, render_template
import requests

app = Flask(__name__)

API_URL = 'https://restcountries.com/v3.1/all'

EUROPEAN_COUNTRIES = [
    'AT', 'BE', 'BG', 'HR', 'CY', 'CZ', 'DK', 'EE', 'FI', 'FR', 'DE', 'GR', 'HU', 'IS', 'IE', 'IT',
    'LV', 'LT', 'LU', 'MT', 'NL', 'NO', 'PL', 'PT', 'RO', 'SK', 'SI', 'ES', 'SE', 'CH', 'GB'
]

def get_country_data():
    response = requests.get(API_URL)
    if response.status_code == 200:
        return response.json()
    else:
        return []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/currencies')
def get_currencies():
    countries = get_country_data()
    currencies = {}
    for country in countries:
        if country['cca2'] in EUROPEAN_COUNTRIES:
            currencies[country['cca2']] = {
                'name': country['name']['common'],
                'currency': list(country['currencies'].values())[0]['name'] if 'currencies' in country else 'No currency data',
                'latlng': country['latlng'] if 'latlng' in country else [0, 0]
            }
    return jsonify(currencies)

@app.route('/languages')
def get_languages():
    countries = get_country_data()
    languages = []
    for country in countries:
        if country['cca2'] in EUROPEAN_COUNTRIES:
            languages.append({
                'name': country['name']['common'],
                'languages': list(country.get('languages', {}).values()),
                'latlng': country['latlng'] if 'latlng' in country else [0, 0]
            })
    return jsonify(languages)

if __name__ == '__main__':
    app.run(debug=True)
