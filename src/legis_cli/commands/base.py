from __future__ import annotations

import argparse
from dataclasses import dataclass
from typing import Any, Generic, TypeVar

from liblegis.backends import Backend

TD = TypeVar("TD", bound="BaseData")

COMMAND_REGISTRY: dict[str, type[Command[Any]]] = {}


@dataclass
class BaseData:
    subparser_name: str


class Command(Generic[TD]):
    name: str
    data_cls: type[TD]

    def __init_subclass__(cls, name: str) -> None:
        if name in COMMAND_REGISTRY:
            raise RuntimeError()
        cls.name = name
        COMMAND_REGISTRY[name] = cls

    def __init__(self, subparser: argparse.ArgumentParser) -> None:
        ...

    def execute(self, backend: Backend, data: TD) -> None:
        ...
