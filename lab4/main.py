from lab4.regex_generator import MAX_REPEAT, validate, RegexGenerator
from lab4.regex_parser import RegexParser

# Main demo
VARIANTS = [
    {
        "id": 1,
        "regex_display": "M?N²(O|P)³Q*R*",
        "regex_parsed": "M?N²(O|P)³Q*R*",
        # Python equivalent for validation (superscripts → {n})
        "python_regex": r"M?N{2}(O|P){3}Q*R*",
        "examples": ["MNNOOOQR", "NNPPPQQQRRR"],
    },
    {
        "id": 2,
        "regex_display": "(X|Y|Z)³8⁺(9|0)",
        "regex_parsed": "(X|Y|Z)³8+(9|0)",
        "python_regex": r"(X|Y|Z){3}8+(9|0)",
        "examples": ["XXX89", "YYY88889"],
    },
    {
        "id": 3,
        "regex_display": "(H|i)(J|K)L*N?",
        "regex_parsed": "(H|i)(J|K)L*N?",
        "python_regex": r"(H|i)(J|K)L*N?",
        "examples": ["HJLLN", "IKLLLLLL"],
    },
]


def run_demo():
    print("=" * 65)
    print("  Variant 2 — Regular Expression String Generator")
    print("=" * 65)

    generator = RegexGenerator(max_repeat=MAX_REPEAT)

    for variant in VARIANTS:
        print(f"\n{'─' * 65}")
        print(f"  Regex #{variant['id']}: {variant['regex_display']}")
        print(f"  Expected examples: {variant['examples']}")
        print()

        # Parse
        parser = RegexParser(variant["regex_parsed"])
        ast = parser.parse()

        # Generate 10 samples
        samples = set()
        attempts = 0
        while len(samples) < 10 and attempts < 200:
            s = generator.generate(ast)
            if validate(s, variant["python_regex"]):
                samples.add(s)
            attempts += 1

        print(f"  Generated strings ({len(samples)} unique):")
        for s in sorted(samples):
            print(f"    {s}")

        # Bonus: processing trace for one string
        print(f"\n  Processing trace (bonus):")
        traced = generator.generate(ast, track=True)
        print(f"  Result: '{traced}'")
        for line in generator.log:
            print(f"  {line}")

    print(f"\n{'=' * 65}")
    print("  All strings validated against Python re.fullmatch ✓")
    print("=" * 65)


if __name__ == "__main__":
    run_demo()