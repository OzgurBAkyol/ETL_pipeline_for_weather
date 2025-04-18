import multiprocessing
import time
from extract_api import run_flask
from load import save_weather_from_api
import requests

def check_api():
    test_url = "http://127.0.0.1:5000/weather"
    try:
        response = requests.get(test_url)
        return response.status_code == 200
    except Exception:
        return False

if __name__ == "__main__":
    flask_process = multiprocessing.Process(target=run_flask)
    flask_process.start()

    print("[INFO] Flask API başlatılıyor...")
    time.sleep(5)

    if not check_api():
        print("[ERROR] Flask API başlatılamadı.")
        flask_process.terminate()
        exit()

    print("[INFO] API çalışıyor. Veri çekiliyor ve kaydediliyor...")
    save_weather_from_api()

    flask_process.terminate()