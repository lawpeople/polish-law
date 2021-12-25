import argparse

from legis_cli.commands import COMMAND_REGISTRY, Command
from legis_cli.commands.base import BaseData
from liblegis.backends import Backend, LocalGitBackend


class CLIApplication:
    """CLI Application that exposes an API to work with legal acts."""

    def __init__(self, backend_cls: type[Backend]) -> None:
        self.backend = backend_cls()
        self.parser = argparse.ArgumentParser(description=self.__doc__)
        self._commands: dict[str, Command[BaseData]] = {}

        self._register_commands()

    def _register_commands(self) -> None:
        subparsers = self.parser.add_subparsers(dest="subparser_name")
        for command_cls in COMMAND_REGISTRY.values():
            subparser = subparsers.add_parser(command_cls.name)
            self._commands[command_cls.name] = command_cls(subparser)

    def run(self) -> None:
        parser_data = self.parser.parse_args()
        subparser_name: str = parser_data.subparser_name
        command = self._commands[subparser_name]
        data = command.data_cls(**parser_data.__dict__)
        command.execute(self.backend, data)


def main() -> None:
    app = CLIApplication(backend_cls=LocalGitBackend)
    app.run()
