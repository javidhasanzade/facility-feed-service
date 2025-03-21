from src.feeds.base import FeedTransformer


class ReserveWithGoogleTransformer(FeedTransformer):
    def transform(self, records: list) -> dict:
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
