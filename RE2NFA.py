from typing import Union
from NFA import NFA_object

class Operator:

    @staticmethod
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

    @staticmethod
    def star(operand: Union[str, NFA_object], previous_NFA: Union[str, NFA_object] = None):
        # check if operand is an string or an NFA_object
        if (not isinstance(operand, NFA_object)) and (type(operand) != str): raise Exception("NFA[star]: operand should be a string or an NFA_object")
        
        if ((not isinstance(operand, NFA_object)) and (type(operand) == str)): # if operand is a string
            # then turn it into an NFA_object
            operand = Operator.symbolToNFA(operand, previous_NFA)
        
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

    @staticmethod
    def concatenate(operand1: Union[str, NFA_object], operand2: Union[str, NFA_object], previous_NFA: Union[str, NFA_object] = None):
        # check if operand1 and operand2 are strings or NFA_objects
        if ((not isinstance(operand1, NFA_object)) and (type(operand1) != str) or (not isinstance(operand2, NFA_object)) and (type(operand2) != str)):
            raise Exception("NFA[union]: operands should be strings or NFA_objects")
        
        if ((not isinstance(operand1, NFA_object)) and (type(operand1) == str)): # if operand1 is a string
            # then turn it into an NFA_object
            operand1 = Operator.symbolToNFA(operand1, [operand2, previous_NFA][((not isinstance(operand2, NFA_object)) and (type(operand2) == str))])
        
        if ((not isinstance(operand2, NFA_object)) and (type(operand2) == str)): # if operand2 is a string
            # then turn it into an NFA_object
            operand2 = Operator.symbolToNFA(operand2, [operand1, previous_NFA][((not isinstance(operand1, NFA_object)) and (type(operand1) == str))])
            
        # 'concatenate' the operands that are NFA_objects
        old_start_state1 = operand1.start_state
        old_start_state2 = operand2.start_state
        # check if list of old_accept_states1 has more than one element
        if len(operand1.accept_states) > 1: raise Exception("NFA[concatenate]: NFA from RE should have only one accept state but operand1 has more than one ->\n" + str(operand1.getData()))
        if len(operand2.accept_states) > 1: raise Exception("NFA[concatenate]: NFA from RE should have only one accept state but operand2 has more than one ->\n" + str(operand2.getData()))
        old_accept_states1 = operand1.accept_states[0]
        old_accept_states2 = operand2.accept_states[0]
        
        new_start_state = old_start_state1
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

    @staticmethod
    def union(operand1: Union[str, NFA_object], operand2: Union[str, NFA_object], previous_NFA: Union[str, NFA_object] = None):
        # check if operand1 and operand2 are strings or NFA_objects
        if ((not isinstance(operand1, NFA_object)) and (type(operand1) != str) or (not isinstance(operand2, NFA_object)) and (type(operand2) != str)):
            raise Exception("NFA[union]: operands should be strings or NFA_objects")
        
        if ((not isinstance(operand1, NFA_object)) and (type(operand1) == str)): # if operand1 is a string
            # then turn it into an NFA_object
            operand1 = Operator.symbolToNFA(operand1, [operand2, previous_NFA][((not isinstance(operand2, NFA_object)) and (type(operand2) == str))])
        
        if ((not isinstance(operand2, NFA_object)) and (type(operand2) == str)): # if operand2 is a string
            # then turn it into an NFA_object
            operand2 = Operator.symbolToNFA(operand2, [operand1, previous_NFA][((not isinstance(operand1, NFA_object)) and (type(operand1) == str))])
            
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

