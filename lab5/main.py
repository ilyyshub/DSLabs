from cnf_normalizer import CFG, CNFNormalizer


def build_variant6_grammar() -> CFG:
    non_terminals = {"S", "A", "B", "C", "E"}
    terminals = {"a", "b"}
    productions = {
        "S": ["aB", "AC"],
        "A": ["a", "ASC", "BC"],
        "B": ["b", "bS"],
        "C": ["ε", "BA"],
        "E": ["bB"],
    }
    return CFG.from_compact(non_terminals, terminals, productions, "S")


def run_demo() -> None:
    grammar = build_variant6_grammar()
    normalizer = CNFNormalizer()
    cnf = normalizer.normalize(grammar)

    print("=" * 80)
    print("FORMAL LANGUAGES & FINITE AUTOMATA - LABORATORY WORK #5")
    print("Topic: Chomsky Normal Form (CNF)")
    print("Variant: 6")
    print("=" * 80)

    for title, step_grammar in normalizer.steps:
        print(f"\n{title}")
        print("-" * 80)
        print(step_grammar.format())

    print("\nVerification")
    print("-" * 80)
    print(f"Is final grammar in CNF? {'YES' if CNFNormalizer.is_cnf(cnf) else 'NO'}")


if __name__ == "__main__":
    run_demo()

