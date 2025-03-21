from abc import ABC, abstractmethod


class FeedTransformer(ABC):
    @abstractmethod
    def transform(self, records: list) -> dict:
        """Transform raw database records into feed format."""
        pass
