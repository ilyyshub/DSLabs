from tokens import TT

KEYWORDS: dict[str, TT] = {
    "let":    TT.LET,
    "fn":     TT.FN,
    "return": TT.RETURN,
    "if":     TT.IF,
    "else":   TT.ELSE,
    "while":  TT.WHILE,
    "end":    TT.END,
    "print":  TT.PRINT,
    "and":    TT.AND,
    "or":     TT.OR,
    "not":    TT.NOT,
    "true":   TT.TRUE,
    "false":  TT.FALSE,
}