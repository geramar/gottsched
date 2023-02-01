class Formula:
    def __init__(self, rare_formula, shadow):
        self._rare_formula = rare_formula
        self._shadow = shadow

    @property
    def elements_with_und(self):
        return self._rare_formula.elements_with_und

    @property
    def elements(self):
        return self._rare_formula.elements

    @property
    def elements_without_modificators(self):
        return self._rare_formula.elements_without_modificators

    @property
    def shadow(self):
        return self._shadow