"""Simple calculator implementation used by tests.

Provides a Calculator class with basic arithmetic methods and a safe
evaluate(expression) helper which parses arithmetic expressions using ast
to avoid using Python's eval on untrusted input.

Methods:
 - add(a, b)
 - subtract(a, b)
 - multiply(a, b)
 - divide(a, b)  # raises ValueError on division by zero
 - power(a, b)
 - sqrt(a)       # raises ValueError for negative input
 - evaluate(expr)  # safe arithmetic expression evaluator

This module intentionally keeps a small, well-tested surface so tests
can exercise the functionality easily.
"""

from __future__ import annotations

import ast
import math
import operator as _op
from typing import Any

__all__ = ["Calculator"]


class _EvalVisitor(ast.NodeVisitor):
    """AST visitor that evaluates simple arithmetic expressions safely.

    Allowed nodes: Expression, BinOp, UnaryOp, Num/Constant, Paren,
    and the operators +, -, *, /, **, //, %, unary + and -.
    """

    _operators = {
        ast.Add: _op.add,
        ast.Sub: _op.sub,
        ast.Mult: _op.mul,
        ast.Div: _op.truediv,
        ast.Pow: _op.pow,
        ast.FloorDiv: _op.floordiv,
        ast.Mod: _op.mod,
    }

    _unary_ops = {ast.UAdd: lambda x: x, ast.USub: lambda x: -x}

    def visit(self, node: ast.AST) -> Any:
        method = "visit_" + node.__class__.__name__
        visitor = getattr(self, method, None)
        if visitor is None:
            raise ValueError(
                f"Unsupported expression element: {node.__class__.__name__}"
            )
        return visitor(node)

    def visit_Expression(self, node: ast.Expression) -> Any:
        return self.visit(node.body)

    def visit_BinOp(self, node: ast.BinOp) -> Any:
        left = self.visit(node.left)
        right = self.visit(node.right)
        op_type = type(node.op)
        if op_type not in self._operators:
            raise ValueError(f"Unsupported operator: {op_type.__name__}")
        return self._operators[op_type](left, right)

    def visit_UnaryOp(self, node: ast.UnaryOp) -> Any:
        operand = self.visit(node.operand)
        op_type = type(node.op)
        if op_type not in self._unary_ops:
            raise ValueError(f"Unsupported unary operator: {op_type.__name__}")
        return self._unary_ops[op_type](operand)

    def visit_Num(self, node: ast.Num) -> Any:  # type: ignore
        return node.n

    def visit_Constant(self, node: ast.Constant) -> Any:  # for py3.8+
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Only numeric constants are allowed")


class Calculator:
    """A lightweight calculator with a small, testable API."""

    def add(self, a: float, b: float) -> float:
        return a + b

    def subtract(self, a: float, b: float) -> float:
        return a - b

    def multiply(self, a: float, b: float) -> float:
        return a * b

    def divide(self, a: float, b: float) -> float:
        if b == 0:
            raise ValueError("division by zero")
        return a / b

    def power(self, a: float, b: float) -> float:
        return a**b

    def sqrt(self, a: float) -> float:
        if a < 0:
            raise ValueError("square root of negative number")
        return math.sqrt(a)

    def evaluate(self, expr: str) -> float:
        """Safely evaluate a simple arithmetic expression and return a number.

        Only basic arithmetic is supported. Raises ValueError for unsupported
        nodes or malformed expressions.
        """
        try:
            parsed = ast.parse(expr, mode="eval")
        except SyntaxError as ex:
            raise ValueError("invalid expression") from ex
        visitor = _EvalVisitor()
        result = visitor.visit(parsed)
        if not isinstance(result, (int, float)):
            raise ValueError("expression did not produce a numeric result")
        return float(result)


if __name__ == "__main__":
    # simple CLI: evaluate expression passed as first argument
    import sys

    if len(sys.argv) < 2:
        print("Usage: python -m src.main '<expression>'")
        sys.exit(2)
    expr = sys.argv[1]
    calc = Calculator()
    try:
        print(calc.evaluate(expr))
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
