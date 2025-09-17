"""Utilities for building and rendering simple ChatGPT-style conversations."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import Iterable, Iterator, Literal

Role = Literal["system", "user", "assistant"]


@dataclass(frozen=True, slots=True)
class Message:
    """A single message in a conversation."""

    role: Role
    content: str

    def __post_init__(self) -> None:  # pragma: no cover - dataclass hook
        content = self.content.strip()
        if not content:
            raise ValueError("message content must not be empty")
        object.__setattr__(self, "content", content)


class Conversation:
    """Container object for a sequence of chat messages."""

    def __init__(self, *, system_prompt: str | None = None) -> None:
        self._messages: list[Message] = []
        if system_prompt:
            self.set_system_prompt(system_prompt)

    def __iter__(self) -> Iterator[Message]:
        return iter(self._messages)

    def add(self, role: Role, content: str) -> Message:
        """Add a message to the conversation and return it."""

        message = Message(role=role, content=content)
        if role == "system" and self._messages and self._messages[0].role == "system":
            self._messages[0] = message
        else:
            self._messages.append(message)
        return message

    def set_system_prompt(self, prompt: str) -> Message:
        """Set or replace the system prompt."""

        return self.add("system", prompt)

    def add_user(self, content: str) -> Message:
        return self.add("user", content)

    def add_assistant(self, content: str) -> Message:
        return self.add("assistant", content)

    @property
    def messages(self) -> tuple[Message, ...]:
        return tuple(self._messages)

    def render_markdown(self) -> str:
        return "\n".join(_format_markdown(self._messages))

    def render_plain(self) -> str:
        return "\n".join(_format_plain(self._messages))

    def stats(self) -> "ConversationStats":
        counts = Counter(message.role for message in self._messages)
        return ConversationStats(
            total_messages=len(self._messages),
            system_messages=counts.get("system", 0),
            user_messages=counts.get("user", 0),
            assistant_messages=counts.get("assistant", 0),
        )


@dataclass(frozen=True, slots=True)
class ConversationStats:
    total_messages: int
    system_messages: int
    user_messages: int
    assistant_messages: int

    def as_dict(self) -> dict[str, int]:
        return {
            "total": self.total_messages,
            "system": self.system_messages,
            "user": self.user_messages,
            "assistant": self.assistant_messages,
        }


ROLE_LABELS = {
    "system": "System",
    "user": "User",
    "assistant": "Assistant",
}


def _format_markdown(messages: Iterable[Message]) -> Iterator[str]:
    for message in messages:
        label = ROLE_LABELS[message.role]
        yield f"- **{label}:** {message.content}"


def _format_plain(messages: Iterable[Message]) -> Iterator[str]:
    for message in messages:
        label = ROLE_LABELS[message.role]
        yield f"{label}: {message.content}"
