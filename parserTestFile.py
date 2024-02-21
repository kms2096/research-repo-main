import enum
import collections
import typing
import math
import re
from State import State
from Action import Action
from Predicate import Predicate
from NewParser import NewParser


class ParserTestFile():
    def __init__(self, literals, action_templates, pddl_objects):
        self.state = State(literals)
        self.action_templates = action_templates
        self.objects = pddl_objects
        self.playerWon = False

    def copyTo(self, other):
        assert isinstance(other, ParserTestFile)
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

parser = NewParser()
object_list = parser.getObjects()
predicate_list = parser.getPredicateDict()
init_array = parser.getinitState()
action_list_test = parser.getActions()

bank_world_domain_0 = ParserTestFile(init_array, action_list_test, object_list)

while not bank_world_domain_0.playerWon:
    print(bank_world_domain_0.prettyPrint())
    enabled_actions = bank_world_domain_0.getLegalNextMoves()
    i = 0
    for enabled_action in enabled_actions:
        print(f"{i}: {enabled_action}")
        i += 1

    user_input = input("What would you like to do next?\n")
    bank_world_domain_0.doMove(enabled_actions[bank_world_domain_0.parseMove(user_input)])
'''
'''


#(:goal (AND (not (alive owner)) (open vault) (has owner gold1)))