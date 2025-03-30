# 🌍 GCP Setup Instructions

This project can be reproduced in any GCP account. Below are **two options** to set up the required GCP infrastructure.

---

## 📌 Prerequisites

Before you begin, make sure:

- You have a **GCP account**
- Billing is enabled
- You have the [Google Cloud CLI](https://cloud.google.com/sdk/docs/install) installed
- You are authenticated:
  ```bash
  gcloud auth login
  gcloud auth application-default login
  ```

# Option 1: Manual Setup in GCP UI

1. Create a new project

    - Go to https://console.cloud.google.com/projectcreate

    - Use a name like de-zoomcamp-pipeline-2025

2. Enable APIs Enable these APIs for the project:

    - IAM API

    - Cloud Resource Manager

    - BigQuery API

    - Cloud Storage API
    
    Enable APIs here - https://console.cloud.google.com/apis/library        

3. Create a service account

    - Name: de-pipeline-service

    - Role: Assign these roles:

        - BigQuery Admin

        - Storage Admin

        - Service Account Admin

        - Project IAM Admin

4. Generate and download service account key

    - Go to: IAM & Admin → Service Accounts

    - Click your service account → Keys → Add Key → JSON

    - Save it as: credentials/gcs_key.json

5. Create a Cloud Storage bucket

    - Name: de2025-ps-ny-bus-data

    - Location: us-central1 (or match your config)

    - Storage class: Standard

6. Create a BigQuery dataset

    - Name: bus_data

    - Location: us-central1 (or match your config)

# Option 2: GCP Setup via gcloud CLI

```bash
### Set your project ID
export PROJECT_ID=de-zoomcamp-pipeline-2025

# Create the project (if not already created manually)
gcloud projects create $PROJECT_ID --name="DE Zoomcamp 2025"

# Set project and billing
gcloud config set project $PROJECT_ID
gcloud beta billing projects link $PROJECT_ID --billing-account=YOUR_BILLING_ACCOUNT_ID

# Enable required APIs
gcloud services enable iam.googleapis.com \
    cloudresourcemanager.googleapis.com \
    bigquery.googleapis.com \
    storage.googleapis.com

# Create the service account
gcloud iam service-accounts create de-pipeline-service \
    --description="Service account for DE pipeline" \
    --display-name="DE Pipeline Service"

# Assign IAM roles
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:de-pipeline-service@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/bigquery.admin"

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:de-pipeline-service@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/storage.admin"

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:de-pipeline-service@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/resourcemanager.projectIamAdmin"

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:de-pipeline-service@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/iam.serviceAccountAdmin"

# Create and download key
gcloud iam service-accounts keys create credentials/gcs_key.json \
    --iam-account="de-pipeline-service@$PROJECT_ID.iam.gserviceaccount.com"

# Create GCS bucket
gsutil mb -l us-central1 -p $PROJECT_ID gs://de2025-ps-ny-bus-data/

# Create BigQuery dataset
bq --location=us-central1 mk --dataset $PROJECT_ID:bus_data
```

✅ Final Step: Verify Setup

Make sure:

- The service account key is placed in credentials/gcs_key.json

- Billing is properly enabled

- Dataset and bucket are in the correct region (us-central1)

- Once the GCP is set up and keys are downloaded, you can run:
```bash
export GOOGLE_APPLICATION_CREDENTIALS=./credentials/gcs_key.json
```