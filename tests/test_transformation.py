import pytest
from src.transformation import transform_records_to_json


def test_transform_records_normal():
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
    result = transform_records_to_json(sample_records)
    assert "data" in result
    assert isinstance(result["data"], list)
    assert result["data"][0]["entity_id"] == "dining-1"

def test_transform_records_empty():
    result = transform_records_to_json([])
    assert "data" in result
    assert result["data"] == []

def test_transform_records_missing_field():
    # Simulate a record missing the 'name' field.
    sample_records = [
        {
            "id": 2,
            # 'name' is missing.
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
    with pytest.raises(KeyError):
        transform_records_to_json(sample_records)
