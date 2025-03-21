from src.feeds.reserve_with_google_feed import ReserveWithGoogleTransformer
from src.feeds.base import FeedTransformer

FEED_TRANSFORMERS = {
    "reservewithgoogle.entity": ReserveWithGoogleTransformer,
    # "other.feed.name": OtherTransformer,
}


def get_transformer(feed_name: str) -> FeedTransformer:
    transformer_cls = FEED_TRANSFORMERS.get(feed_name)
    if not transformer_cls:
        raise ValueError(f"Unsupported feed name: {feed_name}")
    return transformer_cls()
