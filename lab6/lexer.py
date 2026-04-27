from __future__ import annotations

import re
from typing import Iterator

from tokens import Token, TokenType


class LexerError(Exception):
    def __init__(self, message: str, line: int, column: int) -> None:
        super().__init__(f"[line {line}, col {column}] LexerError: {message}")
        self.line = line
        self.column = column


class Lexer:
    """
    Regex-based lexer for the lab DSL.
    Token type classification is done with regular-expression groups.
    """

    _TOKEN_SPEC = [
        ("NEWLINE", r"\n+"),
        ("SKIP", r"[ \t\r]+"),
        ("COMMENT", r"\#[^\n]*"),
        ("FLOAT", r"\d+\.\d+"),
        ("INTEGER", r"\d+"),
        ("STRING", r'"(?:\\.|[^"\\])*"'),
        ("EQ", r"=="),
        ("NEQ", r"!="),
        ("LTE", r"<="),
        ("GTE", r">="),
        ("ASSIGN", r"="),
        ("LT", r"<"),
        ("GT", r">"),
        ("PLUS", r"\+"),
        ("MINUS", r"-"),
        ("STAR", r"\*"),
        ("SLASH", r"/"),
        ("PERCENT", r"%"),
        ("LPAREN", r"\("),
        ("RPAREN", r"\)"),
        ("LBRACKET", r"\["),
        ("RBRACKET", r"\]"),
        ("LBRACE", r"\{"),
        ("RBRACE", r"\}"),
        ("COMMA", r","),
        ("COLON", r":"),
        ("LET", r"\blet\b"),
        ("FN", r"\bfn\b"),
        ("RETURN", r"\breturn\b"),
        ("IF", r"\bif\b"),
        ("ELSE", r"\belse\b"),
        ("WHILE", r"\bwhile\b"),
        ("END", r"\bend\b"),
        ("PRINT", r"\bprint\b"),
        ("AND", r"\band\b"),
        ("OR", r"\bor\b"),
        ("NOT", r"\bnot\b"),
        ("TRUE", r"\btrue\b"),
        ("FALSE", r"\bfalse\b"),
        ("IDENT", r"[A-Za-z_][A-Za-z0-9_]*"),
        ("MISMATCH", r"."),
    ]
    _MASTER = re.compile("|".join(f"(?P<{name}>{pattern})" for name, pattern in _TOKEN_SPEC))

    def __init__(self, source: str) -> None:
        self._source = source

    def tokenize(self) -> list[Token]:
        tokens = list(self._iter_tokens())
        line, column = self._eof_position()
        tokens.append(Token(TokenType.EOF, "", None, line, column))
        return tokens

    def _iter_tokens(self) -> Iterator[Token]:
        line = 1
        col = 1

        for match in self._MASTER.finditer(self._source):
            kind = match.lastgroup
            lexeme = match.group()
            start_line = line
            start_col = col

            if kind == "MISMATCH":
                raise LexerError(f"Unexpected character {lexeme!r}", start_line, start_col)

            if kind != "SKIP":
                token_type = TokenType[kind]
                value = self._token_value(token_type, lexeme)
                yield Token(token_type, lexeme, value, start_line, start_col)

            line, col = self._advance_position(line, col, lexeme)

    @staticmethod
    def _advance_position(line: int, col: int, lexeme: str) -> tuple[int, int]:
        newline_count = lexeme.count("\n")
        if newline_count == 0:
            return line, col + len(lexeme)

        line += newline_count
        tail = lexeme.rsplit("\n", maxsplit=1)[-1]
        return line, len(tail) + 1

    def _eof_position(self) -> tuple[int, int]:
        line = 1
        col = 1
        for part in re.finditer(r".|\n", self._source):
            line, col = self._advance_position(line, col, part.group())
        return line, col

    @staticmethod
    def _token_value(token_type: TokenType, lexeme: str) -> object:
        if token_type is TokenType.INTEGER:
            return int(lexeme)
        if token_type is TokenType.FLOAT:
            return float(lexeme)
        if token_type is TokenType.TRUE:
            return True
        if token_type is TokenType.FALSE:
            return False
        if token_type is TokenType.STRING:
            content = lexeme[1:-1]
            return bytes(content, "utf-8").decode("unicode_escape")
        if token_type is TokenType.COMMENT:
            return lexeme[1:].strip()
        return None
