PROJECT_NAME=airflow
DAG_ID=bus_weather_pipeline
COMPOSE = $(shell command -v docker-compose >/dev/null 2>&1 && echo docker-compose || echo docker compose)

.PHONY: init up down restart rebuild logs trigger list-dags dag-state dag-test bash scheduler-restart webserver-restart

init:
	mkdir -p logs
	mkdir -p plugins	
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
	$(COMPOSE) up -d

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