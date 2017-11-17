from enum import Enum

class NumberAstNode:
    def __init__(self, number, is_int):
        self.number = float(number)
        self._is_int = is_int

    def eval(self, ident_table):
        return self.number

    def is_int(self):
        return self._is_int

    def __repr__(self):
        return 'Num({})'.format(self.number)

class VariableAstNode:
    def __init__(self, name):
        self.name = name

    def eval(self, ident_table):
        return ident_table.get_variable(self.name).get()

    def is_int(self):
        return False

    def __repr__(self):
        return 'Var(`{}`)'.format(self.name)

class FunctionCallAstNode:
    def __init__(self, name, param_nodes):
        self.name = name
        self.param_nodes = param_nodes

    def eval(self, ident_table):
        fn = ident_table.get_function(self.name)
        if len(self.param_nodes) != fn.args_count:
            raise RuntimeError('The function `{}` expects {} arguments, but {} given'
                    .format(self.name, fn.args_count, len(self.param_nodes)))

        return fn.call([n.eval(ident_table) for n in self.param_nodes])

    def __repr__(self):
        params = ', '.join([str(p) for p in self.param_nodes])
        return '`{}`({})'.format(self.name, params)

class AssignmentAstNode:
    def __init__(self, var_name, val_node):
        self.var_name = var_name
        self.val_node = val_node

    def eval(self, ident_table):
        val = self.val_node.eval(ident_table)
        ident_table.get_variable_for_assignment(self.var_name).set(val)
        return val

    def __repr__(self):
        return '(`{}` = {})'.format(self.var_name, self.val_node)

class BinaryOpAstNode:
    def __init__(self, left_node, right_node):
        self.left_node = left_node
        self.right_node = right_node

    def eval(self, ident_table):
        res = self.apply_op(self.left_node.eval(ident_table),
                self.right_node.eval(ident_table))
        if self.left_node.is_int() and self.right_node.is_int():
            return int(res)
        else:
            return res

    def get_symbol(self):
        raise NotImplementedError('BinaryOpAstNode.get_symbol is abstract')

    def apply_op(self, left, right):
        raise NotImplementedError('BinaryOpAstNode.apply_op is abstract')

    def is_int(self):
        return self.left_node.is_int() and self.right_node.is_int()

    def __repr__(self):
        return '({} {} {})'.format(self.left_node, self.get_symbol(),
                self.right_node)

class PlusAstNode(BinaryOpAstNode):
    def apply_op(self, left, right):
        return left + right

    def get_symbol(self):
        return '+'

class MinusAstNode(BinaryOpAstNode):
    def apply_op(self, left, right):
        return left - right

    def get_symbol(self):
        return '-'

class MultiplyAstNode(BinaryOpAstNode):
    def apply_op(self, left, right):
        return left * right

    def get_symbol(self):
        return '*'

class DivideAstNode(BinaryOpAstNode):
    def apply_op(self, left, right):
        return left / right

    def get_symbol(self):
        return '/'

class GreaterAstNode(BinaryOpAstNode):
    def apply_op(self, left, right):
        return left > right

    def get_symbol(self):
        return '>'

class GreaterEqualAstNode(BinaryOpAstNode):
    def apply_op(self, left, right):
        return left >= right

    def get_symbol(self):
        return '>='

class LessAstNode(BinaryOpAstNode):
    def apply_op(self, left, right):
        return left < right

    def get_symbol(self):
        return '<'

class LessEqualAstNode(BinaryOpAstNode):
    def apply_op(self, left, right):
        return left <= right

    def get_symbol(self):
        return '<='

class EqualAstNode(BinaryOpAstNode):
    def apply_op(self, left, right):
        return left == right

    def get_symbol(self):
        return '=='

