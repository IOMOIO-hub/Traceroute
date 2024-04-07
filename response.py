class Response:
    def __init__(self, a_system="", desc="", country=""):
        self._desc = desc
        self._country = country
        self._a_system = a_system

    def to_list(self):
        return [self._desc, self._country, self._a_system]
