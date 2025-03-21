import pytest
from src.database import fetch_facilities_in_chunks


# Fake cursor to simulate async iteration over records.
class FakeCursor:
    def __init__(self, records, raise_error=False):
        self.records = records
        self.raise_error = raise_error

    async def __aiter__(self):
        if self.raise_error:
            raise Exception("Fake cursor error")
        for record in self.records:
            yield record


# Fake transaction context manager.
class FakeTransaction:
    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        pass


# Fake connection mimicking asyncpg's behavior.
class FakeConnection:
    def __init__(self, records, raise_error=False):
        self.records = records
        self.raise_error = raise_error

    def transaction(self):
        return FakeTransaction()

    def cursor(self, query):
        return FakeCursor(self.records, raise_error=self.raise_error)

    async def close(self):
        pass


# Fake connect functions for various scenarios.
async def fake_connect_success(database_url):
    sample_records = [
        {
            "id": 1,
            "name": "Test Facility",
            "phone": "+1-111-111-1111",
            "url": "www.testfacility.com",
            "latitude": 10.0,
            "longitude": 20.0,
            "country": "US",
            "locality": "Testville",
            "region": "TS",
            "postal_code": "12345",
            "street_address": "123 Test St"
        }
    ]
    return FakeConnection(sample_records)


async def fake_connect_empty(database_url):
    return FakeConnection([])


async def fake_connect_error(database_url):
    sample_records = [
        {
            "id": 1,
            "name": "Test Facility",
            "phone": "+1-111-111-1111",
            "url": "www.testfacility.com",
            "latitude": 10.0,
            "longitude": 20.0,
            "country": "US",
            "locality": "Testville",
            "region": "TS",
            "postal_code": "12345",
            "street_address": "123 Test St"
        }
    ]
    return FakeConnection(sample_records, raise_error=True)


@pytest.mark.asyncio
async def test_fetch_facilities_in_chunks_success(monkeypatch):
    monkeypatch.setattr("asyncpg.connect", fake_connect_success)
    chunks = []
    async for chunk in fetch_facilities_in_chunks(chunk_size=1):
        chunks.append(chunk)
    assert len(chunks) == 1
    assert len(chunks[0]) == 1
    record = chunks[0][0]
    assert record["id"] == 1
    assert record["name"] == "Test Facility"


@pytest.mark.asyncio
async def test_fetch_facilities_in_chunks_empty(monkeypatch):
    monkeypatch.setattr("asyncpg.connect", fake_connect_empty)
    chunks = []
    async for chunk in fetch_facilities_in_chunks(chunk_size=1):
        chunks.append(chunk)
    # With no records, nothing should be yielded.
    assert len(chunks) == 0


@pytest.mark.asyncio
async def test_fetch_facilities_in_chunks_error(monkeypatch):
    monkeypatch.setattr("asyncpg.connect", fake_connect_error)
    with pytest.raises(Exception, match="Fake cursor error"):
        async for _ in fetch_facilities_in_chunks(chunk_size=1):
            pass
