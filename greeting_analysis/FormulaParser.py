from elements.Element import Element as Element
from elements.Epithet import Epithet as Epithet
from RareFormula import RareFormula
from JsonDictionaryAnalyzer import JsonDictionaryAnalyzer
from FormulaAnalyzer import FormulaAnalyzer
from Formula import Formula
import re


class FormulaParser:
    def __init__(self, dictionary_analyzer=JsonDictionaryAnalyzer(), formula_analyzer=FormulaAnalyzer()):
        self.dictionary_analyzer = dictionary_analyzer
        self.formula_analyzer = formula_analyzer

    def prepare_elements(self, data):
        elements = []
        data_without_trash = re.sub('[^a-zA-ZäüößÄÖÜ\s]', '', data).split()
        for word_name in data_without_trash:
            current_element = Element(word_name.lower(), self.dictionary_analyzer)
            if not current_element.group.name:
                possible = re.sub(r'([A-ZÄÖÜ])', r' \1', word_name).lower().split()
                for el in possible:
                    if current_element.word.name not in {'p', 'pp'} :
                        elements.append(Element(el.lower(), self.dictionary_analyzer))
            else:
                elements.append(current_element)
        return elements

    def get_rare_formula(self, pre_elements):
        elements = []
        length = len(pre_elements)
        j = 0
        for i in range(len(pre_elements)):
            element = pre_elements[i]
            if i < length - 1 and (element.word.name in self.dictionary_analyzer.prefixes or element.group.name == "H"):
                next_element = pre_elements[i + 1]
                if (next_element.group_type == "Epithet" and element.word.name in self.dictionary_analyzer.prefixes) or \
                        ((next_element.group.name == "S" or next_element.group.name == "R" or
                          next_element.group.name == "und") and element.group.name == "H"):
                    if next_element.group.name == "und":
                        if pre_elements[i+2].group.name == "R":
                            next_element = pre_elements[i+2]
                            j+=1
                        else:
                            continue
                    element = Element(f"{element.word.name} {next_element.word.name}", self.dictionary_analyzer)
                    element.group = next_element.group.name
                    elements.append(element)
                    j += 2
                    continue
            if i == j:
                elements.append(element)
                j += 1
        rare_formula = RareFormula(elements)
        return rare_formula

    def parse(self, data, manual=False) -> Formula:
        pre_elements = self.prepare_elements(data)
        rare_formula = self.get_rare_formula(pre_elements)
        formula = self.formula_analyzer.get_formula(rare_formula, manual)
        return formula

