def union(nfa_1, nfa_2):

    start = max([nfa_1.accept, nfa_2.accept]) + 1
    accept = start + 1

    alphabet = list(set(nfa_1.alphabet + nfa_2.alphabet))
    states = nfa_1.states + nfa_2.states
    states.extend([start, accept])

    empty_trans = {}

    for i in alphabet:
        empty_trans[i] = []

    old_trans = {
        **nfa_1.transition,
        **nfa_2.transition
    }

    transition = {
        start: {
            "ε": [nfa_1.start],
            **empty_trans
        },
        accept: {
            "ε": [nfa_2.start],
            **empty_trans
        },
        **old_trans
    }    

    transition[nfa_1.start]["ε"].append(accept)
    transition[nfa_2.start]["ε"].append(accept)

    return NFA(states, alphabet, transition, start, accept)

def star(nfa):

    start = nfa.accept + 1
    accept = start + 1

    alphabet = nfa.alphabet
    states = nfa.states
    states.extend([start, accept])

    empty_trans = {}

    for i in alphabet:
        empty_trans[i] = []
    
    transition = {
        start: {
            "ε": [nfa.start],
            **empty_trans
        },
        accept: {
            "ε": [],
            **empty_trans
        },
        **nfa.transition
    }    

    transition[nfa.accept]["ε"].append(accept)
    transition[start]["ε"].append(accept)
    transition[nfa.start]["ε"].append(nfa.accept)

    return NFA(states, alphabet, transition, start, accept)

def concat(nfa_1, nfa_2):

    start = nfa_1.start
    accept = nfa_2.accept
    new_node = accept + 1
    alphabet = list(set(nfa_1.alphabet + nfa_2.alphabet))

    empty_trans = {}

    for i in alphabet:
        empty_trans[i] = []

    alphabet = list(set(nfa_1.alphabet + nfa_2.alphabet))
    states = nfa_1.states + nfa_2.states
    states.extend([start, accept])

    transition = {
        **nfa_1.transition,
        **nfa_2.transition
    }

    for i in nfa_1.states:
        for j in nfa_1.alphabet:
            if nfa_1.accept in nfa_1.transition[i][j]:
                transition[i][j].remove(nfa_1.accept)
                transition[i][j].append(new_node)

    transition[new_node] = nfa_2.transition[nfa_2.start]
    transition.pop(nfa_2.start)

    return NFA(states, alphabet, transition, start, accept)

class NFA:
    def __init__(self, states, alphabet, transition, start, accept):
        self.states = states
        self.alphabet = alphabet
        self.transition = transition
        self.start = start
        self.accept = accept

    def print_t(self):
        headers = ['State' ,'ε']
        headers.extend(sorted(self.alphabet))
        print(*headers, sep='\t|')
        for state, transitions_ in self.transition.items():
            row = [state]
            for symbol, next_states in transitions_.items():
                row.append(",".join(map(str, next_states))) if next_states else row.append("")
            print(*row, sep="\t|")
            
    def __str__(self):
        return "States: " + str(self.states) + "\n" + "Alphabet: " + str(self.alphabet) + "\n" + "Start: " + str(self.start) + "\n" + "Accept: "+  str(self.accept)

states_1 = [0, 1]
alphabet_1 = ['a', 'b']
transition_1 = {
    0: {
        "ε": [],
        "a": [1],
        "b": []
    }, 
    1: {
        "ε": [],
        "a": [],
        "b": []
    },
}
start_1 = 0
accept_1 = 1

nfa_1 = NFA(states_1, alphabet_1, transition_1, start_1, accept_1)

states_2 = [2, 3]
alphabet_2 = ['a', 'b']
transition_2 = {
    2: {
        "ε": [],
        "a": [3],
        "b": []
    }, 
    3: {
        "ε": [],
        "a": [],
        "b": []
    },
}
start_2 = 2
accept_2 = 3

nfa_2 = NFA(states_2, alphabet_2, transition_2, start_2, accept_2)

print("-Concat-")
concat_nfa = concat(nfa_1, nfa_2)
concat_nfa.print_t()
print(concat_nfa)

print("-Union-")
union_nfa = union(nfa_1, nfa_2)
print(union_nfa)
union_nfa.print_t()

print("-Star-")
star_nfa = star(union_nfa)
print(star_nfa)
star_nfa.print_t()