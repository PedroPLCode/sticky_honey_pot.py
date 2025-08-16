import pytest
from unittest.mock import patch
from app.utils.exploit_detector import detect_exploit


@pytest.fixture
def mock_patterns():
    return [
        (r"select.+from", "SQL Injection - SELECT"),
        (r"union.+select", "SQL Injection - UNION"),
        (r"drop\s+table", "SQL Injection - DROP"),
    ]


def test_detect_exploit_no_match(mock_patterns):
    with patch("app.utils.exploit_detector.SQL_ATTACK_PATTERNS", mock_patterns):
        result = detect_exploit("this is a safe string")
        assert result is None


def test_detect_exploit_single_match(mock_patterns):
    with patch("app.utils.exploit_detector.SQL_ATTACK_PATTERNS", mock_patterns):
        result = detect_exploit("SELECT * FROM users")
        assert result == ["SQL Injection - SELECT"]


def test_detect_exploit_multiple_matches(mock_patterns):
    with patch("app.utils.exploit_detector.SQL_ATTACK_PATTERNS", mock_patterns):
        result = detect_exploit(
            "UNION SELECT password FROM users; DROP TABLE accounts;"
        )
        assert set(result) == {
            "SQL Injection - UNION",
            "SQL Injection - SELECT",
            "SQL Injection - DROP",
        }


def test_detect_exploit_case_insensitive(mock_patterns):
    with patch("app.utils.exploit_detector.SQL_ATTACK_PATTERNS", mock_patterns):
        result = detect_exploit("SeLeCt id FrOm accounts")
        assert result == ["SQL Injection - SELECT"]
