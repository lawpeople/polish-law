from dataclasses import dataclass

from legis_cli.commands.base import BaseData, Command
from liblegis import Journal
from liblegis.backends import Backend


@dataclass
class GetJournalData(BaseData):
    title: bool


class GetJournalCommand(Command[GetJournalData], name="get-journal"):
    data_cls = GetJournalData

    def execute(self, backend: Backend, data: GetJournalData) -> None:
        journal = Journal(backend)
        for act in journal:
            if data.title is True:
                print(act.title)
