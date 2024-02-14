import RE2NFA

# print(RE2NFA.star('a').getData())

# RE2NFA.star('a').printOut()

# RE2NFA.union('a', 'b').drawOut()

# RE2NFA.concatenate('a', 'b').drawOut()

# RE2NFA.star(RE2NFA.concatenate('a', 'b')).drawOut()

# RE2NFA.star(RE2NFA.concatenate('a', 'b')).reportOut()
converter = RE2NFA.Operation()
converter.process('(a|b)*').drawOut()