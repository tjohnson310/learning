from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
S1 = And(AKnight, AKnave)
knowledge0 = And(
    Not(
        And(AKnight, AKnave)
    ),
    Or(AKnight, AKnave),
    Not(
        And(BKnight, BKnave)
    ),
    Or(BKnight, BKnave),
    Not(
        And(CKnight, CKnave)
    ),
    Or(CKnight, CKnave),

    Implication(
        AKnave, Not(S1)
    ),
    Implication(
        AKnight, S1
    )
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
S2 = And(AKnave, BKnave)
knowledge1 = And(
    Not(
        And(AKnight, AKnave)
    ),
    Or(AKnight, AKnave),
    Not(
        And(BKnight, BKnave)
    ),
    Or(BKnight, BKnave),
    Not(
        And(CKnight, CKnave)
    ),
    Or(CKnight, CKnave),

    Biconditional(
        AKnave, Not(S2)
    ),
    Biconditional(
        AKnight, S2
    )

)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
S3 = Or(Biconditional(AKnight, BKnight), Biconditional(AKnave, BKnave))
S4 = Not(S3)
knowledge2 = And(
    Not(
        And(AKnight, AKnave)
    ),
    Or(AKnight, AKnave),
    Not(
        And(BKnight, BKnave)
    ),
    Or(BKnight, BKnave),
    Not(
        And(CKnight, CKnave)
    ),
    Or(CKnight, CKnave),

    Biconditional(
        AKnight, S3
    ),
    Biconditional(
        BKnight, S4
    ),
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
S5 = And(Or(AKnight, AKnave), Not(And(AKnight, AKnave)))
S6 = Implication(AKnave, Not(S5))
S7 = And(S6, CKnave)
knowledge3 = And(
    Not(
        And(AKnight, AKnave)
    ),
    Or(AKnight, AKnave),
    Not(
        And(BKnight, BKnave)
    ),
    Or(BKnight, BKnave),
    Not(
        And(CKnight, CKnave)
    ),
    Or(CKnight, CKnave),

    Biconditional(
        AKnight, S5
    ),
    Biconditional(
        BKnight, S7
    ),
    Biconditional(
        CKnight, AKnight
    ),

)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
