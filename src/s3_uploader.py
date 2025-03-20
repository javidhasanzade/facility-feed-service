import aioboto3
from src.config import settings


async def upload_file_to_s3(file_path: str, key: str):
    """
    Uploads a file to the AWS S3 bucket.

    Args:
        file_path (str): Local path to the file.
        key (str): The S3 object key (i.e., the file name in the bucket).
    """
    print(settings.AWS_ACCESS_KEY_ID)
    print(settings.AWS_SECRET_ACCESS_KEY)
    session = aioboto3.Session(
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_REGION
    )

    async with session.client("s3") as s3:
        with open(file_path, "rb") as file_data:
            await s3.put_object(
                Bucket=settings.S3_BUCKET,
                Key=key,
                Body=file_data,
                ContentType="application/json",
                ContentEncoding="gzip"
            )
        print(f"Uploaded {key} to S3 bucket {settings.S3_BUCKET}")
