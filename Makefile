# Project Makefile for Bus Delays Data Pipeline
include .env
export

.PHONY: airflow-init airflow-up airflow-down airflow-rebuild airflow-logs airflow-trigger \
        fetch-bus fetch-weather spark-process upload-gcs load-bq run-all-scripts \
        dbt-run dbt-run-full dbt-test dbt-debug dbt-docs tf-init tf-apply tf-destroy \
        clean help


# ------------------------
# 🧪 Python Data Scripts
# ------------------------

fetch-bus:
	poetry run python scripts/fetch_from_api.py

fetch-weather:
	poetry run python scripts/fetch_weather.py

spark-process:
	poetry run python spark_jobs/process_data.py

upload-gcs:
	poetry run python scripts/upload_to_gcs.py

load-bq:
	poetry run python scripts/load_to_bq.py

run-all-scripts: fetch-bus fetch-weather spark-process upload-gcs load-bq		

# ------------------
# 🧱 DBT Commands
# ------------------

DBT_DIR = ./bus_weather_dbt

dbt-run:
	cd $(DBT_DIR) && make run

dbt-run-full:
	cd $(DBT_DIR) && make run-full

dbt-test:
	cd $(DBT_DIR) && make test

dbt-debug:
	cd $(DBT_DIR) && make debug

# ------------------
# 🌀 Airflow Commands
# ------------------

AIRFLOW_DIR = airflow

airflow-init:
	cd $(AIRFLOW_DIR) && make init

airflow-up:
	cd $(AIRFLOW_DIR) && make up

airflow-down:
	cd $(AIRFLOW_DIR) && make down

airflow-restart:
	cd $(AIRFLOW_DIR) && make restart

airflow-rebuild:
	cd $(AIRFLOW_DIR) && make rebuild

airflow-logs:
	cd $(AIRFLOW_DIR) && make logs

airflow-trigger:
	cd $(AIRFLOW_DIR) && make trigger

airflow-list-dags:
	cd $(AIRFLOW_DIR) && make list-dags

airflow-dag-state:
	cd $(AIRFLOW_DIR) && make dag-state

airflow-dag-test:
	cd $(AIRFLOW_DIR) && make dag-test

airflow-bash:
	cd $(AIRFLOW_DIR) && make bash

airflow-scheduler-restart:
	cd $(AIRFLOW_DIR) && make scheduler-restart

airflow-webserver-restart:
	cd $(AIRFLOW_DIR) && make webserver-restart

# ------------------
# ☁️ Terraform (optional)
# ------------------

tf-init:
	$(MAKE) -C terraform init

tf-plan:
	$(MAKE) -C terraform plan

tf-apply:
	$(MAKE) -C terraform apply

tf-destroy:
	$(MAKE) -C terraform destroy

# ------------------
# 🧼 Notebook helpers
# ------------------

start_jupyter:
	poetry install --with test && poetry run python -m ipykernel install --user --name=data-engienering-zoomcamp-project --display-name "Data-Engieneering-Zoomcamp-Project1"

# ------------------
# 🧹Utility
# ------------------

clean:
	# rm -rf logs/*
	# rm -rf $(AIRFLOW_DIR)/logs/*
	# rm -rf $(DBT_DIR)/target $(DBT_DIR)/dbt_packages
	rm -rf data/*

setup:
	poetry install

help:
	@echo "Common Make targets:"
	@echo ""
	@echo " Airflow:"
	@echo "  make airflow-init              # Initialize Airflow metadata DB"
	@echo "  make airflow-up                # Start Airflow containers"
	@echo "  make airflow-down              # Stop Airflow containers"
	@echo "  make airflow-restart           # Restart Airflow containers"
	@echo "  make airflow-rebuild           # Rebuild Airflow containers"
	@echo "  make airflow-logs              # View Airflow logs"
	@echo "  make airflow-trigger           # Trigger DAG manually"
	@echo "  make airflow-list-dags         # List all Airflow DAGs"
	@echo "  make airflow-dag-state         # Get the state of a specific DAG"
	@echo "  make airflow-dag-test          # Test a specific DAG"
	@echo "  make airflow-bash              # Open a bash shell in Airflow container"
	@echo "  make airflow-scheduler-restart # Restart the Airflow scheduler"
	@echo "  make airflow-webserver-restart # Restart the Airflow webserver"
	@echo ""
	@echo " DBT:"
	@echo "  make dbt-run                   # Run DBT models"
	@echo "  make dbt-run-full              # Run DBT models with --full-refresh"
	@echo "  make dbt-test                  # Run DBT tests"
	@echo "  make dbt-debug                 # Debug DBT setup"
	@echo "  make dbt-docs                  # Generate DBT documentation"
	@echo ""
	@echo " Python ETL scripts:"
	@echo "  make fetch-bus                 # Fetch bus data from API"
	@echo "  make fetch-weather             # Fetch weather data from API"
	@echo "  make spark-process             # Run Spark transformation"
	@echo "  make upload-gcs                # Upload data to Google Cloud Storage"
	@echo "  make load-bq                   # Load data into BigQuery"
	@echo "  make run-all-scripts           # Run entire data flow manually"
	@echo ""
	@echo " Terraform:"
	@echo "  make tf-init                   # Initialize Terraform"
	@echo "  make tf-plan                   # Plan Terraform changes"
	@echo "  make tf-apply                  # Apply Terraform infra"
	@echo "  make tf-destroy                # Destroy Terraform infra"
	@echo ""
	@echo " Misc:"
	@echo "  make start_jupyter             # Start Jupyter Notebook"
	@echo "  make clean                     # Remove logs and dbt target"
	@echo "  make setup                     # Install dependencies using Poetry"