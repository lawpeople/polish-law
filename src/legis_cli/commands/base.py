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
    backend_parse_content: bool = False

    def __init_subclass__(cls, name: str) -> None:
        if name in COMMAND_REGISTRY:
            raise RuntimeError()
        cls.name = name
        COMMAND_REGISTRY[name] = cls

    def __init__(self, subparser: argparse.ArgumentParser) -> None:
        for field_name, field in self.data_cls.__dataclass_fields__.items():
            if field_name == "subparser_name":
                continue

            kwargs = {}
            help_text = field.metadata.get("help", "")
            if help_text:
                kwargs["help"] = help_text

            if field.type in (bool, "bool"):
                subparser.add_argument(f"--{field.name}", action="store_true", **kwargs)

            if field.type in (str, "str"):
                subparser.add_argument(field.name, type=str, **kwargs)

    def execute(self, backend: Backend, data: TD) -> None:
        ...
