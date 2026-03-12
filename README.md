# Formal Languages & Finite Automata - Laboratory Works

This repository contains laboratory works for the **Formal Languages & Finite Automata** course.

**Author:** Ciocanu Ilinca  
**University:** Technical University of Moldova  
**Academic Year:** 2025-2026

---

## 📚 Course Information

**Course:** Formal Languages & Finite Automata  
**Instructor:** Cretu Dumitru (with Vasile Drumea and Irina Cojuhari)

---

## 📂 Repository Structure

```
FLFA-Labs/
├── README.md                 # This file
├── lab1/                     # Laboratory Work #1
│   ├── src/
│   │   ├── grammar.py            # Grammar class implementation
│   │   ├── finite_automaton.py   # Finite Automaton class
│   │   └── main.py               # Main demonstration program
│   └── report/
│       └── REPORT.md             # Lab 1 report
│
├── lab2/                     # Laboratory Work #2
│   ├── grammar.py            # Grammar class with Chomsky classification
│   ├── finite_automaton.py   # FA with NFA→DFA conversion
│   ├── main.py               # Main demonstration program
│   ├── variant6_nfa.png
│   ├── variant6_dfa.png
│   ├── variant6_nfa.dot
│   ├── variant6_dfa.dot
│   └── report2.md            # Lab 2 report
│
├── lab3/                     # Laboratory Work #3
│   ├── lexer.py              # Lexer / scanner implementation
│   ├── tokens.py             # Token dataclass and TT enum
│   ├── constants.py          # Keyword dictionary
│   ├── main.py               # Demo and edge-case runner
│   └── raport/
            ├──report_lab3.md
│
└── ...
```

---

## 🎯 Laboratory Works

### Lab 1: Regular Grammars and Finite Automata
**Status:** ✅ Completed  
**Variant:** 6

**Objectives:**
- Implement a Grammar class to represent formal grammars
- Generate valid strings from grammar productions
- Convert Grammar to Finite Automaton
- Validate strings using the Finite Automaton

**Key Features:**
- Support for non-deterministic finite automata (NFA)
- Random string generation using derivation
- Comprehensive string validation

**Variant 6 Grammar:**
```
V_N = {S, I, J, K}
V_T = {a, b, c, e, n, f, m}
Productions:
    S → cI
    I → bJ | fI | eK | e
    J → nJ | cS
    K → nK | m
```

[📄 View Lab 1 Report](./lab1/report/REPORT.md)

---

### Lab 2: Determinism in Finite Automata
**Status:** ✅ Completed  
**Variant:** 6

**Objectives:**
- Classify grammars according to Chomsky hierarchy
- Convert Finite Automaton to Regular Grammar
- Determine if FA is deterministic or non-deterministic
- Implement NFA to DFA conversion (subset construction)
- Generate graphical representations of automata

**Key Features:**
- **Chomsky hierarchy classification** (Types 0-3)
- **Determinism detection** algorithm
- **NFA to DFA conversion** using subset construction
- **Graphviz visualization** for both NFA and DFA
- **13 comprehensive unit tests** with 100% pass rate

**Key Results:**
- ✅ Variant 6 FA is **non-deterministic** (NFA)
- ✅ Successfully converted 5-state NFA to 6-state DFA
- ✅ Non-determinism caused by δ(q1, b) = {q1, q2}

**Variant 6 Automaton:**
```
Q = {q0, q1, q2, q3, q4}
Σ = {a, b}
F = {q4}
Transitions:
    δ(q0, a) = q1
    δ(q1, b) = q1, q2  ← Non-deterministic!
    δ(q2, a) = q4
    δ(q2, b) = q3
    δ(q3, a) = q1
```

[📄 View Lab 2 Report](./lab2/report2.md)

---

### Lab 3: Lexer & Scanner
**Status:** ✅ Completed

**Objectives:**
- Understand the role of lexical analysis in language processing
- Gain familiarity with the internal mechanics of a scanner
- Design and implement a lexer for a non-trivial DSL covering function declarations, control flow, collection literals, Boolean logic, and comments
- Demonstrate the lexer on representative input and verify behaviour on edge cases including malformed input

**DSL Features:**
The lexer targets a small general-purpose scripting language. A sample program illustrating all supported constructs:

