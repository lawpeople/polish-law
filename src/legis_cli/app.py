import argparse

from legis_cli.commands import COMMAND_REGISTRY, Command
from liblegis.backends import Backend, LocalGitBackend


class CLIApplication:
    """CLI Application that exposes an API to work with legal acts."""

    def __init__(self, backend_cls: type[Backend]) -> None:
        self.backend = backend_cls()
        self.parser = argparse.ArgumentParser(description=self.__doc__)
        self._commands: dict[str, Command] = {}

        self._register_commands()

    def _register_commands(self) -> None:
        subparsers = self.parser.add_subparsers()
        for command_cls in COMMAND_REGISTRY.values():
            subparser = subparsers.add_parser(command_cls.name)
            self._commands[command_cls.name] = command_cls(subparser)

    def run(self) -> None:
        self.parser.parse_args()


def main() -> None:
    app = CLIApplication(backend_cls=LocalGitBackend)
    app.run()
