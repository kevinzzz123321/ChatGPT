# ChatGPT Conversation Toolkit

This repository provides a lightweight toolkit for experimenting with simple
ChatGPT-style conversations.  It includes a core library for storing and
formatting messages, together with a small command-line helper that turns a
series of `<role>:<content>` tokens into nicely formatted transcripts.

## Features

- A `Conversation` container that normalises message content and exposes
  helper methods for building a dialogue step-by-step.
- Markdown and plain-text renderers for quickly exporting a transcript.
- Summary statistics describing how many system, user, and assistant messages
  appear in a conversation.
- A CLI (`python -m chatgpt_app.main`) that accepts inline messages and prints
  the formatted output.

## Quick Start

1. Install the project (ideally inside a virtual environment):

   ```bash
   pip install -e .[dev]
   ```

2. Execute the command-line interface, providing messages as
   `<role>:<content>` pairs.  For example:

   ```bash
   python -m chatgpt_app.main --system "Guide the user" \
       "user:Hello" "assistant:Hi there!"
   ```

   Which yields:

   ```
   - **System:** Guide the user
   - **User:** Hello
   - **Assistant:** Hi there!
   ```

3. Run the automated tests to ensure everything is functioning as expected:

   ```bash
   pytest
   ```

## Project Structure

```
├── pyproject.toml
├── src/
│   └── chatgpt_app/
│       ├── __init__.py
│       ├── conversation.py
│       └── main.py
└── tests/
    ├── test_cli.py
    └── test_conversation.py
```

Feel free to extend the conversation helpers, integrate them into your own
applications, or adapt the CLI to suit your workflow.
