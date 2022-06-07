from dataclasses import dataclass, field

from legis_cli.commands.base import BaseData, Command
from liblegis.backends import Backend


@dataclass
class GetArticleData(BaseData):
    legal_address: str = field(
        metadata={"help": "In [Year]/[Position]/[Article] form, e.g. 1918/42/13"}
    )


class GetArticleCommand(Command[GetArticleData], name="get-article"):
    data_cls = GetArticleData
    backend_parse_content = True

    def execute(self, backend: Backend, data: GetArticleData) -> None:
        year, position, article = [int(v) for v in data.legal_address.split("/")]
        legal_act = backend.get_legal_act(year, position)
        print(
            f"Dz.U. {legal_act.year} nr {legal_act.volume} poz. {legal_act.position} "
            f"art. {article}\n\n{legal_act.articles[article - 1].content}"
        )
