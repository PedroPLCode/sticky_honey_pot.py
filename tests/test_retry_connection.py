import pytest
from unittest.mock import patch
from app.utils.retry_connection import retry_connection


def test_retry_connection_success():
    @retry_connection(max_retries=3, delay=0)
    def func():
        return "ok"

    assert func() == "ok"


def test_retry_connection_retries(monkeypatch):
    call_count = {"count": 0}

    @retry_connection(max_retries=3, delay=0)
    def func():
        call_count["count"] += 1
        if call_count["count"] < 3:
            raise ConnectionError("test")
        return "success"

    with patch("app.utils.retry_connection.write_log") as mock_log, patch(
        "time.sleep", return_value=None
    ):
        result = func()
        assert result == "success"
        assert call_count["count"] == 3
        assert mock_log.call_count == 2


def test_retry_connection_max_retries():
    @retry_connection(max_retries=2, delay=0)
    def func():
        raise ConnectionError("always fail")

    with patch("app.utils.retry_connection.write_log") as mock_log, patch(
        "time.sleep", return_value=None
    ):
        with pytest.raises(Exception) as excinfo:
            func()
        assert "Max retries reached" in str(excinfo.value)
        assert mock_log.call_count == 3
