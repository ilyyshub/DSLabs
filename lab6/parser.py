from __future__ import annotations

from ast_nodes import (
    ArrayExpr,
    BinaryExpr,
    CallExpr,
    ExprStatement,
    Expression,
    FunctionStatement,
    IdentifierExpr,
    IfStatement,
    LetStatement,
    LiteralExpr,
    MapExpr,
    PrintStatement,
    Program,
    ReturnStatement,
    Statement,
    UnaryExpr,
    WhileStatement,
)
from tokens import Token, TokenType


class ParserError(Exception):
    def __init__(self, message: str, token: Token) -> None:
        super().__init__(f"[line {token.line}, col {token.column}] ParserError: {message}")
        self.token = token


class Parser:
    def __init__(self, tokens: list[Token]) -> None:
        self._tokens = tokens
        self._idx = 0

    def parse(self) -> Program:
        statements: list[Statement] = []
        self._skip_trivia()
        while not self._is_at_end():
            statements.append(self._statement())
            self._skip_trivia()
        return Program(statements)

    def _statement(self) -> Statement:
        if self._match(TokenType.LET):
            return self._let_statement()
        if self._match(TokenType.PRINT):
            return PrintStatement(self._expression())
        if self._match(TokenType.RETURN):
            return ReturnStatement(self._expression())
        if self._match(TokenType.IF):
            return self._if_statement()
        if self._match(TokenType.WHILE):
            return self._while_statement()
        if self._match(TokenType.FN):
            return self._function_statement()
        return ExprStatement(self._expression())

    def _let_statement(self) -> LetStatement:
        name = self._consume(TokenType.IDENT, "Expected variable name after 'let'.")
        self._consume(TokenType.ASSIGN, "Expected '=' in let statement.")
        value = self._expression()
        return LetStatement(name.lexeme, value)

    def _if_statement(self) -> IfStatement:
        condition = self._expression()
        self._skip_trivia()
        then_body = self._parse_block({TokenType.ELSE, TokenType.END})
        else_body = None
        if self._match(TokenType.ELSE):
            self._skip_trivia()
            else_body = self._parse_block({TokenType.END})
        self._consume(TokenType.END, "Expected 'end' after if statement.")
        return IfStatement(condition, then_body, else_body)

    def _while_statement(self) -> WhileStatement:
        condition = self._expression()
        self._skip_trivia()
        body = self._parse_block({TokenType.END})
        self._consume(TokenType.END, "Expected 'end' after while statement.")
        return WhileStatement(condition, body)

    def _function_statement(self) -> FunctionStatement:
        name = self._consume(TokenType.IDENT, "Expected function name after 'fn'.")
        self._consume(TokenType.LPAREN, "Expected '(' after function name.")
        params: list[str] = []
        if not self._check(TokenType.RPAREN):
            while True:
                param = self._consume(TokenType.IDENT, "Expected parameter name.")
                params.append(param.lexeme)
                if not self._match(TokenType.COMMA):
                    break
        self._consume(TokenType.RPAREN, "Expected ')' after parameter list.")
        self._skip_trivia()
        body = self._parse_block({TokenType.END})
        self._consume(TokenType.END, "Expected 'end' after function body.")
        return FunctionStatement(name.lexeme, params, body)

    def _parse_block(self, stop_tokens: set[TokenType]) -> list[Statement]:
        stmts: list[Statement] = []
        self._skip_trivia()
        while not self._check_any(stop_tokens) and not self._is_at_end():
            stmts.append(self._statement())
            self._skip_trivia()
        return stmts

    def _expression(self) -> Expression:
        return self._or()

    def _or(self) -> Expression:
        expr = self._and()
        while self._match(TokenType.OR):
            op = self._previous().lexeme
            right = self._and()
            expr = BinaryExpr(expr, op, right)
        return expr

    def _and(self) -> Expression:
        expr = self._equality()
        while self._match(TokenType.AND):
            op = self._previous().lexeme
            right = self._equality()
            expr = BinaryExpr(expr, op, right)
        return expr

    def _equality(self) -> Expression:
        expr = self._comparison()
        while self._match(TokenType.EQ, TokenType.NEQ):
            op = self._previous().lexeme
            right = self._comparison()
            expr = BinaryExpr(expr, op, right)
        return expr

    def _comparison(self) -> Expression:
        expr = self._term()
        while self._match(TokenType.LT, TokenType.LTE, TokenType.GT, TokenType.GTE):
            op = self._previous().lexeme
            right = self._term()
            expr = BinaryExpr(expr, op, right)
        return expr

    def _term(self) -> Expression:
        expr = self._factor()
        while self._match(TokenType.PLUS, TokenType.MINUS):
            op = self._previous().lexeme
            right = self._factor()
            expr = BinaryExpr(expr, op, right)
        return expr

    def _factor(self) -> Expression:
        expr = self._unary()
        while self._match(TokenType.STAR, TokenType.SLASH, TokenType.PERCENT):
            op = self._previous().lexeme
            right = self._unary()
            expr = BinaryExpr(expr, op, right)
        return expr

    def _unary(self) -> Expression:
        if self._match(TokenType.NOT, TokenType.MINUS):
            op = self._previous().lexeme
            return UnaryExpr(op, self._unary())
        return self._call()

    def _call(self) -> Expression:
        expr = self._primary()
        while True:
            if self._match(TokenType.LPAREN):
                args: list[Expression] = []
                if not self._check(TokenType.RPAREN):
                    while True:
                        args.append(self._expression())
                        if not self._match(TokenType.COMMA):
                            break
                self._consume(TokenType.RPAREN, "Expected ')' after function call arguments.")
                expr = CallExpr(expr, args)
                continue
            break
        return expr

    def _primary(self) -> Expression:
        if self._match(TokenType.INTEGER, TokenType.FLOAT, TokenType.STRING):
            return LiteralExpr(self._previous().value)
        if self._match(TokenType.TRUE, TokenType.FALSE):
            return LiteralExpr(self._previous().value)
        if self._match(TokenType.IDENT):
            return IdentifierExpr(self._previous().lexeme)
        if self._match(TokenType.LPAREN):
            expr = self._expression()
            self._consume(TokenType.RPAREN, "Expected ')' after expression.")
            return expr
        if self._match(TokenType.LBRACKET):
            return self._array_literal()
        if self._match(TokenType.LBRACE):
            return self._map_literal()
        raise ParserError("Expected expression.", self._peek())

    def _array_literal(self) -> ArrayExpr:
        elements: list[Expression] = []
        if not self._check(TokenType.RBRACKET):
            while True:
                elements.append(self._expression())
                if not self._match(TokenType.COMMA):
                    break
        self._consume(TokenType.RBRACKET, "Expected ']' after array literal.")
        return ArrayExpr(elements)

    def _map_literal(self) -> MapExpr:
        entries: list[tuple[str, Expression]] = []
        if not self._check(TokenType.RBRACE):
            while True:
                key_token = self._consume_any(
                    [TokenType.STRING, TokenType.IDENT],
                    "Expected map key (string or identifier).",
                )
                key = key_token.value if key_token.type is TokenType.STRING else key_token.lexeme
                self._consume(TokenType.COLON, "Expected ':' after map key.")
                value = self._expression()
                entries.append((str(key), value))
                if not self._match(TokenType.COMMA):
                    break
        self._consume(TokenType.RBRACE, "Expected '}' after map literal.")
        return MapExpr(entries)

    def _match(self, *types: TokenType) -> bool:
        for token_type in types:
            if self._check(token_type):
                self._advance()
                return True
        return False

    def _check(self, token_type: TokenType) -> bool:
        if self._is_at_end():
            return token_type is TokenType.EOF
        return self._peek().type is token_type

    def _check_any(self, token_types: set[TokenType]) -> bool:
        return self._peek().type in token_types

    def _advance(self) -> Token:
        if not self._is_at_end():
            self._idx += 1
        return self._previous()

    def _peek(self) -> Token:
        return self._tokens[self._idx]

    def _previous(self) -> Token:
        return self._tokens[self._idx - 1]

    def _is_at_end(self) -> bool:
        return self._peek().type is TokenType.EOF

    def _consume(self, token_type: TokenType, message: str) -> Token:
        if self._check(token_type):
            return self._advance()
        raise ParserError(message, self._peek())

    def _consume_any(self, token_types: list[TokenType], message: str) -> Token:
        for token_type in token_types:
            if self._check(token_type):
                return self._advance()
        raise ParserError(message, self._peek())

    def _skip_trivia(self) -> None:
        while self._match(TokenType.NEWLINE, TokenType.COMMENT):
            pass
