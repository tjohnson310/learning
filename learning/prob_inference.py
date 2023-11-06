"""Using the pomegranate library to represent probability data"""

# First,create the nodes and provide a probability dist. for each one:

from pomegranate import *

# Rain node has no parents
rain = Node(DiscreteDistribution({
    "none": 0.7,
    "light": 0.2,
    "heavy": 0.1
}), name="rain")

# Track maintenance node is conditional on rain
maintenance = Node(ConditionalProbabilityTable([
    ["none", "yes", 0.4],
    ["none", "no", 0.6],
    ["light", "yes", 0.2],
    ["light", "no", 0.8],
    ["heavy", "yes", 0.1],
    ["heavy", "no", 0.9]
], [rain.distribution]), name="maintenance")

# Train node is conditional on rain and maintenance
train = Node(ConditionalProbabilityTable([
    ["none", "yes", "on time", 0.8],
    ["none", "yes", "delayed", 0.2],
    ["none", "no", "on time", 0.9],
    ["none", "no", "delayed", 0.1],
    ["light", "yes", "on time", 0.6],
    ["light", "yes", "delayed", 0.4],
    ["light", "no", "on time", 0.7],
    ["light", "no", "delayed", 0.3],
    ["heavy", "yes", "on time", 0.4],
    ["heavy", "yes", "delayed", 0.6],
    ["heavy", "no", "on time", 0.5],
    ["heavy", "no", "delayed", 0.5],
], [rain.distribution, maintenance.distribution]), name="train")

# Appointment node is conditional on train
appointment = Node(ConditionalProbabilityTable([
    ["on time", "attend", 0.9],
    ["on time", "miss", 0.1],
    ["delayed", "attend", 0.6],
    ["delayed", "miss", 0.4]
], [train.distribution]), name="appointment")


# Second, we create the model by adding all the nodes and then describing which
# node is the parent of which other node by adding edges between them (recall
# that Bayesian network is a directed graph, consisting of nodes with arrows
# between them).

# Create a Bayesian Network and add states
model = BayesianNetwork()
model.add_states(rain, maintenance, train, appointment)

# Add edges connecting nodes
model.add_edge(rain, maintenance)
model.add_edge(rain, train)
model.add_edge(maintenance, train)
model.add_edge(train, appointment)

# Finalize model
model.bake()


# Now, to ask how probable a certain event is, we run the model with the
# values we are interested in. In this example, we want to ask what is the
# probability that there is no rain, no track maintenance, the train is on
# time, and we attend the meeting.

# Calculate probability for a given observation
probability = model.probability([["none", "no", "on time", "attend"]])

print(probability)


# Otherwise, we could use the program to provide probability distributions
# for all variables given some observed evidence. In the following case, we know
# that the train was delayed. Given this information, we compute and print the
# probability distributions of the variables Rain, Maintenance, and Appointment.

# Calculate predictions based on the evidence that the train was delayed
predictions = model.predict_proba({
    "train": "delayed"
})

# Print predictions for each node
for node, prediction in zip(model.states, predictions):
    if isinstance(prediction, str):
        print(f"{node.name}: {prediction}")
    else:
        print(f"{node.name}")
        for value, probability in prediction.parameters[0].items():
            print(f"    {value}: {probability:.4f}")


# The code above used inference by enumeration. However, this way of computing
# probability is inefficient, especially when there are many variables in the model.
# A different way to go about this would be abandoning exact inference in favor
# of approximate inference. Doing this, we lose some precision in the generated
# probabilities, but often this imprecision is negligible. Instead, we gain a
# scalable method of calculating probabilities.
