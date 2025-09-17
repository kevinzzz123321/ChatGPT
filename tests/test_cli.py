import pytest

from chatgpt_app.main import build_parser, render_conversation


def test_render_conversation_with_markdown():
    messages = [("user", "Hello"), ("assistant", "Hi there!")]
    output = render_conversation(messages, system_prompt="Be friendly", format="markdown")
    assert output.splitlines() == [
        "- **System:** Be friendly",
        "- **User:** Hello",
        "- **Assistant:** Hi there!",
    ]


def test_render_conversation_with_plain_output():
    messages = [("user", "Hello"), ("assistant", "Hi there!")]
    output = render_conversation(messages, system_prompt=None, format="plain")
    assert output.splitlines() == [
        "User: Hello",
        "Assistant: Hi there!",
    ]


def test_parser_rejects_invalid_role():
    parser = build_parser()
    with pytest.raises(SystemExit):
        parser.parse_args(["robot:Beep boop"])


def test_parser_rejects_empty_content():
    parser = build_parser()
    with pytest.raises(SystemExit):
        parser.parse_args(["user:   "])
