from Group import Group


class Epithet(Group):
    def get_correlation(self):
        return self.analyzer.get_nomination(self.name)

    def get_subtype(self):
        return "Epithet"