import pytest

from chatgpt_app.conversation import Conversation


def test_conversation_adds_and_formats_messages():
    convo = Conversation(system_prompt="You are a helpful assistant.")
    convo.add_user("Hello there!")
    convo.add_assistant("Hi! How can I assist you today?")

    markdown = convo.render_markdown().splitlines()
    assert markdown == [
        "- **System:** You are a helpful assistant.",
        "- **User:** Hello there!",
        "- **Assistant:** Hi! How can I assist you today?",
    ]

    plain = convo.render_plain().splitlines()
    assert plain == [
        "System: You are a helpful assistant.",
        "User: Hello there!",
        "Assistant: Hi! How can I assist you today?",
    ]


def test_replacing_system_prompt():
    convo = Conversation(system_prompt="Old prompt")
    convo.set_system_prompt("New prompt")
    assert [msg.content for msg in convo.messages] == ["New prompt"]


def test_empty_message_raises_error():
    convo = Conversation()
    with pytest.raises(ValueError):
        convo.add_user("   ")


def test_stats_reporting():
    convo = Conversation()
    convo.add_user("Hi")
    convo.add_assistant("Hello")
    convo.set_system_prompt("Talk nicely")
    convo.add_assistant("Sure")
    stats = convo.stats()
    assert stats.as_dict() == {
        "total": 4,
        "system": 1,
        "user": 1,
        "assistant": 2,
    }
