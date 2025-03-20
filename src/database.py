import asyncpg
from src.config import settings
from src.logger import setup_logger

logger = setup_logger("database")

async def fetch_facilities_in_chunks(chunk_size: int = settings.CHUNK_SIZE):
    conn = await asyncpg.connect(settings.DATABASE_URL)
    try:
        query = """
            SELECT id, name, phone, url, latitude, longitude,
                   country, locality, region, postal_code, street_address
            FROM facility;
        """
        records_chunk = []
        async with conn.transaction():
            async for record in conn.cursor(query):
                records_chunk.append(record)
                if len(records_chunk) >= chunk_size:
                    logger.info("Yielding a chunk", extra={"chunk_size": len(records_chunk)})
                    yield records_chunk
                    records_chunk = []
        if records_chunk:
            yield records_chunk
    except Exception as e:
        logger.exception("Error fetching facilities", extra={"error": str(e)})
        raise
    finally:
        await conn.close()
