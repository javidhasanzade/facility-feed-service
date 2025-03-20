def transform_records_to_json(records):
    """
    Transforms a list of facility records into the JSON feed format.

    Each record is expected to have the following fields:
    id, name, phone, url, latitude, longitude, country, locality, region, postal_code, street_address

    Returns a dictionary in the format:
    {
      "data": [
          {
              "entity_id": "dining-1",  # using id from the record
              "name": "Sample Eatery 1",
              "telephone": "+1-415-876-5432",
              "url": "www.sampleeatery1.com",
              "location": {
                  "latitude": 37.404570,
                  "longitude": -122.033160,
                  "address": {
                      "country": "US",
                      "locality": "Sunnyvale",
                      "region": "CA",
                      "postal_code": "94089",
                      "street_address": "815 11th Ave"
                  }
              }
          },
          ... more records ...
      ]
    }
    """
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
    return {"data": data}
