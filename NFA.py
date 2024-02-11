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
            "alphabet": self.alphabet,
            "transitions": self.transitions,
            "start_state": self.start_state,
            "accept_states": self.accept_states
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

    def drawOut(self):
        from graphviz import Digraph
        dot = Digraph()
        for state in self.states:
            if state in self.accept_states:
                dot.node(str(state), shape='doublecircle')
            else:
                dot.node(str(state))
        for state, symbol_transitions in self.transitions.items():
            for symbol, next_states in symbol_transitions.items():
                for next_state in next_states:
                    if symbol == '':
                        dot.edge(str(state), str(next_state), label='ε')
                    else:
                        dot.edge(str(state), str(next_state), label=symbol)
        dot.render('output/NFA.gv', view=True)