import os
import gzip
import json
import tempfile
import pytest
from src.file_manager import generate_feed_file, generate_metadata_file


def test_generate_feed_file_success():
    sample_feed = {"data": [{"entity_id": "dining-1",
                             "name": "Test Facility"}]}
    with tempfile.TemporaryDirectory() as temp_dir:
        filename = generate_feed_file(sample_feed, output_dir=temp_dir)
        filepath = os.path.join(temp_dir, filename)
        assert os.path.exists(filepath)
        with gzip.open(filepath, "rt", encoding="utf-8") as f:
            data = json.load(f)
        assert data == sample_feed

def test_generate_metadata_file_success():
    feed_files = ["feed1.json.gz", "feed2.json.gz"]
    with tempfile.TemporaryDirectory() as temp_dir:
        filename = generate_metadata_file(feed_files, output_dir=temp_dir)
        filepath = os.path.join(temp_dir, filename)
        assert os.path.exists(filepath)
        with gzip.open(filepath, "rt", encoding="utf-8") as f:
            data = json.load(f)
        assert "generation_timestamp" in data
        assert data["name"]
        assert data["data_file"] == feed_files

def test_generate_feed_file_error(monkeypatch):
    # Force os.makedirs to raise an OSError.
    monkeypatch.setattr(os, "makedirs",
                        lambda path, exist_ok: (_ for _ in ()).throw(OSError("Fake error")))
    sample_feed = {"data": [{"entity_id": "dining-1",
                             "name": "Test Facility"}]}
    with pytest.raises(OSError, match="Fake error"):
        generate_feed_file(sample_feed, output_dir="dummy_dir")


def test_generate_metadata_file_error(monkeypatch):
    monkeypatch.setattr(os, "makedirs",
                        lambda path, exist_ok: (_ for _ in ()).throw(OSError("Fake error")))
    with pytest.raises(OSError, match="Fake error"):
        generate_metadata_file(["feed1.json.gz"], output_dir="dummy_dir")
