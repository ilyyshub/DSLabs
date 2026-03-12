from __future__ import annotations
from typing import List
from tokens import Token
from constants import *

# ─────────────────────────────────────────────
#  Lexer
# ─────────────────────────────────────────────

class Lexer:
    """
    Scanner that consumes a source string character by character
    and emits a flat list of Token objects.
    """

    def __init__(self, source: str) -> None:
        self._src: str = source
        self._pos: int = 0
        self._line: int = 1
        self._col: int = 1
        self._tokens: List[Token] = []

    # ── public interface ──────────────────────────────────────────────────

    def tokenize(self) -> List[Token]:
        while not self._at_end():
            self._scan_token()
        self._tokens.append(Token(TT.EOF, "", None, self._line, self._col))
        return self._tokens

    # ── character helpers ─────────────────────────────────────────────────

    def _at_end(self) -> bool:
        return self._pos >= len(self._src)

    def _peek(self, offset: int = 0) -> str:
        idx = self._pos + offset
        return self._src[idx] if idx < len(self._src) else "\0"

    def _advance(self) -> str:
        ch = self._src[self._pos]
        self._pos += 1
        if ch == "\n":
            self._line += 1
            self._col = 1
        else:
            self._col += 1
        return ch

    def _match(self, expected: str) -> bool:
        if self._at_end() or self._src[self._pos] != expected:
            return False
        self._advance()
        return True

    # ── token emission ────────────────────────────────────────────────────

    def _make(self, tt: TT, lexeme: str, value: object, line: int, col: int) -> None:
        self._tokens.append(Token(tt, lexeme, value, line, col))

    # ── scan dispatch ─────────────────────────────────────────────────────

    def _scan_token(self) -> None:
        start_line = self._line
        start_col  = self._col
        ch = self._advance()

        # ── whitespace (skip, except newlines) ────────────────────────────
        if ch in (" ", "\t", "\r"):
            return

        if ch == "\n":
            self._make(TT.NEWLINE, "\\n", None, start_line, start_col)
            return

        # ── comment ───────────────────────────────────────────────────────
        if ch == "#":
            buf = "#"
            while not self._at_end() and self._peek() != "\n":
                buf += self._advance()
            self._make(TT.COMMENT, buf, buf[1:].strip(), start_line, start_col)
            return

        # ── string literal ────────────────────────────────────────────────
        if ch == '"':
            self._scan_string(start_line, start_col)
            return

        # ── numeric literal ───────────────────────────────────────────────
        if ch.isdigit():
            self._scan_number(ch, start_line, start_col)
            return

        # ── identifier / keyword ──────────────────────────────────────────
        if ch.isalpha() or ch == "_":
            self._scan_ident(ch, start_line, start_col)
            return

        # ── two-character operators ───────────────────────────────────────
        if ch == "=" and self._match("="):
            self._make(TT.EQ,     "==", None, start_line, start_col); return
        if ch == "!" and self._match("="):
            self._make(TT.NEQ,    "!=", None, start_line, start_col); return
        if ch == "<" and self._match("="):
            self._make(TT.LTE,    "<=", None, start_line, start_col); return
        if ch == ">" and self._match("="):
            self._make(TT.GTE,    ">=", None, start_line, start_col); return

        # ── single-character operators / delimiters ───────────────────────
        single = {
            "=": TT.ASSIGN,
            "<": TT.LT,     ">": TT.GT,
            "+": TT.PLUS,   "-": TT.MINUS,
            "*": TT.STAR,   "/": TT.SLASH,  "%": TT.PERCENT,
            "(": TT.LPAREN, ")": TT.RPAREN,
            "[": TT.LBRACKET, "]": TT.RBRACKET,
            "{": TT.LBRACE,   "}": TT.RBRACE,
            ",": TT.COMMA,  ":": TT.COLON,
        }
        if ch in single:
            self._make(single[ch], ch, None, start_line, start_col)
            return

        # ── unknown ───────────────────────────────────────────────────────
        self._make(TT.UNKNOWN, ch, None, start_line, start_col)

    # ── specialised scanners ──────────────────────────────────────────────

    def _scan_string(self, line: int, col: int) -> None:
        buf = ""
        while not self._at_end() and self._peek() != '"':
            ch = self._advance()
            if ch == "\\":               # simple escape handling
                nxt = self._advance()
                buf += {"n": "\n", "t": "\t", "\\": "\\", '"': '"'}.get(nxt, nxt)
            else:
                buf += ch
        if self._at_end():
            raise LexerError("Unterminated string literal", line, col)
        self._advance()                  # closing "
        self._make(TT.STRING, f'"{buf}"', buf, line, col)

    def _scan_number(self, first: str, line: int, col: int) -> None:
        buf = first
        while not self._at_end() and self._peek().isdigit():
            buf += self._advance()
        if self._peek() == "." and self._peek(1).isdigit():
            buf += self._advance()       # consume '.'
            while not self._at_end() and self._peek().isdigit():
                buf += self._advance()
            self._make(TT.FLOAT, buf, float(buf), line, col)
        else:
            self._make(TT.INTEGER, buf, int(buf), line, col)

    def _scan_ident(self, first: str, line: int, col: int) -> None:
        buf = first
        while not self._at_end() and (self._peek().isalnum() or self._peek() == "_"):
            buf += self._advance()
        tt = KEYWORDS.get(buf, TT.IDENT)
        value = None
        if tt == TT.TRUE:
            value = True
        elif tt == TT.FALSE:
            value = False
        self._make(tt, buf, value, line, col)


# ─────────────────────────────────────────────
#  Lexer Error
# ─────────────────────────────────────────────

class LexerError(Exception):
    def __init__(self, message: str, line: int, column: int) -> None:
        super().__init__(f"[line {line}, col {column}] LexerError: {message}")
        self.line = line
        self.column = column


