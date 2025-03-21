from src.config import settings


def test_config_fields():
    # Ensure that essential configuration fields are not empty.
    assert settings.DATABASE_URL, "DATABASE_URL should not be empty"
    assert settings.AWS_REGION, "AWS_REGION should not be empty"
    assert settings.S3_BUCKET, "S3_BUCKET should not be empty"
    assert settings.CHUNK_SIZE > 0, "CHUNK_SIZE must be a positive integer"
    assert settings.FEED_NAME, "FEED_NAME should not be empty"
