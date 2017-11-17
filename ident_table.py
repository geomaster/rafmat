import function
from variable import Variable

FUNCTIONS = {
        'sin': function.SinFunction(),
        'cos': function.CosFunction(),
        'tan': function.TanFunction(),
        'ctg': function.CtgFunction(),
        'sqrt': function.SqrtFunction(),
        'pow': function.PowFunction(),
        'log': function.LogFunction()
        }

class IdentTable:
    def __init__(self):
        self.variables = {}

    def get_variable_for_assignment(self, name):
        var = None
        if name not in self.variables.keys():
            var = Variable()
            self.variables[name] = var
        else:
            var = self.variables[name]

        return var

    def get_variable(self, name):
        if name not in self.variables.keys():
            raise RuntimeError('Variable `{}` does not exist'.format(name))

        return self.variables[name]

    def get_function(self, name):
        if name not in FUNCTIONS.keys():
            raise RuntimeError('Function `{}` does not exist'.format(name))

        return FUNCTIONS[name]
