import requests
from utils.retry_connection import retry_connection
from utils.exception_handler import exception_handler
from config import IP_API_URL

@exception_handler()
@retry_connection()
def geoip_lookup(ip):
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
            "isp": data.get("isp", "Unknown")
        }