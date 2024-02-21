import enum
import collections
import typing
import math
import re
from State import State
from Action import Action
from Predicate import Predicate


class ArthurDomain():
    def __init__(self, literals, action_templates, pddl_objects):
        self.state = State(literals)
        self.action_templates = action_templates
        self.objects = pddl_objects
        self.playerWon = False

    def copyTo(self, other):
        assert isinstance(other, ArthurDomain)
        other.state = self.state
        other.playerWon = False

    def getCurrState(self):
        return self.state

    def getLegalNextMoves(self):
        return self.state.check_fully_bound_actions(
            self.state.get_possible_actions(self.objects, self.action_templates))

    # should be some number from 0 to the number of enabled actions
    def parseMove(self, inputStr):
        try:
            return int(inputStr)
        except ValueError:
            return None

    def doMove(self, move):
        isinstance(move, Action)

        # do user sanitization and validation here
        self.state.update(move)

    def prettyPrint(self):
        return self.state.__str__()


object_list = ["ARTHUR", "EXCALIBUR", "WOODS", "LAKE"]

predicate_list = [
    Predicate("player", ["x"], False),
    Predicate("character", ["x"], False),
    Predicate("alive", ["x"], False),
    Predicate("at", ["x", "y"], False),
    Predicate("location", ["x"], False),
    Predicate("connected", ["x", "y"], False),
    Predicate("location", ["x"], False),
    Predicate("connected", ["x", "y"], False),
    Predicate("sword", ["x"], False),
    Predicate("at", ["x", "y"], False),
]

predicate_list[0].set_binding(predicate_list[0].parameters[0], object_list[0])
predicate_list[1].set_binding(predicate_list[1].parameters[0], object_list[0])
predicate_list[2].set_binding(predicate_list[2].parameters[0], object_list[0])

predicate_list[3].set_binding(predicate_list[3].parameters[0], object_list[0])
predicate_list[3].set_binding(predicate_list[3].parameters[1], object_list[2])

predicate_list[4].set_binding(predicate_list[4].parameters[0], object_list[2])

predicate_list[5].set_binding(predicate_list[5].parameters[0], object_list[2])
predicate_list[5].set_binding(predicate_list[5].parameters[1], object_list[3])

predicate_list[6].set_binding(predicate_list[6].parameters[0], object_list[3])

predicate_list[7].set_binding(predicate_list[7].parameters[0], object_list[3])
predicate_list[7].set_binding(predicate_list[7].parameters[1], object_list[2])

predicate_list[8].set_binding(predicate_list[8].parameters[0], object_list[1])

predicate_list[9].set_binding(predicate_list[9].parameters[0], object_list[1])
predicate_list[9].set_binding(predicate_list[9].parameters[1], object_list[3])

action_list = [
    Action("move", ["mover", "location", "oldlocation"]),
    Action("take", ["taker", "thing", "place"])
]

action_list[0].add_precondition(Predicate("character", ["mover"], False))
action_list[0].add_precondition(Predicate("location", ["location"], False))
action_list[0].add_precondition(Predicate("location", ["oldlocation"], False))
action_list[0].add_precondition(Predicate("at", ["mover", "oldlocation"], False))
action_list[0].add_precondition(Predicate("at", ["mover", "location"], True))
action_list[0].add_precondition(Predicate("alive", ["mover"], False))
action_list[0].add_precondition(Predicate("connected", ["location", "oldlocation"], False))

action_list[0].add_effect(Predicate("at", ["mover", "oldlocation"], True))
action_list[0].add_effect(Predicate("at", ["mover", "location"], False))

action_list[1].add_precondition(Predicate("character", ["taker"], False))
action_list[1].add_precondition(Predicate("alive", ["taker"], False))
action_list[1].add_precondition(Predicate("at", ["taker", "place"], False))
action_list[1].add_precondition(Predicate("at", ["thing", "place"], False))

action_list[1].add_effect(Predicate("at", ["thing", "place"], True))
action_list[1].add_effect(Predicate("has", ["taker", "thing"], False))


arthur_domain_0 = ArthurDomain(predicate_list, action_list, object_list)

while not arthur_domain_0.playerWon:
    print(arthur_domain_0.prettyPrint())
    enabled_actions = arthur_domain_0.getLegalNextMoves()
    i = 0
    for enabled_action in enabled_actions:
        print(f"{i}: {enabled_action}")
        i += 1

    user_input = input("What would you like to do next?\n")
    arthur_domain_0.doMove(enabled_actions[arthur_domain_0.parseMove(user_input)])
