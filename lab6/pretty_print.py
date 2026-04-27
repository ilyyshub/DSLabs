from __future__ import annotations

from ast_nodes import (
    ArrayExpr,
    BinaryExpr,
    CallExpr,
    ExprStatement,
    FunctionStatement,
    IdentifierExpr,
    IfStatement,
    LetStatement,
    LiteralExpr,
    MapExpr,
    PrintStatement,
    Program,
    ReturnStatement,
    UnaryExpr,
    WhileStatement,
)
from tokens import Token


def print_tokens(tokens: list[Token]) -> None:
    header = f"{'TYPE':<12} {'LEXEME':<16} {'VALUE':<14} {'LINE':>4} {'COL':>4}"
    print(header)
    print("-" * len(header))
    for token in tokens:
        value = repr(token.value) if token.value is not None else ""
        print(f"{token.type.name:<12} {token.lexeme!r:<16} {value:<14} {token.line:>4} {token.column:>4}")


def print_ast(program: Program) -> None:
    print("Program")
    roots = [_stmt_to_tree(stmt) for stmt in program.statements]
    _print_branches(roots, prefix="")


def _print_branches(nodes: list[tuple[str, list[tuple[str, list]]]], prefix: str) -> None:
    for i, (label, children) in enumerate(nodes):
        is_last = i == len(nodes) - 1
        branch = "`-- " if is_last else "|-- "
        print(f"{prefix}{branch}{label}")
        child_prefix = f"{prefix}{'    ' if is_last else '|   '}"
        _print_branches(children, child_prefix)


def _stmt_to_tree(stmt: object) -> tuple[str, list[tuple[str, list]]]:
    if isinstance(stmt, LetStatement):
        return (f"Let({stmt.name})", [_expr_to_tree(stmt.value)])
    if isinstance(stmt, PrintStatement):
        return ("Print", [_expr_to_tree(stmt.expression)])
    if isinstance(stmt, ReturnStatement):
        return ("Return", [_expr_to_tree(stmt.expression)])
    if isinstance(stmt, ExprStatement):
        return ("ExprStmt", [_expr_to_tree(stmt.expression)])
    if isinstance(stmt, WhileStatement):
        return (
            "While",
            [
                ("Condition", [_expr_to_tree(stmt.condition)]),
                ("Body", [_stmt_to_tree(s) for s in stmt.body]),
            ],
        )
    if isinstance(stmt, IfStatement):
        children: list[tuple[str, list]] = [
            ("Condition", [_expr_to_tree(stmt.condition)]),
            ("Then", [_stmt_to_tree(s) for s in stmt.then_body]),
        ]
        if stmt.else_body is not None:
            children.append(("Else", [_stmt_to_tree(s) for s in stmt.else_body]))
        return ("If", children)
    if isinstance(stmt, FunctionStatement):
        return (
            f"Function({stmt.name}, params={stmt.params})",
            [_stmt_to_tree(s) for s in stmt.body],
        )
    return (repr(stmt), [])


def _expr_to_tree(expr: object) -> tuple[str, list[tuple[str, list]]]:
    if isinstance(expr, LiteralExpr):
        return (f"Literal({expr.value!r})", [])
    if isinstance(expr, IdentifierExpr):
        return (f"Identifier({expr.name})", [])
    if isinstance(expr, UnaryExpr):
        return (f"Unary({expr.op})", [_expr_to_tree(expr.operand)])
    if isinstance(expr, BinaryExpr):
        return (f"Binary({expr.op})", [_expr_to_tree(expr.left), _expr_to_tree(expr.right)])
    if isinstance(expr, CallExpr):
        return (
            "Call",
            [
                ("Callee", [_expr_to_tree(expr.callee)]),
                ("Args", [_expr_to_tree(arg) for arg in expr.args]),
            ],
        )
    if isinstance(expr, ArrayExpr):
        return ("Array", [_expr_to_tree(el) for el in expr.elements])
    if isinstance(expr, MapExpr):
        return ("Map", [(f"Key({key!r})", [_expr_to_tree(value)]) for key, value in expr.entries])
    return (repr(expr), [])
