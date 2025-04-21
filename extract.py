import os
import requests
from flask import Flask, jsonify

app = Flask(__name__)

API_URL = os.getenv("WEATHER_API_URL", "https://api.open-meteo.com/v1/forecast")
LATITUDE = float(os.getenv("LATITUDE", 39.7767))  # Eskişehir
LONGITUDE = float(os.getenv("LONGITUDE", 30.5206))
FLASK_PORT = int(os.getenv("FLASK_PORT", 5000))

def get_weather():
    params = {
        "latitude": LATITUDE,
        "longitude": LONGITUDE,
        "current_weather": "true"
    }

    try:
        response = requests.get(API_URL, params=params, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed: {e}"}

    data = response.json()
    if 'current_weather' in data:
        weather_data = {
            "time": data['current_weather'].get('time'),
            "temperature": data['current_weather'].get('temperature'),
            "wind_speed": data['current_weather'].get('windspeed')
        }
        return weather_data
    else:
        return {"error": "Invalid API response structure"}

@app.route('/weather', methods=['GET'])
def weather_api():
    return jsonify(get_weather())

def run_flask():
    print(f"[INFO] Starting Flask API on port {FLASK_PORT}...")
    app.run(debug=True, use_reloader=False, port=FLASK_PORT)

if __name__ == '__main__':
    run_flask()