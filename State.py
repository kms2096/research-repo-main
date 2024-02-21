from Action import *


class State:
    # literals should be fully bound predicates when being passed in
    def __init__(self, literals):
        # for iterating, perhaps using dict in the future will eliminate need
        # for this if it's iterable
        self.state_dictionary = dict()
        for literal in literals:
            self.state_dictionary[f"{literal.to_string_ignoring_negation()}"] = not literal.is_negated

    def update(self, taken_action):
        for effect in taken_action.effects:
                self.state_dictionary[f"{effect.to_string_ignoring_negation()}"] = not effect.is_negated

    def check_fully_bound_actions(self, possible_actions):
        enabled_actions = []
        for possible_action in possible_actions:
            if not possible_action.is_fully_bound:
                print(f"Action {possible_action} was not fully bound")
                return
            in_state = True
            for precondition in possible_action.preconditions:
                if not self.precondition_in_state(precondition):
                    in_state = False
                    break
            if in_state:
                enabled_actions.append(possible_action)

        return enabled_actions

    def precondition_in_state(self, precondition):
        if precondition.is_negated:
            if not self.state_dictionary.__contains__(precondition.to_string_ignoring_negation()):
                return True
            return not self.state_dictionary.get(precondition.to_string_ignoring_negation())
        else:
            if not self.state_dictionary.__contains__(precondition.to_string_ignoring_negation()):
                return False
        return self.state_dictionary.get(precondition.to_string_ignoring_negation())

    # action_templates is a list of Actions
    def get_possible_actions(self, pddl_objects, action_templates):
        possible_actions = []
        for action in action_templates:
            self.compute_action_binds(pddl_objects, action, possible_actions)

        return possible_actions

    # current action is an action that's initially unbound.
    def compute_action_binds(self, objects, current_action, set_of_binds):
        if not current_action.is_fully_bound():
            for pddl_object in objects:
                copy_action = Action("", "")
                copy_action.__copy__(current_action)
                # find the first unbound parameter then break
                for parameter in copy_action.parameters:
                    if copy_action.bindings[parameter].__contains__("?"):
                        copy_action.set_binding(parameter, pddl_object)
                        self.compute_action_binds(objects, copy_action, set_of_binds)
                        break

        else:
            set_of_binds.append(current_action)

        return set_of_binds

    def __str__(self):
        statement_to_print = ""
        for key in self.state_dictionary.keys():
            if self.state_dictionary.get(key):
                statement_to_print += f"{key}\n"

        return statement_to_print


# object_list = ["arthur", "bill"]
#
# predicate_list = [
#     Predicate("player", ["player"], False),
#     Predicate("character", ["character"], False),
# ]
#
# predicate_list[0].set_binding("player", object_list[0])
# predicate_list[1].set_binding("character", object_list[0])
#
# action_list = [
#     Action("kill", ["victim"]),
#     Action("transform", ["preTransformCharacter", "postTransformCharacter"])
# ]
# action_list[0].add_precondition(Predicate("alive", ["victim"], True))
# action_list[0].add_effect(Predicate("alive", ["victim"], False))
# action_list[1].add_precondition(Predicate("character", ["preTransformCharacter"], False))
# action_list[1].add_effect(Predicate("character", ["preTransformCharacter"], True))
# action_list[1].add_effect(Predicate("character", ["postTransformCharacter"], False))
#
# new_state = State(predicate_list)
#
# print(new_state.state_dictionary)
#
# print(new_state)

# print("fully bound actions:\n")
# for fully_bound_action in new_state.get_possible_actions(object_list, action_list):
#     print(fully_bound_action)

# print("enabled actions:\n")
# for enabled_action in new_state.check_fully_bound_actions(new_state.get_possible_actions(object_list, action_list)):
#     print(enabled_action)
#
# new_state.update(new_state.check_fully_bound_actions(new_state.get_possible_actions(object_list, action_list))[1])
#
# print(new_state)
# print(new_state.state_dictionary)
# print(predicate_list[0].to_string_ignoring_negation())
# print(new_state.state_dictionary.get_val(f"{predicate_list[0].to_string_ignoring_negation()}"))
# print(new_state.state_dictionary.get_val(f"{predicate_list[1].to_string_ignoring_negation()}"))
# print(new_state.state_dictionary.get_val(f"{predicate_list[2].to_string_ignoring_negation()}"))

