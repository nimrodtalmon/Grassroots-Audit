#!/usr/bin/env python3
"""Small finite controls for the supplied Calculus (11)/GSC (19) review.

These implement only the displayed operations in the report. They are not
tests of the GLP implementation, a general theorem prover, or a compiler.
Run: python3 calculus/calculus-math-controls-2026-11-25.py
"""
from collections import Counter
from itertools import permutations


def english_to_logic(add, delete, conditions, forbidden, guards):
    return (frozenset(add), frozenset(delete),
            frozenset(conditions) | frozenset(delete),
            frozenset(forbidden), frozenset(guards))


def logic_to_english(clause):
    add, delete, required, forbidden, guards = clause
    return add, delete, required - delete, forbidden, guards


state = ('A', 'token')
t1 = (frozenset(), frozenset({state}), frozenset(), frozenset(), frozenset({'A'}))
t2 = (t1[0], t1[1], frozenset({state}), t1[3], t1[4])
assert t1 != t2
assert english_to_logic(*t1) == english_to_logic(*t2)
assert logic_to_english(english_to_logic(*t2)) == t1
print('ROUND_TRIP: different full texts translate to the same clause; explicit deletion precondition disappears.')


def unguarded_clause_valid(head, body):
    holders = {h for h, _, _ in head | body}
    changed = {h for h, p, sign in head if (h, p, not sign) in body}
    return len(holders) <= 1 or holders <= changed


head = {('A', 'p', True)}
body = {('A', 'p', False), ('A', 'knows(B)', True)}
extra_head = ('B', 'q', True)
extra_body = ('B', 'q', False)
assert unguarded_clause_valid(head, body)
assert unguarded_clause_valid(head | {extra_head}, body | {extra_body})
valid_orders = []
for order in permutations(('head', 'body')):
    h, b = set(head), set(body)
    ok = True
    for op in order:
        (h if op == 'head' else b).add(extra_head if op == 'head' else extra_body)
        ok = ok and unguarded_clause_valid(h, b)
    if ok:
        valid_orders.append(order)
assert valid_orders == []
print('AUGMENTATION: the simultaneous result is valid; neither order of one-literal augmentations is valid.')


# Standard Set(Agent) equality erases the syntactic occurrence of B.
a, b = 'a', 'b'
empty_bag = ('bag', frozenset())
bag_expression = ('bag', frozenset({b}) - frozenset({b}))
assert bag_expression == empty_bag
source = {a: {empty_bag}, b: set()}


def cross_enabled(c):
    return (a in c and b in c and bag_expression in c[a]
            and ('u',) not in c[a] and ('v',) not in c[b])


assert cross_enabled(source)
assert not cross_enabled({a: source[a]})
assert not cross_enabled({b: source[b]})
target = {a: source[a] | {('u',)}, b: source[b] | {('v',)}}
assert all(target[x] != source[x] for x in source)
assert b not in empty_bag[1]
print('ADT_SUPPORT: bag({B} minus {B}) equals bag(empty); its syntactic graph edge supplies no stored record.')
print('CROSS_ENABLEDNESS: the unguarded two-agent act is enabled after independent unary preparation.')


# The collection control is conditional on checking the clause before expansion.
def flag_transaction(participants, c):
    return ({x: c[x] for x in participants},
            {x: c[x] | {'flag'} for x in participants})


c = {a: frozenset({'ready'}), b: frozenset({'ready', 'flag'})}
t_ab = flag_transaction({a, b}, c)
t_a = flag_transaction({a}, c)
closure_a = (dict(c), {**c, **t_a[1]})
assert t_ab == closure_a
assert set(t_a[0]) != set(t_ab[0])
print('COLLECTION_CONDITIONAL: pre-expansion unary checking permits two different participant sets with the same closure transition.')


# GSC Proposition 42 uses multiset production; the literal set analogue does not.
record, flag = ('record', b), ('flag',)
before_set = {record}
after_set = before_set | {record, flag}
assert after_set - before_set == {flag}
before_bag = Counter({record: 1})
after_bag = before_bag + Counter({record: 1, flag: 1})
assert (after_bag - before_bag)[record] == 1
print('WITNESSING: adding an already-held record creates a new multiset occurrence but no new set record.')

print('All six controls passed. No GLP/catalogue/cascade tests were run.')
