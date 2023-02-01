from abc import ABC, abstractmethod
from typing import Optional
import Root
import Word


class Group(ABC):
    def __init__(self, name: Optional[str], analyzer):
        self.name = name
        self.analyzer = analyzer

    def __eq__(self, other):
        if isinstance(other, str):
            return self.name == other
        elif isinstance(other, self.__class__):
            return self.name == other.name
        else:
            return NotImplemented

    def get_words(self) -> set[Word]:
        return self.analyzer.get_words_from_group(self.name)

    def get_roots(self) -> set[Root]:
        return self.analyzer.get_roots(self.name)

    def get_name(self) -> str:
        return self.name

    def get_meaning(self) -> str:
        return self.analyzer.get_meaning_from_group(self.name)

    @abstractmethod
    def get_correlation(self):
        pass

    @abstractmethod
    def get_subtype(self):
        pass

