import unittest

from cnf_normalizer import CFG, CNFNormalizer
from main import build_variant6_grammar


class TestCNFNormalizer(unittest.TestCase):
    def test_variant6_reaches_cnf(self) -> None:
        grammar = build_variant6_grammar()
        normalizer = CNFNormalizer()
        cnf = normalizer.normalize(grammar)

        self.assertTrue(CNFNormalizer.is_cnf(cnf))
        self.assertNotIn("E", cnf.non_terminals)  # inaccessible in variant grammar

    def test_bonus_generic_input_grammar(self) -> None:
        grammar = CFG.from_compact(
            non_terminals={"S", "A", "B"},
            terminals={"a", "b"},
            productions={
                "S": ["AB", "a", "ε"],
                "A": ["aA", "a"],
                "B": ["bB", "b"],
            },
            start_symbol="S",
        )

        normalizer = CNFNormalizer()
        cnf = normalizer.normalize(grammar)

        self.assertTrue(CNFNormalizer.is_cnf(cnf))


if __name__ == "__main__":
    unittest.main()

