import argparse

from legis_cli.commands.base import Command
from liblegis import Journal
from liblegis.backends import Backend, LocalGitBackend


class GetJournalCommand(Command, name="get-journal"):
    def __init__(self, subparser: argparse.ArgumentParser) -> None:
        subparser.add_argument("--title", action="store_true")

    def execute(self, backend: Backend, data: argparse.Namespace) -> None:
        journal = Journal(backend_cls=LocalGitBackend)
        for act in journal:
            if data.title is True:
                print(act.title)
