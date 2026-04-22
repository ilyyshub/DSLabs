# Laboratory Work: Chomsky Normal Form
**Course:** Formal Languages & Finite Automata  
**Topic:** Chomsky Normal Form (CNF)  
**Variant:** 6  
**Authors of the assignment:** Cretu Dumitru, Vasile Drumea, Irina Cojuhari  

---

## Introduction

Chomsky Normal Form (CNF) is a standard normal form for context-free grammars in which each production is restricted to one of two shapes:

1. `A -> BC` (two non-terminals)
2. `A -> a` (one terminal)

Optionally, the start symbol may derive `ε` in the special case where the language contains the empty string.

Normalizing a grammar to CNF is important for formal analysis and algorithmic processing (for example, CYK parsing), because it enforces a uniform production structure while preserving the generated language (modulo the standard handling of `ε`).

In the context of formal language theory, CNF is not only a theoretical construction but also a practical representation used by parsers and verification procedures. A grammar expressed in CNF has a constrained and predictable structure, which simplifies proof techniques, parser implementation, and complexity analysis of recognition algorithms.

This report documents the complete transformation of the given Variant 6 context-free grammar into CNF. The transformation is performed as a sequence of standard, language-preserving rewriting phases. Each phase targets a specific class of productions that are incompatible with CNF constraints, and each intermediate grammar is inspected to validate correctness.

### Objectives

The objectives of this laboratory work are:

1. Implement a correct and reusable normalization pipeline for converting a context-free grammar to CNF.
2. Apply the pipeline to the provided Variant 6 grammar.
3. Record and inspect intermediate grammars after each transformation stage.
4. Validate that the final grammar satisfies CNF rules.
5. Demonstrate that the implementation is generic and can process grammars beyond the required variant.

For Variant 6, the input grammar is:

`G = (VN, VT, P, S)` with:

- `VN = {S, A, B, C, E}`
- `VT = {a, b}`
- `S = S`
- Productions:
  - `S -> aB`
  - `S -> AC`
  - `A -> a`
  - `A -> ASC`
  - `A -> BC`
  - `B -> b`
  - `B -> bS`
  - `C -> ε`
  - `C -> BA`
  - `E -> bB`

### Initial Observations About the Input Grammar

Before normalization, the grammar contains several forms that must be transformed:

1. A nullable production: `C -> ε`.
2. Mixed terminal and non-terminal production bodies with length greater than 1, such as `S -> aB` and `B -> bS`.
3. A production body of length 3: `A -> ASC`, which violates CNF arity constraints.
4. A potentially inaccessible non-terminal (`E`) from the start symbol.

These observations motivate the exact order of the normalization pipeline implemented in the solution.

---

## Design and Implementation

### Approach

The solution is implemented as a reusable `CNFNormalizer` class in `lab5/cnf_normalizer.py`.  
It is designed as a generic transformation pipeline that can process arbitrary context-free grammars (bonus objective), not only Variant 6.

The implementation emphasizes separation of concerns: each transformation stage is implemented as a dedicated procedure with a clear contract. This design makes the pipeline easier to test, reason about, and reuse. Instead of hard-coding rules for one grammar instance, the code works with an abstract grammar representation and performs symbol-level rewrites algorithmically.

The grammar representation is encapsulated in a `CFG` dataclass:

- `non_terminals: set[str]`
- `terminals: set[str]`
- `productions: dict[str, set[tuple[str, ...]]]`
- `start_symbol: str`

This representation supports deterministic processing and avoids duplicate productions through `set` semantics. It also allows each production right-hand side to be treated as a sequence of symbols, which simplifies rule inspection and conversion during normalization.

### Normalization Pipeline

The normalizer applies the required sequence:

1. Eliminate `ε`-productions
2. Eliminate renaming (unit) productions
3. Eliminate inaccessible symbols
4. Eliminate non-productive symbols
5. Convert to strict CNF
   - replace terminals inside longer RHS using dedicated non-terminals
   - binarize productions longer than 2 symbols

The order above is intentional. Removing `ε`-productions and unit productions early prevents these forms from reappearing after structural CNF conversion and reduces the number of cases that later stages must process. Pruning inaccessible and non-productive symbols further simplifies the grammar before introducing helper symbols during CNF enforcement.

Implementation details:

- Nullable set computation is iterative until fixpoint.
- Unit-production removal uses transitive unit-closure for each non-terminal.
- Accessibility starts from the start symbol and follows non-terminal references.
- Productivity is computed bottom-up from terminal-generating rules.
- CNF enforcement introduces fresh helper symbols (`T_*`, `X_*`) as needed.

