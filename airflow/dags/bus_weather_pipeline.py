from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime
import os
import sys
from datetime import timedelta

# Make local project modules importable inside Airflow
sys.path.append("/opt/airflow/scripts")  

from fetch_from_api import fetch_bus_data
from fetch_weather import fetch_weather_data
from upload_to_gcs import upload_to_gcs
from load_to_bq import load_parquet_to_bq

default_args = {
    "owner": "airflow",
    "start_date": datetime(2024, 1, 1),
    "retries": 1,
}

with DAG(
    dag_id="bus_weather_pipeline",
    default_args=default_args,
    description="ETL pipeline: Bus delays + weather → GCS + BQ",
    schedule_interval=None,
    catchup=False,
    tags=["de-zoomcamp", "bus", "weather"],
) as dag:    
    fetch_bus = PythonOperator(
        task_id="fetch_bus_data",
        python_callable=fetch_bus_data,
        retries=2,
        retry_delay=timedelta(minutes=2),
        execution_timeout=timedelta(minutes=15),  
    )

    fetch_weather = PythonOperator(
        task_id="fetch_weather_data",
        python_callable=fetch_weather_data,
    )

    process_data = BashOperator(
        task_id="process_data",
        bash_command="python ./spark_jobs/process_data.py",  
        cwd="/opt/airflow", 
    )

    upload = PythonOperator(
        task_id="upload_to_gcs",
        python_callable=upload_to_gcs,
    )

    load_to_bq = PythonOperator(
        task_id="load_to_bq",
        python_callable=load_parquet_to_bq,
    )
    
    dbt_run = BashOperator(
        task_id="run_dbt_models",
        bash_command="cd /opt/airflow/dbt && dbt run --full-refresh --profiles-dir .dbt",
    )

    dbt_test = BashOperator(
        task_id="test_dbt_models",
        bash_command="cd /opt/airflow/dbt && dbt test --profiles-dir .dbt",
    )

    # Define the task pipeline
    [fetch_bus, fetch_weather] >> process_data >> upload >> load_to_bq >> dbt_run >> dbt_test
    