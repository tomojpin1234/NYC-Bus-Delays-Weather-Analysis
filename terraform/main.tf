# GCS bucket
resource "google_storage_bucket" "data_lake" {
  name     = var.gcs_bucket_name
  location = var.region
  force_destroy = true
  uniform_bucket_level_access = true
}

# BigQuery dataset
resource "google_bigquery_dataset" "dataset" {
  dataset_id                  = var.bq_dataset
  location                    = var.region
  delete_contents_on_destroy = true
}

# Service Account
resource "google_service_account" "de_service" {
  account_id   = "de-pipeline-service"
  display_name = "Data Engineering Pipeline Service Account"

  lifecycle {
    prevent_destroy = false
    ignore_changes = [display_name]
  }
}

# IAM Roles for the service account
resource "google_project_iam_member" "storage_access" {
  project = var.project_id
  role    = "roles/storage.admin"
  member  = "serviceAccount:${google_service_account.de_service.email}"
}

resource "google_project_iam_member" "bigquery_access" {
  project = var.project_id
  role    = "roles/bigquery.admin"
  member  = "serviceAccount:${google_service_account.de_service.email}"
}

output "service_account_email" {
  value = google_service_account.de_service.email
}