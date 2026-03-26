# ─────────────────────────────────────────────
# AST Node definitions
# ─────────────────────────────────────────────
from dataclasses import dataclass
from typing import List

@dataclass
class Node:
    """Base class for all AST nodes."""
    pass


@dataclass
class Literal(Node):
    """A single literal character."""
    char: str


@dataclass
class Concatenation(Node):
    """A sequence of nodes: AB"""
    children: List[Node]


@dataclass
class Alternation(Node):
    """A choice between nodes: A|B|C"""
    choices: List[Node]


@dataclass
class Quantifier(Node):
    """A quantified node: A? A* A+ A{n} A{m,n}"""
    child: Node
    min_rep: int
    max_rep: int   # -1 means unbounded (will be capped at MAX_REPEAT)

