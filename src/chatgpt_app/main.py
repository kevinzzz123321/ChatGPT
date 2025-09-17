"""Command line helpers for formatting ChatGPT-style conversations."""

from __future__ import annotations

import argparse
from typing import Iterable, Sequence

from .conversation import Conversation, ROLE_LABELS


def _parse_message(token: str) -> tuple[str, str]:
    try:
        role_part, content_part = token.split(":", 1)
    except ValueError as exc:  # pragma: no cover - defensive branch
        raise argparse.ArgumentTypeError(
            "Messages must be in the format '<role>:<content>'"
        ) from exc

    role = role_part.strip().lower()
    if role not in ROLE_LABELS:
        valid = ", ".join(sorted(ROLE_LABELS))
        raise argparse.ArgumentTypeError(f"Unknown role '{role}'. Valid roles: {valid}.")

    content = content_part.strip()
    if not content:
        raise argparse.ArgumentTypeError("Message content must not be empty.")
    return role, content


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "messages",
        nargs="*",
        type=_parse_message,
        help=(
            "Conversation messages provided as '<role>:<content>' tokens. "
            "Valid roles: system, user, assistant."
        ),
    )
    parser.add_argument(
        "--system",
        dest="system_prompt",
        help="Optional system prompt that seeds the conversation.",
    )
    parser.add_argument(
        "--format",
        choices=("markdown", "plain"),
        default="markdown",
        help="Output format for the rendered conversation.",
    )
    return parser


def render_conversation(messages: Sequence[tuple[str, str]], *, system_prompt: str | None, format: str) -> str:
    conversation = Conversation(system_prompt=system_prompt)
    for role, content in messages:
        conversation.add(role, content)

    if format == "markdown":
        return conversation.render_markdown()
    return conversation.render_plain()


def main(argv: Iterable[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    output = render_conversation(
        args.messages,
        system_prompt=args.system_prompt,
        format=args.format,
    )
    print(output)
    return 0


if __name__ == "__main__":  # pragma: no cover - CLI entry point
    raise SystemExit(main())
