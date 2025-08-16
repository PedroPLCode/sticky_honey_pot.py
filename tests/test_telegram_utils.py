from unittest.mock import MagicMock, AsyncMock, patch, ANY
from app.utils.telegram_utils import send_telegram


def test_send_telegram_success():
    test_msg = "Test success"

    mock_bot = MagicMock()
    mock_bot.send_message = AsyncMock()

    with patch("app.utils.telegram_utils.Bot", return_value=mock_bot), patch(
        "app.utils.telegram_utils.write_log"
    ) as mock_log:

        result = send_telegram(test_msg)

        assert result is True
        mock_bot.send_message.assert_awaited_once_with(chat_id=ANY, text=test_msg)
        mock_log.assert_called_once()
        assert "sent successfully" in mock_log.call_args[0][0]


def test_send_telegram_failure(monkeypatch):
    test_msg = "Test fail"

    with patch(
        "app.utils.telegram_utils.Bot", side_effect=Exception("Fake fail")
    ), patch("app.utils.telegram_utils.write_log") as mock_log:

        result = send_telegram(test_msg)

        assert result is False
        mock_log.assert_called_once()
        assert "Sending failed" in mock_log.call_args[0][0]
