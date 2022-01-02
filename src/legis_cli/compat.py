import argparse

try:
    _argcomplete_imported = True
    import argcomplete
except ImportError:
    _argcomplete_imported = False


def enable_argcomplete_if_available(parser: argparse.ArgumentParser) -> None:
    if _argcomplete_imported is True:
        argcomplete.autocomplete(parser)


__all__ = ["enable_argcomplete_if_available"]
