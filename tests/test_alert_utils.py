import pytest
import sys
import os
from unittest.mock import patch
from app.utils.alert_utils import save_log_and_send_telegram, create_alert_log_msg

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


@pytest.mark.parametrize("msg", ["test message", "🚨 alert!"])
@patch("app.utils.alert_utils.send_telegram")
@patch("app.utils.alert_utils.write_log")
def test_save_log_and_send_telegram(mock_write_log, mock_send_telegram, msg):
    result = save_log_and_send_telegram(msg)
    assert result is None
    mock_write_log.assert_called_once_with(msg)
    mock_send_telegram.assert_called_once_with(msg)


def test_create_alert_log_msg_without_threats():
    msg = create_alert_log_msg(
        timestamp="2025-07-26 10:00:00",
        ip="192.168.1.1",
        port=22,
        service="ssh",
        data="some payload",
        geo={"country": "Poland", "city": "Warsaw", "isp": "Orange"},
    )
    assert "!!! HONEYPOT ALERT !!!" in msg
    assert "IP: 192.168.1.1 Port: 22 (ssh)" in msg
    assert "Data: `some payload`" in msg
    assert "Location: Poland, Warsaw (Orange)" in msg
    assert "Threats:" not in msg


def test_create_alert_log_msg_with_threats():
    threats = ["Brute Force", "Port Scan"]
    msg = create_alert_log_msg(
        timestamp="2025-07-26 10:00:00",
        ip="8.8.8.8",
        port="443",
        service="https",
        data="malicious request",
        geo={"country": "USA", "city": "Mountain View", "isp": "Google"},
        threats=threats,
    )
    assert "Threats: Brute Force, Port Scan" in msg
    assert "IP: 8.8.8.8 Port: 443 (https)" in msg
    assert "malicious request" in msg
