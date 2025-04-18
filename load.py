import psycopg
import requests
from datetime import datetime
from transform import transform_weather_data

DB_CONFIG = {
    "dbname": "postgres",
    "user": "postgres",
    "password": "7991",
    "host": "localhost",
    "port": "5432"
}

def init_db():
    with psycopg.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS weather_data (
                    time TIMESTAMP PRIMARY KEY,
                    temperature FLOAT,
                    wind_speed FLOAT,
                    warning TEXT
                )
            """)
            conn.commit()

def save_weather_from_api():
    url = "http://127.0.0.1:5000/weather"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
    except Exception as e:
        print("API bağlantı hatası:", e)
        return

    weather_data = response.json()

    if "error" in weather_data:
        print("API Hatası:", weather_data["error"])
        return

    transformed_data = transform_weather_data(weather_data)

    try:
        weather_time = datetime.strptime(transformed_data['time'], "%Y-%m-%dT%H:%M")
    except Exception as e:
        print("Zaman formatı hatalı:", e)
        return

    with psycopg.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO weather_data (time, temperature, wind_speed, warning)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (time) DO UPDATE SET
                    temperature = EXCLUDED.temperature,
                    wind_speed = EXCLUDED.wind_speed,
                    warning = EXCLUDED.warning
            """, (
                weather_time,
                transformed_data['temperature'],
                transformed_data['wind_speed'],
                transformed_data.get('warning')
            ))
            conn.commit()
    print("Veri başarıyla kaydedildi:", transformed_data)
