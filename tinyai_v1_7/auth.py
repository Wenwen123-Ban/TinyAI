"""Developer admin authentication for TinyAI v1.7."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class DeveloperAccount:
    username: str
    password: str


DEFAULT_DEVELOPER = DeveloperAccount(username="devadmin", password="tinyai-dev-1700")


def login(username: str, password: str) -> bool:
    return username == DEFAULT_DEVELOPER.username and password == DEFAULT_DEVELOPER.password
