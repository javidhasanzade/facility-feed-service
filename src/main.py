import asyncio
import os
from src.config import settings
from src.database import fetch_facilities_in_chunks
from src.feeds.factory import get_transformer
from src.file_manager import generate_feed_file, generate_metadata_file
from src.s3_uploader import upload_file_to_s3
from src.logger import setup_logger

logger = setup_logger("main")


async def main():
    logger.info("Starting feed generation",
                extra={"feed_name": settings.FEED_NAME})

    # Get the appropriate transformer using the strategy pattern
    try:
        transformer = get_transformer(settings.FEED_NAME)
    except ValueError as e:
        logger.error("Unsupported feed type",
                     extra={"error": str(e)})
        return

    feed_files = []

    try:
        async for chunk in fetch_facilities_in_chunks():
            logger.info("Fetched records chunk",
                        extra={"record_count": len(chunk)})
            feed_json = transformer.transform(chunk)
            file_name = generate_feed_file(feed_json)
            feed_files.append(file_name)

        if not feed_files:
            logger.warning("No feed files generated")
            return

        metadata_file = generate_metadata_file(feed_files)
        all_files = feed_files + [metadata_file]

        for file_name in all_files:
            file_path = os.path.join("output", file_name)
            logger.info("Uploading file to S3",
                        extra={"file": file_name})
            await upload_file_to_s3(file_path, file_name)

        logger.info("Feed generation completed successfully")

    except Exception as e:
        logger.exception("Unhandled error occurred",
                         extra={"error": str(e)})


if __name__ == "__main__":
    asyncio.run(main())
