import re
import app.config as config


def test_env_variables(monkeypatch):
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "test_token")
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "12345")
    import importlib

    importlib.reload(config)
    assert config.TELEGRAM_BOT_TOKEN == "test_token"
    assert config.TELEGRAM_CHAT_ID == "12345"


def test_constants_types():
    assert isinstance(config.IP_API_URL, str)
    assert isinstance(config.LOG_DIR, str)
    assert isinstance(config.PORTS, dict)
    assert isinstance(config.BANNER, dict)
    assert isinstance(config.SQL_ATTACK_PATTERNS, list)


def test_sql_attack_patterns_structure():
    for pattern, description in config.SQL_ATTACK_PATTERNS:
        assert isinstance(pattern, str)
        assert isinstance(description, str)
        re.compile(pattern)
