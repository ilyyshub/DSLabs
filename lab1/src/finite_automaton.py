from typing import Set, Dict, Tuple, Union


class FiniteAutomaton:


    def __init__(self, states: Set[str], alphabet: Set[str],
                 transitions: Dict[Tuple[str, str], Union[str, Set[str]]],
                 initial_state: str, final_states: Set[str]):

        #Initialize the Finite Automaton.

        """
        Args:
            states: Set of states
            alphabet: Set of symbols (terminals)
            transitions: Transition function as dictionary
                        {(state, symbol): next_state} for DFA or
                        {(state, symbol): {set of next_states}} for NFA
            initial_state: Starting state
            final_states: Set of accepting states
        """
        self.Q = states
        self.Sigma = alphabet
        self.delta = transitions
        self.q0 = initial_state
        self.F = final_states

    def string_belongs_to_language(self, input_string: str) -> bool:

        # Start with a set of current possible states (for NFA support)
        current_states = {self.q0}

        # Process each symbol in the input string
        for symbol in input_string:
            # Check if symbol is in alphabet
            if symbol not in self.Sigma:
                return False

            # Compute next set of states
            next_states = set()

            for state in current_states:
                # Check if there's a transition for this state and symbol
                transition_key = (state, symbol)
                if transition_key in self.delta:
                    next_state_or_set = self.delta[transition_key]

                    # Handle both DFA (single state) and NFA (set of states)
                    if isinstance(next_state_or_set, set):
                        next_states.update(next_state_or_set)
                    else:
                        next_states.add(next_state_or_set)

            # If no valid transitions found, reject
            if not next_states:
                return False

            current_states = next_states

        # Check if any of the final states is in our set of current states
        return bool(current_states & self.F)

    def __str__(self) -> str:
        #String representation of the automaton.
        result = "Finite Automaton:\n"
        result += f"  Q (States) = {self.Q}\n"
        result += f"  Σ (Alphabet) = {self.Sigma}\n"
        result += f"  q0 (Initial state) = {self.q0}\n"
        result += f"  F (Final states) = {self.F}\n"
        result += "  δ (Transitions):\n"
        for (state, symbol), next_state in sorted(self.delta.items()):
            if isinstance(next_state, set):
                result += f"    δ({state}, {symbol}) = {next_state}\n"
            else:
                result += f"    δ({state}, {symbol}) = {next_state}\n"
        return result