from grammar import Grammar
from finite_automaton import FiniteAutomaton


def main():

    #Main client program to demonstrate Grammar and Finite Automaton functionality.
    #This implements Variant 6.

    print("=" * 70)
    print("LABORATORY WORK #1: Regular Grammars and Finite Automata")
    print("Variant 6")
    print("=" * 70)
    print()

    # Define the grammar for Variant 6
    # V_N = {S, I, J, K}
    # V_T = {a, b, c, e, n, f, m}
    # Productions:
    #   S → cI
    #   I → bJ | fI | eK | e
    #   J → nJ | cS
    #   K → nK | m

    non_terminals = {'S', 'I', 'J', 'K'}
    terminals = {'a', 'b', 'c', 'e', 'n', 'f', 'm'}

    productions = {
        'S': ['cI'],
        'I': ['bJ', 'fI', 'eK', 'e'],
        'J': ['nJ', 'cS'],
        'K': ['nK', 'm']
    }

    start_symbol = 'S'

    # Create the grammar object
    grammar = Grammar(non_terminals, terminals, productions, start_symbol)

    print("GRAMMAR DEFINITION:")
    print(grammar)
    print()

    # Task 3.b: Generate 5 valid strings
    print("=" * 70)
    print("TASK 1: Generate 5 valid strings from the grammar")
    print("=" * 70)
    print()

    generated_strings = []
    for i in range(5):
        string = grammar.generate_string()
        generated_strings.append(string)
        print(f"String {i + 1}: {string}")

    print()

    # Task 3.c: Convert Grammar to Finite Automaton
    print("=" * 70)
    print("TASK 2: Convert Grammar to Finite Automaton")
    print("=" * 70)
    print()

    fa = grammar.to_finite_automaton()
    print(fa)
    print()

    # Task 3.d: Check if strings belong to the language
    print("=" * 70)
    print("TASK 3: Check if strings belong to the language")
    print("=" * 70)
    print()

    # Test with generated strings
    print("Testing generated strings:")
    for i, string in enumerate(generated_strings):
        belongs = fa.string_belongs_to_language(string)
        status = "ACCEPTED" if belongs else "REJECTED"
        print(f"  String {i + 1}: '{string}' -> {status}")

    print()

    # Test with some additional strings (valid and invalid)
    test_strings = [
        ("cbe", True),  # S - cI - cbJ - cbeK - cbem (should fail, ends with e not m)
        ("cbem", True),  # S - cI - cbJ - cbeK - cbem (valid)
        ("ce", True),  # S - cI - ce (valid)
        ("cfbe", True),  # S - cI - cfI - cfbJ - cfbeK - cfbem (should fail)
        ("cbncm", True),  # S - cI - cbJ - cbnJ - cbncS - cbncI - cbnce
        ("abc", False),  # Invalid (doesn't start with c)
        ("", False),  # Empty string
        ("c", False),  # Incomplete
    ]

    print("Testing additional strings:")
    for string, expected in test_strings:
        belongs = fa.string_belongs_to_language(string)
        status = "ACCEPTED" if belongs else "REJECTED"
        expected_str = "(expected)" if belongs == expected else "(unexpected!)"
        print(f"  '{string}' -> {status} {expected_str}")


    print()
    print("=" * 70)
    print("DEMONSTRATION COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()