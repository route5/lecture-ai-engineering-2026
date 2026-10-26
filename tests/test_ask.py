from types import SimpleNamespace
from unittest.mock import Mock

import app.ask as ask_module


def _mock_client(monkeypatch, response):
    client = Mock()
    client.models.generate_content.return_value = response
    monkeypatch.setattr(ask_module, "get_api_key", lambda: "test-key")
    monkeypatch.setattr(ask_module.genai, "Client", Mock(return_value=client))


def test_ask_prints_input_and_output_token_counts(monkeypatch, capsys):
    response = SimpleNamespace(
        text="answer",
        usage_metadata=SimpleNamespace(
            prompt_token_count=12,
            candidates_token_count=5,
        ),
    )
    _mock_client(monkeypatch, response)

    assert ask_module.ask("question") == "answer"
    assert capsys.readouterr().out == "[トークン数] 入力: 12, 出力: 5\n"


def test_ask_reports_unavailable_token_counts(monkeypatch, capsys):
    response = SimpleNamespace(text="answer", usage_metadata=None)
    _mock_client(monkeypatch, response)

    assert ask_module.ask("question") == "answer"
    assert capsys.readouterr().out == "[トークン数] 入力: 不明, 出力: 不明\n"
