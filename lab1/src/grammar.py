import random
from typing import List, Dict, Set


class Grammar:

    def __init__(self, non_terminals: Set[str], terminals: Set[str],
                 productions: Dict[str, List[str]], start_symbol: str):

        #Initialize the grammar.

        self.V_N = non_terminals
        self.V_T = terminals
        self.P = productions
        self.S = start_symbol

    def generate_string(self, max_depth: int = 20) -> str:

        #Generate a valid string from the grammar using derivation.
        #max_depth: Maximum depth to prevent infinite recursion

        current_string = self.S
        depth = 0

        # Continue deriving until no non-terminals remain or max depth reached
        while depth < max_depth:
            # Find the first non-terminal in the current string
            non_terminal_found = None
            non_terminal_position = -1

            for i, char in enumerate(current_string):
                if char in self.V_N:
                    non_terminal_found = char
                    non_terminal_position = i
                    break

            # If no non-terminal found, we have a complete string
            if non_terminal_found is None:
                return current_string

            # Get possible productions for this non-terminal
            if non_terminal_found in self.P:
                productions = self.P[non_terminal_found]
                # Randomly choose one production
                chosen_production = random.choice(productions)

                # Replace the non-terminal with the chosen production
                current_string = (current_string[:non_terminal_position] +
                                  chosen_production +
                                  current_string[non_terminal_position + 1:])

            depth += 1

        return current_string

    def to_finite_automaton(self):

        #Convert this grammar to a Finite Automaton.

        from finite_automaton import FiniteAutomaton

        # States: all non-terminals plus a final state
        states = self.V_N.copy()
        final_state = 'qf'
        states.add(final_state)

        # Alphabet: all terminals
        alphabet = self.V_T.copy()

        # Start state: the start symbol
        start_state = self.S

        # Final states: will include the final state
        final_states = {final_state}

        # Transitions: δ(state, symbol) -> set of possible next states (NFA)
        # Format: {(from_state, symbol): {set of to_states}}
        transitions = {}

        # Process each production rule
        for non_terminal, productions in self.P.items():
            for production in productions:
                if len(production) == 0:
                    # epsilon-production: A → epsilon means A is also a final state
                    final_states.add(non_terminal)
                elif len(production) == 1:
                    if production[0] in self.V_T:
                        # A → a (terminal only): transition to final state
                        key = (non_terminal, production[0])
                        if key not in transitions:
                            transitions[key] = set()
                        transitions[key].add(final_state)
                    elif production[0] in self.V_N:
                        # A → B (non-terminal only): epsilon-transition, not handled in simple FA
                        pass
                elif len(production) == 2:
                    # A → aB (terminal followed by non-terminal)
                    if production[0] in self.V_T and production[1] in self.V_N:
                        terminal = production[0]
                        next_state = production[1]
                        key = (non_terminal, terminal)
                        if key not in transitions:
                            transitions[key] = set()
                        transitions[key].add(next_state)

        return FiniteAutomaton(states, alphabet, transitions, start_state, final_states)

    def __str__(self) -> str:
        #String representation of the grammar
        result = "Grammar:\n"
        result += f"  V_N = {self.V_N}\n"
        result += f"  V_T = {self.V_T}\n"
        result += f"  S = {self.S}\n"
        result += "  Productions:\n"
        for non_terminal, productions in self.P.items():
            for production in productions:
                result += f"    {non_terminal} → {production if production else 'ε'}\n"
        return result