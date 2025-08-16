from unittest.mock import patch
from datetime import datetime
from app.utils.logs_utils import write_log


def test_write_log_creates_file_and_writes_message(tmp_path, capsys):
    test_msg = "Test honeypot log"
    fake_log_dir = tmp_path / "logs"

    with patch("app.utils.logs_utils.LOG_DIR", str(fake_log_dir)):
        write_log(test_msg)

        today = datetime.now().strftime("%Y-%m-%d")
        log_file = fake_log_dir / f"honeypot_log_{today}.txt"
        assert log_file.exists()

        content = log_file.read_text(encoding="utf-8")
        assert test_msg in content
        assert "[" in content

        captured = capsys.readouterr()
        assert test_msg in captured.out
        assert "[" in captured.out
