from enum import Enum

class TokenType(Enum):
    DECIMAL_NUMBER = 0,
    INTEGER_NUMBER = 1,
    IDENT = 2
    PAR_OPEN = 3
    PAR_CLOSE = 4
    OP_PLUS = 5
    OP_MINUS = 6
    OP_MULTIPLY = 7
    OP_DIVIDE = 8
    OP_GREATER = 9
    OP_GREATER_EQUAL = 10
    OP_LESS = 11
    OP_LESS_EQUAL = 12
    OP_EQUAL = 13
    OP_ASSIGN = 14
    COMMA = 15

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __repr__(self):
        return '{}(\'{}\')'.format(self.type.name, self.value)
