import os
import psycopg
import requests
from datetime import datetime
from transform import transform_weather_data

DB_CONFIG = {
    "dbname": os.getenv("DB_NAME", "postgres"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", "****"),
    "host": os.getenv("DB_HOST", "******"),
    "port": os.getenv("DB_PORT", "****")
}

API_URL = os.getenv("WEATHER_API_URL", "http://127.0.0.1:5000/weather")

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
    try:
        response = requests.get(API_URL, timeout=5)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"API bağlantı hatası: {e}")
        return

    weather_data = response.json()

    if "error" in weather_data:
        print(f"API Hatası: {weather_data['error']}")
        return

    transformed_data = transform_weather_data(weather_data)

    weather_time = transformed_data['time']
    if isinstance(weather_time, str):
        try:
            weather_time = datetime.strptime(weather_time, "%Y-%m-%dT%H:%M")
        except ValueError as e:
            print(f"Zaman formatı hatalı: {e}")
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