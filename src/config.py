from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # Database configuration
    DATABASE_URL: str = "postgres://user:password@localhost:5432/mydb"

    # AWS S3 configuration
    AWS_REGION: str = "eu-central-1"
    S3_BUCKET: str = "reservewithgoogle-entity-dev-usw2"

    # AWS credentials (for local testing; production should use IAM roles)
    AWS_ACCESS_KEY_ID: str = ""
    AWS_SECRET_ACCESS_KEY: str = ""

    # Processing configuration
    CHUNK_SIZE: int = 100

    # Feed specific settings
    FEED_NAME: str = "reservewithgoogle.entity"


settings = Settings()
