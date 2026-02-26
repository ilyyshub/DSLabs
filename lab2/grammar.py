class Grammar:
    def __init__(self, non_terminals, terminals, productions, start_symbol):
        """
        Initialize a grammar.

        Args:
            non_terminals: Set of non-terminal symbols
            terminals: Set of terminal symbols
            productions: Dictionary mapping non-terminals to lists of production rules
            start_symbol: The start symbol of the grammar
        """
        self.VN = non_terminals
        self.VT = terminals
        self.P = productions
        self.S = start_symbol

    def classify_chomsky(self):
        """
        Classify the grammar according to Chomsky hierarchy.

        Returns:
            String indicating the grammar type: "Type 0", "Type 1", "Type 2", or "Type 3"
        """
        if self.is_type3():
            return "Type 3 (Regular Grammar)"
        elif self.is_type2():
            return "Type 2 (Context-Free Grammar)"
        elif self.is_type1():
            return "Type 1 (Context-Sensitive Grammar)"
        else:
            return "Type 0 (Unrestricted Grammar)"

    def is_type3(self):
        """
        Check if grammar is Type 3 (Regular).
        Regular grammar: A -> aB or A -> a (right-regular) or A -> Ba or A -> a (left-regular)
        """
        is_right_regular = True
        is_left_regular = True

        for non_terminal in self.P:
            for production in self.P[non_terminal]:
                # Empty production
                if production == '':
                    continue

                # Check right-regular: A -> a or A -> aB
                if len(production) == 1:
                    if production not in self.VT:
                        is_right_regular = False
                elif len(production) == 2:
                    if not (production[0] in self.VT and production[1] in self.VN):
                        is_right_regular = False
                else:
                    is_right_regular = False

                # Check left-regular: A -> a or A -> Ba
                if len(production) == 1:
                    if production not in self.VT:
                        is_left_regular = False
                elif len(production) == 2:
                    if not (production[0] in self.VN and production[1] in self.VT):
                        is_left_regular = False
                else:
                    is_left_regular = False

        return is_right_regular or is_left_regular

    def is_type2(self):
        """
        Check if grammar is Type 2 (Context-Free).
        Context-free grammar: A -> α where A is a single non-terminal and α is any string
        """
        for non_terminal in self.P:
            # Left side must be a single non-terminal
            if len(non_terminal) != 1 or non_terminal not in self.VN:
                return False
        return True

    def is_type1(self):
        """
        Check if grammar is Type 1 (Context-Sensitive).
        Context-sensitive grammar: αAβ -> αγβ where |αγβ| >= |αAβ| (non-contracting)
        """
        for non_terminal in self.P:
            for production in self.P[non_terminal]:
                # Check non-contracting property (except for S -> ε)
                if production == '' and non_terminal != self.S:
                    return False
                if len(production) < len(non_terminal):
                    return False
        return True

    def __str__(self):
        result = f"Grammar:\n"
        result += f"  Non-terminals: {self.VN}\n"
        result += f"  Terminals: {self.VT}\n"
        result += f"  Start symbol: {self.S}\n"
        result += f"  Productions:\n"
        for non_terminal in self.P:
            for production in self.P[non_terminal]:
                result += f"    {non_terminal} -> {production if production else 'ε'}\n"
        return result