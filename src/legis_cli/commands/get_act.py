import argparse

from legis_cli.commands.base import Command
from liblegis.backends import Backend


class GetActCommand(Command, name="get-act"):
    def __init__(self, subparser: argparse.ArgumentParser) -> None:
        subparser.add_argument(
            "legal_act", type=str, help="In [Year]/[Position] form, e.g. 1918/42"
        )

    def execute(self, backend: Backend, data: argparse.Namespace) -> None:
        legal_act_addr: str = data.legal_act
        year, position = [int(v) for v in legal_act_addr.split("/")]
        legal_act = backend.get_legal_act(year, position)
        print(
            f"Dz.U. {legal_act.year} nr {legal_act.volume} poz. {legal_act.position}"
            f"\n\n{legal_act.content}"
        )
