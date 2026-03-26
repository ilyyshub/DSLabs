import random
import re
from typing import List

from lab4.ast_def import Alternation, Node, Quantifier, Literal, Concatenation

# ─────────────────────────────────────────────
# Generator: walks the AST and builds strings
# ─────────────────────────────────────────────

MAX_REPEAT = 5 # Maximum repetitions for * and + quantifiers (to avoid infinite strings)

class RegexGenerator:
    """
    Generates random strings conforming to the parsed AST.
    Keeps a processing log for the bonus objective.
    """

    def __init__(self, max_repeat: int = MAX_REPEAT):
        self.max_repeat = max_repeat
        self.log: List[str] = []
        self._step = 0

    def _log(self, msg: str):
        self._step += 1
        self.log.append(f"  Step {self._step:02d}: {msg}")

    def generate(self, node: Node, *, track: bool = False) -> str:
        self.log = []
        self._step = 0
        result = self._gen(node, track=track)
        return result

    def _gen(self, node: Node, *, track: bool) -> str:
        if isinstance(node, Literal):
            if track:
                self._log(f"Literal → emit '{node.char}'")
            return node.char

        if isinstance(node, Concatenation):
            if track:
                self._log(f"Concatenation of {len(node.children)} parts — processing each in order")
            parts = []
            for child in node.children:
                parts.append(self._gen(child, track=track))
            return ''.join(parts)

        if isinstance(node, Alternation):
            chosen = random.choice(node.choices)
            if track:
                label = self._describe(chosen)
                all_labels = [self._describe(c) for c in node.choices]
                self._log(f"Alternation {{{', '.join(all_labels)}}} → chose '{label}'")
            return self._gen(chosen, track=track)

        if isinstance(node, Quantifier):
            lo = node.min_rep
            hi = node.max_rep if node.max_rep != -1 else self.max_repeat
            count = random.randint(lo, hi)
            if track:
                self._log(
                    f"Quantifier {{{lo},{hi if node.max_rep != -1 else '∞ (capped ' + str(self.max_repeat) + ')'}}} "
                    f"→ repeat {count} time(s)"
                )
            return ''.join(self._gen(node.child, track=track) for _ in range(count))

        raise TypeError(f"Unknown node type: {type(node)}")

    def _describe(self, node: Node) -> str:
        if isinstance(node, Literal):
            return node.char
        if isinstance(node, Concatenation):
            return ''.join(self._describe(c) for c in node.children)
        if isinstance(node, Alternation):
            return '|'.join(self._describe(c) for c in node.choices)
        if isinstance(node, Quantifier):
            suffix = {(0, 1): '?', (0, -1): '*', (1, -1): '+'}.get(
                (node.min_rep, node.max_rep), f'{{{node.min_rep},{node.max_rep}}}'
            )
            return self._describe(node.child) + suffix
        return '?'


# ─────────────────────────────────────────────
# Validator: use Python's re module to verify
# ─────────────────────────────────────────────

def validate(string: str, python_regex: str) -> bool:
    """
    Validate that a generated string fully matches the equivalent Python regex.
    """
    return bool(re.fullmatch(python_regex, string, re.IGNORECASE))


