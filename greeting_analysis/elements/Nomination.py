from Group import Group


class Nomination(Group):
    def get_correlation(self):
        return self.analyzer.get_epithets(self.name)

    def get_subtype(self):
        return "Nomination"