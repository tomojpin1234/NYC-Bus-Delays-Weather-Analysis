from google.cloud import bigquery

PROJECT_ID = "de-zoomcamp-pipeline-2025"
DATASET_ID = "bus_data"
TABLE_ID = "stg_bus_weather"
BUCKET_NAME = "de2025-ps-ny-bus-data"
GCS_PATH = f"gs://{BUCKET_NAME}/data/bus_weather_joined/*.parquet"

def load_parquet_to_bq():
    client = bigquery.Client(project=PROJECT_ID)

    table_ref = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}"

    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.PARQUET,
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
        autodetect=True,
    )

    print(f"📥 Loading from: {GCS_PATH}")
    print(f"➡️ Into table: {table_ref}")

    load_job = client.load_table_from_uri(
        GCS_PATH,
        table_ref,
        job_config=job_config
    )

    load_job.result()  # Wait for job to complete

    print(f"✅ Loaded {load_job.output_rows} rows into {table_ref}")

if __name__ == "__main__":
    load_parquet_to_bq()