from DictionaryAnalyzer import DictionaryAnalyzer
import json

class JsonDictionaryAnalyzer(DictionaryAnalyzer):
    def __init__(self, address="greeting_analysis/elements/dictionary.json"):
        self.address = address
        self.dictionary = json.load(open(self.address, encoding="utf-8"))
        self.word_to_root = self.dictionary["word_to_root"]
        self.root_to_nomination = self.dictionary["root_to_nomination"]
        self.root_to_epithet = self.dictionary["root_to_epithet"]
        self.root_to_modificator = self.dictionary["root_to_modificator"]
        self.root_to_group = {**self.root_to_epithet, **self.root_to_nomination, **self.root_to_modificator}
        self.analogs = self.dictionary["analogs"]
        self.word_to_translation = self.dictionary["word_to_translation"]
        self.group_to_meaning = self.dictionary["group_to_meaning"]
        self.correlations = self.dictionary["correlations"]
        self.prefixes = self.dictionary["prefixes"]

    def set_value(self, section, key, value=None):
        if section != "prefixes":
            self.dictionary[section][key] = value
        else:
            self.dictionary[section].append(key)
        json.dump(self.dictionary, open(self.address, "w", encoding="utf-8"))
        self.dictionary = json.load(open(self.address, encoding="utf-8"))

    def del_value(self, section, key):
        if section != "prefixes":
            del self.dictionary[section][key]
        else:
            self.dictionary[section].remove(key)
        json.dump(self.dictionary, open(self.address, "w", encoding="utf-8"))
        self.dictionary = json.load(open(self.address, encoding="utf-8"))

