import asyncio
from src.config import settings
from src.database import fetch_facilities_in_chunks
from src.transformation import transform_records_to_json
from src.file_manager import generate_feed_file, generate_metadata_file
from src.s3_uploader import upload_file_to_s3
from src.logger import setup_logger
import os

logger = setup_logger("main")


async def main():
    logger.info("Starting service", extra={"database_url": settings.DATABASE_URL})
    feed_files = []

    try:
        # Process each chunk from the database.
        async for chunk in fetch_facilities_in_chunks():
            logger.info("Fetched a chunk", extra={"record_count": len(chunk)})
            feed_json = transform_records_to_json(chunk)
            file_name = generate_feed_file(feed_json)
            feed_files.append(file_name)
            # For demonstration, process only the first chunk.
            break

        if feed_files:
            metadata_file = generate_metadata_file(feed_files)
        else:
            logger.warning("No feed files were generated")
            return

        # Upload feed and metadata files to S3.
        for file in feed_files + [metadata_file]:
            file_path = os.path.join("output", file)
            logger.info("Uploading file to S3", extra={"file_path": file_path})
            await upload_file_to_s3(file_path, file)

    except Exception as e:
        logger.exception("An error occurred during execution", extra={"error": str(e)})


if __name__ == "__main__":
    asyncio.run(main())
