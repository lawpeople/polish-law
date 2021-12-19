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
        backend_method = self._backend.get_first_legal_act
        if self._backend.cursor is not None:
            backend_method = self._backend.get_next_legal_act

        legal_act = backend_method()
        if legal_act is None:
            raise StopIteration()
        return legal_act