class Operation:
    
    @staticmethod
    def split_list(processing_list: list, key: str):
        result = []
        current_group = []

        for item in processing_list:
            if item == key:
                if current_group:
                    result.append(current_group)
                    current_group = []
            else:
                current_group.append(item)

        if current_group:
            result.append(current_group)

        return result

    last_NFA = None
    RE = []
    
    def __init__(self, re: str = None):
        if re != None: self.setRE(re)

    def resolveByOrder(self, processing_list: list):
        # resolve by order of operations
        # 1. star
        # 2. concatenate
        # 3. union
        
        # resolve star
        print("RE2NFA[Operation][resolveByOrder]: invoking resolveStar with processing_list ->", processing_list)
        processing_list = self.resolveStar(processing_list)
        print("RE2NFA[Operation][resolveByOrder]: processing_list after resolveStar ->", processing_list)
    
        # resolve concatenate
        concatenate_resolved = {}
        concatenate_chunks = Operation.split_list(processing_list, '|')
        print("RE2NFA[Operation][resolveByOrder]: split processing_list by | to target concatenate ->", concatenate_chunks)
        temp = []
        print("RE2NFA[Operation][resolveByOrder]: invoking resolveConcatenate chunk by chunk")
        for chunk in concatenate_chunks: 
            print("RE2NFA[Operation][resolveByOrder]: invoking resolveConcatenate with chunk ->", chunk)
            temp.append(self.resolveConcatenate(chunk))
        print("RE2NFA[Operation][resolveByOrder]: result of resolveConcatenate ->", temp)
        processing_list = temp
        
        # resolve union
        print("RE2NFA[Operation][resolveByOrder]: invoking resolveUnion with processing_list ->", processing_list)
        processing_list = self.resolveUnion(processing_list)
        print("RE2NFA[Operation][resolveByOrder]: processing_list after resolveUnion ->", processing_list)
        
        return processing_list

    def resolveUnion(self, processing_list: list):
        print("RE2NFA[Operation][resolveUnion]: resolving union with processing_list ->", processing_list)
        if (len(processing_list) == 1): return processing_list[0]
        if (len(processing_list) > 2): return self.resolveUnion([self.resolveUnion(processing_list[:-1]), processing_list[-1]])
        if (len(processing_list) == 2): return Operator.union(processing_list[0], processing_list[1], self.last_NFA)

    def resolveConcatenate(self, processing_list: list):
        print("RE2NFA[Operation][resolveConcatenate]: resolving concatenate with processing_list ->", processing_list)
        if len(processing_list) == 1: return processing_list[0]
        if len(processing_list) > 2: return self.resolveConcatenate([self.resolveConcatenate(processing_list[:-1]), processing_list[-1]])
        if len(processing_list) == 2: return Operator.concatenate(processing_list[0], processing_list[1], self.last_NFA)

    def resolveStar(self, processing_list: list):
        print("RE2NFA[Operation][resolveStar]: resolving star with processing_list ->", processing_list)
        star_resolved = {}
        for i in range(len(processing_list)):
            if processing_list[i] == '*':
                if (i == 0): raise Exception("RE2NFA[resolveByOrder]: * should not be at the beginning of the list ->\n" + "".join(processing_list))
                if (processing_list[i - 1] == '|'): raise Exception("RE2NFA[resolveByOrder]: * should not be after | ->\n" + "".join(processing_list))
                resolved = Operator.star(processing_list[i - 1], self.last_NFA)
                self.last_NFA = resolved
                star_resolved[i] = resolved
        print("RE2NFA[Operation][resolveStar]: star_resolved ->", star_resolved)
        for i in (sorted(star_resolved.keys(), reverse=True)):
            processing_list.pop(i)
            processing_list[i - 1] = star_resolved[i]
        return processing_list

    def resolveParentheses(self, processing_list: list):
        
        print("RE2NFA[Operation][resolveParentheses]: resolving parentheses with processing_list ->", processing_list)
        
        # Find the most inner parentheses
        inner_parentheses_open = -1
        inner_parentheses_close = -1
        for i in (range(len(processing_list))):
            if processing_list[i] == '(':
                inner_parentheses_open = i
            if processing_list[i] == ')':
                inner_parentheses_close = i
                break
        if (inner_parentheses_open == -1) and (inner_parentheses_close == -1): return processing_list
        inner_parentheses_content = processing_list[inner_parentheses_open + 1:inner_parentheses_close]
        print(inner_parentheses_content)
        if len(inner_parentheses_content) == 0: raise Exception("RE2NFA[findInnerParenthesesContent]: inner_parentheses_content is empty near ->\n" + "".join(processing_list) + "\ninner_parentheses_open at index: " + str(inner_parentheses_open) + "\ninner_parentheses_close at index: " + str(inner_parentheses_close))
        if len(inner_parentheses_content) == 1: 
            processing_list.pop(inner_parentheses_close)
            processing_list.pop(inner_parentheses_open)
            print(processing_list)
            return self.resolveParentheses(processing_list)
        resolved_inner_parentheses_content = [self.resolveByOrder(inner_parentheses_content)]
        print("RE2NFA[Operation][resolveParentheses]: found a parenthese to resolve->", resolved_inner_parentheses_content)
        return self.resolveParentheses(processing_list[:inner_parentheses_open + 1] + resolved_inner_parentheses_content + processing_list[inner_parentheses_close:])
        

    def process(self, re: str = None):
        if re == None: re = self.RE
        else: self.setRE(re)
        
        last_NFA = None
        
        processing_list = self.resolveParentheses(self.RE)
        processing_list = self.resolveByOrder(processing_list)
        return processing_list

    def setRE(self, re: str):
        # remove all spaces from re
        re = re.replace(' ', '')
        re = re.replace('.', '')
        # turn re into a list, so we can iterate over it and store NFA_objects
        self.RE = list(re)