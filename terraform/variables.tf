variable "project_id" {
  type        = string
  description = "Your GCP project ID"
}

variable "region" {
  type        = string
  default     = "us-central1"
}

variable "gcs_bucket_name" {
  type        = string
  description = "GCS bucket to store processed data"
}

variable "bq_dataset" {
  type        = string
  description = "BigQuery dataset name"
}