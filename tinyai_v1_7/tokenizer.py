"""Tokenization module for TinyAI v1.7."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any

NUMBER_REGEX = re.compile(r"[0-9]+(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?")
WORD_REGEX = re.compile(r"[A-Za-z_]+")
OP_REGEX = re.compile(r"[+\-*/^<>=]")
TOKEN_REGEX = re.compile(
    r"[0-9]+(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?|[A-Za-z_]+|[+\-*/^<>=]"
)


@dataclass(slots=True)
class Token:
    """A minimal token model with optional numeric payload."""

    raw: str
    kind: str
    value: float | None = None
    metadata: dict[str, Any] | None = None


class Tokenizer:
    """Single-pass tokenizer using regex extraction."""

    def tokenize(self, text: str) -> list[Token]:
        tokens: list[Token] = []
        for match in TOKEN_REGEX.finditer(text.lower()):
            lexeme = match.group(0)
            if NUMBER_REGEX.fullmatch(lexeme):
                tokens.append(Token(raw=lexeme, kind="number", value=float(lexeme)))
            elif WORD_REGEX.fullmatch(lexeme):
                tokens.append(Token(raw=lexeme, kind="word"))
            elif OP_REGEX.fullmatch(lexeme):
                tokens.append(Token(raw=lexeme, kind="operator"))
        return tokens
