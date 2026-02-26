from grammar import Grammar
from finite_automaton import FiniteAutomaton
from collections import defaultdict


def create_variant6_fa():
    """
    Create the finite automaton for Variant 6.

    Variant 6:
    Q = {q0,q1,q2,q3,q4}
    Σ = {a,b}
    F = {q4}
    δ(q0,a) = q1
    δ(q1,b) = q1
    δ(q1,b) = q2  # Note: This makes it non-deterministic!
    δ(q2,b) = q3
    δ(q3,a) = q1
    δ(q2,a) = q4
    """
    states = {'q0', 'q1', 'q2', 'q3', 'q4'}
    alphabet = {'a', 'b'}
    final_states = {'q4'}
    start_state = 'q0'

    # Transitions (note: q1,b can go to both q1 and q2 - this is NFA)
    transitions = defaultdict(list)
    transitions[('q0', 'a')] = ['q1']
    transitions[('q1', 'b')] = ['q1', 'q2']  # Non-deterministic transition
    transitions[('q2', 'b')] = ['q3']
    transitions[('q3', 'a')] = ['q1']
    transitions[('q2', 'a')] = ['q4']

    return FiniteAutomaton(states, alphabet, transitions, start_state, final_states)


def create_example_grammar():
    """
    Create an example grammar from previous lab for Chomsky classification.
    This is a Type 3 (Regular) grammar.
    """
    non_terminals = {'S', 'A', 'B'}
    terminals = {'a', 'b', 'c'}
    productions = {
        'S': ['aA', 'bB'],
        'A': ['aA', 'bB', 'c'],
        'B': ['bB', 'a']
    }
    start_symbol = 'S'

    return Grammar(non_terminals, terminals, productions, start_symbol)


def save_graphviz(automaton, filename):
    """Save automaton visualization in DOT format."""
    dot_content = automaton.to_graphviz()
    with open(filename, 'w') as f:
        f.write(dot_content)
    print(f"\n Graphviz DOT file saved: {filename}")
    print(f"  To visualize, use: dot -Tpng lab2/{filename} -o lab2/{filename.replace('.dot', '.png')}")


def main():
    print("=" * 80)
    print("FORMAL LANGUAGES & FINITE AUTOMATA - LABORATORY WORK #2")
    print("Variant 6: Determinism and NFA to DFA Conversion")
    print("=" * 80)

    # Part 1: Grammar Classification (Chomsky Hierarchy)
    print("\n" + "=" * 80)
    print("PART 1: CHOMSKY HIERARCHY CLASSIFICATION")
    print("=" * 80)

    grammar = create_example_grammar()
    print("\n" + str(grammar))
    print(f"Chomsky Classification: {grammar.classify_chomsky()}")

    # Part 2: Finite Automaton Analysis
    print("\n" + "=" * 80)
    print("PART 2: FINITE AUTOMATON ANALYSIS (VARIANT 6)")
    print("=" * 80)

    # Create the FA
    fa = create_variant6_fa()
    print("\n" + str(fa))

    # Task 3b: Determine if FA is deterministic
    print("\n" + "-" * 80)
    print("Task 3b: Determinism Check")
    print("-" * 80)
    is_det = fa.is_deterministic()
    print(f"\nIs the automaton deterministic? {'YES (DFA)' if is_det else 'NO (NFA)'}")

    if not is_det:
        print("\nReason: The transition δ(q1, b) leads to multiple states: {q1, q2}")
        print("This violates the determinism property where each (state, symbol) pair")
        print("must lead to exactly one state.")

    # Task 3a: Convert FA to Regular Grammar
    print("\n" + "-" * 80)
    print("Task 3a: Conversion to Regular Grammar")
    print("-" * 80)

    regular_grammar = fa.to_regular_grammar()
    print("\n" + str(regular_grammar))
    print(f"Grammar Classification: {regular_grammar.classify_chomsky()}")

    # Task 3c: Convert NFA to DFA
    print("\n" + "-" * 80)
    print("Task 3c: NFA to DFA Conversion")
    print("-" * 80)

    if not is_det:
        print("\nApplying subset construction algorithm...")
        dfa = fa.nfa_to_dfa()

        print("\nResulting DFA:")
        print(str(dfa))

        print(f"\nIs the resulting automaton deterministic? {'YES (DFA)' if dfa.is_deterministic() else 'NO (NFA)'}")

        # Compare state counts
        print(f"\nState count comparison:")
        print(f"  Original NFA: {len(fa.Q)} states")
        print(f"  Resulting DFA: {len(dfa.Q)} states")

        # Task 3d: Generate visualizations
        print("\n" + "-" * 80)
        print("Task 3d: Graphical Representation")
        print("-" * 80)

        save_graphviz(fa, 'variant6_nfa.dot')
        save_graphviz(dfa, 'variant6_dfa.dot')

    print("\nAll tasks completed successfully!")
    print("=" * 80)


if __name__ == "__main__":
    main()