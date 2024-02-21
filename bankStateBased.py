import enum
import collections
import typing
import math
import re
from State import State
from Action import Action
from Predicate import Predicate
from Parser import Parser


class BankWorldDomain():
    def __init__(self, literals, action_templates, pddl_objects):
        self.state = State(literals)
        self.action_templates = action_templates
        self.objects = pddl_objects
        self.playerWon = False

    def copyTo(self, other):
        assert isinstance(other, BankWorldDomain)
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


parser = Parser()
object_list = parser.getObjects()
pred_dict = parser.getPredicateDict()
init_array = parser.getinitState()

print('Objects: ')
print(parser.getObjects())
print('\nPredicates: ')
for key in pred_dict:
    print(pred_dict[key])
print('\nInitial State: ')
print([str(x) for x in init_array])

print('\n')


#parser.readPredicate()

'''
                #0                         #3                               #6              #8
object_list = ["SAM", "LOBBY", "GUN1", "OWNER", "OUTSIDE", "VAULT-ROOM", "VAULT", "GOLD1", "GOLD2"]
'''
predicate_list = [
    Predicate("player", ["x"], False), #0
    Predicate("character", ["x"], False),
    Predicate("at", ["x", "y"], False),
    Predicate("has", ["x", "y"], False), #3
    Predicate("object", ["x"], False),
    Predicate("location", ["x"], False), #5
    Predicate("color", ["x", "y"], False),
    Predicate("alive", ["x"], False), #7
    Predicate("gun", ["x"], False),
    Predicate("connected", ["x", "y"], False),
    Predicate("closed", ["x"], False), #10
    Predicate("thing", ["x"], False),
    Predicate("in", ["x", "y"], False), #12

    #Duplicates
    Predicate("character", ["x"], False), #13
    Predicate("alive", ["x"], False),
    Predicate("thing", ["x"], False),
    Predicate("location", ["x"], False), #16
    Predicate("location", ["x"], False), 
    Predicate("at", ["x", "y"], False), #18
    Predicate("at", ["x", "y"], False), #19
    Predicate("connected", ["x", "y"], False),
    Predicate("connected", ["x", "y"], False), #21
    Predicate("connected", ["x", "y"], False), #22
    Predicate("in", ["x", "y"], False), #23
]

predicate_list[0].set_binding(predicate_list[0].parameters[0], object_list[0])

predicate_list[1].set_binding(predicate_list[1].parameters[0], object_list[0])
predicate_list[13].set_binding(predicate_list[1].parameters[0], object_list[3])

predicate_list[2].set_binding(predicate_list[2].parameters[0], object_list[0])
predicate_list[2].set_binding(predicate_list[2].parameters[1], object_list[1])
predicate_list[18].set_binding(predicate_list[18].parameters[0], object_list[3])
predicate_list[18].set_binding(predicate_list[18].parameters[1], object_list[4])
predicate_list[19].set_binding(predicate_list[19].parameters[0], object_list[6])
predicate_list[19].set_binding(predicate_list[19].parameters[1], object_list[5])

predicate_list[3].set_binding(predicate_list[3].parameters[0], object_list[0])
predicate_list[3].set_binding(predicate_list[3].parameters[1], object_list[2])

predicate_list[5].set_binding(predicate_list[5].parameters[0], object_list[5])
predicate_list[16].set_binding(predicate_list[16].parameters[0], object_list[4])
predicate_list[17].set_binding(predicate_list[17].parameters[0], object_list[1])

predicate_list[7].set_binding(predicate_list[7].parameters[0], object_list[0])
predicate_list[14].set_binding(predicate_list[14].parameters[0], object_list[3])

predicate_list[8].set_binding(predicate_list[8].parameters[0], object_list[2])

predicate_list[9].set_binding(predicate_list[9].parameters[0], object_list[4])
predicate_list[9].set_binding(predicate_list[9].parameters[1], object_list[1])
predicate_list[20].set_binding(predicate_list[20].parameters[0], object_list[1])
predicate_list[20].set_binding(predicate_list[20].parameters[1], object_list[5])
predicate_list[21].set_binding(predicate_list[21].parameters[0], object_list[1])
predicate_list[21].set_binding(predicate_list[21].parameters[1], object_list[4])
predicate_list[22].set_binding(predicate_list[22].parameters[0], object_list[5])
predicate_list[22].set_binding(predicate_list[22].parameters[1], object_list[1])

