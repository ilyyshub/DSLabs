from typing import List
from lab3.lexer import LexerError, Lexer
from lab3.tokens import TT, Token


# ─────────────────────────────────────────────
#  Pretty-printer util
# ─────────────────────────────────────────────

def pretty_print(tokens: List[Token]) -> None:
    header = f"{'TYPE':<15} {'LEXEME':<20} {'VALUE':<20} {'LINE':>4} {'COL':>4}"
    print(header)
    print("-" * len(header))
    for tok in tokens:
        val = repr(tok.value) if tok.value is not None else ""
        print(f"{tok.type.name:<15} {tok.lexeme:<20} {val:<20} {tok.line:>4} {tok.column:>4}")


# ─────────────────────────────────────────────
#  Demo
# ─────────────────────────────────────────────
SAMPLE_PROGRAM = """\
# Fibonacci — recursive function demo
fn fib(n)
  if n <= 1
    return n
  end
  return fib(n - 1) + fib(n - 2)
end

let result = fib(10)
print result

# Array and map literals
let primes = [2, 3, 5, 7, 11]
let config = { "host": "localhost", "port": 8080 }

# Boolean and comparison
let x = 3.14
let flag = x > 2.0 and not false
if flag
  print "pi is large"
else
  print "unexpected"
end

# While loop with modulo
let i = 0
while i < 5
  let i = i + 1
  let rem = i % 2
  print rem
end
"""


def main() -> None:
    print("=" * 60)
    print("  DSL Lexer Demo")
    print("=" * 60)
    print("\nSource program:\n")
    print(SAMPLE_PROGRAM)
    print("\nToken stream:\n")
    lexer = Lexer(SAMPLE_PROGRAM)
    tokens = lexer.tokenize()
    pretty_print(tokens)
    print(f"\nTotal tokens emitted: {len(tokens)}")

    # ── Edge-case samples ──────────────────────────────────────────────────
    edge_cases = [
        ('Integers & floats',  "42 3.14 0 100.0"),
        ('Strings & escapes',  r'"hello\nworld"  "tab\there"'),
        ('All comparison ops', "a == b != c <= d >= e < f > g"),
        ('Nested call',        "fn outer(x) return inner(x + 1) end"),
        ('Unterminated str',   '"oops'),
    ]

    print("\n" + "=" * 60)
    print("  Edge-case tests")
    print("=" * 60)
    for name, src in edge_cases:
        print(f"\n[{name}]  src = {src!r}")
        try:
            toks = Lexer(src).tokenize()
            for t in toks:
                if t.type != TT.EOF:
                    print(f"  {t}")
        except LexerError as e:
            print(f"  !! {e}")


if __name__ == "__main__":
    main()