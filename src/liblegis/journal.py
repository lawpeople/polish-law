from collections.abc import Iterable, Iterator

from liblegis.backends import Backend
from liblegis.legal_act import LegalAct


class Journal(Iterable[LegalAct]):
    def __init__(
        self,
        backend_cls: type[Backend],
    ) -> None:
        self._backend = backend_cls()

    def __iter__(self) -> Iterator[LegalAct]:
        return self

    def __next__(self) -> LegalAct:
        if self._backend.cursor is None:
            return self._backend.get_legal_act(1918, 1)
        else:
            next_legal_act = self._backend.get_next_legal_act()
            if next_legal_act is None:
                raise StopIteration()
            return next_legal_act