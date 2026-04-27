# Laboratory Work: Parser & Building an Abstract Syntax Tree
**Course:** Formal Languages & Finite Automata  
**Topic:** Parser and AST Construction  
**Authors of the assignment:** Cretu Dumitru, Vasile Drumea, Irina Cojuhari

---

## 1. Introduction

Syntactic analysis (parsing) is the compilation stage that transforms a linear token stream into a structured representation governed by grammar rules. In compiler architecture, this stage follows lexical analysis and precedes semantic analysis or execution.

Although a concrete parse tree can preserve every grammar production used in derivation, practical implementations often use an **Abstract Syntax Tree (AST)**. The AST intentionally removes syntactic noise and retains only semantically meaningful constructs, which makes it an effective intermediate representation for interpretation, static checking, optimization, and code generation.

This laboratory work extends the lexer-centered implementation from Lab 3 with full syntax analysis for the same DSL, resulting in a consistent front-end pipeline:

1. source text -> regex-based lexical analysis;
2. token sequence -> recursive-descent parsing;
3. parser output -> hierarchical AST.

---

## 2. Objectives

The work was developed to satisfy both theoretical and implementation objectives:

1. Study parsing as a formal process for extracting syntactic structure.
2. Design and implement a reusable AST model for a non-trivial DSL.
3. Introduce an explicit `TokenType` classifier suitable for parser integration.
4. Classify tokens through regular expressions, not ad-hoc character checks.
5. Implement a parser that handles declarations, control flow, function definitions, collections, and expressions with operator precedence.
6. Demonstrate and test the complete lexer-parser-AST flow on representative programs.

---

## 3. Language Scope Processed in Lab 6

The syntax supported by the parser corresponds to the DSL introduced in Lab 3:

1. Variable declarations: `let x = expression`
2. Output statements: `print expression`
3. Return statements: `return expression`
4. Function declarations: `fn name(params) ... end`
5. Conditional statements: `if condition ... [else ...] end`
6. Loops: `while condition ... end`
7. Expression statements (e.g., standalone calls)
8. Literals and values:
   - integers, floats, strings, booleans
   - arrays: `[e1, e2, ...]`
   - maps: `{ "key": value, ... }`
9. Operators:
   - arithmetic: `+ - * / %`
   - comparison: `== != < <= > >=`
   - logical: `and or not`
10. Comments and line structure:
   - line comments (`# ...`)
   - newline tokens preserved as structural trivia

---

## 4. Implementation Overview

The implementation for this laboratory is organized into dedicated modules:

1. `lab6/tokens.py` - token type system and token data model.
2. `lab6/lexer.py` - regex-driven lexical analyzer.
3. `lab6/ast_nodes.py` - AST class hierarchy.
4. `lab6/parser.py` - recursive-descent parser.
5. `lab6/pretty_print.py` - token table printer and tree-style AST printer.
6. `lab6/main.py` - executable demonstration.
7. `lab6/test_parser.py` - automated tests for lexical categorization and AST construction.

This separation enforces clear responsibilities and allows each phase to be tested independently.

---

## 5. Token Type System and Lexical Analysis

### 5.1 TokenType definition

`TokenType` is implemented as an enum and covers all lexical categories required by the parser:

1. Literals: `INTEGER`, `FLOAT`, `STRING`, `TRUE`, `FALSE`
2. Identifiers: `IDENT`
3. Keywords: `LET`, `FN`, `RETURN`, `IF`, `ELSE`, `WHILE`, `END`, `PRINT`, `AND`, `OR`, `NOT`
4. Operators: `PLUS`, `MINUS`, `STAR`, `SLASH`, `PERCENT`, `EQ`, `NEQ`, `LT`, `LTE`, `GT`, `GTE`, `ASSIGN`
5. Delimiters: `LPAREN`, `RPAREN`, `LBRACKET`, `RBRACKET`, `LBRACE`, `RBRACE`, `COMMA`, `COLON`
6. Structural/special: `NEWLINE`, `COMMENT`, `EOF`

Each token stores `(type, lexeme, value, line, column)`, enabling precise parser diagnostics.

### 5.2 Regex-based identification

Token recognition is performed by a single combined regular expression containing named groups. The lexer scans the input left-to-right and maps each matched group name to a `TokenType` value.

Important implementation details:

1. Multi-character operators (`==`, `!=`, `<=`, `>=`) are matched before single-character alternatives.
2. Keywords use word boundaries (`\b`) to avoid partial matches inside identifiers.
3. Values are decoded during lexing:
   - integers -> `int`
   - floats -> `float`
   - `true`/`false` -> `bool`
   - strings -> unescaped Python string
4. Source position tracking is preserved for every token.

This approach directly satisfies the requirement to classify token types through regular expressions.

---

## 6. AST Design

The AST model in `ast_nodes.py` is split into `Statement` and `Expression` families.

### 6.1 Statement nodes

