from logic import *

# Create new classes, each having a name, or a symbol, representing each proposition.
rain = Symbol("rain")  # It is raining.
hagrid = Symbol("hagrid")  # Harry visited Hagrid
dumbledore = Symbol("dumbledore")  # Harry visited Dumbledore

# Save sentences into the KB
knowledge = And(  # Starting from the "And" logical connective, because each proposition represents knowledge that
                  # we know to be true.

    Implication(Not(rain), hagrid),  # ¬(It is raining) → (Harry visited Hagrid)

    Or(hagrid, dumbledore),  # (Harry visited Hagrid) ∨ (Harry visited Dumbledore).

    Not(And(hagrid, dumbledore)),  # ¬(Harry visited Hagrid ∧ Harry visited Dumbledore) i.e. Harry did not visit both
                                   # Hagrid and Dumbledore.

    dumbledore  # Harry visited Dumbledore. Note that while previous propositions contained multiple symbols with
                # connectors, this is a proposition consisting of one symbol. This means that we take as a fact that,
                # in this KB, Harry visited Dumbledore.
    )


def check_all(knwldg, query, symbols, model):
    # If model has an assignment for each symbol
    # (The logic below might be a little confusing: we start with a list of symbols. The function is recursive,
    # and every time it calls itself it pops one symbol from the symbols list and generates models from it. Thus,
    # when the symbols list is empty, we know that we finished generating models with every possible truth assignment
    # of symbols.)
    if not symbols:

        # If knowledge base is true in model, then query must also be true
        if knwldg.evaluate(model):
            return query.evaluate(model)
        return True
    else:

        # Choose one of the remaining unused symbols
        remaining = symbols.copy()
        p = remaining.pop()

        # Create a model where the symbol is true
        model_true = model.copy()
        model_true[p] = True

        # Create a model where the symbol is false
        model_false = model.copy()
        model_false[p] = False

        # Ensure entailment holds in both models
        return(check_all(knwldg, query, remaining, model_true) and check_all(knwldg, query, remaining, model_false))
