class Referee(object):
    def __init__(self):
        self.command = Command()


class Stage(object):
    def __init__(self):
        pass


class Command(object):
    def __init__(self, name="HALT"):
        self.name = name


class Team(object):
    def __init__(self):
        pass
