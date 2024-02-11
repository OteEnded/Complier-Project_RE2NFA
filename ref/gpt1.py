class NFA:
    def __init__(self, states, alphabet, transitions, start_state, accept_states):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.start_state = start_state
        self.accept_states = accept_states

def epsilon_closure(states, transitions):
    closure = set(states)
    stack = list(states)

    while stack:
        current_state = stack.pop()
        epsilon_transitions = transitions.get((current_state, ''), [])

        for state in epsilon_transitions:
            if state not in closure:
                closure.add(state)
                stack.append(state)

    return frozenset(closure)

def re_to_nfa(regexp):
    states = set()
    alphabet = set()
    transitions = {}
    start_state = 0
    accept_states = set()
    state_counter = 1

    def add_state():
        nonlocal state_counter
        state = state_counter
        state_counter += 1
        return state

    def handle_char(char):
        nonlocal states, alphabet, transitions, state_counter

        start = add_state()
        end = add_state()

        states.add(start)
        states.add(end)
        alphabet.add(char)

        transitions.setdefault((start, char), []).append(end)

        return start, end

    def handle_concatenation(exp1, exp2):
        nonlocal states, alphabet, transitions

        start1, end1 = convert(exp1)
        start2, end2 = convert(exp2)

        states.remove(end1)
        alphabet.remove('')

        transitions.setdefault((end1, ''), []).append(start2)

        return start1, end2

    def handle_union(exp1, exp2):
        nonlocal states, alphabet, transitions

        start = add_state()
        end = add_state()

        start1, end1 = convert(exp1)
        start2, end2 = convert(exp2)

        states.add(start)
        states.add(end)
        alphabet.discard('')

        transitions.setdefault((start, ''), []).extend([start1, start2])
        transitions.setdefault((end1, ''), []).append(end)
        transitions.setdefault((end2, ''), []).append(end)

        return start, end

    def handle_closure(exp):
        nonlocal states, alphabet, transitions

        start = add_state()
        end = add_state()

        start1, end1 = convert(exp)

        states.add(start)
        states.add(end)
        alphabet.discard('')

        transitions.setdefault((start, ''), []).extend([start1, end])
        transitions.setdefault((end1, ''), []).extend([start1, end])

        return start, end

    def convert(exp):
        if len(exp) == 1:
            return handle_char(exp)
        elif exp[1] == '*':
            return handle_closure(exp[0])
        elif '|' in exp:
            i = exp.index('|')
            return handle_union(exp[:i], exp[i+1:])
        elif '.' in exp:
            i = exp.index('.')
            return handle_concatenation(exp[:i], exp[i+1:])

    start, end = convert(regexp)

    accept_states.add(end)

    epsilon_transitions = transitions.setdefault((start, ''), [])
    epsilon_transitions.append(end)

    epsilon_closure_states = epsilon_closure({start}, transitions)

    return NFA(states, alphabet, transitions, epsilon_closure_states, accept_states)

def print_nfa(nfa):
    print("States:", nfa.states)
    print("Alphabet:", nfa.alphabet)
    print("Transitions:")
    for (state, symbol), next_states in nfa.transitions.items():
        print(f"  {state} --{[symbol, 'ε'][symbol == '']}--> {next_states}")
    print("Start State:", nfa.start_state)
    print("Accept States:", nfa.accept_states)

# Example usage:
regexp_input = "(b(a|b))*abb"
nfa = re_to_nfa(regexp_input)
print_nfa(nfa)
