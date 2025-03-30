PROJECT_NAME=airflow
DAG_ID=bus_weather_pipeline
COMPOSE=docker compose

init:
	$(COMPOSE) down -v
	$(COMPOSE) build
	$(COMPOSE) up airflow-init

up:
	$(COMPOSE) up -d

down:
	$(COMPOSE) down

restart:
	$(COMPOSE) down
	$(COMPOSE) up -d

rebuild:
	$(COMPOSE) down -v
	$(COMPOSE) build
	$(COMPOSE) up airflow-init
	$(COMPOSE) up 

logs:
	$(COMPOSE) logs -f

trigger:
	$(COMPOSE) exec airflow-webserver airflow dags trigger $(DAG_ID)

list-dags:
	$(COMPOSE) exec airflow-webserver airflow dags list

dag-state:
	$(COMPOSE) exec airflow-webserver airflow dags state $(DAG_ID) latest

dag-test:
	$(COMPOSE) exec airflow-webserver airflow dags test $(DAG_ID) 2024-01-01

bash:
	$(COMPOSE) exec airflow-webserver bash

scheduler-restart:
	$(COMPOSE) restart airflow-scheduler

webserver-restart:
	$(COMPOSE) restart airflow-webserver