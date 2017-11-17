import math

class SinFunction:
    def __init__(self):
        self.args_count = 1

    def call(self, args):
        return math.sin(args[0])

class CosFunction:
    def __init__(self):
        self.args_count = 1

    def call(self, args):
        return math.cos(args[0])

class TanFunction:
    def __init__(self):
        self.args_count = 1

    def call(self, args):
        return math.tan(args[0])

class CtgFunction:
    def __init__(self):
        self.args_count = 1

    def call(self, args):
        return 1 / math.tan(args[0])

class SqrtFunction:
    def __init__(self):
        self.args_count = 1

    def call(self, args):
        return math.sqrt(args[0])

class PowFunction:
    def __init__(self):
        self.args_count = 2

    def call(self, args):
        return math.pow(args[0], args[1])

class LogFunction:
    def __init__(self):
        self.args_count = 1

    def call(self, args):
        return math.log10(args[0])
