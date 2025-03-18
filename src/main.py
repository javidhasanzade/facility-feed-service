import asyncio
from src.config import settings
from src.database import fetch_facilities_in_chunks

async def main():
    print("Starting service with the following configuration:")
    print(f"Database URL: {settings.DATABASE_URL}")
    print(f"AWS Region: {settings.AWS_REGION}")
    print(f"S3 Bucket: {settings.S3_BUCKET}")
    print("Fetching data from the database...")

    # Fetch and process the first chunk for demonstration purposes.
    async for chunk in fetch_facilities_in_chunks():
        print(f"Fetched a chunk with {len(chunk)} records.")
        break

if __name__ == "__main__":
    asyncio.run(main())
