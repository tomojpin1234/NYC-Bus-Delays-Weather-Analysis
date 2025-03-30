# Makefile for dbt project

GOOGLE_APPLICATION_CREDENTIALS := ../credentials/gcs_key.json
DBT_PROFILES_DIR := .dbt

# Run all dbt commands with proper env context
DBT_RUN         = GOOGLE_APPLICATION_CREDENTIALS=$(GOOGLE_APPLICATION_CREDENTIALS) poetry run dbt run --profiles-dir $(DBT_PROFILES_DIR)
DBT_RUN_FULL    = GOOGLE_APPLICATION_CREDENTIALS=$(GOOGLE_APPLICATION_CREDENTIALS) poetry run dbt run --full-refresh --profiles-dir $(DBT_PROFILES_DIR)
DBT_TEST        = GOOGLE_APPLICATION_CREDENTIALS=$(GOOGLE_APPLICATION_CREDENTIALS) poetry run dbt test --profiles-dir $(DBT_PROFILES_DIR)
DBT_DOCS_GEN    = GOOGLE_APPLICATION_CREDENTIALS=$(GOOGLE_APPLICATION_CREDENTIALS) poetry run dbt docs generate --profiles-dir $(DBT_PROFILES_DIR)
DBT_DOCS_SERVE  = GOOGLE_APPLICATION_CREDENTIALS=$(GOOGLE_APPLICATION_CREDENTIALS) poetry run dbt docs serve --profiles-dir $(DBT_PROFILES_DIR)
DBT_DEBUG       = GOOGLE_APPLICATION_CREDENTIALS=$(GOOGLE_APPLICATION_CREDENTIALS) poetry run dbt debug --profiles-dir $(DBT_PROFILES_DIR)

# Default target
all: run

debug:
	$(DBT_DEBUG)

run:
	$(DBT_RUN)

run-full:
	$(DBT_RUN_FULL)

test:
	$(DBT_TEST)

docs:
	$(DBT_DOCS_GEN)
	$(DBT_DOCS_SERVE)

clean:
	rm -rf target