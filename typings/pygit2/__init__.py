from __future__ import annotations

from typing import Iterator


class Repository:
    head: Reference

    def __init__(self, path: str) -> None:
        ...

    def walk(self, oid: Oid) -> Iterator[Commit]:
        ...


class Reference:
    target: Oid


class Oid:
    ...


class Commit:
    message: str
