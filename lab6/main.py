from __future__ import annotations

from lexer import Lexer
from parser import Parser
from pretty_print import print_ast, print_tokens


SAMPLE_PROGRAM = """\
# Fibonacci parser demo
fn fib(n)
  if n <= 1
    return n
  end
  return fib(n - 1) + fib(n - 2)
end

let result = fib(8)
print result

let primes = [2, 3, 5, 7]
let config = { "host": "localhost", "port": 8080 }
let check = result > 3 and not false
"""


def main() -> None:
    print("=" * 70)
    print("Lab 6 - Regex Lexer + Parser + AST")
    print("=" * 70)
    print("\nSource program:\n")
    print(SAMPLE_PROGRAM)

    tokens = Lexer(SAMPLE_PROGRAM).tokenize()
    print("\nToken stream:\n")
    print_tokens(tokens)

    ast = Parser(tokens).parse()
    print("\nAST:\n")
    print_ast(ast)


if __name__ == "__main__":
    main()
