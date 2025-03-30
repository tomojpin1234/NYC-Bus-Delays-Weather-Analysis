import requests
import pandas as pd
from datetime import datetime, timedelta
import os

# NYC coordinates
LAT = 40.7128
LON = -74.0060

# Date range (can be changed later)
START_DATE = "2023-01-01"
END_DATE = datetime.today().date()

# Output path
OUTPUT_DIR = "data/weather/"
OUTPUT_FILE = OUTPUT_DIR + "weather_nyc.csv"

def fetch_weather_data():
    print("🌦️  Fetching historical weather data for NYC...")

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("📁 Ensured data/raw/ directory exists.")

    url = (
        f"https://archive-api.open-meteo.com/v1/archive?"
        f"latitude={LAT}&longitude={LON}"
        f"&start_date={START_DATE}&end_date={END_DATE}"
        f"&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,windspeed_10m_max"
        f"&timezone=America%2FNew_York"
    )

    response = requests.get(url)
    response.raise_for_status()

    data = response.json()

    df = pd.DataFrame(data["daily"])
    df.rename(columns={"time": "date"}, inplace=True)
    df["date"] = pd.to_datetime(df["date"])

    df.to_csv(OUTPUT_FILE, index=False)
    print(f"✅ Weather data saved to: {OUTPUT_FILE}")

if __name__ == "__main__":
    fetch_weather_data()