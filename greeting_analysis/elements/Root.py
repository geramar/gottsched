from typing import Optional
import Group
import Word


class Root:
    def __init__(self, name: Optional[str], analyzer):
        self.name = name
        self.analyzer = analyzer

    def get_name(self):
        return self.name

    def get_words(self) -> set[Word]:
        return self.analyzer.get_words_from_root(self.name)

    def get_group(self) -> Group:
        return self.analyzer.get_group_from_root(self.name)

    def get_meaning(self) -> str:
        return self.analyzer.get_meaning_from_root(self.name)