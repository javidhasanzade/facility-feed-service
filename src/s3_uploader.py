import aioboto3
from src.config import settings
from src.logger import setup_logger

logger = setup_logger("s3_uploader")

async def upload_file_to_s3(file_path: str, key: str):
    """
    Uploads a file to AWS S3.
    """
    session = aioboto3.Session(
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_REGION
    )
    try:
        async with session.client("s3") as s3:
            with open(file_path, "rb") as file_data:
                await s3.put_object(
                    Bucket=settings.S3_BUCKET,
                    Key=key,
                    Body=file_data,
                    ContentType="application/json",
                    ContentEncoding="gzip"
                )
        logger.info("Uploaded file to S3", extra={"file_path": file_path, "key": key})
    except Exception as e:
        logger.exception("Error uploading file to S3", extra={"file_path": file_path, "error": str(e)})
        raise
