import requests

def geoip_lookup(ip):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}")
        data = response.json()
        return {
            "country": data.get("country", "Unknown"),
            "region": data.get("regionName", "Unknown"),
            "city": data.get("city", "Unknown"),
            "isp": data.get("isp", "Unknown")
        }
    except:
        return {"country": "Unknown", "region": "Unknown", "city": "Unknown", "isp": "Unknown"}
