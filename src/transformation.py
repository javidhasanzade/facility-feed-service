from src.logger import setup_logger

logger = setup_logger("transformation")


def transform_records_to_json(records):
    """
    Transforms a list of facility records into the JSON feed format.
    """
    try:
        data = []
        for record in records:
            facility = {
                "entity_id": f"dining-{record['id']}",
                "name": record['name'],
                "telephone": record['phone'],
                "url": record['url'],
                "location": {
                    "latitude": record['latitude'],
                    "longitude": record['longitude'],
                    "address": {
                        "country": record['country'],
                        "locality": record['locality'],
                        "region": record['region'],
                        "postal_code": record['postal_code'],
                        "street_address": record['street_address']
                    }
                }
            }
            data.append(facility)
        logger.info("Transformation complete",
                    extra={"record_count": len(data)})
        return {"data": data}
    except Exception as e:
        logger.exception("Error in transformation", extra={"error": str(e)})
        raise
