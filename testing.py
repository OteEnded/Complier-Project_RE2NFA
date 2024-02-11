import RE2NFA

# print(RE2NFA.star('a').getData())

# RE2NFA.star('a').printOut()

# RE2NFA.union('a', 'b').drawOut()

# RE2NFA.concatenate('a', 'b').drawOut()

# RE2NFA.star(RE2NFA.concatenate('a', 'b')).drawOut()

# RE2NFA.Operator.star(RE2NFA.Operator.concatenate('a', 'b')).reportOut()

# a_star = RE2NFA.Operator.star('a')
# b_star = RE2NFA.Operator.star('b', a_star)
# # b_star.reportOut()
# RE2NFA.Operator.concatenate(a_star, "b").reportOut()

converter = RE2NFA.Operation()

# print(converter.process('abba*b'))

converter.process('(a|b)*abb').reportOut()


