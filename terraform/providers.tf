terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }

  required_version = ">= 1.4.0"
}

provider "google" {
  project = var.project_id
  region  = var.region

  credentials = fileexists("credentials/gcs_key.json") ? file("credentials/gcs_key.json") : null
}