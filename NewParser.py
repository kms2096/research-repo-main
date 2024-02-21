from State import State
from Action import Action
from Predicate import Predicate

class NewParser:
    def readObjects(self, fileName):
        with open(fileName) as file:
            for line in file:
                # Reads only after the objects token
                if '(:objects' in line:
                    line = line.split()
                    line.pop(0)

                    while '(:INIT' not in line[0].strip():
                        line[0] = line[0].strip(')')
                        objects_array.append(line.pop(0))

                        if len(line) == 0:
                            line = file.readline().split()

    
    # Reads in the initial state from the problem file
    def readInitState(self, fileName):
        localPred = ''
        localArray = []
        with open(fileName) as file:
            for line in file:
                # Reads only after the initial token
                if '(:INIT' in line:
                    line = line.strip('(:INIT').split()
                    # Reads until it reaches the next token
                    while '(:goal' not in line[0].strip():
                        # Reads until the line is empty
                        while len(line) != 0:
                            # Adds the predicate to the array
                            if '(' in line[0]:
                                line[0] = line[0].lstrip('(')
                                localPred = line.pop(0)
                            # Last variable for this predicate 
                            if line[0].strip()[-1] == ')':
                                line[0] = line[0].rstrip(')')
                                localArray.append(line.pop(0))
                                # Creating the predicate
                                init_array.append(Predicate(localPred, localArray, False))
                                localArray = []
                            # Additional variable for this predicate
                            else:
                                localArray.append(line.pop(0))

                        line = file.readline().split()

    # Reads in the possible predicates from the domain file
    def readPredicate(self, fileName):
        localName = ''
        localArray = []
        with open(fileName) as file:
            for line in file:
                # Reads only after the predicate token
                if '(:predicates' in line:
                    line = file.readline()
                    # Reads until the final ')' - takes up whole line
                    while line.strip()[0] != ')':
                        # Gets rid of whitespace and '('
                        line = line.strip().lstrip('(').split()
                        localName = line.pop(0)
                        # Goes over the remaining variables in the sliceLine array
                        for vars in line:
                            # Gets rid of the characters around it
                            localArray.append(vars.strip('?)'))
                        # Creates new predicate object and sets it to the dictionary
                        predicate_dictionary[localName] = Predicate(localName, localArray, False)
                        localArray = []
                        # Reads in the next line
                        line = file.readline()

    # Sets the objects to the corresponding variable in the initial state
    def setPredsToObjects(self):
        # Loop through initial state dictionary
        for i, state in enumerate(init_array):
                # Loop through objects array
                for obj in objects_array:
                    # Loops the 
                    for j, vars in enumerate(init_array[i].parameters):
                    # Check if the words match, and set it
                    # Set object to the predicate
                        if obj == vars.upper():
                            init_array[i].set_binding(init_array[i].parameters[j], vars.upper())
                            break

    def readActions(self, fileName):
        # Name of action
        actionName = ''
        # List of parameters
        parameters = []
        
        with open(fileName) as file:
            for line in file:
                line = line.split()

                # Read (:action token - take rest of the line and assign it to the actionName
                if '(:action' in line:
                    actionName = line.pop(-1)

                # Read :parameters token - take the rest before the ')' and add them to a list
                if ':parameters' in line:
                    line.pop(0)
                    
                    for params in line:
                        if params.strip()[-1] == ')':
                            parameters.append(params.strip(')?'))
                            action_dictionary.append(Action(actionName, parameters))
                            parameters = []

                        else:
                            parameters.append(params.strip('(?'))

                if ':precondition' in line:
                    fileParser.readActionsHelper(file, 'precondition')
                
                if ':effect' in line:
                    fileParser.readActionsHelper(file, 'effect')

            line = file.readline()
    
    def readActionsHelper(self, file, token):
        localName = ''
        localArray = []
        negated = False

        line = file.readline()
        line = file.readline().split()

        # Reads until the final ')' - takes up whole line
        while ')' not in line[0].strip():
            if 'not' in line[0]:
                negated = True
                line.pop(0)

            else:
                negated = False

            # Gets the name
            if '(' in line[0]:
                line[0] = line[0].lstrip('(')
                localName = line.pop(0)

            while '?' in line[0]:
                line[0] = line[0].strip('?')

                if ')' in line[0]:
                    localArray.append(line[0].strip(')'))
                    predicateObject = Predicate(localName, localArray, negated)
                    localArray = []
                    line.pop(0)
                    length = len(action_dictionary) - 1

                    if token == 'effect':
                        action_dictionary[length].add_effect(predicateObject)
                    
                    if token == 'precondition':
                        action_dictionary[length].add_precondition(predicateObject)

                    if len(line) == 0:
                        line = file.readline().split()
                        break
                    
                else:
                    localArray.append(line.pop(0))

    def getObjects(self):
        return objects_array
    
    def getinitState(self):
        return init_array
    
    def getPredicateDict(self):
        return predicate_dictionary
    
    def getActions(self):
        return action_dictionary


predicate_dictionary = {}
action_dictionary = []
objects_array = []
init_array = []
fileParser = NewParser()

fileParser.readPredicate('domain.pddl')
fileParser.readObjects('prob01.pddl')
fileParser.readInitState('prob01.pddl')
fileParser.setPredsToObjects()
fileParser.readActions('domain.pddl')

print("\nObjects Array:")
print(objects_array)

print("\nInit State:")
print([str(x) for x in init_array])

print("\nPredicate Array:")
for key in predicate_dictionary:
    print(predicate_dictionary[key])
#print('\n')
print("\nActions:")
i = 0
while i < len(action_dictionary):
    print(action_dictionary[i])
    i += 1