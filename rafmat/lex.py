from .token import TokenType, Token
from .match_result import MatchResult

LITERAL_TOKENS = [
        # 2 chars
        TokenType.OP_GREATER_EQUAL,
        TokenType.OP_LESS_EQUAL,
        TokenType.OP_EQUAL,

        # 1 char
        TokenType.PAR_OPEN,
        TokenType.PAR_CLOSE,

        TokenType.OP_PLUS,
        TokenType.OP_MINUS,
        TokenType.OP_MULTIPLY,
        TokenType.OP_DIVIDE,
        TokenType.OP_GREATER,
        TokenType.OP_LESS,
        TokenType.OP_ASSIGN,

        TokenType.COMMA
        ]

TOKEN_LITERALS = {
        TokenType.OP_GREATER_EQUAL: '>=',
        TokenType.OP_LESS_EQUAL:    '<=',
        TokenType.OP_EQUAL:         '==',

        TokenType.PAR_OPEN:         '(',
        TokenType.PAR_CLOSE:        ')',

        TokenType.OP_PLUS:          '+',
        TokenType.OP_MINUS:         '-',
        TokenType.OP_MULTIPLY:      '*',
        TokenType.OP_DIVIDE:        '/',
        TokenType.OP_GREATER:       '>',
        TokenType.OP_LESS:          '<',
        TokenType.OP_ASSIGN:        '=',

        TokenType.COMMA:            ','
        }

def try_match_literal(stream, token_type, target):
    n = len(target)
    if stream[:n] == target:
        return MatchResult(True, Token(token_type, target), n)

    return MatchResult(False, None, 0)

def is_valid_in_number(c):
    return c == '.' or c.isdigit()

def try_match_number(stream):
    if not is_valid_in_number(stream[0]):
        return MatchResult(False, None, 0)

    seen_period = False
    t = TokenType.INTEGER_NUMBER
    for (i, c) in enumerate(stream):
        if c == '.':
            t = TokenType.DECIMAL_NUMBER
            if seen_period:
                return MatchResult(False, None, 0)
            else:
                seen_period = True

        if not is_valid_in_number(c):
            return MatchResult(True, Token(t, stream[:i]), i)

    return MatchResult(True, Token(t, stream), len(stream))

def is_valid_in_ident(c, is_first_char):
    if is_first_char:
        return c.isalpha() or c == '_'
    else:
        return c.isalnum() or c == '_'

def try_match_ident(stream):
    if not is_valid_in_ident(stream[0], True):
        return MatchResult(False, None, stream)

    for (i, c) in enumerate(stream):
        if not is_valid_in_ident(c, i == 0):
            return MatchResult(True, Token(TokenType.IDENT, stream[:i]), i)

    return MatchResult(True, Token(TokenType.IDENT, stream), len(stream))

class LexError(ValueError):
    def __init__(self, pos, message):
        self.pos = pos
        self.message = message

def lex(stream):
    tokens = []
    pos = 0
    while pos < len(stream):
        rest = stream[pos:]
        if rest[0] == ' ':
            pos += 1
            continue

        result = MatchResult(False, None, 0)
        for token_type in LITERAL_TOKENS:
            literal = TOKEN_LITERALS[token_type]
            result = try_match_literal(rest, token_type, literal)

            if result.succeeded:
                break

        if not result.succeeded:
            result = try_match_number(rest)

        if not result.succeeded:
            result = try_match_ident(rest)

        if not result.succeeded:
            raise LexError(pos, "No suitable token at character `{}`".format(rest[0]))

        tokens.append(result.token)
        pos += result.advance

    return tokens


