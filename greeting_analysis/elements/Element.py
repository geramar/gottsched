from Word import Word
from Root import Root
from Group import Group
from Nomination import Nomination
from Epithet import Epithet
from Modificator import Modificator
from UnknownGroup import UnknownGroup


class Element:
    def __init__ (self, word_name, analyzer):
        self.analyzer = analyzer
        self.word_name = word_name
        self._group = self.word.get_group()
        self._word_dependence = False

    @property
    def __word_dependence(self):
        return self._word_dependence

    @__word_dependence.setter
    def __word_dependence (self, value):
        self._word_dependence = value

    @property
    def word(self):
        return Word(self.word_name, self.analyzer)

    @word.setter
    def word(self, word_name):
        self.word_name = word_name
        self.__word_dependence = True

    @property
    def root(self):
        return self.word.get_root()

    @property
    def group(self):
        if self.__word_dependence:
            return self.word.get_group()
        else:
            return self._group

    @group.setter
    def group(self, group_name):
        if group_name in self.analyzer.root_to_nomination.values():
            self._group = Nomination(group_name, self.analyzer)
        elif group_name in self.analyzer.root_to_epithet.values():
            self._group = Epithet(group_name, self.analyzer)
        elif group_name in self.analyzer.root_to_modificator.values():
            self._group = Modificator(group_name, self.analyzer)
        else:
            self._group = UnknownGroup(None, self.analyzer)
        self.__word_dependence = False

    @property
    def translation(self):
        return self.word.get_translation()

    @property
    def meaning(self):
        return self.word.get_meaning()

    @property
    def correlation(self):
        return self.word.get_group_correlation()

    @property
    def group_type(self):
        return self.group.get_subtype()