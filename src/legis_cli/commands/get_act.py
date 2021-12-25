from dataclasses import dataclass, field

from legis_cli.commands.base import BaseData, Command
from liblegis.backends import Backend


@dataclass
class GetActData(BaseData):
    legal_act: str = field(metadata={"help": "In [Year]/[Position] form, e.g. 1918/42"})


class GetActCommand(Command[GetActData], name="get-act"):
    data_cls = GetActData

    def execute(self, backend: Backend, data: GetActData) -> None:
        year, position = [int(v) for v in data.legal_act.split("/")]
        legal_act = backend.get_legal_act(year, position)
        print(
            f"Dz.U. {legal_act.year} nr {legal_act.volume} poz. {legal_act.position}"
            f"\n\n{legal_act.content}"
        )