predicate_list[10].set_binding(predicate_list[10].parameters[0], object_list[6])

predicate_list[11].set_binding(predicate_list[11].parameters[0], object_list[7])
predicate_list[15].set_binding(predicate_list[15].parameters[0], object_list[8])

predicate_list[12].set_binding(predicate_list[12].parameters[0], object_list[7])
predicate_list[12].set_binding(predicate_list[12].parameters[1], object_list[6])
predicate_list[23].set_binding(predicate_list[23].parameters[0], object_list[8])
predicate_list[23].set_binding(predicate_list[23].parameters[1], object_list[6])

action_list = [
    Action("shoot-person", ["shooter", "victim", "location", "gun"]), #0
    Action("open-vault", ["opener", "thing", "room"]),                   #1
    Action("move-location", ["mover", "location", "oldlocation"]),   #2
    Action("take-thing", ["taker", "thing", "vault", "vault-room"])   #3
]

action_list[0].add_precondition(Predicate("character", ["shooter"], False))
action_list[0].add_precondition(Predicate("character", ["victim"], False))
action_list[0].add_precondition(Predicate("location", ["location"], False))
action_list[0].add_precondition(Predicate("gun", ["gun"], False))
action_list[0].add_precondition(Predicate("alive", ["shooter"], False))
action_list[0].add_precondition(Predicate("alive", ["victim"], False))
action_list[0].add_precondition(Predicate("at", ["shooter", "location"], False))
action_list[0].add_precondition(Predicate("at", ["victim", "location"], False))
action_list[0].add_precondition(Predicate("has", ["shooter", "gun"], False))
action_list[0].add_precondition(Predicate("has", ["victim", "gun"], True))

action_list[0].add_effect(Predicate("alive", ["victim"], True))

action_list[1].add_precondition(Predicate("character", ["opener"], False))
action_list[1].add_precondition(Predicate("alive", ["opener"], False))
action_list[1].add_precondition(Predicate("at", ["opener", "room"], False))
action_list[1].add_precondition(Predicate("at", ["thing", "room"], False))
action_list[1].add_precondition(Predicate("open", ["thing"], True))
action_list[1].add_precondition(Predicate("closed", ["thing"], False))

action_list[1].add_effect(Predicate("closed", ["thing"], True))
action_list[1].add_effect(Predicate("open", ["thing"], False))

action_list[2].add_precondition(Predicate("character", ["mover"], False))
action_list[2].add_precondition(Predicate("location", ["location"], False))
action_list[2].add_precondition(Predicate("location", ["oldlocation"], False))
action_list[2].add_precondition(Predicate("alive", ["mover"], False))
action_list[2].add_precondition(Predicate("at", ["mover", "oldlocation"], False))
action_list[2].add_precondition(Predicate("at", ["mover", "location"], True))
action_list[2].add_precondition(Predicate("connected", ["location", "oldlocation"], False))

action_list[2].add_effect(Predicate("at", ["mover", "location"], False))
action_list[2].add_effect(Predicate("at", ["mover", "oldlocation"], True))

action_list[3].add_precondition(Predicate("character", ["taker"], False))
action_list[3].add_precondition(Predicate("alive", ["taker"], False))
action_list[3].add_precondition(Predicate("at", ["taker", "vault-room"], False))
action_list[3].add_precondition(Predicate("in", ["thing", "vault"], False))
action_list[3].add_precondition(Predicate("open", ["vault"], False))
action_list[3].add_precondition(Predicate("thing", ["thing"], False))

action_list[3].add_effect(Predicate("in", ["thing", "vault"], True))
action_list[3].add_effect(Predicate("has", ["taker", "thing"], False))



bank_world_domain_0 = BankWorldDomain(predicate_list, action_list, object_list)

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