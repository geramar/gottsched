import Root
import Group


class Word:
    def __init__(self, name: str, analyzer): #analyzer: DictionaryAnalyzer
        self.name = name
        self.analyzer = analyzer

    def get_name(self):
        return self.name

    def get_normalized_name(self):
        return self.analyzer.get_normalisation(self.name)

    def get_root(self) -> Root:
        return self.analyzer.get_root(self.name)

    def get_group(self) -> Group:
        return self.analyzer.get_group_from_word(self.name)

    def get_translation(self) -> str:
        return self.analyzer.get_translation(self.name)

    def get_meaning(self) -> str:
        return self.analyzer.get_meaning_from_word(self.name)

    def get_group_correlation(self):
        return self.get_group().get_correlation()

