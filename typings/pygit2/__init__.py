from __future__ import annotations

from typing import Iterator

GIT_SORT_NONE = 0
GIT_SORT_TOPOLOGICAL = 1
GIT_SORT_TIME = 2
GIT_SORT_REVERSE = 4


class Repository:
    head: Reference

    def __init__(self, path: str) -> None:
        ...

    def walk(self, oid: Oid, sort_mode: int = GIT_SORT_NONE) -> Iterator[Commit]:
        ...

    def revparse_single(self, revision: str) -> Commit:
        ...


class Reference:
    target: Oid


class Oid:
    ...


class Commit:
    message: str
    short_id: str
