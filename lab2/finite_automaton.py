from grammar import Grammar
from collections import defaultdict, deque

class FiniteAutomaton:
    def __init__(self, states, alphabet, transitions, start_state, final_states):
        """
        Initialize a finite automaton.

        Args:
            states: Set of states (Q)
            alphabet: Set of input symbols (Σ)
            transitions: Dictionary representing transition function δ
            start_state: Initial state (q0)
            final_states: Set of accepting/final states (F)
        """
        self.Q = states
        self.Sigma = alphabet
        self.delta = transitions
        self.q0 = start_state
        self.F = final_states

    def is_deterministic(self):
        """
        Determine whether the FA is deterministic or non-deterministic.

        A FA is deterministic if:
        1. For each state and input symbol, there is at most one transition
        2. No epsilon transitions exist

        Returns:
            Boolean indicating if the FA is deterministic
        """
        for (state, symbol) in self.delta:
            # Check if there are multiple transitions for same state-symbol pair
            if len(self.delta[(state, symbol)]) > 1:
                return False

            # Check for epsilon transitions
            if symbol == 'ε' or symbol == '':
                return False

        return True

    def to_regular_grammar(self):
        """
        Convert finite automaton to regular grammar.

        For each transition δ(qi, a) = qj:
        - If qj is not final: add production qi -> a qj
        - If qj is final: add productions qi -> a qj and qi -> a

        Returns:
            Grammar object representing the equivalent regular grammar
        """
        non_terminals = self.Q.copy()
        terminals = self.Sigma.copy()
        productions = defaultdict(list)
        start_symbol = self.q0

        # Convert transitions to productions
        for (state, symbol), next_states in self.delta.items():
            for next_state in next_states:
                # Add production: state -> symbol next_state
                production = symbol + next_state
                if production not in productions[state]:
                    productions[state].append(production)

                # If next_state is final, also add: state -> symbol
                if next_state in self.F:
                    if symbol not in productions[state]:
                        productions[state].append(symbol)

        # If start state is final, add S -> ε
        if self.q0 in self.F:
            if '' not in productions[self.q0]:
                productions[self.q0].append('')

        return Grammar(non_terminals, terminals, dict(productions), start_symbol)

    def nfa_to_dfa(self):
        """
        Convert NFA to DFA using subset construction algorithm.

        Returns:
            FiniteAutomaton object representing the equivalent DFA
        """
        # New DFA components
        dfa_states = set()
        dfa_transitions = {}
        dfa_start_state = frozenset([self.q0])
        dfa_final_states = set()

        # Queue for BFS
        unmarked_states = deque([dfa_start_state])
        dfa_states.add(dfa_start_state)

        # Map frozenset to string representation for cleaner state names
        state_name_map = {dfa_start_state: '{' + ','.join(sorted(dfa_start_state)) + '}'}

        while unmarked_states:
            current_state_set = unmarked_states.popleft()

            # For each symbol in alphabet
            for symbol in self.Sigma:
                # Find all states reachable from current_state_set with symbol
                next_state_set = set()
                for state in current_state_set:
                    if (state, symbol) in self.delta:
                        next_state_set.update(self.delta[(state, symbol)])

                if next_state_set:
                    next_state_frozen = frozenset(next_state_set)

                    # Add to DFA states if new
                    if next_state_frozen not in dfa_states:
                        dfa_states.add(next_state_frozen)
                        unmarked_states.append(next_state_frozen)
                        state_name_map[next_state_frozen] = '{' + ','.join(sorted(next_state_frozen)) + '}'

                    # Add transition
                    current_name = state_name_map[current_state_set]
                    next_name = state_name_map[next_state_frozen]
                    dfa_transitions[(current_name, symbol)] = [next_name]

        # Determine final states (any set containing a final state from original NFA)
        for state_set in dfa_states:
            if any(state in self.F for state in state_set):
                dfa_final_states.add(state_name_map[state_set])

        # Convert state names
        dfa_states_names = {state_name_map[s] for s in dfa_states}
        dfa_start_name = state_name_map[dfa_start_state]

        return FiniteAutomaton(
            dfa_states_names,
            self.Sigma,
            dfa_transitions,
            dfa_start_name,
            dfa_final_states
        )

    def to_graphviz(self):
        """
        Generate DOT format representation for visualization.

        Returns:
            String containing DOT format graph description
        """
        dot = "digraph FiniteAutomaton {\n"
        dot += "    rankdir=LR;\n"
        dot += "    node [shape = circle];\n"

        # Mark final states with double circle
        if self.F:
            final_states_str = " ".join(f'"{state}"' for state in self.F)
            dot += f"    node [shape = doublecircle]; {final_states_str};\n"
            dot += "    node [shape = circle];\n"

        # Add invisible start node
        dot += '    "" [shape=none];\n'
        dot += f'    "" -> "{self.q0}";\n'

        # Add transitions
        for (state, symbol), next_states in sorted(self.delta.items()):
            for next_state in next_states:
                dot += f'    "{state}" -> "{next_state}" [label="{symbol}"];\n'

        dot += "}\n"
        return dot

    def __str__(self):
        result = "Finite Automaton:\n"
        result += f"  States (Q): {self.Q}\n"
        result += f"  Alphabet (Σ): {self.Sigma}\n"
        result += f"  Start state (q0): {self.q0}\n"
        result += f"  Final states (F): {self.F}\n"
        result += f"  Transitions (δ):\n"
        for (state, symbol), next_states in sorted(self.delta.items()):
            for next_state in next_states:
                result += f"    δ({state}, {symbol}) = {next_state}\n"
        return result