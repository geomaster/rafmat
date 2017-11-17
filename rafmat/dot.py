import rafmat.ast_node as an

def dot_repr_node(node, guid):
    if isinstance(node, an.Number):
        return 'n{} [label="Num({})"]'.format(guid, node.number)
    elif isinstance(node, an.Variable):
        return 'n{} [label="Var(`{}`)"]'.format(guid, node.name)
    elif isinstance(node, an.FunctionCall):
        return 'n{} [label="FnCall(`{}`)"]'.format(guid, node.name)
    elif isinstance(node, an.Assignment):
        return 'n{} [label="Assign(Var(`{}`))"]'.format(guid, node.var_node.name)
    elif isinstance(node, an.BinaryOp):
        return 'n{} [label="{}"]'.format(guid, node.get_symbol())
    else:
        return 'n{} [label="Unknown"]'.format(guid)

def dot_repr_nodes(nodes):
    res = ';\n'.join([dot_repr_node(node, i) for (i, node) in enumerate(nodes)])

    node_map = {}
    for (i, node) in enumerate(nodes):
        node_map[node] = i

    return (res, node_map)

def collect_nodes(node, nodes):
    nodes.append(node)
    if isinstance(node, an.BinaryOp):
        nodes = collect_nodes(node.left_node, nodes)
        nodes = collect_nodes(node.right_node, nodes)
    elif isinstance(node, an.FunctionCall):
        for p in node.param_nodes:
            nodes = collect_nodes(p, nodes)
    elif isinstance(node, an.Assignment):
        nodes = collect_nodes(node.val_node, nodes)

    return nodes

def dot_repr(node, node_map):
    node_id = node_map[node]
    if isinstance(node, an.FunctionCall):
        return '\n'.join(['n{} -> n{};'.format(node_id, node_map[param_node]) for
            param_node in node.param_nodes])
    elif isinstance(node, an.Assignment):
        return 'n{} -> n{};'.format(node_id, node_map[node.val_node])
    elif isinstance(node, an.BinaryOp):
        return 'n{} -> n{};\nn{} -> n{};'.format(node_id,
                node_map[node.left_node], node_id, node_map[node.right_node])
    else:
        return ''

def to_dot(node):
    nodes = collect_nodes(node, [])
    (nodes_dot, node_map) = dot_repr_nodes(nodes)

    return 'digraph AST {}\n{}\n{}\n{}'.format('{', nodes_dot,
            '\n'.join(dot_repr(node, node_map) for node in nodes), '}')

