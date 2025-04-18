import requests
from flask import Flask, jsonify

app = Flask(__name__)

def get_weather():
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 39.7767,  # Eskişehir
        "longitude": 30.5206,
        "current_weather": "true"
    }

    try:
        response = requests.get(url, params=params, timeout=10)
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
    print("[INFO] Starting Flask API...")
    app.run(debug=True, use_reloader=False, port=5000)

if __name__ == '__main__':
    run_flask()
