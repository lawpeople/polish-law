from __future__ import annotations

import argparse

from liblegis.backends import Backend

COMMAND_REGISTRY: dict[str, type[Command]] = {}


class Command:
    name: str

    def __init_subclass__(cls, name: str) -> None:
        if name in COMMAND_REGISTRY:
            raise RuntimeError()
        cls.name = name
        COMMAND_REGISTRY[name] = cls

    def __init__(self, subparser: argparse.ArgumentParser) -> None:
        ...

    def execute(self, backend: Backend, data: argparse.Namespace) -> None:
        ...
