from Formula import Formula
from FormulaParser import FormulaParser
from Schema import Schema


class SchemaMaker:
    def _get_schema_elements(self, elements, modificators=True, detailed_roles=True):
        schema_elements = []
        modificators_number = 0
        for element in elements:
            group_name = element.group.name
            group_type = element.group_type
            if group_type == "Modificator":
                if not modificators:
                    continue
                else:
                    group_name = f"{group_name}("
                    modificators_number += 1
            elif group_name == "R":
                if detailed_roles:
                    name = element.word.name.split()
                    detail = name[0][0].upper() if len(name) == 1 else name[1][0].upper()
                    group_name = f"{group_name}{detail}"
                else:
                    if schema_elements[-1] == "R":
                        continue
            if group_type == "Nomination" and modificators_number:
                brackets = ")" * modificators_number
                group_name = f"{brackets}-{group_name}"
                modificators_number = 0
            schema_elements.append(group_name)
        return schema_elements

    def _get_shadow_index(self, elements, shadow):
        groups = [element.group.name for element in elements]
        nomination_index = groups.index(shadow.nomination)
        shadow_index = nomination_index + shadow.relative_position
        return shadow_index

    def _create_schema(self, formula, modificators=True, detailed_roles=True, manual=False):
        elements = formula.elements if modificators else formula.elements_without_modificators
        schema_elements = self._get_schema_elements(elements, modificators, detailed_roles)
        shadow = formula.shadow
        if shadow:
            shadow_index = self._get_shadow_index(elements, shadow)
            schema_elements.insert(shadow_index, f"[{'-'.join(shadow.groups_list)}]")
        schema = "-".join(schema_elements).replace("(-", "(").replace("-)", ")")
        return schema

    def get_schema(self, greeting, manual=False):
        formula = FormulaParser().parse(greeting, manual)
        if not formula:
            return None
        short = self._create_schema(formula, False, False)
        long = self._create_schema(formula, True, True)
        only_modificators = self._create_schema(formula, True, False)
        only_roles = self._create_schema(formula, False, True)
        schema = Schema(short, long, only_modificators, only_roles)
        return schema

