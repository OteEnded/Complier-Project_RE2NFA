from typing import Union
from NFA import NFA_object

def symbolToNFA(symbol: str, previous_NFA: Union[str, NFA_object] = None):
    start_state = 1
    if ((previous_NFA != None) and (isinstance(previous_NFA, NFA_object))):
        start_state += max(previous_NFA.states)
    accept_state = start_state + 1
    
    return NFA_object(
        states=[start_state, accept_state],
        alphabet=[symbol],
        transitions={start_state: {symbol: [accept_state]}, accept_state: {}},
        start_state=start_state,
        accept_states=[accept_state]
    )

def star(operand: Union[str, NFA_object]):
    
    # check if operand is an string or an NFA_object
    if (not isinstance(operand, NFA_object)) and (type(operand) != str): raise Exception("NFA[star]: operand should be a string or an NFA_object")
    
    if ((not isinstance(operand, NFA_object)) and (type(operand) == str)): # if operand is a string
        # then turn it into an NFA_object
        operand = symbolToNFA(operand)
    
    # 'star' the operand that is an NFA_object
    old_start_state = operand.start_state
    # check if list of old_accept_states has more than one element
    if len(operand.accept_states) > 1: raise Exception("NFA[star]: NFA from RE should have only one accept state")
    old_accept_states = operand.accept_states[0]
    
    new_start_state = max(operand.states) + 1
    new_accept_state = new_start_state + 1
    
    new_NFA = NFA_object(
        states=operand.states + [new_start_state, new_accept_state],
        alphabet=operand.alphabet,
        transitions=operand.transitions,
        start_state=new_start_state,
        accept_states=[new_accept_state]
    )
    
    new_NFA.addTransition(new_start_state, '', [old_start_state, new_accept_state])
    new_NFA.addTransition(old_accept_states, '', [old_start_state, new_accept_state])
    
    return new_NFA

def concatenate(operand1: Union[str, NFA_object], operand2: Union[str, NFA_object]):
    # check if operand1 and operand2 are strings or NFA_objects
    if ((not isinstance(operand1, NFA_object)) and (type(operand1) != str) or (not isinstance(operand2, NFA_object)) and (type(operand2) != str)):
        raise Exception("NFA[union]: operands should be strings or NFA_objects")
    
    if ((not isinstance(operand1, NFA_object)) and (type(operand1) == str)): # if operand1 is a string
        # then turn it into an NFA_object
        operand1 = symbolToNFA(operand1, operand2)
    
    if ((not isinstance(operand2, NFA_object)) and (type(operand2) == str)): # if operand2 is a string
        # then turn it into an NFA_object
        operand2 = symbolToNFA(operand2, operand1)
        
    # 'concatenate' the operands that are NFA_objects
    old_start_state1 = operand1.start_state
    old_start_state2 = operand2.start_state
    # check if list of old_accept_states1 has more than one element
    if len(operand1.accept_states) > 1: raise Exception("NFA[concatenate]: NFA from RE should have only one accept state but operand1 has more than one ->\n" + str(operand1.getData()))
    if len(operand2.accept_states) > 1: raise Exception("NFA[concatenate]: NFA from RE should have only one accept state but operand2 has more than one ->\n" + str(operand2.getData()))
    old_accept_states1 = operand1.accept_states[0]
    old_accept_states2 = operand2.accept_states[0]
    
    new_start_state = operand1.start_state
    new_accept_state = old_accept_states2
    
    new_NFA = NFA_object(
        states=operand1.states + operand2.states,
        alphabet=operand1.alphabet + operand2.alphabet,
        transitions={**operand1.transitions, **operand2.transitions},
        start_state=new_start_state,
        accept_states=[new_accept_state]
    )
    
    new_NFA.addTransition(old_accept_states1, '', old_start_state2)
    
    return new_NFA

def union(operand1: Union[str, NFA_object], operand2: Union[str, NFA_object]):
    # check if operand1 and operand2 are strings or NFA_objects
    if ((not isinstance(operand1, NFA_object)) and (type(operand1) != str) or (not isinstance(operand2, NFA_object)) and (type(operand2) != str)):
        raise Exception("NFA[union]: operands should be strings or NFA_objects")
    
    if ((not isinstance(operand1, NFA_object)) and (type(operand1) == str)): # if operand1 is a string
        # then turn it into an NFA_object
        operand1 = symbolToNFA(operand1, operand2)
    
    if ((not isinstance(operand2, NFA_object)) and (type(operand2) == str)): # if operand2 is a string
        # then turn it into an NFA_object
        operand2 = symbolToNFA(operand2, operand1)
        
    # 'union' the operands that are NFA_objects
    old_start_state1 = operand1.start_state
    old_start_state2 = operand2.start_state
    # check if list of old_accept_states1 and old_accept_states2 has more than one element
    if len(operand1.accept_states) > 1: raise Exception("NFA[union]: NFA from RE should have only one accept state but operand1 has more than one ->\n" + str(operand1.getData()))
    if len(operand2.accept_states) > 1: raise Exception("NFA[union]: NFA from RE should have only one accept state but operand2 has more than one ->\n" + str(operand2.getData()))
    old_accept_states1 = operand1.accept_states[0]
    old_accept_states2 = operand2.accept_states[0]
    
    new_start_state = max(max(operand1.states), max(operand2.states)) + 1
    new_accept_state = new_start_state + 1
    
    new_NFA = NFA_object(
        states= operand1.states + operand2.states + [new_start_state, new_accept_state],
        alphabet=operand1.alphabet,
        transitions={**operand1.transitions, **operand2.transitions},
        start_state=new_start_state,
        accept_states=[new_accept_state]
    )
    
    new_NFA.addTransition(new_start_state, '', [old_start_state1, old_start_state2])
    new_NFA.addTransition(old_accept_states1, '', new_accept_state)
    new_NFA.addTransition(old_accept_states2, '', new_accept_state)
    
    return new_NFA




def process(re: str):
    # remove all spaces from re
    re = re.replace(' ', '')
    # add a '.' between two symbols or a symbol and a '(' or a ')' or a '*' or a '|'
    
    