import requests
from app.utils.retry_connection import retry_connection
from app.utils.exception_handler import exception_handler
from app.config import IP_API_URL


@exception_handler()
@retry_connection()
def geoip_lookup(ip: str):
    """
    Performs a GeoIP lookup for the given IP address using an external API.

    Args:
        ip (str): The IP address to look up.

    Returns:
        dict: A dictionary containing geographic and network information about the IP address, including:
            - country (str): Country name.
            - country_code (str): Country code.
            - region (str): Region code.
            - regionName (str): Region name.
            - city (str): City name.
            - zip (str): ZIP/postal code.
            - lat (float): Latitude.
            - lon (float): Longitude.
            - timezone (str): Timezone.
            - as (str): Autonomous system information.
            - org (str): Organization name.
            - mobile (bool): Whether the IP is mobile.
            - proxy (bool): Whether the IP is a proxy.
            - hosting (bool): Whether the IP is hosting.
            - reverse (str): Reverse DNS name.
            - isp (str): ISP name.

    Raises:
        requests.RequestException: If the API request fails.
        ValueError: If the response cannot be parsed as JSON.
    """
    response = requests.get(f"{IP_API_URL}{ip}")
    data = response.json()
    return {
        "country": data.get("country", "Unknown"),
        "country_code": data.get("countryCode", "Unknown"),
        "region": data.get("region", "Unknown"),
        "regionName": data.get("regionName", "Unknown"),
        "city": data.get("city", "Unknown"),
        "zip": data.get("zip", "Unknown"),
        "lat": data.get("lat", 0.0),
        "lon": data.get("lon", 0.0),
        "timezone": data.get("timezone", "Unknown"),
        "as": data.get("as", "Unknown"),
        "org": data.get("org", "Unknown"),
        "mobile": data.get("mobile", False),
        "proxy": data.get("proxy", False),
        "hosting": data.get("hosting", False),
        "reverse": data.get("reverse", "Unknown"),
        "isp": data.get("isp", "Unknown"),
    }
