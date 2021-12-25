import argparse
from dataclasses import dataclass

from legis_cli.commands.base import BaseData, Command
from liblegis import Journal
from liblegis.backends import Backend, LocalGitBackend


@dataclass
class GetJournalData(BaseData):
    title: bool


class GetJournalCommand(Command[GetJournalData], name="get-journal"):
    data_cls = GetJournalData

    def __init__(self, subparser: argparse.ArgumentParser) -> None:
        subparser.add_argument("--title", action="store_true")

    def execute(self, backend: Backend, data: GetJournalData) -> None:
        journal = Journal(backend_cls=LocalGitBackend)
        for act in journal:
            if data.title is True:
                print(act.title)
