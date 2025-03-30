from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_date, year, month

# Paths
BUS_CSV = "data/raw/bus_breakdowns_cleaned.csv"
WEATHER_CSV = "data/weather/weather_nyc.csv"
OUTPUT_PATH = "data/processed/bus_weather_joined/"

def main():     
    spark = SparkSession.builder \
        .appName("BusDelaysWeatherJoin") \
        .config("spark.driver.memory", "1g") \
        .config("spark.executor.memory", "1g") \
        .config("spark.sql.legacy.timeParserPolicy", "LEGACY") \
        .getOrCreate()

    # Load and prepare bus breakdowns
    print("🚍 Reading bus breakdown data...")
    bus_df = spark.read.csv(BUS_CSV, header=True, inferSchema=True)
    bus_df = bus_df.withColumn("date", to_date(col("Occurred_On"), "MM/dd/yyyy"))

    # Load and prepare weather data
    print("🌦️  Reading weather data...")
    weather_df = spark.read.csv(WEATHER_CSV, header=True, inferSchema=True)
    weather_df = weather_df.withColumn("date", to_date(col("date")))

    # Join on cleaned date
    print("🔗 Joining on date...")
    joined_df = bus_df.join(weather_df, on="date", how="left")

    # Add partition columns
    joined_df = joined_df.withColumn("year", year(col("date"))) \
                         .withColumn("month", month(col("date")))

    # Select relevant fields
    selected = joined_df.select(
        "date", "Boro", "Bus_Company_Name", "Reason", "How_Long_Delayed",
        "Number_Of_Students_On_The_Bus", "temperature_2m_max", "temperature_2m_min",
        "precipitation_sum", "windspeed_10m_max", "year", "month"
    )

    # Write to partitioned Parquet
    print("💾 Saving joined dataset to Parquet...")
    selected.write.mode("overwrite") \
        .partitionBy("year", "month") \
        .parquet(OUTPUT_PATH)

    print(f"✅ Done! Output saved to: {OUTPUT_PATH}")

if __name__ == "__main__":
    main()