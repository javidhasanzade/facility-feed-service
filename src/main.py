import asyncio
from src.database import fetch_facilities_in_chunks
from src.transformation import transform_records_to_json
from src.file_manager import generate_feed_file, generate_metadata_file
from src.s3_uploader import upload_file_to_s3
import os

async def main():
    print("Starting service...")
    feed_files = []

    # Process each chunk from the database.
    async for chunk in fetch_facilities_in_chunks():
        print(f"Fetched a chunk with {len(chunk)} records.")
        feed_json = transform_records_to_json(chunk)
        file_name = generate_feed_file(feed_json)
        feed_files.append(file_name)
        # For now, process only the first chunk for demonstration.
        break

    # Generate metadata file if feed files exist.
    if feed_files:
        metadata_file = generate_metadata_file(feed_files)
    else:
        print("No feed files were generated.")
        return

    # Upload generated feed files to S3.
    for file in feed_files + [metadata_file]:
        file_path = os.path.join("output", file)
        print(f"Uploading {file_path} to S3...")
        await upload_file_to_s3(file_path, file)

if __name__ == "__main__":
    asyncio.run(main())
