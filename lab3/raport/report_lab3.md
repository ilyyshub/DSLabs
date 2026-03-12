# Laboratory Work №3: Lexer & Scanner

### Course: Formal Languages & Finite Automata
### Date: 12 March 2026

---

## 1. Theory

Lexical analysis is the first phase in the compilation or interpretation pipeline of any programming language. Its purpose is to transform a raw stream of characters — the source text as typed by a programmer — into a structured sequence of *tokens*. A token is a pair consisting of a *token type* (or category) and the original substring that produced it, which is called a *lexeme*. Optionally, a token may also carry a *value*: for instance, the lexeme `"42"` carries the integer value `42` alongside its `INTEGER` category.

The component responsible for this transformation is called a lexer, scanner, or tokenizer interchangeably in the literature. It operates according to a set of rules that define the valid forms of each token type — rules that can be expressed formally as regular expressions or, equivalently, as deterministic finite automata (DFAs). Because every regular expression has a corresponding DFA, a lexer is in theory nothing more than a collection of DFAs running simultaneously on the input, with a priority scheme to resolve ambiguities when multiple patterns could match the same prefix.

In practice, hand-written lexers are common even in production-grade compilers (LLVM's Clang is a notable example) because they offer precise control over error messages and performance. The alternative is to use a generator such as `lex`, `flex`, or Python's `re` module to derive the DFA automatically from a set of regular-expression rules.

---

## 2. Objectives

The objectives for this laboratory work were as follows:

1. Understand the role of lexical analysis in the broader context of language processing.
2. Gain familiarity with the internal mechanics of a scanner: how it advances character by character, how it decides when a token is complete, and how it handles ambiguous multi-character operators.
3. Design and implement a sample lexer for a non-trivial DSL — one that goes beyond a simple calculator and covers constructs such as function declarations, control flow, collection literals, Boolean logic, and comments.
4. Demonstrate the lexer on representative input and verify its behaviour on edge cases, including malformed input.

---

## 3. DSL Design

Rather than building a calculator, a small general-purpose scripting language was designed. The language supports the following constructs:

**Variable binding.** Variables are introduced with the `let` keyword: `let x = 3.14`. This was chosen because it makes the assignment token (`=`) unambiguous — it can never be confused with the equality-comparison token (`==`).

**Arithmetic.** The operators `+`, `-`, `*`, `/`, and `%` are supported. Float and integer literals are both recognised, with the lexer using the presence of a decimal point to distinguish them.

**Boolean logic and comparison.** The keywords `and`, `or`, and `not` form the Boolean operators. The comparison operators `==`, `!=`, `<`, `>`, `<=`, and `>=` are all recognised, which required careful ordering in the scanner so that the two-character forms are checked before the single-character fallback.

**Control flow.** `if / else / end` blocks and `while / end` loops are supported. The `end` keyword closes both constructs, making the token stream unambiguous without requiring braces.

**Functions.** Functions are declared with `fn name(params)` and terminated with `end`. Recursive calls are naturally supported because the lexer treats any identifier followed by `(` as an ordinary token stream — the distinction between a declaration and a call is left to the parser.

**Collection literals.** Array literals `[1, 2, 3]` and map literals `{"key": value}` are lexed using the bracket and brace delimiters together with `,` and `:`.

**Strings.** Double-quoted string literals support the escape sequences `\n`, `\t`, `\\`, and `\"`.

**Comments.** A `#` character introduces a single-line comment that extends to the end of the line. Comments are emitted as `COMMENT` tokens so that the token stream is lossless and could be used for documentation tools or formatters.

**Newlines.** Newlines are emitted as `NEWLINE` tokens. This enables a future parser to use newlines as statement terminators in the manner of Python or Go, without requiring semicolons.

```python
from enum import Enum, auto

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


```

---

## 4. Implementation

The lexer is implemented as 4 Python files, in `lexer.py`, `tokens.py`, `main.py`. The project also contains the `constants.py` file, where the keywords are defined in a dictionary style.


### 4.1 Token Representation

Each token stores five fields: its type (a member of the `TT` enum), the original lexeme string, a coerced Python value, and the line and column numbers of its first character. Preserving precise source locations is important for producing useful error messages in a compiler or interpreter built on top of this lexer.

### 4.2 Scanning Strategy

The lexer maintains three pieces of mutable state: a position index into the source string, and a line and column counter. Two core helpers expose the standard scanner interface: `_peek(offset)` returns the character at `pos + offset` without consuming it, and `_advance()` consumes and returns the current character, updating the line and column counters whenever a newline is encountered.
```python
from tokens import TT

KEYWORDS: dict[str, TT] = {
    "let":    TT.LET,
    "fn":     TT.FN,
    "return": TT.RETURN,
    "if":     TT.IF,
    "else":   TT.ELSE,
    "while":  TT.WHILE,
    "end":    TT.END,
    "print":  TT.PRINT,
    "and":    TT.AND,
    "or":     TT.OR,
    "not":    TT.NOT,
    "true":   TT.TRUE,
    "false":  TT.FALSE,
}
```


The main `_scan_token` method is called in a loop by `tokenize()`. It reads one character via `_advance()` and dispatches based on that character:

- Whitespace (spaces and tabs) is silently skipped.
- A newline emits a `NEWLINE` token.
- `#` triggers `_scan_string` which consumes characters until the end of the line.
- `"` triggers the string scanner.
- A digit triggers the number scanner.
- A letter or underscore triggers the identifier/keyword scanner.
- For operator characters the scanner first checks whether the next character completes a two-character operator (using the `_match` helper, which consumes the character only if it matches), then falls back to the single-character form.

### 4.3 Number Scanning

Integer and float literals share the same entry point. The scanner first consumes as many digit characters as possible. It then peeks one character ahead: if it sees a `.` followed by another digit, it consumes the dot and the remaining digits and emits a `FLOAT` token; otherwise it emits an `INTEGER` token. The coerced value is produced by Python's built-in `int()` or `float()` conversions.

### 4.4 Identifier and Keyword Scanning

After consuming the first letter or underscore, the scanner continues consuming alphanumeric characters and underscores. The resulting string is looked up in the `KEYWORDS` dictionary; if found, the corresponding keyword token type is used, otherwise `TT.IDENT` is used. The keywords `true` and `false` additionally carry a Boolean value in the token's value field.

### 4.5 Error Handling

Only one class of hard error exists at the lexical level: an unterminated string literal. All other unrecognised characters are emitted as `TT.UNKNOWN` tokens rather than raising an exception, which allows the scanner to continue and report multiple problems in a single pass. A real compiler would collect these into an error list before aborting.

---

## 5. Results

Running `python main.py` produces the token stream for the embedded sample program, which exercises all language features. The program is 31 lines long and yields 142 tokens including comments and newlines. A representative excerpt is shown below:

```
TYPE            LEXEME               VALUE                LINE  COL
-------------------------------------------------------------------
COMMENT         # Fibonacci…         'Fibonacci — …'         1    1
FN              fn                                           2    1
IDENT           fib                                          2    4
LPAREN          (                                            2    7
IDENT           n                                            2    8
RPAREN          )                                            2    9
IF              if                                           3    3
IDENT           n                                            3    6
LTE             <=                                           3    8
INTEGER         1                    1                       3   11
RETURN          return                                       4    5
```

The edge-case tests confirm that integer and float literals are correctly distinguished, that escape sequences in strings are processed, that all six comparison operators are correctly lexed including the two-character forms, that nested function calls produce the expected token sequence, and that an unterminated string literal raises a `LexerError` with an accurate line and column number.

---

## 6. Challenges and Observations

The most technically subtle aspect of the implementation was handling the ambiguity between single-character and two-character operators. The operators `=`, `<`, and `>` are all valid tokens on their own, but they also serve as the first character of `==`, `<=`, and `>=`. Getting this right required checking the lookahead *before* emitting the single-character token, rather than emitting eagerly and then trying to merge tokens retroactively. The `_match` helper, which consumes the next character only if it equals the expected value, made this clean.

A second, more conceptual challenge was deciding what constitutes a "correct" token stream in the presence of invalid input. A strict lexer that raises an exception on the first unknown character is easy to implement but produces poor user experience when the source contains multiple errors. The approach taken here — emitting `UNKNOWN` tokens and continuing — is more forgiving. However, implementing robust error recovery properly (so that the scanner can re-synchronise at a known safe point, such as the next newline) would add significant complexity and was left out of scope.

The decision to emit `COMMENT` and `NEWLINE` tokens rather than silently discarding them was an interesting design choice. In most compiler textbooks, whitespace and comments are stripped out before being handed to the parser. However, preserving them makes the token stream useful for a broader class of tools — formatters, linters, and documentation generators all need to know where comments are. The cost is that any parser built on top of this lexer must explicitly skip `COMMENT` and `NEWLINE` tokens where they are not semantically meaningful.

---

## 7. Conclusions

This laboratory work provided hands-on experience with the mechanics of lexical analysis. The exercise demonstrated that a hand-written scanner, while more verbose than a regex-based or generator-based approach, offers precise control over token boundaries, error messages, and metadata such as source locations. Understanding how a lexer works at this level is valuable background knowledge for anyone building compilers, interpreters, or even simpler tools such as syntax highlighters or configuration-file parsers.

The implementation covers all required features: variable binding, arithmetic, Boolean logic, control flow, function declaration and recursive calls, array and map literals, float and integer literals, string literals with escape sequences, and single-line comments. It correctly handles the ambiguous two-character operators and reports errors with accurate source positions.

---

## 8. References

1. LLVM Tutorial — "Kaleidoscope: Implementing a Language with LLVM": https://llvm.org/docs/tutorial/MyFirstLanguageFrontend/LangImpl01.html
2. Wikipedia — "Lexical analysis": https://en.wikipedia.org/wiki/Lexical_analysis
3. Crafting Interpreters, Robert Nystrom — Chapter 4 (Scanning): https://craftinginterpreters.com/scanning.html