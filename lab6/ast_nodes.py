from __future__ import annotations

from dataclasses import dataclass


class Node:
    pass


class Statement(Node):
    pass


class Expression(Node):
    pass


@dataclass
class Program(Node):
    statements: list[Statement]


@dataclass
class LetStatement(Statement):
    name: str
    value: Expression


@dataclass
class PrintStatement(Statement):
    expression: Expression


@dataclass
class ReturnStatement(Statement):
    expression: Expression


@dataclass
class IfStatement(Statement):
    condition: Expression
    then_body: list[Statement]
    else_body: list[Statement] | None


@dataclass
class WhileStatement(Statement):
    condition: Expression
    body: list[Statement]


@dataclass
class FunctionStatement(Statement):
    name: str
    params: list[str]
    body: list[Statement]


@dataclass
class ExprStatement(Statement):
    expression: Expression


@dataclass
class LiteralExpr(Expression):
    value: object


@dataclass
class IdentifierExpr(Expression):
    name: str


@dataclass
class UnaryExpr(Expression):
    op: str
    operand: Expression


@dataclass
class BinaryExpr(Expression):
    left: Expression
    op: str
    right: Expression


@dataclass
class CallExpr(Expression):
    callee: Expression
    args: list[Expression]


@dataclass
class ArrayExpr(Expression):
    elements: list[Expression]


@dataclass
class MapExpr(Expression):
    entries: list[tuple[str, Expression]]
