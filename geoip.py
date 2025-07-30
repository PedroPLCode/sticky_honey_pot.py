import requests
from retry_connection import retry_connection
from exception_handler import exception_handler
from config import IP_API_URL

@exception_handler()
@retry_connection()
def geoip_lookup(ip):
        response = requests.get(f"{IP_API_URL}{ip}")
        data = response.json()
        return {
            "country": data.get("country", "Unknown"),
            "region": data.get("regionName", "Unknown"),
            "city": data.get("city", "Unknown"),
            "isp": data.get("isp", "Unknown")
        }