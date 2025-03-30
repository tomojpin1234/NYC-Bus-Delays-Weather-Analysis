import requests
import pandas as pd
from tqdm import tqdm
import os 
import time

URL = "https://data.cityofnewyork.us/api/views/ez4e-fazm/rows.csv?accessType=DOWNLOAD"
RAW_FILE = "data/raw/bus_breakdowns.csv"

def download_with_progress(url, output_path):
    print("⬇️ Starting download...")

    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    block_size = 1024  # 1 KiB

    with open(output_path, 'wb') as file, tqdm(
        desc="📥 Downloading",
        total=total_size,
        unit='iB',
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        downloaded = 0
        print_every_mb = 5 * 1024 * 1024  # 5 MB
        last_logged = 0

        for data in response.iter_content(block_size):
            file.write(data)
            bar.update(len(data))
            downloaded += len(data)
            
            if downloaded - last_logged >= print_every_mb:
                print(f"🫀 Downloaded {(downloaded / (1024 * 1024)):.1f} MB so far...")
                last_logged = downloaded

    print(f"✅ Download completed: {output_path}")

def fetch_bus_data():
    print("🚍 [START] Fetching bus breakdown data...")

    os.makedirs("data/raw", exist_ok=True)
    print("📁 Ensured data/raw/ directory exists.")

    # Write heartbeat every 5s during download
    print("🌐 Starting download...")
    for i in range(5):
        print(f"🫀 Heartbeat {i+1}/5 before download")
        time.sleep(1)

    download_with_progress(URL, RAW_FILE)
    print("📊 Reading and saving CSV in chunks...")

    input_path = RAW_FILE
    output_path = "data/raw/bus_breakdowns_cleaned.csv"

    chunk_size = 100_000
    rows_total = 0

    # Clear or create new output file
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        pass

    for i, chunk in enumerate(pd.read_csv(input_path, chunksize=chunk_size, low_memory=True)):
        rows_total += len(chunk)
        print(f"🧩 Processed chunk {i + 1}: {len(chunk)} rows (total: {rows_total})")

        # Write to cleaned output
        chunk.to_csv(output_path, mode='a', index=False, header=(i == 0))

    print(f"✅ Cleaned CSV saved to: {output_path}")
    print(f"🧮 Total rows written: {rows_total}")

if __name__ == "__main__":
    fetch_bus_data()