"""
Variant 2 - Regular Expression String Generator

Regular expressions:
  1. M?N²(O|P)³Q*R*
  2. (X|Y|Z)³8*(9|0)*
  3. (H|i)(J|K)L*N?
"""

import random
import re
from typing import List, Optional, Tuple

from lab4.ast_def import Alternation, Node, Quantifier, Literal, Concatenation

# Maximum repetitions for * and + quantifiers (to avoid infinite strings)
# MAX_REPEAT = 5


# ─────────────────────────────────────────────
# Lexer & Parser for a subset of regex syntax
# ─────────────────────────────────────────────

class RegexParser:
    """
    Parses a simplified regex string into an AST.

    Supported syntax:
      - Literals: any alphanumeric character
      - Grouping: (A|B|C)
      - Alternation: A|B inside groups
      - Quantifiers:  ? * + {n} {n,m}
      - Superscript digits as quantifiers: ² ³ etc. (Unicode)
    """

    SUPERSCRIPTS = {
        '⁰': 0, '¹': 1, '²': 2, '³': 3, '⁴': 4,
        '⁵': 5, '⁶': 6, '⁷': 7, '⁸': 8, '⁹': 9,
    }

    def __init__(self, pattern: str):
        self.pattern = pattern
        self.pos = 0

    def peek(self) -> Optional[str]:
        if self.pos < len(self.pattern):
            return self.pattern[self.pos]
        return None

    def consume(self) -> str:
        ch = self.pattern[self.pos]
        self.pos += 1
        return ch

    def parse(self) -> Node:
        node = self._parse_alternation()
        if self.pos != len(self.pattern):
            raise ValueError(
                f"Unexpected character '{self.pattern[self.pos]}' at position {self.pos}"
            )
        return node

    def _parse_alternation(self) -> Node:
        """Parse A|B|C at the current level."""
        choices = [self._parse_concatenation()]
        while self.peek() == '|':
            self.consume()  # eat '|'
            choices.append(self._parse_concatenation())
        if len(choices) == 1:
            return choices[0]
        return Alternation(choices)

    def _parse_concatenation(self) -> Node:
        """Parse a sequence of atoms."""
        children = []
        while self.peek() not in (None, '|', ')'):
            children.append(self._parse_quantified())
        if len(children) == 1:
            return children[0]
        return Concatenation(children)

    def _parse_quantified(self) -> Node:
        """Parse an atom optionally followed by a quantifier."""
        atom = self._parse_atom()
        quantifier = self._try_parse_quantifier()
        if quantifier is None:
            return atom
        min_r, max_r = quantifier
        return Quantifier(atom, min_r, max_r)

    def _parse_atom(self) -> Node:
        ch = self.peek()
        if ch is None:
            raise ValueError("Unexpected end of pattern")

        if ch == '(':
            self.consume()  # eat '('
            node = self._parse_alternation()
            if self.peek() != ')':
                raise ValueError("Expected ')'")
            self.consume()  # eat ')'
            return node

        # Superscript digit used as a literal prefix quantifier base
        # is handled by the caller (_parse_quantifier).
        # Here we just consume a normal literal character.
        if ch.isalnum() or ch in '_':
            self.consume()
            return Literal(ch)

        raise ValueError(f"Unexpected character '{ch}' at position {self.pos}")

    def _try_parse_quantifier(self) -> Optional[Tuple[int, int]]:
        """
        Try to read a quantifier after an atom.
        Returns (min, max) or None if no quantifier present.
        max == -1 means unbounded.
        """
        ch = self.peek()
        if ch is None:
            return None

        if ch == '?':
            self.consume()
            return (0, 1)
        if ch == '*':
            self.consume()
            return 0, -1
        if ch == '+':
            self.consume()
            return (1, -1)
        if ch == '{':
            self.consume()  # eat '{'
            num_str = ''
            while self.peek() and self.peek().isdigit():
                num_str += self.consume()
            if self.peek() == ',':
                self.consume()
                num_str2 = ''
                while self.peek() and self.peek().isdigit():
                    num_str2 += self.consume()
                if self.peek() != '}':
                    raise ValueError("Expected '}'")
                self.consume()
                return (int(num_str), int(num_str2) if num_str2 else -1)
            if self.peek() != '}':
                raise ValueError("Expected '}'")
            self.consume()
            n = int(num_str)
            return (n, n)

        # Unicode superscript digits
        if ch in self.SUPERSCRIPTS:
            self.consume()
            n = self.SUPERSCRIPTS[ch]
            return (n, n)

        return None