### Transformation Rationale by Stage

1. `ε`-elimination: nullable symbols are identified through a fixpoint computation; then all combinations of nullable symbol omission are generated for affected productions while preserving language equivalence under standard CNF assumptions.
2. Unit-production elimination: for each non-terminal, transitive unit reachability is computed so that indirect renaming chains can be replaced with direct non-unit productions.
3. Inaccessibility elimination: only symbols reachable from the start symbol are retained, ensuring no unreachable fragment remains in the grammar.
4. Non-productivity elimination: symbols that cannot derive terminal strings are removed with all dependent productions.
5. Strict CNF conversion: terminals occurring inside longer bodies are mapped to dedicated terminal non-terminals, and bodies longer than two symbols are binarized via fresh helper non-terminals.

### Correctness Considerations

To preserve correctness, the implementation avoids in-place mutation patterns that could invalidate iteration state while rewriting production maps. Intermediate sets and snapshots are used where needed, then committed as new production structures. This approach lowers the risk of accidental rule loss, duplicate insertion, or partial rewrites.

### Executable Entry Point

`lab5/main.py` builds the Variant 6 grammar and runs the full pipeline, printing every intermediate grammar after each transformation step.

This step-by-step output is important for traceability: it allows direct verification that each stage applies the expected structural changes and that no unintended transformations are introduced.

---

## Results

Running:

```bash
cd lab5
python3 main.py
```

produces all intermediate grammars and the final CNF grammar.  
The final verification result is:

`Is final grammar in CNF? YES`

During normalization, symbol `E` is removed as inaccessible (it cannot be reached from the start symbol).

### Interpretation of Results

The reported result confirms that all final productions conform to CNF constraints:

1. Binary non-terminal productions of the form `A -> BC`.
2. Single-terminal productions of the form `A -> a`.

The elimination of `E` demonstrates that grammar simplification stages are functioning correctly and are not merely cosmetic. Removing inaccessible symbols reduces grammar size and helps maintain a minimal and analyzable final representation.

Because intermediate grammars are printed after every phase, the conversion process is auditable. This provides practical evidence that each stage contributes to normalization and that the final `YES` result is consistent with the full transformation trace.

---

## Bonus Objective (Generic Grammar Support)

The normalizer accepts any grammar provided through `CFG.from_compact(...)` (or directly via `CFG`), as long as symbols and productions are specified.

This is validated through unit tests with an additional grammar different from Variant 6, confirming that the same normalization pipeline still yields CNF.

From an engineering perspective, this generic support increases the utility of the implementation beyond a single assignment instance. It also validates that the algorithmic design is grammar-independent and correctly handles varying production structures under the same normalization strategy.

---

## Difficulties Encountered

The main implementation challenge was safely transforming productions while introducing helper non-terminals.  
In particular, binarization must avoid mutating dictionaries during iteration. This was solved by iterating over a snapshot of production items and writing results into a new structure.

Another subtle point was preserving a correct start symbol when it appears on right-hand sides; a fresh start symbol is introduced in that case to keep transformations sound.

An additional practical difficulty was ensuring that transformation order did not reintroduce forms removed by earlier stages. The pipeline sequencing and independent stage validation helped prevent this issue and ensured predictable normalization behavior.

---

## Conclusions

This laboratory work shows that CNF conversion is a deterministic multi-phase transformation process that can be implemented cleanly and generically.  
The Variant 6 grammar was normalized successfully, all required elimination steps were performed, and the resulting grammar satisfies CNF constraints.

The implementation also fulfills the bonus requirement by supporting normalization of arbitrary input grammars through a reusable class interface.

Overall, the final artifact combines theoretical correctness with practical usability: it follows standard formal-language transformations, provides transparent intermediate outputs, and is structured as reusable code suitable for further experiments (e.g., parser integration or comparative grammar analysis).

---

## Source Code

Files added for this lab:

- `lab5/cnf_normalizer.py` — reusable grammar and CNF normalization logic
- `lab5/main.py` — Variant 6 runner and step-by-step output
- `lab5/test_cnf.py` — tests for Variant 6 and generic-grammar bonus case

Run:

```bash
cd lab5
python3 main.py
python3 -m unittest -v test_cnf.py
```

The first command sequence demonstrates the full normalization workflow for Variant 6, while the unit test command validates both assignment-specific behavior and the generic grammar-processing capability required by the bonus objective.

