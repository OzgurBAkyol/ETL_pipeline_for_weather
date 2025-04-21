import os
import multiprocessing
import time
import requests
from extract import run_flask
from load import save_weather_from_api

API_URL = os.getenv("WEATHER_API_URL", "http://127.0.0.1:5000/weather")
FLASK_STARTUP_DELAY = int(os.getenv("FLASK_STARTUP_DELAY", 5))

def check_api():
    try:
        response = requests.get(API_URL)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

if __name__ == "__main__":
    flask_process = multiprocessing.Process(target=run_flask)
    flask_process.start()

    print("[INFO] Flask API başlatılıyor...")
    time.sleep(FLASK_STARTUP_DELAY)

    if not check_api():
        print(f"[ERROR] Flask API {API_URL} başlatılamadı.")
        flask_process.terminate()
        exit()

    print("[INFO] API çalışıyor. Veri çekiliyor ve kaydediliyor...")
    save_weather_from_api()

    flask_process.terminate()