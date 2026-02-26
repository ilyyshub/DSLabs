# Laboratory Work #2: Determinism in Finite Automata

**Course:** Formal Languages & Finite Automata  
**Author:** Cretu Dumitru  
**Variant:** 6  
**Date:** February 2026

---

## Table of Contents

1. [Objectives](#objectives)
2. [Theory](#theory)
3. [Implementation](#implementation)
4. [Results and Analysis](#results-and-analysis)
5. [Conclusions](#conclusions)
6. [References](#references)

---

## Objectives

The main objectives of this laboratory work are:

1. Understand what an automaton is and what it can be used for
2. Implement grammar classification based on Chomsky hierarchy
3. Convert a finite automaton to a regular grammar
4. Determine whether a finite automaton is deterministic or non-deterministic
5. Implement NFA to DFA conversion using subset construction algorithm
6. Represent the finite automaton graphically

---

## Theory

### Finite Automata

A **finite automaton (FA)** is a mathematical model of computation used to represent and recognize patterns in strings. It consists of:

- **Q**: A finite set of states
- **Σ**: A finite set of input symbols (alphabet)
- **δ**: A transition function δ: Q × Σ → P(Q)
- **q₀**: An initial/start state (q₀ ∈ Q)
- **F**: A set of final/accepting states (F ⊆ Q)

### Determinism vs Non-determinism

A finite automaton is **deterministic (DFA)** if:
1. For each state and input symbol, there is exactly one transition
2. No ε (epsilon) transitions exist

A finite automaton is **non-deterministic (NFA)** if:
1. For some state and input symbol, there are multiple possible transitions
2. ε-transitions may exist

**Important:** Every NFA can be converted to an equivalent DFA using the **subset construction algorithm**.

### Chomsky Hierarchy

The Chomsky hierarchy classifies grammars into four types:

- **Type 0 (Unrestricted)**: No restrictions on productions
- **Type 1 (Context-Sensitive)**: Productions of form αAβ → αγβ where |αγβ| ≥ |αAβ|
- **Type 2 (Context-Free)**: Productions of form A → α where A is a single non-terminal
- **Type 3 (Regular)**: Productions of form A → aB or A → a (right-regular)

Regular grammars and finite automata are equivalent in their expressive power.

### Subset Construction Algorithm

The algorithm to convert NFA to DFA:

1. Start with the initial state {q₀}
2. For each unmarked state set S and each input symbol a:
   - Compute T = δ(S, a) = union of δ(q, a) for all q in S
   - If T is not already a state, add it to the DFA states
   - Add transition from S to T on symbol a
3. Mark S as processed
4. Repeat until all states are marked
5. Final states are those containing at least one NFA final state

---

## Implementation

### Project Structure

```
lab2-finite-automata/
├── grammar.py              # Grammar class with Chomsky classification
├── finite_automaton.py     # FiniteAutomaton class with all conversions
├── main.py                 # Main demonstration program
├── test_automata.py        # Unit tests
├── variant6_nfa.dot        # Graphviz representation of NFA
├── variant6_dfa.dot        # Graphviz representation of DFA
└── report2.md               # This report
```

### Grammar Class

The `Grammar` class implements Chomsky hierarchy classification:

```python
class Grammar:
    def __init__(self, non_terminals, terminals, productions, start_symbol):
        self.VN = non_terminals    # Non-terminal symbols
        self.VT = terminals         # Terminal symbols
        self.P = productions        # Production rules
        self.S = start_symbol       # Start symbol
    
    def classify_chomsky(self):
        """Classify grammar according to Chomsky hierarchy."""
        if self.is_type3():
            return "Type 3 (Regular Grammar)"
        elif self.is_type2():
            return "Type 2 (Context-Free Grammar)"
        elif self.is_type1():
            return "Type 1 (Context-Sensitive Grammar)"
        else:
            return "Type 0 (Unrestricted Grammar)"
```

### FiniteAutomaton Class

The `FiniteAutomaton` class implements all required functionality:

#### 1. Determinism Check

```python
def is_deterministic(self):
    """Check if the FA is deterministic."""
    for (state, symbol) in self.delta:
        if len(self.delta[(state, symbol)]) > 1:
            return False  # Multiple transitions
        if symbol == 'ε' or symbol == '':
            return False  # Epsilon transition
    return True
```

#### 2. FA to Regular Grammar Conversion

```python
def to_regular_grammar(self):
    """Convert FA to regular grammar."""
    productions = defaultdict(list)
    
    for (state, symbol), next_states in self.delta.items():
        for next_state in next_states:
            # Add production: state -> symbol next_state
            production = symbol + next_state
            productions[state].append(production)
            
            # If next_state is final: state -> symbol
            if next_state in self.F:
                productions[state].append(symbol)
    
    return Grammar(self.Q, self.Sigma, dict(productions), self.q0)
```

#### 3. NFA to DFA Conversion (Subset Construction)

```python
def nfa_to_dfa(self):
    """Convert NFA to DFA using subset construction."""
    dfa_states = set()
    dfa_transitions = {}
    dfa_start_state = frozenset([self.q0])
    
    unmarked_states = deque([dfa_start_state])
    dfa_states.add(dfa_start_state)
    
    while unmarked_states:
        current_state_set = unmarked_states.popleft()
        
        for symbol in self.Sigma:
            next_state_set = set()
            for state in current_state_set:
                if (state, symbol) in self.delta:
                    next_state_set.update(self.delta[(state, symbol)])
            
            if next_state_set:
                next_state_frozen = frozenset(next_state_set)
                if next_state_frozen not in dfa_states:
                    dfa_states.add(next_state_frozen)
                    unmarked_states.append(next_state_frozen)
                
                # Add transition
                dfa_transitions[(current, symbol)] = [next]
    
    return FiniteAutomaton(...)
```

### Variant 6 Specification

The given finite automaton for Variant 6:

- **Q** = {q0, q1, q2, q3, q4}
- **Σ** = {a, b}
- **q₀** = q0
- **F** = {q4}
- **Transitions:**
  - δ(q0, a) = q1
  - δ(q1, b) = q1
  - δ(q1, b) = q2  ← **Non-deterministic!**
  - δ(q2, b) = q3
  - δ(q3, a) = q1
  - δ(q2, a) = q4

---

## Results and Analysis

### 1. Chomsky Hierarchy Classification

An example grammar was tested:

```
Non-terminals: {S, A, B}
Terminals: {a, b, c}
Productions:
  S -> aA | bB
  A -> aA | bB | c
  B -> bB | a

Classification: Type 3 (Regular Grammar)
```

This grammar is regular because all productions follow the pattern A → aB or A → a.

### 2. Determinism Analysis

**Input NFA (Variant 6):**

```
States: {q0, q1, q2, q3, q4}
Alphabet: {a, b}
Start state: q0
Final states: {q4}

Transitions:
  δ(q0, a) = q1
  δ(q1, b) = q1
  δ(q1, b) = q2  ← Multiple transitions!
  δ(q2, a) = q4
  δ(q2, b) = q3
  δ(q3, a) = q1
```

**Result:** The automaton is **non-deterministic (NFA)**.

**Reason:** The transition δ(q1, b) leads to two different states: {q1, q2}. This violates the determinism property where each (state, symbol) pair must lead to exactly one state.

### 3. FA to Regular Grammar Conversion

The NFA was successfully converted to a regular grammar:

```
Non-terminals: {q0, q1, q2, q3, q4}
Terminals: {a, b}
Start symbol: q0

Productions:
  q0 -> aq1
  q1 -> bq1 | bq2
  q2 -> bq3 | aq4 | a
  q3 -> aq1
```

Note: The production `q2 -> a` exists because q4 (the target of δ(q2, a)) is a final state.

### 4. NFA to DFA Conversion

**Subset Construction Results:**

```
Original NFA: 5 states
Resulting DFA: 6 states

DFA States:
  {q0}         - Initial state
  {q1}         - After 'a' from {q0}
  {q1,q2}      - After 'b' from {q1}
  {q1,q2,q3}   - After 'b' from {q1,q2}
  {q4}         - After 'a' from {q1,q2}
  {q1,q4}      - After 'a' from {q1,q2,q3}

Final DFA states: {{q4}, {q1,q4}}
```

**Key Observations:**

1. The DFA has 6 states (one more than the NFA)
2. States are now sets of original NFA states
3. All transitions are deterministic (one transition per state-symbol pair)
4. Any state containing q4 is a final state

**DFA Transitions:**

```
δ({q0}, a) = {q1}
δ({q1}, b) = {q1,q2}
δ({q1,q2}, a) = {q4}
δ({q1,q2}, b) = {q1,q2,q3}
δ({q1,q2,q3}, a) = {q1,q4}
δ({q1,q2,q3}, b) = {q1,q2,q3}
δ({q1,q4}, b) = {q1,q2}
```

### 5. Graphical Representation

The automata were visualized using Graphviz. The DOT files generate clear state diagrams showing:

- States as circles
- Final states as double circles
- Transitions as labeled arrows
- An incoming arrow to the start state

**NFA Visualization:**
- Shows the non-deterministic transition from q1 with label 'b' going to both q1 and q2
- 5 states clearly visible
- Simple, clean structure

**DFA Visualization:**
- Shows compound states like {q1,q2}
- 6 states with more complex structure
- All transitions are deterministic
- Clearly shows which states are final



---

## Conclusions

### Key Findings

1. **Chomsky Hierarchy Classification**
   - Successfully implemented an algorithm to classify grammars into the four Chomsky types
   - The classification is based on the structure and restrictions of production rules
   - Regular grammars (Type 3) have the most restrictive form

2. **Determinism Analysis**
   - Variant 6's finite automaton is non-deterministic (NFA)
   - Non-determinism arises from the transition δ(q1, b) leading to multiple states
   - Determinism can be checked algorithmically by examining the transition function

3. **NFA to DFA Conversion**
   - The subset construction algorithm successfully converts any NFA to an equivalent DFA
   - The resulting DFA may have more states (2^n in worst case, where n is NFA state count)
   - For Variant 6: 5 NFA states → 6 DFA states
   - The conversion preserves the language accepted by the automaton

4. **FA-Grammar Equivalence**
   - Finite automata and regular grammars are equivalent in expressive power
   - Conversion between them is straightforward and algorithmic
   - Both models accept exactly the regular languages

### Practical Insights

- Non-determinism in automata theory is not about randomness but about multiple possible paths
- DFA is easier to implement in practice but NFA is more intuitive to design
- The subset construction algorithm is fundamental in compiler design and lexical analysis
- Graphical representations greatly aid in understanding automaton behavior

### Learning Outcomes

Through this laboratory work, I have:
- Deepened understanding of automata theory and formal language classification
- Implemented core algorithms used in compiler construction
- Gained practical experience with graph theory and state machines
- Understood the theoretical foundations of regular expressions and pattern matching
- Developed skills in algorithm implementation

### Future Work

Possible extensions to this project:
1. Implement DFA minimization algorithm (Hopcroft's algorithm)
2. Add support for ε-transitions and ε-closure computation
3. Implement string acceptance testing for both NFA and DFA
4. Create an interactive web interface for automaton visualization
5. Add more grammar types and conversion algorithms

## Appendix: Code Examples

### Running the Program

```bash
# Run main demonstration
python main.py

# Generate visualizations
dot -Tpng lab2/variant6_nfa.dot -o lab2/variant6_nfa.png
dot -Tpng lab2variant6_dfa.dot -o lab2/variant6_dfa.png
```

### Sample Output

```
================================================================================
FORMAL LANGUAGES & FINITE AUTOMATA - LABORATORY WORK #2
Variant 6: Determinism and NFA to DFA Conversion
================================================================================

PART 1: CHOMSKY HIERARCHY CLASSIFICATION
Grammar Classification: Type 3 (Regular Grammar)

PART 2: FINITE AUTOMATON ANALYSIS (VARIANT 6)
Is the automaton deterministic? NO (NFA)
Reason: The transition δ(q1, b) leads to multiple states: {q1, q2}

PART 3: NFA TO DFA CONVERSION
Original NFA: 5 states
Resulting DFA: 6 states
Is the resulting automaton deterministic? YES (DFA)

All tasks completed successfully!
================================================================================
```

---

## References

1. Hopcroft, J. E., Motwani, R., & Ullman, J. D. (2006). *Introduction to Automata Theory, Languages, and Computation* (3rd ed.). Pearson.

2. Sipser, M. (2012). *Introduction to the Theory of Computation* (3rd ed.). Cengage Learning.

3. Chomsky, N. (1956). "Three models for the description of language". *IRE Transactions on Information Theory*, 2(3), 113-124.

4. Course materials: "Formal Languages & Finite Automata" by Cretu Dumitru, with contributions from Vasile Drumea and Irina Cojuhari.

5. Graphviz - Graph Visualization Software. https://graphviz.org/

---

