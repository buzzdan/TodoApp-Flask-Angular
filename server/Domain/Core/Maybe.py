class Maybe:
    def __init__(self, value=None):
        self._values = []
        if value:
            self._values.append(value)

    def exists(self):
        return len(self._values) > 0

    def values(self):
        return self._values
