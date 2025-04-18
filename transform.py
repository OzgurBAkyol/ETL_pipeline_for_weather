from datetime import datetime


def transform_weather_data(data):
    if "error" in data:
        return data

    transformed = {}

    try:
        transformed["time"] = datetime.strptime(data["time"], "%Y-%m-%dT%H:%M")

        transformed["temperature"] = float(data["temperature"]) # float
        transformed["wind_speed"] = float(data["wind_speed"])

        wind = transformed["wind_speed"]
        if wind < 5:
            transformed["wind_category"] = "light"
        elif wind < 15:
            transformed["wind_category"] = "moderate"
        else:
            transformed["wind_category"] = "strong"

    except Exception as e:
        return {"error": f"Transform error: {e}"}

    return transformed
