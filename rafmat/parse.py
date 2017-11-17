import rafmat.ast_node as an
from enum import Enum
from .token import Token, TokenType
from .parse_result import ParseResult

OP_PRIORITY = {
        # Assignment
        TokenType.OP_ASSIGN: 0,

        # Comparison
        TokenType.OP_GREATER: 1,
        TokenType.OP_LESS: 1,
        TokenType.OP_GREATER_EQUAL: 1,
        TokenType.OP_LESS_EQUAL: 1,
        TokenType.OP_EQUAL: 1,

        # Arithmetic
        TokenType.OP_PLUS: 2,
        TokenType.OP_MINUS: 2,
        TokenType.OP_MULTIPLY: 3,
        TokenType.OP_DIVIDE: 3,
        }

class ParseError(ValueError):
    def __init__(self, pos, message):
        self.pos = pos
        self.message = message

def is_operator(token):
    return token.type in OP_PRIORITY.keys()

def is_operand(token):
    return token.type in [ TokenType.DECIMAL_NUMBER, TokenType.INTEGER_NUMBER, TokenType.IDENT ]

def node_from_operand(operand):
    if operand.type == TokenType.IDENT:
        return an.VariableAstNode(operand.value)
    elif operand.type == TokenType.INTEGER_NUMBER:
        return an.NumberAstNode(operand.value, True)
    elif operand.type == TokenType.DECIMAL_NUMBER:
        return an.NumberAstNode(operand.value, False)
    else:
        raise ValueError("Not a valid operand: " + str(operand))

def node_from_function_call(name, tokens, pos):
    if tokens[pos].type != TokenType.PAR_OPEN:
        raise ValueError("Unexpected function call parse params")

    pos += 1
    level = 0
    tokens_in_arg = []
    args = []

    while pos < len(tokens):
        token = tokens[pos]

        if token.type == TokenType.PAR_CLOSE:
            level -= 1

        if token.type == TokenType.PAR_OPEN:
            level += 1

        if token.type == TokenType.COMMA or level < 0:
            args.append(tokens_in_arg)
            tokens_in_arg = []
        else:
            tokens_in_arg.append(token)

        if level < 0:
            pos += 1
            break

        pos += 1

    return ParseResult(an.FunctionCallAstNode(name,
        [parse_parenthesised(parenthesize(arg), 0).node for
        arg in args]), pos)

def node_from_operator(operator, left_operand, right_operand):
    t = operator.type
    if t == TokenType.OP_PLUS:
        return an.PlusAstNode(left_operand, right_operand)
    elif t == TokenType.OP_MINUS:
        return an.MinusAstNode(left_operand, right_operand)
    elif t == TokenType.OP_MULTIPLY:
        return an.MultiplyAstNode(left_operand, right_operand)
    elif t == TokenType.OP_DIVIDE:
        return an.DivideAstNode(left_operand, right_operand)
    elif t == TokenType.OP_GREATER:
        return an.GreaterAstNode(left_operand, right_operand)
    elif t == TokenType.OP_GREATER_EQUAL:
        return an.GreaterEqualAstNode(left_operand, right_operand)
    elif t == TokenType.OP_LESS:
        return an.LessAstNode(left_operand, right_operand)
    elif t == TokenType.OP_LESS_EQUAL:
        return an.LessEqualAstNode(left_operand, right_operand)
    elif t == TokenType.OP_EQUAL:
        return an.EqualAstNode(left_operand, right_operand)
    elif t == TokenType.OP_ASSIGN:
        if not isinstance(left_operand, an.VariableAstNode):
            raise ParseError(-1, "Invalid assignment")

        return an.AssignmentAstNode(left_operand.name, right_operand)
    else:
        raise ValueError("Not a valid operator: " + str(operator))

def parse_operand(tokens, pos):
    operand = tokens[pos]
    operand_node = None

    if operand.type == TokenType.PAR_OPEN:
        # recursive descent
        result = parse_parenthesised(tokens, pos)
        operand_node = result.node
        pos = result.new_pos + 1
    else:
        if not is_operand(operand):
            raise ParseError(pos, "Not a valid operand: {}".format(operand))

        if operand.type == TokenType.IDENT and pos < len(tokens) - 1 and tokens[pos + 1].type == TokenType.PAR_OPEN:
            result = node_from_function_call(operand.value, tokens, pos + 1)
            pos = result.new_pos
            operand_node = result.node
        else:
            operand_node = node_from_operand(operand)
            pos += 1

    return ParseResult(operand_node, pos)


def parse_priority(tokens, pos, priority):
    result = parse_operand(tokens, pos)
    pos = result.new_pos
    node = result.node

    while pos < len(tokens):
        operator = tokens[pos]
        if operator.type == TokenType.PAR_CLOSE:
            break

        if not is_operator(operator):
            raise ParseError(pos, "Not a valid operator: {}".format(operator))

        if OP_PRIORITY[operator.type] <= priority:
            break

        pos += 1
        result = parse_operand(tokens, pos)
        other = result.node
        pos = result.new_pos
        node = node_from_operator(operator, node, other)

    return ParseResult(node, pos)

def parenthesize(tokens):
    return [Token(TokenType.PAR_OPEN, '(')] + tokens + [Token(TokenType.PAR_CLOSE, ')')]

def parse_parenthesised(tokens, pos):
    if tokens[pos].type != TokenType.PAR_OPEN:
        raise ParseError(pos, "Internal error: expected PAR_OPEN")

    pos += 1
    result = parse_operand(tokens, pos)
    pos = result.new_pos
    node = result.node

    while pos < len(tokens):
        operator = tokens[pos]

        if operator.type == TokenType.PAR_CLOSE:
            break

        if not is_operator(operator):
            raise ParseError(pos, "Invalid operator: {}".format(operator))

        pos += 1
        result = parse_priority(tokens, pos, OP_PRIORITY[operator.type])
        pos = result.new_pos
        other = result.node
        node = node_from_operator(operator, node, other)

    if pos >= len(tokens):
        raise ParseError(pos, "Unbalanced parentheses")

    return ParseResult(node, pos)

def parse(tokens):
    return parse_parenthesised(parenthesize(tokens), 0).node
