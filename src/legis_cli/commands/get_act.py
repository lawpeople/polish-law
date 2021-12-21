import argparse

from legis_cli.commands.base import Command


class GetActCommand(Command, name="get-act"):
    def __init__(self, subparser: argparse.ArgumentParser) -> None:
        subparser.add_argument(
            "legal-act", type=str, help="In [Year]/[Position] form, e.g. 1918/42"
        )
