import ast
import operator

# Supported operators mapping
_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}


def _eval_node(node: ast.AST) -> float:
    """Recursively evaluate an AST node representing a simple expression."""
    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        op_type = type(node.op)
        if op_type not in _OPERATORS:
            raise ValueError(f"Unsupported operator: {op_type.__name__}")
        return _OPERATORS[op_type](left, right)
    if isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand)
        if isinstance(node.op, ast.UAdd):
            return +operand
        if isinstance(node.op, ast.USub):
            return -operand
        raise ValueError(f"Unsupported unary operator: {type(node.op).__name__}")
    if isinstance(node, ast.Num):
        return node.n
    raise ValueError(f"Unsupported expression element: {type(node).__name__}")


def evaluate(expression: str) -> float:
    """Evaluate a simple arithmetic expression and return the result."""
    tree = ast.parse(expression, mode="eval")
    return _eval_node(tree.body)


def main() -> None:
    print("Simple Calculator. Type 'exit' to quit.")
    while True:
        expr = input('> ')
        if expr.lower() in {"exit", "quit"}:
            break
        try:
            result = evaluate(expr)
            print(result)
        except Exception as exc:
            print(f"Error: {exc}")


if __name__ == "__main__":
    main()
