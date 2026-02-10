# Formal Languages & Finite Automata - Laboratory Works

This repository contains laboratory works for the **Formal Languages & Finite Automata** course.

**Author:** Ciocanu Ilinca 
**University:** Technical University of Moldova
**Academic Year:** 2025-2026

---

## 📚 Course Information

**Course:** Formal Languages & Finite Automata  
**Instructor:** Cretu Dumitru (with Vasile Drumea and Irina Cojuhari)

---

## 📂 Repository Structure

```
FLFA-Labs/
├── README.md                 # This file
├── lab1/                     # Laboratory Work #1
│   ├── src/
│   │   ├── grammar.py       # Grammar class implementation
│   │   ├── finite_automaton.py  # Finite Automaton class
│   │   └── main.py          # Main demonstration program
│   └── report/
│       └── REPORT.md        # Lab 1 report
├── lab2/                     # Laboratory Work #2 (future)
├── lab3/                     # Laboratory Work #3 (future)
└── ...
```

---

## 🎯 Laboratory Works

### Lab 1: Regular Grammars and Finite Automata
**Status:**  Completed  
**Variant:** 6

**Objectives:**
- Implement a Grammar class to represent formal grammars
- Generate valid strings from grammar productions
- Convert Grammar to Finite Automaton
- Validate strings using the Finite Automaton

**Key Features:**
- Support for non-deterministic finite automata (NFA)
- Random string generation using derivation
- Comprehensive string validation

[📄 View Lab 1 Report](./lab1/report/REPORT.md)

---

## 🚀 How to Run

### Prerequisites
- Python 3.7 or higher
- No external dependencies required (uses only Python standard library)

### Running Lab 1

```bash
# Navigate to lab1 directory
cd lab1/src

# Run the main program
python main.py
```

### Expected Output

The program will:
1. Display the grammar definition
2. Generate 5 random valid strings
3. Show the converted Finite Automaton
4. Validate generated strings and test cases

---

## 💻 Implementation Details

### Programming Language
**Python** was chosen for its:
- Clear and readable syntax
- Excellent built-in data structures (sets, dictionaries)
- Easy setup and execution
- Strong support for object-oriented programming

### Technologies Used
- Python 3.x
- Type hints for better code documentation
- Object-oriented design patterns

---

## 📝 Variant Information

**Variant 6:**
```
V_N = {S, I, J, K}
V_T = {a, b, c, e, n, f, m}
Productions:
    S → cI
    I → bJ | fI | eK | e
    J → nJ | cS
    K → nK | m
```

---

## 📖 Learning Outcomes

Through these laboratory works, I have learned:
- The theory of formal languages and grammars
- Implementation of regular grammars and finite automata
- Conversion between different formal models
- Algorithm design for string generation and validation
- Non-deterministic vs deterministic automata

---

## 📄 License

This project is created for educational purposes as part of university coursework.

---
