# terraform/Makefile

GOOGLE_CREDENTIALS := ../credentials/gcs_key.json

export GOOGLE_APPLICATION_CREDENTIALS := $(GOOGLE_CREDENTIALS)

init:
	terraform init

plan:
	terraform plan

apply:
	terraform apply -auto-approve

destroy:
	terraform destroy -auto-approve