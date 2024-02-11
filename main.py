import NFA

def main():
    
    # Example usage:
    nfa = NFA.NFA_object(
        [1, 2, 3, 4],
        {'a', 'b'},
        {1: {'a': [2]}, 2: {'b': [3]}, 3: {'a': [4], 'b': [4]}, 4: {'': [3]}},
        1,
        [4]
    )

    # Print the graph
    nfa.printOut()
        
main()
exit(0)