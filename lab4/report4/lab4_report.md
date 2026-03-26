# Laboratory Work: Regular Expressions
**Course:** Formal Languages & Finite Automata  
**Topic:** Regular Expressions — Generation of Valid Strings  
**Variant:** 2  
**Authors of the assignment:** Cretu Dumitru, Vasile Drumea, Irina Cojuhari  

---

## Introduction

Regular expressions are one of the most fundamental tools in the theory of formal languages. They provide a compact, declarative
syntax for describing entire sets of strings — called regular languages — through a small set of operations: literal matching, 
concatenation, alternation, and repetition. Originally introduced by Stephen Kleene in the 1950s as part of his work on finite 
automata, regular expressions have since become ubiquitous in programming, compiler design, text processing, and protocol 
specification.

The objective of this laboratory work is not merely to recognise whether a given string conforms to a pattern, which is the 
classical use case, but to take the inverse path: given a regular expression, generate strings that belong to the language 
it describes. This reversal of the typical direction requires a genuine understanding of the expression's structure rather 
than a superficial familiarity with matching APIs.

Variant 2 of the assignment provides three regular expressions that must be interpreted and used as generators:

1. `M?N²(O|P)³Q*R*`
2. `(X|Y|Z)³8*(9|0)*`
3. `(H|i)(J|K)L*N?`

The implementation must be dynamic — the expressions are supplied as input strings and parsed at runtime — and must 
handle all standard quantifiers as well as Unicode superscript digits used as shorthand for exact repetition counts.

---

## Design and Implementation

### Approach: Parse Tree (AST) Based Generation

The core decision was to build a proper recursive-descent parser that converts the input regex string into an Abstract Syntax Tree (AST). 
This approach separates concerns cleanly: parsing logic is independent of generation logic, and new quantifier forms or operators
can be added without touching the generator.

The AST uses five node types.

`Literal` holds a single character. `Concatenation` holds an ordered list of child nodes whose strings are emitted in sequence. 
`Alternation` holds a list of choices, of which exactly one is selected at random during generation. 
`Quantifier` wraps any node with a minimum and maximum repetition count; 
when the maximum is unbounded (i.e., the `*` or `+` operator), it is capped at a configurable limit to prevent arbitrarily 
long strings.

### Lexer and Parser

The `RegexParser` class implements a straightforward recursive-descent strategy with three mutually recursive procedures 
corresponding to the three levels of precedence: alternation (lowest), concatenation (middle), and atom with quantifier (highest). 
A single `pos` cursor advances through the input string.

Unicode superscript digits (`²`, `³`, etc.) are recognised as quantifiers immediately after an atom, equivalent to the `{n}` form.
This allows the notation used in the assignment — which is common in mathematical descriptions of formal grammars — to be parsed
directly without any preprocessing step.

### Generator

The `RegexGenerator` class walks the AST with a simple recursive `_gen` method. For `Alternation` nodes it calls `random.choice`;
for `Quantifier` nodes it calls `random.randint(min, max)` and repeats the child's generation that many times. The generation of a
single string is therefore a single depth-first traversal of the tree.

An optional `track` flag enables the bonus feature: every decision made during traversal is appended to a log list with a sequential
step number, producing a human-readable trace of the processing sequence.

### Validation

Each generated string is cross-checked against Python's standard `re.fullmatch` function using an equivalent Python regex 
(with `{n}` instead of superscript digits). This provides an independent correctness guarantee entirely separate from the 
generator's own logic.

---

## Results

Below are sample outputs obtained by running the generator ten times for each expression. Strings are shown after deduplication
to illustrate the variety of the produced language.

### Regex 1: `M?N²(O|P)³Q*R*`

The optional `M`, the mandatory double `N`, exactly three choices from `{O, P}`, and zero-to-five repetitions of `Q` and `R` 
individually yield strings such as:

```
MNNOOOQQRRR
MNNOOPQQQQQRRRR
MNNPPPQRR
NNOOPQQQQR
NNPPPQQQQQRRRR
```