```
# Fibonacci — recursive function demo
fn fib(n)
  if n <= 1
    return n
  end
  return fib(n - 1) + fib(n - 2)
end

let result = fib(10)
print result

let primes = [2, 3, 5, 7, 11]
let config = { "host": "localhost", "port": 8080 }

let x = 3.14
let flag = x > 2.0 and not false
```

| Construct | Syntax |
|---|---|
| Variable binding | `let x = 3.14` |
| Arithmetic | `+`, `-`, `*`, `/`, `%` |
| Boolean logic | `and`, `or`, `not` |
| Comparison | `==`, `!=`, `<`, `>`, `<=`, `>=` |
| Control flow | `if / else / end`, `while / end` |
| Functions | `fn name(params) … end` |
| Arrays | `[1, 2, 3]` |
| Maps | `{"key": value}` |
| Strings | `"hello\nworld"` (with escape sequences) |
| Comments | `# single-line` |

**Key Results:**
- ✅ Sample program (31 lines) correctly tokenised into **142 tokens**
- ✅ All six comparison operators correctly lexed, including two-character forms
- ✅ Integer and float literals correctly distinguished
- ✅ String escape sequences processed
- ✅ Unterminated string literals raise `LexerError` with accurate line and column

**Token types defined:**
```python
class TT(Enum):
    INTEGER, FLOAT, STRING, BOOL       # Literals
    IDENT                              # Identifiers
    LET, FN, RETURN, IF, ELSE         # Keywords
    WHILE, END, PRINT, AND, OR        #
    NOT, TRUE, FALSE                   #
    PLUS, MINUS, STAR, SLASH, PERCENT # Arithmetic
    EQ, NEQ, LT, GT, LTE, GTE        # Comparison
    ASSIGN                             # =
    LPAREN, RPAREN, LBRACKET          # Delimiters
    RBRACKET, LBRACE, RBRACE          #
    COMMA, COLON, NEWLINE             #
    COMMENT, EOF, UNKNOWN             # Special
```

[📄 View Lab 3 Report](./lab3/README.md)

---

## 🚀 How to Run

### Prerequisites
- Python 3.8 or higher
- Graphviz (optional, for Lab 2 visualization)
  ```bash
  # Ubuntu/Debian
  sudo apt-get install graphviz

  # macOS
  brew install graphviz

  # Windows
  # Download from https://graphviz.org/download/
  ```

### Running Lab 1

```bash
cd lab1/src
python main.py
```

The program will display the grammar definition, generate 5 random valid strings, show the converted Finite Automaton, and validate generated strings and test cases.

### Running Lab 2

```bash
cd lab2

# Run the main demonstration
python main.py

# Run unit tests
python test_automata.py

# Generate visualizations (requires Graphviz)
dot -Tpng variant6_nfa.dot -o variant6_nfa.png
dot -Tpng variant6_dfa.dot -o variant6_dfa.png
```

The program will classify a grammar using the Chomsky hierarchy, analyse the Variant 6 FA for determinism, convert the NFA to a DFA using subset construction, and generate DOT files for visualization.

### Running Lab 3

```bash
cd lab3
python main.py
```

The program will tokenise the embedded sample program and print the full token stream, then run a suite of edge-case tests covering numeric literals, escape sequences, all comparison operators, nested function calls, and error handling.

---

## 💻 Implementation Details

### Programming Language
**Python** was chosen for its clear and readable syntax, excellent built-in data structures (sets, dictionaries, defaultdict), strong support for object-oriented programming, and comprehensive standard library.

### Technologies Used
- **Python 3.8+** with type hints
- **Object-oriented design** patterns
- **Graphviz** for automata visualization (Lab 2)
- **unittest** framework for comprehensive testing (Lab 2)
- **Collections library** (defaultdict, deque) for efficient algorithms
- **Enum** module for expressive token type definitions (Lab 3)

### Algorithms Implemented

**Lab 1:**
- Random string generation via derivation
- NFA string validation with backtracking
- Grammar to FA conversion

**Lab 2:**
- Chomsky hierarchy classification
- Subset construction (NFA → DFA conversion)
- Determinism detection
- FA to regular grammar conversion
- Graph generation in DOT format

