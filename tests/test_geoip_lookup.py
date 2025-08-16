from unittest.mock import patch, MagicMock
from requests.exceptions import RequestException
from app.utils.geoip_lookup import geoip_lookup
from app.config import IP_API_URL


def test_geoip_lookup_success():
    test_ip = "8.8.8.8"
    mock_response_data = {
        "country": "United States",
        "countryCode": "US",
        "region": "CA",
        "regionName": "California",
        "city": "Mountain View",
        "zip": "94035",
        "lat": 37.386,
        "lon": -122.0838,
        "timezone": "America/Los_Angeles",
        "as": "AS15169 Google LLC",
        "org": "Google LLC",
        "mobile": False,
        "proxy": False,
        "hosting": False,
        "reverse": "dns.google",
        "isp": "Google LLC",
    }
    mock_response = MagicMock()
    mock_response.json.return_value = mock_response_data
    with patch(
        "app.utils.geoip_lookup.requests.get", return_value=mock_response
    ) as mock_get:
        result = geoip_lookup(test_ip)
        mock_get.assert_called_once_with(f"{IP_API_URL}{test_ip}")
        assert result["country"] == "United States"
        assert result["city"] == "Mountain View"
        assert result["lat"] == 37.386


def test_geoip_lookup_request_exception():
    test_ip = "8.8.8.8"
    with patch(
        "app.utils.geoip_lookup.requests.get",
        side_effect=RequestException("API failure"),
    ):
        result = geoip_lookup(test_ip)
        assert result is None


def test_geoip_lookup_missing_fields():
    test_ip = "1.1.1.1"
    mock_response_data = {}
    mock_response = MagicMock()
    mock_response.json.return_value = mock_response_data
    with patch("app.utils.geoip_lookup.requests.get", return_value=mock_response):
        result = geoip_lookup(test_ip)
        assert result["country"] == "Unknown"
        assert result["lat"] == 0.0
        assert result["proxy"] is False
