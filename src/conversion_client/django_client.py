"""Cache Conversion client."""
from functools import lru_cache
from src.conversion_client.conversion_client import CurrencyConversionClient


@lru_cache
def get_keycloak_client() -> CurrencyConversionClient:
    """Create an instance of a CurrencyConversionClient using singleton pattern."""
    return CurrencyConversionClient()
