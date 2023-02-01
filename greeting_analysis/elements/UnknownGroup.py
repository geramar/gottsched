from Group import Group


class UnknownGroup(Group):
    def get_correlation(self):
        return None

    def get_subtype(self):
        return "UnknownType"