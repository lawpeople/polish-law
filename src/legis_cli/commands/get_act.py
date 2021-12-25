import argparse
from dataclasses import dataclass

from legis_cli.commands.base import BaseData, Command
from liblegis.backends import Backend


@dataclass
class GetActData(BaseData):
    legal_act: str


class GetActCommand(Command[GetActData], name="get-act"):
    data_cls = GetActData

    def __init__(self, subparser: argparse.ArgumentParser) -> None:
        subparser.add_argument(
            "legal_act", type=str, help="In [Year]/[Position] form, e.g. 1918/42"
        )

    def execute(self, backend: Backend, data: GetActData) -> None:
        year, position = [int(v) for v in data.legal_act.split("/")]
        legal_act = backend.get_legal_act(year, position)
        print(
            f"Dz.U. {legal_act.year} nr {legal_act.volume} poz. {legal_act.position}"
            f"\n\n{legal_act.content}"
        )
