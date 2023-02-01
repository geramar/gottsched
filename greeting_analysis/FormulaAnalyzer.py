from RareFormula import RareFormula
from Formula import Formula
from Shadow import Shadow
from ManualAnalyzer import ManualAnalyzer

class FormulaAnalyzer:
    def __init__(self):
        self.sequence = {'h1': 1, 'h2': 2, 'H': 3, 's3': 4, 's4': 5, 'S': 6, 'r5': 7, 'r6': 8, 'R': 9}
        self.indexes = {value:key for (key,value) in self.sequence.items()}

    def _get_shadow(self, elements):
        previous_index = 0
        for i in range(1, len(elements)):
            element = elements[i]
            group = element.group.name
            index = self.sequence[group]
            shadow_groups = []
            if index < previous_index:
                if element.group_type == "Epithet":
                    shadow_groups.append(group)
                    for j in range(i+1, len(elements)):
                        group = elements[j].group.name
                        index = self.sequence[group]
                        if index < previous_index:
                            shadow_groups.append(group)
                    nomination = self.indexes[previous_index]
                    relative_position = -1
                else:
                    nomination = group
                    for j in range(i-1):
                        group = elements[j].group.name
                        cur_index = self.sequence[group]
                        if cur_index > index:
                            shadow_groups.append(group)
                    shadow_groups.append(self.indexes[previous_index])
                    relative_position = 1
                shadow = Shadow(shadow_groups, nomination, relative_position)
                return shadow
            previous_index = index
        return None

    def _check_H(self, rare_formula):
        groups = rare_formula.groups
        index = groups.index("H")
        if ("S" in groups and groups.index("S") < index) or ("R" in groups and groups.index("R") - 1 == index):
            rare_formula.change_group(index, "R")
        return rare_formula

    def get_formula(self, rare_formula: RareFormula, manual=False):
        groups = rare_formula.groups
        if "H" in groups:
            rare_formula = self._check_H(rare_formula)
        if all(groups):
            shadow = self._get_shadow(rare_formula.elements_without_modificators)
            return Formula(rare_formula, shadow)
        else:
            if manual:
                if len(set(groups)) > 2:
                    manual_analyzer = ManualAnalyzer()
                    new_rare_formula = manual_analyzer.analyze(rare_formula)
                    if new_rare_formula:
                        return self.get_formula(new_rare_formula)
            return None








