from typing import Union

class NFA_object:
    
    states = []
    alphabet = []
    transitions = {} # {state: {symbol: [next_state1, next_state2, ...], ...}, ...}
    start_state = 0
    accept_states = []
    
    
    def __init__(self, states: list, alphabet: list, transitions: dict, start_state: int, accept_states: list):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.start_state = start_state
        self.accept_states = accept_states
        
        
    def getData(self):
        data = {
            "states": self.states,
            "alphabet": [],
            "transitions": {},
            "start_state": 0,
            "accept_states": []
        }
        return data
    
    def addTransition(self, state: int, symbol: str, next_state: Union[int, list]):
        if state not in self.states: raise Exception("NFA[addTransition]: state not in states")
        if ((symbol not in self.alphabet) and (symbol != '')): raise Exception("NFA[addTransition]: symbol not in alphabet")
        
        if state not in self.transitions: self.transitions[state] = {}
        if symbol not in self.transitions[state]: self.transitions[state][symbol] = []
        if (type(next_state) == list):
            for ns in next_state:
                if ns not in self.states: raise Exception("NFA[addTransition]: next_state not in states")
                self.transitions[state][symbol].append(ns)
        else:
            if next_state not in self.states: raise Exception("NFA[addTransition]: next_state not in states")
            self.transitions[state][symbol].append(next_state)

    def printOut(self):
        print("States:", self.states)
        print("Alphabet:", self.alphabet)
        print("Transitions:")
        for state, symbol_transitions in self.transitions.items():
            for symbol, next_states in symbol_transitions.items():
                for next_state in next_states:
                    print(f"  {state} --{[symbol, 'ε'][symbol == '']}--> {next_state}")
        print("Start State:", self.start_state)
        print("Accept States:", self.accept_states)

def star(operand: Union[str, NFA_object]):
    
    # check if operand is an string or an NFA_object
    if (not isinstance(operand, NFA_object)) and (type(operand) != str): raise Exception("NFA[star]: operand should be a string or an NFA_object")
    
    if ((not isinstance(operand, NFA_object)) and (type(operand) == str)): # if operand is a string
        # then turn it into an NFA_object
        operand = NFA_object(
            states=[1, 2],
            alphabet=[operand],
            transitions={
                1: {
                    operand: [2]
                }, 
                2: {}
            },
            start_state=1,
            accept_states=[2]
        )
    
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