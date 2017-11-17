from enum import Enum

class Number:
    def __init__(self, number, is_int):
        self.number = float(number)
        self._is_int = is_int

    def eval(self, ident_table):
        return self.number

    def is_int(self):
        return self._is_int

    def eval_for_comparison(self, ident_table):
        return self.eval(ident_table)

    def visit_children(self, fn):
        return

    def __repr__(self):
        return 'Num({})'.format(self.number)

class Variable:
    def __init__(self, name):
        self.name = name

    def eval(self, ident_table):
        return ident_table.get_variable(self.name).get()

    def is_int(self):
        return False

    def eval_for_comparison(self, ident_table):
        return self.name

    def visit_children(self, fn):
        return

    def __repr__(self):
        return 'Var(`{}`)'.format(self.name)

class FunctionCall:
    def __init__(self, name, param_nodes):
        self.name = name
        self.param_nodes = param_nodes

    def eval(self, ident_table):
        fn = ident_table.get_function(self.name)
        if len(self.param_nodes) != fn.args_count:
            raise RuntimeError('The function `{}` expects {} arguments, but {} given'
                    .format(self.name, fn.args_count, len(self.param_nodes)))

        return fn.call([n.eval(ident_table) for n in self.param_nodes])

    def is_int(self):
        return False

    def eval_for_comparison(self, ident_table):
        return self.eval(ident_table)

    def visit_children(self, fn):
        for p in self.param_nodes:
            fn(p)

    def __repr__(self):
        params = ', '.join([str(p) for p in self.param_nodes])
        return '`{}`({})'.format(self.name, params)

class Assignment:
    def __init__(self, var_node, val_node):
        self.var_node = var_node
        self.val_node = val_node

    def eval(self, ident_table):
        var_name = self.var_node.eval_for_comparison(ident_table)
        val = self.val_node.eval(ident_table)
        ident_table.get_variable_for_assignment(var_name).set(val)
        return val

    def eval_for_comparison(self, ident_table):
        return self.var_node.eval_for_comparison(ident_table)

    def visit_children(self, fn):
        fn(self.var_node)

    def __repr__(self):
        return '(`{}` = {})'.format(self.var_node, self.val_node)

class BinaryOp:
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
        raise NotImplementedError('BinaryOp.get_symbol is abstract')

    def apply_op(self, left, right):
        raise NotImplementedError('BinaryOp.apply_op is abstract')

    def is_int(self):
        return self.left_node.is_int() and self.right_node.is_int()

    def eval_for_comparison(self, ident_table):
        return self.var_name

    def visit_children(self, fn):
        fn(self.left_node)
        fn(self.right_node)

    def __repr__(self):
        return '({} {} {})'.format(self.left_node, self.get_symbol(),
                self.right_node)

class ComparisonOp(BinaryOp):
    def eval(self, ident_table):
        left_c = self.left_node.eval_for_comparison(ident_table)
        right_c = self.right_node.eval_for_comparison(ident_table)
        left_e = self.left_node.eval(ident_table)
        right_e = self.right_node.eval(ident_table)
        return left_e and right_e and bool(self.apply_op(left_c, right_c))

    def eval_for_comparison(self, ident_table):
        return self.right_node.eval_for_comparison(ident_table)

class Plus(BinaryOp):
    def apply_op(self, left, right):
        return left + right

    def get_symbol(self):
        return '+'

class Minus(BinaryOp):
    def apply_op(self, left, right):
        return left - right

    def get_symbol(self):
        return '-'

class Multiply(BinaryOp):
    def apply_op(self, left, right):
        return left * right

    def get_symbol(self):
        return '*'

class Divide(BinaryOp):
    def apply_op(self, left, right):
        return left / right

    def get_symbol(self):
        return '/'

class Greater(ComparisonOp):
    def apply_op(self, left, right):
        return left > right

    def get_symbol(self):
        return '>'

class GreaterEqual(ComparisonOp):
    def apply_op(self, left, right):
        return left >= right

    def get_symbol(self):
        return '>='

class Less(ComparisonOp):
    def apply_op(self, left, right):
        return left < right

    def get_symbol(self):
        return '<'

class LessEqual(ComparisonOp):
    def apply_op(self, left, right):
        return left <= right

    def get_symbol(self):
        return '<='

class Equal(ComparisonOp):
    def apply_op(self, left, right):
        return left == right

    def get_symbol(self):
        return '=='

