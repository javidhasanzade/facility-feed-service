import os
import time
import gzip
import json
from typing import Dict, List

from src.config import settings
from src.logger import setup_logger

logger = setup_logger("file_manager")


def generate_feed_file(feed_json: Dict, output_dir="output") -> str:
    """
    Writes feed_json to a gzip-compressed JSON file.
    """
    try:
        os.makedirs(output_dir, exist_ok=True)
        timestamp = int(time.time())
        filename = f"facility_feed_{timestamp}.json.gz"
        file_path = os.path.join(output_dir, filename)
        with gzip.open(file_path, "wt", encoding="utf-8") as f:
            json.dump(feed_json, f)
        logger.info("Generated feed file", extra={"file_path": file_path})
        return filename
    except Exception as e:
        logger.exception("Error generating feed file", extra={"error": str(e)})
        raise


def generate_metadata_file(feed_files: List[str], output_dir="output") -> str:
    """
    Creates a metadata file listing all generated feed files.
    """
    try:
        os.makedirs(output_dir, exist_ok=True)
        metadata = {
            "generation_timestamp": int(time.time()),
            "name": settings.FEED_NAME,
            "data_file": feed_files
        }
        filename = "metadata.json.gz"
        file_path = os.path.join(output_dir, filename)
        with gzip.open(file_path, "wt", encoding="utf-8") as f:
            json.dump(metadata, f)
        logger.info("Generated metadata file", extra={"file_path": file_path})
        return filename
    except Exception as e:
        logger.exception("Error generating metadata file",
                         extra={"error": str(e)})
        raise
