from State import State
from Action import Action
from Predicate import Predicate

class Parser:
    # Reads in the object from the problem file
    def readObjects(self):
        #with open('arthur/prob01.pddl') as file:
        with open('prob01.pddl') as file:
            for line in file:
                # Reads only after the objects token
                if '(:objects' in line:
                    line = line.split()
                    line.pop(0)
                    line[-1] = line[-1].rstrip(')')
                    objects_array.extend(line)
        #return objects_array
    
    # Reads in the initial state from the problem file
    def readInitState(self):
        localPred = ''
        localArray = []
        #with open('arthur/prob01.pddl') as file:
        with open('prob01.pddl') as file:
            for line in file:
                # Reads only after the initial token
                if '(:INIT' in line:
                    line = line.strip('(:INIT')
                    slicedLine = line.split()
                    # Reads until it reaches the next token
                    while '(:goal' not in slicedLine[0].strip():# != '))':
                    #while slicedLine[0].strip()[-2:] != '))' or slicedLine[0][-1] == '\n':
                        # Reads until the line is empty
                        while len(slicedLine) != 0:
                            # Adds the predicate to the array
                            if '(' in slicedLine[0]:
                                slicedLine[0] = slicedLine[0].lstrip('(')
                                localPred = slicedLine.pop(0)
                            # Last variable for this predicate 
                            if slicedLine[0].strip()[-1] == ')':
                                slicedLine[0] = slicedLine[0].rstrip(')')
                                localArray.append(slicedLine.pop(0))
                                # Creating the predicate
                                predicateObject = Predicate(localPred, localArray, False)
                                init_array.append(predicateObject)
                                localArray = []
                            # Additional variable for this predicate
                            else:
                                pred = slicedLine.pop(0)
                                localArray.append(pred)

                        # Resets the slicedLine and splits the next line from the file
                        slicedLine = ''
                        line = file.readline()
                        slicedLine = line.split()

    # Reads in the possible predicates from the domain file
    def readPredicate(self):
        localName = ''
        localArray = []
        #with open('arthur/domain.pddl') as file:
        with open('domain.pddl') as file:
            for line in file:
                # Reads only after the predicate token
                if '(:predicates' in line:
                    line = file.readline()
                    # Reads until the final ')' - takes up whole line
                    while line.strip()[0] != ')':
                        # Gets rid of whitespace and '('
                        slicedLine = line.strip()
                        slicedLine = slicedLine.lstrip('(')
                        slicedLine = slicedLine.split()
                        localName = slicedLine.pop(0)
                        # Goes over the remaining variables in the sliceLine array
                        for vars in slicedLine:
                            # Gets rid of the characters around it
                            vars = vars.strip('?)')
                            localArray.append(vars)
                        # Creates new predicate object and sets it to the dictionary
                        predicateObject = Predicate(localName, localArray, False)
                        localArray = []
                        predicate_dictionary[localName] = predicateObject
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


    def readActions(self):
        # Name of action
        actionName = ''
        # List of parameters
        parameters = []
        
        slicedLine = []
        #with open('arthur/domain.pddl') as file:
        with open('domain.pddl') as file:
            for line in file:
                # Read (:action token - take rest of the line and assign it to the actionName
                if '(:action' in line:
                    slicedLine = line.split()
                    actionName = slicedLine.pop(-1)

                # Read :parameters token - take the rest before the ')' and add them to a list
                if ':parameters' in line:
                    slicedLine = line.split()
                    slicedLine.pop(0)
                    
                    for params in slicedLine:
                        if params.strip()[-1] == ')':
                            params = params.strip(')?')
                            parameters.append(params)
                            actionObject = Action(actionName, parameters)
                            parameters = []
                            action_dictionary.append(actionObject)

                        else:
                            params = params.strip('(?')
                            parameters.append(params)

                if ':precondition' in line:
                    localName = ''
                    localArray = []
                    negated = False

                    line = file.readline()
                    line = file.readline()
                    slicedLine = line.split()
                    
                    # Reads until the final ')' - takes up whole line
                    while ')' not in slicedLine[0].strip():
                        if 'not' in slicedLine[0]:
                            negated = True
                            slicedLine.pop(0)
                        else:
                            negated = False

                        # Gets the name
                        if '(' in slicedLine[0]:
                            slicedLine[0] = slicedLine[0].lstrip('(')
                            localName = slicedLine.pop(0)

                        while '?' in slicedLine[0]:
                            slicedLine[0] = slicedLine[0].strip('?')

                            if ')' in slicedLine[0]:
                                slicedLine[0] = slicedLine[0].strip(')')
                                localArray.append(slicedLine[0])
                                predicateObject = Predicate(localName, localArray, negated)
                                localArray = []
                                slicedLine.pop(0)
                                length = len(action_dictionary) - 1
                                action_dictionary[length].add_precondition(predicateObject)

                                if len(slicedLine) == 0:
                                    line = file.readline()
                                    slicedLine = line.split()
                                    break
                                
                            else:
                                localArray.append(slicedLine[0])
                                slicedLine.pop(0)
                
                if ':effect' in line:
                    localName = ''
                    localArray = []
                    negated = False

                    line = file.readline()
                    line = file.readline()
                    slicedLine = line.split()

                    # Reads until the final ')' - takes up whole line
                    while ')' not in slicedLine[0].strip():
                        if 'not' in slicedLine[0]:
                            negated = True
                            slicedLine.pop(0)
                        else:
                            negated = False

                        # Gets the name
                        if '(' in slicedLine[0]:
                            slicedLine[0] = slicedLine[0].lstrip('(')
                            localName = slicedLine.pop(0)

                        while '?' in slicedLine[0]:
                            slicedLine[0] = slicedLine[0].strip('?')

                            if ')' in slicedLine[0]:
                                slicedLine[0] = slicedLine[0].strip(')')
                                localArray.append(slicedLine[0])
                                predicateObject = Predicate(localName, localArray, negated)
                                localArray = []
                                slicedLine.pop(0)
                                length = len(action_dictionary) - 1
                                action_dictionary[length].add_effect(predicateObject)

                                if len(slicedLine) == 0:
                                    line = file.readline()
                                    slicedLine = line.split()
                                    break
                                
                            else:
                                localArray.append(slicedLine[0])
                                slicedLine.pop(0)

            line = file.readline()
        

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
fileParser = Parser()

fileParser.readPredicate()
fileParser.readObjects()
fileParser.readInitState()
fileParser.setPredsToObjects()
fileParser.readActions()

#print("\nObjects Array:")
#print(objects_array)

#print("\nInit State:")
#print([str(x) for x in init_array])

#print("\nPredicate Array:")
#for key in predicate_dictionary:
    #print(predicate_dictionary[key])

#print("\nActions:")
#i = 0
#while i < len(action_dictionary):
 #   print(action_dictionary[i])
  #  i += 1

