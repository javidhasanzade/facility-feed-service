import asyncio
import os
import tempfile
import gzip
import json
import pytest
from src.s3_uploader import upload_file_to_s3
from unittest.mock import MagicMock


@pytest.mark.asyncio
async def test_upload_file_to_s3_success(tmp_path, monkeypatch):
    # Create a temporary gzip file with sample data.
    temp_file = tmp_path / "test.json.gz"
    sample_data = {"data": [{"entity_id": "dining-1", "name": "Test Facility"}]}
    with gzip.open(temp_file, "wt", encoding="utf-8") as f:
        json.dump(sample_data, f)

    # Define a fake client with a fake_put_object that succeeds.
    class FakeClient:
        async def put_object(self, *args, **kwargs):
            return {"ResponseMetadata": {"HTTPStatusCode": 200}}

    # Define a fake session that returns the FakeClient in its context manager.
    class FakeSession:
        async def __aenter__(self):
            return FakeClient()
        async def __aexit__(self, exc_type, exc, tb):
            pass

    # Monkeypatch aioboto3.Session to return an instance of FakeSession.
    monkeypatch.setattr("src.s3_uploader.aioboto3.Session", lambda **kwargs: type("DummySession", (), {"client": lambda self, service: FakeSession()})())

    # This should complete without raising exceptions.
    await upload_file_to_s3(str(temp_file), "test_key.json.gz")

@pytest.mark.asyncio
async def test_upload_file_to_s3_error(tmp_path, monkeypatch):
    # Create a temporary gzip file with sample data.
    temp_file = tmp_path / "test.json.gz"
    sample_data = {"data": [{"entity_id": "dining-1", "name": "Test Facility"}]}
    with gzip.open(temp_file, "wt", encoding="utf-8") as f:
        json.dump(sample_data, f)

    # Define a fake client that raises an exception when put_object is called.
    class FakeClient:
        async def put_object(self, *args, **kwargs):
            raise Exception("Fake S3 error")

    # Define a fake session that returns the FakeClient in its context manager.
    class FakeSession:
        async def __aenter__(self):
            return FakeClient()
        async def __aexit__(self, exc_type, exc, tb):
            pass

    monkeypatch.setattr("src.s3_uploader.aioboto3.Session", lambda **kwargs: type("DummySession", (), {"client": lambda self, service: FakeSession()})())

    # Verify that the exception is raised.
    with pytest.raises(Exception, match="Fake S3 error"):
        await upload_file_to_s3(str(temp_file), "test_key.json.gz")
