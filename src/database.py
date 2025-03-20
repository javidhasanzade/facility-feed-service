import asyncpg
from src.config import settings

async def fetch_facilities_in_chunks(chunk_size: int = settings.CHUNK_SIZE):
    """
    Connects to the PostgreSQL database, fetches facility records,
    and yields them in chunks of 'chunk_size' records.
    """
    conn = await asyncpg.connect(settings.DATABASE_URL)
    try:
        query = """
            SELECT 
                id, name, phone, url, latitude, longitude, 
                country, locality, region, postal_code, street_address
            FROM facility;
        """
        records_chunk = []
        async with conn.transaction():
            async for record in conn.cursor(query):
                records_chunk.append(record)
                if len(records_chunk) >= chunk_size:
                    yield records_chunk
                    records_chunk = []
        if records_chunk:
            yield records_chunk
    finally:
        await conn.close()
