from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from typing import Dict, Iterable, List, Set, Tuple


Production = Tuple[str, ...]


@dataclass
class CFG:
    non_terminals: Set[str]
    terminals: Set[str]
    productions: Dict[str, Set[Production]]
    start_symbol: str

    @classmethod
    def from_compact(
        cls,
        non_terminals: Set[str],
        terminals: Set[str],
        productions: Dict[str, List[str]],
        start_symbol: str,
    ) -> "CFG":
        symbols = sorted(non_terminals | terminals, key=len, reverse=True)
        parsed: Dict[str, Set[Production]] = {}

        for left, rhs_list in productions.items():
            parsed[left] = set()
            for rhs in rhs_list:
                rhs = rhs.strip()
                if rhs in {"", "ε", "epsilon"}:
                    parsed[left].add(tuple())
                    continue

                parsed_rhs: List[str] = []
                i = 0
                while i < len(rhs):
                    matched = None
                    for symbol in symbols:
                        if rhs.startswith(symbol, i):
                            matched = symbol
                            break
                    if matched is None:
                        raise ValueError(f"Cannot parse RHS '{rhs}' at position {i}")
                    parsed_rhs.append(matched)
                    i += len(matched)
                parsed[left].add(tuple(parsed_rhs))

        return cls(
            non_terminals=set(non_terminals),
            terminals=set(terminals),
            productions=parsed,
            start_symbol=start_symbol,
        )

    def clone(self) -> "CFG":
        return CFG(
            non_terminals=set(self.non_terminals),
            terminals=set(self.terminals),
            productions={k: set(v) for k, v in self.productions.items()},
            start_symbol=self.start_symbol,
        )

    def format(self) -> str:
        lines = [
            f"VN = {{{', '.join(sorted(self.non_terminals))}}}",
            f"VT = {{{', '.join(sorted(self.terminals))}}}",
            f"S = {self.start_symbol}",
            "P:",
        ]
        for left in sorted(self.productions):
            rhs_strings = []
            for rhs in sorted(self.productions[left], key=lambda r: (len(r), r)):
                rhs_strings.append("".join(rhs) if rhs else "ε")
            lines.append(f"  {left} -> {' | '.join(rhs_strings)}")
        return "\n".join(lines)


