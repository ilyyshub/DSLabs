# Laboratory Work #1: Regular Grammars and Finite Automata

**Course:** Formal Languages & Finite Automata  
**Author:** Ciocanu Ilinca 
**Variant:** 6  

---

## Table of Contents
1. [Objectives](#objectives)
2. [Theory](#theory)
3. [Implementation](#implementation)
4. [Results and Screenshots](#results-and-screenshots)
5. [Conclusions](#conclusions)
6. [References](#references)

---

## Objectives

The main objectives of this laboratory work were:

1. **Understand formal languages** - Learn what constitutes a formal language and its components (alphabet, vocabulary, grammar)
2. **Implement a Grammar class** - Create a type/class to represent a formal grammar with its productions
3. **Generate strings** - Implement functionality to generate valid strings from the language defined by the grammar
4. **Grammar to FA conversion** - Convert a Grammar object to a Finite Automaton
5. **String validation** - Implement a method to check if strings belong to the language accepted by the finite automaton

---

## Theory

### Formal Language
A **formal language** is defined by:
- **Alphabet (Σ)**: A finite set of symbols/characters
- **Vocabulary (V)**: Set of valid words formed from the alphabet
- **Grammar (G)**: Set of rules (productions) that define how to form valid strings

### Grammar Components
A grammar G is formally defined as a 4-tuple: **G = (V_N, V_T, P, S)** where:
- **V_N**: Set of non-terminal symbols (variables)
- **V_T**: Set of terminal symbols (alphabet)
- **P**: Set of production rules
- **S**: Start symbol (S ∈ V_N)

### Regular Grammar
A **regular grammar** is a grammar where all production rules are of one of these forms:
- A → aB (right-linear)
- A → a
- A → ε (epsilon/empty string)

Where A, B ∈ V_N and a ∈ V_T.

### Finite Automaton
A **Finite Automaton (FA)** is defined as a 5-tuple: **FA = (Q, Σ, δ, q0, F)** where:
- **Q**: Finite set of states
- **Σ**: Alphabet (input symbols)
- **δ**: Transition function δ: Q × Σ → Q (for DFA) or δ: Q × Σ → 2^Q (for NFA)
- **q0**: Initial state (q0 ∈ Q)
- **F**: Set of final/accepting states (F ⊆ Q)

### Grammar to FA Conversion
For a right-linear regular grammar:
1. Each non-terminal becomes a state
2. Add a final state qf
3. For production A → aB: add transition δ(A, a) = B
4. For production A → a: add transition δ(A, a) = qf
5. Start symbol S becomes initial state q0

---

## Implementation

### Variant 6 Grammar Definition

```
V_N = {S, I, J, K}
V_T = {a, b, c, e, n, f, m}
P = {
    S → cI
    I → bJ
    I → fI
    I → eK
    I → e
    J → nJ
    J → cS
    K → nK
    K → m
}
Start symbol: S
```

### Class Structure

#### 1. Grammar Class (`grammar.py`)

```python
class Grammar:
    def __init__(self, non_terminals, terminals, productions, start_symbol):
        """Initialize grammar with V_N, V_T, P, and S"""
        
    def generate_string(self, max_depth=20):
        """Generate a random valid string by applying productions"""
        
    def to_finite_automaton(self):
        """Convert grammar to equivalent Finite Automaton"""
```

**String Generation Algorithm:**
1. Start with the start symbol S
2. Find leftmost non-terminal in current string
3. Randomly select a production for that non-terminal
4. Replace the non-terminal with the production
5. Repeat until no non-terminals remain or max depth reached

**Grammar to FA Conversion:**
- Creates states Q = V_N ∪ {qf}
- Maps each production rule to appropriate transitions
- Handles non-determinism when multiple productions exist for same symbol

#### 2. Finite Automaton Class (`finite_automaton.py`)

```python
class FiniteAutomaton:
    def __init__(self, states, alphabet, transitions, initial_state, final_states):
        """Initialize FA with Q, Σ, δ, q0, and F"""
        
    def string_belongs_to_language(self, input_string):
        """Check if string is accepted by the automaton using state transitions"""
```

**String Acceptance Algorithm (NFA):**
1. Start with set of current states = {q0}
2. For each symbol in input string:
   - For each current state, find all possible next states
   - Update current states to the union of all next states
3. Accept if any final state is in current states set

#### 3. Main Program (`main.py`)

Demonstrates:
- Grammar instantiation with Variant 6 data
- Generation of 5 valid strings
- Conversion to Finite Automaton
- Validation of generated and test strings

### Key Implementation Details

**Non-Deterministic Finite Automaton (NFA):**
The grammar has a non-deterministic aspect:
- Production `I → e` creates: δ(I, e) = qf
- Production `I → eK` creates: δ(I, e) = K

This results in δ(I, e) = {K, qf}, making it an NFA. The implementation handles this by:
- Storing transitions as sets of states
- Using a set-based state tracking algorithm
- Supporting both DFA and NFA formats

---

## Results and Screenshots

### Generated Strings (Sample Run)

```
String 1: cbccfe
String 2: cem
String 3: cfennm
String 4: cbnccfe
String 5: cbccfenm
```

### Finite Automaton Structure

```
Q (States) = {S, I, J, K, qf}
Σ (Alphabet) = {a, b, c, e, f, m, n}
q0 (Initial state) = S
F (Final states) = {qf}

Transitions:
  δ(S, c) = {I}
  δ(I, b) = {J}
  δ(I, e) = {K, qf}    ← Non-deterministic!
  δ(I, f) = {I}
  δ(J, c) = {S}
  δ(J, n) = {J}
  δ(K, n) = {K}
  δ(K, m) = {qf}
```

### String Validation Results

All generated strings were successfully validated:
- ✓ `cbccfe` - ACCEPTED
- ✓ `cem` - ACCEPTED
- ✓ `cfennm` - ACCEPTED
- ✓ `cbnccfe` - ACCEPTED
- ✓ `cbccfenm` - ACCEPTED

Additional test cases:
- ✓ `ce` - ACCEPTED (S → cI → ce)
- ✗ `abc` - REJECTED (doesn't start with 'c')
- ✗ `c` - REJECTED (incomplete derivation)

### Example Derivations

**String: "cem"**
```
S → cI → ceK → cem
```

**String: "cbccfe"**
```
S → cI → cbJ → cbcS → cbcI → cbcfI → cbcfe
```

---

## Conclusions

This laboratory work successfully demonstrated:

1. **Grammar Implementation**: Created a functional Grammar class that correctly represents formal grammar with non-terminals, terminals, productions, and start symbol.

2. **String Generation**: Implemented a random derivation algorithm that generates valid strings by repeatedly applying production rules until only terminals remain.

3. **Grammar-FA Equivalence**: Successfully converted a regular grammar to an equivalent Finite Automaton, handling the non-deterministic nature arising from multiple productions.

4. **NFA Support**: Recognized and properly handled non-determinism in the FA (when I → e and I → eK both exist), implementing an NFA acceptance algorithm using set-based state tracking.

5. **Validation**: Confirmed that all strings generated by the grammar are accepted by the converted automaton, verifying the correctness of both implementations.

### Key Learnings:
- Regular grammars and finite automata are equivalent in expressive power
- Non-determinism can arise naturally from grammar productions
- NFA acceptance requires tracking multiple possible states simultaneously
- Python's set operations are ideal for implementing NFA algorithms

### Challenges Faced:
- Initially implemented as DFA, which couldn't handle the non-determinism from `I → e` and `I → eK`
- Resolved by updating to support NFA with set-based transitions
- Learned the importance of considering all production rules when designing the automaton

---

## References

1. Course materials: "Intro to formal languages. Regular grammars. Finite Automata" by Cretu Dumitru
2. Hopcroft, J. E., Motwani, R., & Ullman, J. D. (2006). *Introduction to Automata Theory, Languages, and Computation*
3. Sipser, M. (2012). *Introduction to the Theory of Computation*
4. Python Documentation: https://docs.python.org/3/