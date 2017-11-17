class Variable:
    def __init__(self):
        self.value = None
        self._is_int = False

    def get(self):
        return self.value

    def is_int(self):
        return self._is_int

    def set(self, value, is_int = False):
        self.value = value
        self._is_int = is_int