1. `Program(statements)`
2. `LetStatement(name, value)`
3. `PrintStatement(expression)`
4. `ReturnStatement(expression)`
5. `IfStatement(condition, then_body, else_body)`
6. `WhileStatement(condition, body)`
7. `FunctionStatement(name, params, body)`
8. `ExprStatement(expression)`

### 6.2 Expression nodes

1. `LiteralExpr(value)`
2. `IdentifierExpr(name)`
3. `UnaryExpr(op, operand)`
4. `BinaryExpr(left, op, right)`
5. `CallExpr(callee, args)`
6. `ArrayExpr(elements)`
7. `MapExpr(entries)`

The model is intentionally minimal but semantically explicit. It is suitable for direct extension toward an interpreter or type checker.

---

## 7. Parser Architecture and Grammar Handling

The parser uses recursive descent and consumes a full token list emitted by the lexer.

### 7.1 High-level parsing strategy

1. Parse a top-level sequence of statements until `EOF`.
2. Ignore trivia tokens (`NEWLINE`, `COMMENT`) between syntactic units.
3. Dispatch statements by leading token (`let`, `if`, `while`, `fn`, etc.).
4. Parse expressions with precedence-aware methods.
5. Raise `ParserError` with line/column context on syntax violations.

### 7.2 Expression precedence layers

The parser enforces standard precedence via method decomposition:

1. `or`
2. `and`
3. equality (`==`, `!=`)
4. comparison (`<`, `<=`, `>`, `>=`)
5. additive (`+`, `-`)
6. multiplicative (`*`, `/`, `%`)
7. unary (`not`, unary `-`)
8. calls and primary expressions

This guarantees deterministic construction of `BinaryExpr`/`UnaryExpr` nodes with correct operator binding.

### 7.3 Block-based constructs

1. `if ... [else ...] end`
2. `while ... end`
3. `fn name(params) ... end`

For each construct, the parser collects nested statement lists until the expected terminator is reached. This yields AST subtrees that preserve lexical nesting and execution structure.

---

## 8. AST Visualization and Output

The AST printer was implemented in `pretty_print.py` and later upgraded to a branch-style tree representation using connectors (`|--`, `` `-- ``). This output format is more appropriate for structural verification than flat indentation because parent-child relations are visually explicit.

`main.py` demonstrates the complete workflow:

1. load sample source program,
2. tokenize and print token table,
3. parse token stream into `Program`,
4. render the AST tree.

---

## 9. Validation and Results

### 9.1 Demonstration run

Running:

```bash
cd lab6
python3 main.py
```

produces:

1. tokenized output with exact source coordinates;
2. AST tree that includes:
   - function definition subtree,
   - nested conditional subtree,
   - call expressions with arguments,
   - array and map literal nodes,
   - logical/comparison/arithmetic operator nodes.

### 9.2 Automated tests

`test_parser.py` verifies:

1. **Lexical classification correctness** for representative token categories (`LET`, `GTE`, `AND`, `NOT`, `STRING`, `EOF`).
2. **Syntactic construction correctness** by parsing a program with:
   - function declaration,
   - `if/else` block,
   - post-function `let` and `print` statements,
   and asserting the resulting AST node types and structure.

These checks provide confidence that the implementation is both syntactically correct and stable for the intended DSL subset.

---

## 10. Difficulties and Engineering Decisions

The main technical considerations were:

1. **Token matching order in regex lexer**  
   Correct precedence between multi-character and single-character operators had to be preserved to avoid incorrect token splitting.

2. **Trivia handling**  
   `NEWLINE` and `COMMENT` tokens are retained by the lexer for transparency, but skipped at parse boundaries to keep grammar rules clean.

3. **Parser clarity vs. extensibility**  
   A layered precedence parser was chosen because it is explicit, easy to debug, and simple to extend with new operators.

4. **AST granularity**  
   The node set was kept compact while still representing all constructs required for future interpretation.

---

## 11. Conclusions

The laboratory objectives were fully achieved. The resulting implementation delivers a complete syntax-analysis stage for the DSL from Lab 3:

1. A formal token taxonomy (`TokenType`) suitable for parser integration.
2. Regex-based lexical categorization compliant with the assignment requirement.
3. A structured AST model for statements and expressions.
4. A working recursive-descent parser that extracts syntactic information and builds ASTs.
5. Demonstration and automated tests validating both lexical and syntactic behavior.

From a formal-languages perspective, this lab bridges theory and implementation by moving from regular-pattern token recognition to context-free structural parsing and hierarchical abstract representation.

---

## 12. Source Files Added in Lab 6

1. `lab6/tokens.py`
2. `lab6/lexer.py`
3. `lab6/ast_nodes.py`
4. `lab6/parser.py`
5. `lab6/pretty_print.py`
6. `lab6/main.py`
7. `lab6/test_parser.py`
8. `lab6/report6/lab6_report.md`

---

## 13. References

1. Aho, Lam, Sethi, Ullman - *Compilers: Principles, Techniques, and Tools*.
2. Grune, Jacobs - *Parsing Techniques: A Practical Guide*.
3. Nystrom, Robert - *Crafting Interpreters* (chapters on scanning and parsing).
