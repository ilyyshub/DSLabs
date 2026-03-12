# DSL - Small Scripting Language

from __future__ import annotations
from dataclasses import dataclass
from enum import Enum, auto

# ─────────────────────────────────────────────
#  Token Types - TT
# ─────────────────────────────────────────────

class TT(Enum):
    # Literals
    INTEGER     = auto()
    FLOAT       = auto()
    STRING      = auto()
    BOOL        = auto()

    # Identifiers
    IDENT       = auto()

    # Keywords
    LET         = auto()
    FN          = auto()
    RETURN      = auto()
    IF          = auto()
    ELSE        = auto()
    WHILE       = auto()
    END         = auto()
    PRINT       = auto()
    AND         = auto()
    OR          = auto()
    NOT         = auto()
    TRUE        = auto()
    FALSE       = auto()

    # Arithmetic operators
    PLUS        = auto()
    MINUS       = auto()
    STAR        = auto()
    SLASH       = auto()
    PERCENT     = auto()

    # Comparison operators
    EQ          = auto()   # ==
    NEQ         = auto()   # !=
    LT          = auto()   # <
    GT          = auto()   # >
    LTE         = auto()   # <=
    GTE         = auto()   # >=

    # Assignment
    ASSIGN      = auto()   # =

    # Delimiters
    LPAREN      = auto()
    RPAREN      = auto()
    LBRACKET    = auto()
    RBRACKET    = auto()
    LBRACE      = auto()
    RBRACE      = auto()
    COMMA       = auto()
    COLON       = auto()
    NEWLINE     = auto()

    # Special
    COMMENT     = auto()
    EOF         = auto()
    UNKNOWN     = auto()


# ─────────────────────────────────────────────
#  Token dataclass
# ─────────────────────────────────────────────

@dataclass
class Token:
    type:    TT
    lexeme:  str
    value:   object        # coerced Python value (int, float, str, bool, None)
    line:    int
    column:  int

    def __repr__(self) -> str:
        val = f", value={self.value!r}" if self.value is not None else ""
        return f"Token({self.type.name}, {self.lexeme!r}{val}, line={self.line}, col={self.column})"

