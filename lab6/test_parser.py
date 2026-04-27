from __future__ import annotations

import unittest

from ast_nodes import FunctionStatement, IfStatement, LetStatement, PrintStatement
from lexer import Lexer
from parser import Parser
from tokens import TokenType


class TestLab6Parser(unittest.TestCase):
    def test_regex_token_classification(self) -> None:
        src = 'let x = 10\nif x >= 10 and not false\n  print "ok"\nend\n'
        tokens = Lexer(src).tokenize()
        token_types = [t.type for t in tokens]
        self.assertIn(TokenType.LET, token_types)
        self.assertIn(TokenType.GTE, token_types)
        self.assertIn(TokenType.AND, token_types)
        self.assertIn(TokenType.NOT, token_types)
        self.assertIn(TokenType.STRING, token_types)
        self.assertEqual(token_types[-1], TokenType.EOF)

    def test_builds_ast_for_function_and_if(self) -> None:
        src = """\
fn f(n)
  if n <= 1
    return n
  else
    return n - 1
  end
end
let y = f(3)
print y
"""
        program = Parser(Lexer(src).tokenize()).parse()
        self.assertEqual(len(program.statements), 3)
        self.assertIsInstance(program.statements[0], FunctionStatement)
        self.assertIsInstance(program.statements[1], LetStatement)
        self.assertIsInstance(program.statements[2], PrintStatement)
        function_stmt = program.statements[0]
        self.assertIsInstance(function_stmt.body[0], IfStatement)


if __name__ == "__main__":
    unittest.main()