The `M?` prefix makes it absent in roughly half the samples, and all eight combinations of O/P in three positions appear across
repeated runs.

### Regex 2: `(X|Y|Z)³8⁺(9|0)`

Three letters chosen independently from `{X, Y, Z}`, followed by one-to-five eights (`8⁺`), followed by exactly one digit from
`{9, 0}`:

```
XXX88880
XXY8889
YYX888889
ZYX88889
ZYZ888889
```

The `8⁺` quantifier guarantees at least one `8` is always present, and the trailing `(9|0)` with no quantifier means the string
always ends with exactly one digit.

### Regex 3: `(H|i)(J|K)L*N?`

One letter from `{H, i}`, one from `{J, K}`, zero-to-five `L`s, and an optional trailing `N`:

```
HJLLL
HJN
HKLLLN
iJLLLLL
iKLLN
```

It is worth noting that the assignment uses lowercase `i` rather than uppercase `I` in this expression, which is preserved
faithfully in the implementation.

---

## Processing Trace (Bonus Objective)

The bonus feature attaches a step-by-step log to each generation run. An example trace for Regex 1 producing 
the string `MNNOOPQQQQRRRRR` looks as follows:

```
Step 01: Concatenation of 5 parts — processing each in order
Step 02: Quantifier {0,1} → repeat 1 time(s)
Step 03: Literal → emit 'M'
Step 04: Quantifier {2,2} → repeat 2 time(s)
Step 05: Literal → emit 'N'
Step 06: Literal → emit 'N'
Step 07: Quantifier {3,3} → repeat 3 time(s)
Step 08: Alternation {O, P} → chose 'O'
Step 09: Literal → emit 'O'
Step 10: Alternation {O, P} → chose 'O'
Step 11: Literal → emit 'O'
Step 12: Alternation {O, P} → chose 'P'
Step 13: Literal → emit 'P'
Step 14: Quantifier {0,∞ (capped 5)} → repeat 4 time(s)
Step 15–18: Literal → emit 'Q' (×4)
Step 19: Quantifier {0,∞ (capped 5)} → repeat 5 time(s)
Step 20–24: Literal → emit 'R' (×5)
```

This trace exposes the tree traversal order directly and demonstrates that the generator is genuinely interpreting 
the expression's structure rather than following a hardcoded path.

---

## Difficulties Encountered

The first notable challenge was the superscript digit notation. Python's `re` module does not recognise `²` or `³` 
as quantifiers, so the parser had to handle them as first-class syntax. 
Building a lookup table of Unicode code points and treating them identically to `{n}` resolved this cleanly.

A subtler difficulty arose when designing the trace feature. Because the generator is recursive and alternation nodes make random
choices, the same trace location can produce different labels on different runs. Ensuring that the log reflects the choices actually
made, rather than describing the possibilities in the abstract, required logging inside the generation function itself, 
after the random selection, rather than before it.

The question of capping unbounded repetitions also required a deliberate design decision. A cap of five is applied globally, 
matching the assignment's specification, but the cap is a parameter so that different limits can be applied to different expression 
sets without modifying the parser or generator code.

---

## Conclusions

This laboratory work demonstrated that regular expressions are not merely pattern-matching tools but formal objects with a 
well-defined compositional structure. By building an AST-based parser and a recursive generator, it became clear that the 
set of strings described by a regular expression is entirely determined by the tree structure of the expression, and that 
generating members of this set is structurally identical to evaluating the expression — the only difference is that choices 
resolve randomly rather than by matching against an input.

The implementation successfully handles all three Variant 2 expressions, produces validated output, and provides a human-readable
trace of the generation process. All generated strings were independently verified against Python's `re.fullmatch`, confirming correctness across all tested runs.

---

## Source Code

The complete implementation is contained in multiple files: `regex_generator.py`, `regex_parser.py`, `ast_def.py`, `main.py` . 
It requires only Python's standard library (`random`, `re`, `dataclasses`). Running it directly prints ten sample strings per regex along with a processing trace.

```bash
python main.py
```