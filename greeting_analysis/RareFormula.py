from elements.Element import Element


class RareFormula():
    def __init__(self, elements: list[Element]):
        self._elements_with_und = elements

    @property
    def elements_with_und(self):
        return self._elements_with_und

    @property
    def elements(self):
        return [element for element in self.elements_with_und if element.group.name != "und"]

    @property
    def elements_without_modificators(self):
        return [element for element in self.elements if element.group_type != 'Modificator']

    @property
    def groups(self):
        return [element.group.name for element in self.elements_without_modificators]

    @property
    def words(self):
        return [element.word.name for element in self.elements_without_modificators]

    @property
    def indexes(self):
        words_with_und = [element.word.name for element in self.elements_with_und]
        indexes = [words_with_und.index(element) for element in self.words]
        return indexes

    def change_group(self, index, group_name):
        self._elements_with_und[index].group = group_name

    def change_word(self, index, word_name):
        self._elements_with_und[index].word = word_name

    def delete_element(self, index):
        self._elements_with_und.pop(index)