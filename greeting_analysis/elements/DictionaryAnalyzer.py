from Nomination import Nomination
from Epithet import Epithet
from Modificator import Modificator
from Word import Word
from Root import Root
from UnknownGroup import UnknownGroup
from Group import Group
from typing import Optional
from Dictionary import Dictionary
import json

class DictionaryAnalyzer:
    def __init__(self, dictionary: Dictionary):
        self.word_to_root = dictionary.word_to_root
        self.root_to_group = dictionary.root_to_group
        self.root_to_nomination = dictionary.root_to_nomination
        self.root_to_epithet = dictionary.root_to_epithet
        self.root_to_modificator = dictionary.root_to_modificator
        self.analogs = dictionary.analogs
        self.word_to_translation = dictionary.word_to_translation
        self.group_to_meaning = dictionary.group_to_meaning
        self.correlations = dictionary.correlations
        self.prefixes = dictionary.prefixes

    def get_normalisation(self, name: str) -> Optional[str]:
        if name in self.word_to_root:
            return name
        elif name in self.analogs:
            return self.analogs[name]
        else:
            return None

    def get_root(self, word_name: str) -> Root:
        name = self.get_normalisation(word_name)
        root_name = None if name not in self.word_to_root else self.word_to_root[name]
        return Root(root_name, self)

    def get_group_from_root(self, root_name: str) -> Group:
        group_name = None if root_name not in self.root_to_group else self.root_to_group[root_name]
        if root_name in self.root_to_nomination:
            return Nomination(group_name, self)
        elif root_name in self.root_to_epithet:
            return Epithet(group_name, self)
        elif root_name in self.root_to_modificator:
            return Modificator(group_name, self)
        else:
            return UnknownGroup(None, self)

    def get_group_from_word(self, word_name: str) -> Group:
        root_name = self.get_root(word_name).get_name()
        return self.get_group_from_root(root_name)

    def get_roots(self, group_name) -> set[Root]:
        roots = set()
        for root, cur_group in self.root_to_group.items():
            if cur_group == group_name:
                roots.add(Root(root, self))
        return roots

    def get_words_from_root(self, root_name: str) -> set[Word]:
        words = set()
        for word, cur_root in self.word_to_root.items():
            if cur_root == root_name:
                words.add(Word(word, self))
        return words

    def get_words_from_group(self, group_name: str) -> set[Word]:
        roots = [root.get_name() for root in self.get_roots(group_name)]
        words = set()
        for root_name in roots:
            words |= self.get_words_from_root(root_name)
        return words

    def get_meaning_from_group(self, group_name: str) -> str:
        meaning = None if group_name not in self.group_to_meaning else self.group_to_meaning[group_name]
        return meaning

    def get_meaning_from_root(self, root_name: str) -> str:
        group_name = self.get_group_from_root(root_name).get_name()
        return self.get_meaning_from_group(group_name)

    def get_meaning_from_word(self, word_name: str) -> str:
        group_name = self.get_group_from_word(word_name).get_name()
        return self.get_meaning_from_group(group_name)

    def get_translation(self, word_name: str) -> str:
        translation = None if self.get_normalisation(word_name) not in self.word_to_translation \
            else self.word_to_translation[self.get_normalisation(word_name)]
        return translation

    def get_epithets(self, nomination_name: str) -> list[Epithet]:
        epithets = self.correlations[nomination_name]
        return [Epithet(epithet_name, self) for epithet_name in epithets]

    def get_nomination(self, epithet_name: str) -> Nomination:
        nomination_name = self.correlations[epithet_name]
        return Nomination(nomination_name, self)
