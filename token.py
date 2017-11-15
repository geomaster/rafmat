from enum import Enum

class TokenType(Enum):
    NUMBER = 0
    IDENT = 1
    PAR_OPEN = 2
    PAR_CLOSE = 3
    OP_PLUS = 4
    OP_MINUS = 5
    OP_MULTIPLY = 6
    OP_DIVIDE = 7
    OP_GREATER = 8
    OP_GREATER_EQUAL = 9
    OP_LESS = 10
    OP_LESS_EQUAL = 11
    OP_EQUAL = 12
    OP_ASSIGN = 13
    COMMA = 14

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __repr__(self):
        return '{}(\'{}\')'.format(self.type.name, self.value)