**Lab 3:**
- Single-pass character-by-character scanning
- Lookahead-based disambiguation of multi-character operators
- Maximal-munch number and identifier scanning
- Lossless token stream (comments and newlines preserved)
- Graceful error recovery via `UNKNOWN` tokens

---

## 📊 Testing

### Lab 1
Manual testing with multiple test cases, validation of generated strings, and edge case handling.

### Lab 2
13 unit tests covering all functionality with a 100% pass rate across grammar classification, DFA/NFA detection, FA to grammar conversion, NFA to DFA conversion, Graphviz generation, and variant-specific functionality.

```bash
cd lab2
python test_automata.py
# Ran 13 tests in 0.001s — OK ✓
```

### Lab 3
Edge-case tests embedded in `main.py` covering integer and float literal disambiguation, string escape sequences, all six comparison operators, nested function calls, and unterminated string error reporting.

---

## 📈 Visualizations (Lab 2)

### NFA Visualization
<img src="lab2/variant6_nfa.png" alt="NFA" width="400">

Shows the non-deterministic transition δ(q1, b) = {q1, q2}. Five states; double circle indicates the final state q4.

### DFA Visualization
<img src="lab2/variant6_dfa.png" alt="DFA" width="600">

Compound states such as {q1,q2} arise from subset construction. Six states with fully deterministic transitions and two final states: {q4} and {q1,q4}.

**View online:** Copy any `.dot` file to https://dreampuf.github.io/GraphvizOnline/

---

## 📖 Learning Outcomes

### Theoretical Concepts
- Theory of formal languages and grammars
- Chomsky hierarchy and grammar classification
- Regular expressions and regular languages
- Deterministic vs non-deterministic automata
- Equivalence between different formal models
- Lexical analysis and the role of a scanner in a compiler pipeline

### Practical Skills
- Implementation of regular grammars and finite automata
- Subset construction algorithm for NFA to DFA conversion
- Hand-written scanner design: advancing, peeking, and matching
- Token type design and source-location tracking
- Algorithm design for string generation and validation
- Graph theory and visualization techniques
- Software testing with unit tests

### Software Engineering
- Clean code principles and object-oriented design patterns
- Comprehensive testing strategies
- Version control best practices
- Technical documentation

---

## 🔍 Key Algorithms

### Subset Construction (NFA → DFA)
```
1. Start with initial state {q0}
2. For each unmarked state set S and symbol a:
   - Compute T = union of δ(q,a) for all q in S
   - Add T to DFA states if new
   - Create transition S →(a)→ T
3. Mark S as processed
4. Repeat until all states marked
5. Final states = sets containing NFA final states
```

### Chomsky Classification
```
Type 3 (Regular):            A → aB or A → a
Type 2 (Context-Free):       A → α  (single non-terminal on left)
Type 1 (Context-Sensitive):  αAβ → αγβ  (non-contracting)
Type 0 (Unrestricted):       no restrictions
```

### Lexer Scanning Loop (Lab 3)
```
1. Peek at current character
2. Skip whitespace; emit NEWLINE for '\n'
3. If '#': consume until end of line → COMMENT token
4. If '"': consume until closing '"' (handle escapes) → STRING token
5. If digit: consume digits; if '.' follows digit → FLOAT else INTEGER
6. If letter/'_': consume alphanumerics → look up in KEYWORDS, else IDENT
7. If operator: check one character ahead for two-character form (==, !=, <=, >=)
8. Otherwise: emit UNKNOWN and continue
9. Append EOF at end of source
```

---

## 🎓 Academic Integrity

This repository represents original work completed as part of university coursework. The implementations follow academic guidelines and are intended for educational purposes.

---

## 📧 Contact

**Ciocanu Ilinca**  
Technical University of Moldova  
Academic Year: 2025-2026

---

## 📄 License

This project is created for educational purposes as part of university coursework.

---

## 🙏 Acknowledgments

- **Instructors:** Cretu Dumitru, Vasile Drumea, Irina Cojuhari for excellent course materials
- **Graphviz community** for powerful visualization tools
- **Classic textbooks:** Hopcroft, Motwani & Ullman; Sipser for theoretical foundations
- **Crafting Interpreters** by Robert Nystrom for practical lexer design guidance

---

**Last Updated:** March 2026