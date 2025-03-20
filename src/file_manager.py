import os
import time
import gzip
import json
from src.config import settings


def generate_feed_file(feed_json, output_dir="output"):
    """
    Writes the feed_json dictionary to a gzip-compressed JSON file.

    The file is named with the format:
      facility_feed_<timestamp>.json.gz

    Args:
        feed_json (dict): The JSON structure from transformation.
        output_dir (str): The directory to store generated files.

    Returns:
        str: The generated file name.
    """
    os.makedirs(output_dir, exist_ok=True)
    timestamp = int(time.time())
    filename = f"facility_feed_{timestamp}.json.gz"
    file_path = os.path.join(output_dir, filename)

    # Write the JSON data into a gzip-compressed file.
    with gzip.open(file_path, "wt", encoding="utf-8") as f:
        json.dump(feed_json, f)

    print(f"Generated feed file: {file_path}")
    return filename


def generate_metadata_file(feed_files, output_dir="output"):
    """
    Creates a metadata file that lists all generated feed files.

    The metadata file has the structure:
    {
        "generation_timestamp": <current_unix_timestamp>,
        "name": <settings.FEED_NAME>,
        "data_file": [<list_of_feed_file_names>]
    }

    The file is named metadata.json.gz and is gzip-compressed.

    Args:
        feed_files (list): A list of feed file names (strings).
        output_dir (str): The directory to store generated files.

    Returns:
        str: The generated metadata file name.
    """
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

    print(f"Generated metadata file: {file_path}")
    return filename
