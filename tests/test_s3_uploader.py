import gzip
import json
import pytest
from src.s3_uploader import upload_file_to_s3


# Define a fake client with a fake_put_object that succeeds.
class FakeClient:
    def __init__(self, should_fail=False):
        self.should_fail = should_fail

    async def put_object(self, *args, **kwargs):
        if self.should_fail:
            raise Exception("Fake S3 error")  # Simulating an S3 failure
        return {"ResponseMetadata": {"HTTPStatusCode": 200}}


# Define a fake session that returns the FakeClient in its context manager.
class FakeSession:
    def __init__(self, should_fail=False):
        self.should_fail = should_fail

    async def __aenter__(self):
        return FakeClient(should_fail=self.should_fail)

    async def __aexit__(self, exc_type, exc, tb):
        pass


def create_dummy_session(should_fail=False, **kwargs):
    return type("DummySession", (),
                {"client": lambda self, service: FakeSession(
                    should_fail=should_fail)})()


@pytest.mark.asyncio
async def test_upload_file_to_s3_success(tmp_path, monkeypatch):
    # Create a temporary gzip file with sample data.
    temp_file = tmp_path / "test.json.gz"
    sample_data = {"data": [{"entity_id": "dining-1",
                             "name": "Test Facility"}]}
    with gzip.open(temp_file, "wt", encoding="utf-8") as f:
        json.dump(sample_data, f)

    # Monkeypatch aioboto3.Session to return an instance of FakeSession.
    monkeypatch.setattr("src.s3_uploader.aioboto3.Session",
                        create_dummy_session)

    # This should complete without raising exceptions.
    await upload_file_to_s3(str(temp_file), "test_key.json.gz")


@pytest.mark.asyncio
async def test_upload_file_to_s3_error(tmp_path, monkeypatch):
    # Create a temporary gzip file with sample data.
    temp_file = tmp_path / "test.json.gz"
    sample_data = {"data": [{"entity_id": "dining-1",
                             "name": "Test Facility"}]}
    with gzip.open(temp_file, "wt", encoding="utf-8") as f:
        json.dump(sample_data, f)

    # Monkeypatch aioboto3.Session to return a failing FakeSession.
    monkeypatch.setattr("src.s3_uploader.aioboto3.Session",
                        lambda **kwargs: create_dummy_session(
                            should_fail=True))

    # Verify that the exception is raised.
    with pytest.raises(Exception, match="Fake S3 error"):
        await upload_file_to_s3(str(temp_file), "test_key.json.gz")
