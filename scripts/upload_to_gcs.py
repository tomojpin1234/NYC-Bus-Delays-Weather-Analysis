import os
from google.cloud import storage

BUCKET_NAME = "de2025-ps-ny-bus-data"
SOURCE_FOLDER = "data/processed/bus_weather_joined"
DESTINATION_PREFIX = "data/bus_weather_joined"

def upload_to_gcs(bucket_name=BUCKET_NAME, source_folder=SOURCE_FOLDER, destination_prefix=DESTINATION_PREFIX):
    client = storage.Client()
    bucket = client.bucket(bucket_name)

    for root, _, files in os.walk(source_folder):
        for file in files:
            local_path = os.path.join(root, file)
            rel_path = os.path.relpath(local_path, source_folder)
            blob_path = os.path.join(destination_prefix, rel_path).replace("\\", "/")

            blob = bucket.blob(blob_path)
            blob.upload_from_filename(local_path)

            print(f"✅ Uploaded: {blob_path}")

if __name__ == "__main__":
    print("☁️  Uploading local files to GCS...")
    upload_to_gcs(BUCKET_NAME, SOURCE_FOLDER, DESTINATION_PREFIX)
    print("✅ Upload complete.")