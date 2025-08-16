from unittest.mock import patch
from app.utils.exception_handler import exception_handler


def test_exception_handler_returns_value_when_no_exception():
    @exception_handler(default_return="default")
    def func(x, y):
        return x + y

    result = func(2, 3)
    assert result == 5


def test_exception_handler_returns_default_on_exception():
    @exception_handler(default_return="default")
    def func():
        raise ValueError("test error")

    with patch("app.utils.alert_utils.save_log_and_send_telegram") as mock_alert:
        result = func()
        assert result == "default"
        mock_alert.assert_called_once()
        assert "func" in mock_alert.call_args[0][0]
        assert "test error" in mock_alert.call_args[0][0]


def test_exception_handler_preserves_args_kwargs():
    @exception_handler(default_return=0)
    def func(a, b=0):
        return a + b

    result = func(3, b=4)
    assert result == 7
