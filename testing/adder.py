from data.model import NodeTemplate, SimpleNode, DataModel

import random

class AdderNode(NodeTemplate):
    name = "Adder"
    input_vars = ["value-1", "value-2"]
    output_vars = ["sum"]

    @staticmethod
    def new():
        return SimpleNode(AdderNode)

test_model = DataModel()

coordinates = [
    [50,50], [50, 350], [400, 200], [750,50], [750, 350]]
    
for j in range(5):
    n = AdderNode.new()
    n.location = coordinates[j]
    i = test_model.add_node(n)
    n.name = "Adder {0}".format(i)
    
test_model.add_link((0, "sum"), (2, "value-1"))
test_model.add_link((1, "sum"), (2, "value-2"))
test_model.add_link((2, "sum"), (3, "value-1"))

    
                