class CNFNormalizer:
    def __init__(self) -> None:
        self.steps: List[Tuple[str, CFG]] = []
        self._counter = 0

    def normalize(self, grammar: CFG) -> CFG:
        g = grammar.clone()
        g = self._ensure_start_not_on_rhs(g)
        self._record("Initial grammar", g)

        g = self._eliminate_epsilon(g)
        self._record("1) After epsilon elimination", g)

        g = self._eliminate_unit(g)
        self._record("2) After renaming (unit rule) elimination", g)

        g = self._eliminate_inaccessible(g)
        self._record("3) After inaccessible symbol elimination", g)

        g = self._eliminate_nonproductive(g)
        self._record("4) After non-productive symbol elimination", g)

        g = self._replace_terminals_in_long_rules(g)
        g = self._binarize(g)
        self._record("5) Chomsky Normal Form", g)

        return g

    @staticmethod
    def is_cnf(grammar: CFG) -> bool:
        for left, rhs_set in grammar.productions.items():
            for rhs in rhs_set:
                if len(rhs) == 0:
                    if left != grammar.start_symbol:
                        return False
                elif len(rhs) == 1:
                    if rhs[0] not in grammar.terminals:
                        return False
                elif len(rhs) == 2:
                    if rhs[0] not in grammar.non_terminals or rhs[1] not in grammar.non_terminals:
                        return False
                else:
                    return False
        return True

    def _record(self, title: str, grammar: CFG) -> None:
        self.steps.append((title, grammar.clone()))

    def _fresh_nonterminal(self, grammar: CFG, prefix: str) -> str:
        while True:
            candidate = f"{prefix}{self._counter}"
            self._counter += 1
            if candidate not in grammar.non_terminals and candidate not in grammar.terminals:
                grammar.non_terminals.add(candidate)
                grammar.productions.setdefault(candidate, set())
                return candidate

    def _ensure_start_not_on_rhs(self, grammar: CFG) -> CFG:
        appears = any(
            grammar.start_symbol in rhs
            for rhs_set in grammar.productions.values()
            for rhs in rhs_set
        )
        if not appears:
            return grammar

        new_start = self._fresh_nonterminal(grammar, "S0_")
        grammar.productions[new_start].add((grammar.start_symbol,))
        grammar.start_symbol = new_start
        return grammar

    def _nullable_set(self, grammar: CFG) -> Set[str]:
        nullable: Set[str] = set()
        changed = True
        while changed:
            changed = False
            for left, rhs_set in grammar.productions.items():
                for rhs in rhs_set:
                    if len(rhs) == 0 or all(sym in nullable for sym in rhs):
                        if left not in nullable:
                            nullable.add(left)
                            changed = True
        return nullable

    def _eliminate_epsilon(self, grammar: CFG) -> CFG:
        nullable = self._nullable_set(grammar)
        start_nullable = grammar.start_symbol in nullable
        new_productions: Dict[str, Set[Production]] = {nt: set() for nt in grammar.non_terminals}

        for left, rhs_set in grammar.productions.items():
            for rhs in rhs_set:
                if len(rhs) == 0:
                    continue

                nullable_positions = [i for i, sym in enumerate(rhs) if sym in nullable]
                new_productions[left].add(rhs)

                for k in range(1, len(nullable_positions) + 1):
                    for pos_group in combinations(nullable_positions, k):
                        candidate = tuple(sym for i, sym in enumerate(rhs) if i not in pos_group)
                        if len(candidate) > 0:
                            new_productions[left].add(candidate)

        if start_nullable:
            new_productions[grammar.start_symbol].add(tuple())

        grammar.productions = new_productions
        return grammar

    def _eliminate_unit(self, grammar: CFG) -> CFG:
        unit_closure: Dict[str, Set[str]] = {nt: {nt} for nt in grammar.non_terminals}

        changed = True
        while changed:
            changed = False
            for a in grammar.non_terminals:
                for b in list(unit_closure[a]):
                    for rhs in grammar.productions.get(b, set()):
                        if len(rhs) == 1 and rhs[0] in grammar.non_terminals and rhs[0] not in unit_closure[a]:
                            unit_closure[a].add(rhs[0])
                            changed = True

        new_productions: Dict[str, Set[Production]] = {nt: set() for nt in grammar.non_terminals}
        for a in grammar.non_terminals:
            for b in unit_closure[a]:
                for rhs in grammar.productions.get(b, set()):
                    if not (len(rhs) == 1 and rhs[0] in grammar.non_terminals):
                        new_productions[a].add(rhs)

        grammar.productions = new_productions
        return grammar

    def _eliminate_inaccessible(self, grammar: CFG) -> CFG:
        accessible: Set[str] = {grammar.start_symbol}
        changed = True
        while changed:
            changed = False
            for left in list(accessible):
                for rhs in grammar.productions.get(left, set()):
                    for sym in rhs:
                        if sym in grammar.non_terminals and sym not in accessible:
                            accessible.add(sym)
                            changed = True

        grammar.non_terminals = accessible
        grammar.productions = {nt: grammar.productions.get(nt, set()) for nt in accessible}
        return grammar

    def _eliminate_nonproductive(self, grammar: CFG) -> CFG:
        productive: Set[str] = set()
        changed = True
        while changed:
            changed = False
            for left, rhs_set in grammar.productions.items():
                for rhs in rhs_set:
                    if all(sym in grammar.terminals or sym in productive for sym in rhs):
                        if left not in productive:
                            productive.add(left)
                            changed = True

        grammar.non_terminals = grammar.non_terminals & productive
        filtered: Dict[str, Set[Production]] = {}
        for left in grammar.non_terminals:
            kept_rhs = set()
            for rhs in grammar.productions.get(left, set()):
                if all(sym in grammar.terminals or sym in grammar.non_terminals for sym in rhs):
                    kept_rhs.add(rhs)
            filtered[left] = kept_rhs

        grammar.productions = filtered
        return grammar

    def _replace_terminals_in_long_rules(self, grammar: CFG) -> CFG:
        terminal_proxy: Dict[str, str] = {}

        for left in list(grammar.productions.keys()):
            replaced_rhs: Set[Production] = set()
            for rhs in grammar.productions[left]:
                if len(rhs) >= 2:
                    new_rhs = list(rhs)
                    for i, sym in enumerate(rhs):
                        if sym in grammar.terminals:
                            if sym not in terminal_proxy:
                                proxy = self._fresh_nonterminal(grammar, f"T_{sym}_")
                                terminal_proxy[sym] = proxy
                            new_rhs[i] = terminal_proxy[sym]
                    replaced_rhs.add(tuple(new_rhs))
                else:
                    replaced_rhs.add(rhs)
            grammar.productions[left] = replaced_rhs

        for terminal, proxy in terminal_proxy.items():
            grammar.productions[proxy].add((terminal,))

        return grammar

    def _binarize(self, grammar: CFG) -> CFG:
        new_productions: Dict[str, Set[Production]] = {nt: set() for nt in grammar.non_terminals}
        original_items = list(grammar.productions.items())
        for left, rhs_set in original_items:
            for rhs in rhs_set:
                if len(rhs) <= 2:
                    new_productions[left].add(rhs)
                    continue

                current_left = left
                symbols = list(rhs)
                while len(symbols) > 2:
                    new_nt = self._fresh_nonterminal(grammar, "X_")
                    first = symbols.pop(0)
                    new_productions.setdefault(current_left, set()).add((first, new_nt))
                    current_left = new_nt
                    new_productions.setdefault(current_left, set())
                new_productions[current_left].add(tuple(symbols))

        for nt in grammar.non_terminals:
            new_productions.setdefault(nt, set())
        grammar.productions = new_productions
        return grammar
