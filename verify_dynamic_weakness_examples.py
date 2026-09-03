from fractions import Fraction
import math

# 1. Sequential G* checks.
# cell -> (m1,a1,m2,a2)
G = {
    (0,0):(0,0,1,1),
    (0,1):(2,1,0,0),
    (1,0):(1,1,1,1),
    (1,1):(1,1,2,1),
}

# P1 first: P2's exact best response after each row.
def p2_response(row):
    feasible = [c for c in (0,1) if G[(row,c)][3] == 1]
    return max(feasible, key=lambda c:G[(row,c)][2])
responses = {r:p2_response(r) for r in (0,1)}
assert responses == {0:0, 1:1}
# P1 can choose only rows whose induced cell is exact for P1.
feasible_rows = [r for r in (0,1) if G[(r,responses[r])][1] == 1]
assert feasible_rows == [1]
assert (1,responses[1]) == (1,1)

# P2 first: P1's exact best response after each column.
def p1_response(col):
    feasible = [r for r in (0,1) if G[(r,col)][1] == 1]
    return max(feasible, key=lambda r:G[(r,col)][0])
responses2 = {c:p1_response(c) for c in (0,1)}
assert responses2 == {0:1, 1:0}
feasible_cols = [c for c in (0,1) if G[(responses2[c],c)][3] == 1]
assert feasible_cols == [0]
assert (responses2[0],0) == (1,0)

# 2. Stag Hunt constrained branch.
def stag_branch(alpha):
    return (1 + math.sqrt(4*alpha - 3))/2
for alpha in (0.82, 0.9, 0.99, 0.9999):
    p = stag_branch(alpha)
    assert p > 0.75
    assert abs(p*(1-p) - (1-alpha)) < 1e-12
assert abs(stag_branch(0.999999999999) - 1.0) < 2e-6

# 3. Minimum sufficient punishment.
def vc(delta):
    return 3/(1-delta)
def vd(delta,k):
    return 5 + sum(delta**t for t in range(1,k+1)) + delta**(k+1)*3/(1-delta)
def kstar(delta):
    if delta < 0.5:
        return None
    if delta == 0.5:
        return math.inf
    k=0
    while delta**(k+1) > 2*delta - 1:
        k += 1
    return k
assert kstar(0.9) == 2
assert vd(0.9,1) > vc(0.9) and vd(0.9,2) <= vc(0.9)
assert kstar(0.6) == 3
assert vd(0.6,2) > vc(0.6) and vd(0.6,3) <= vc(0.6)
assert kstar(0.5) == math.inf
assert kstar(0.49) is None

# Exact rational spot-check for delta=9/10.
d = Fraction(9,10)
VC = Fraction(3,1)/(1-d)
def VDrat(k):
    return Fraction(5,1) + sum((d**t for t in range(1,k+1)), Fraction(0,1)) + d**(k+1)*Fraction(3,1)/(1-d)
assert VDrat(1) == Fraction(151,5)  # 30.2
assert VDrat(2) == Fraction(1429,50)  # 28.58
assert VC == 30

# 4. Minimal disclosure toy check.
weights = {'contraindication':10, 'genetic_marker':3, 'address':1}
sufficient = [
    {'contraindication'},
    {'contraindication','genetic_marker'},
    {'contraindication','address'},
    {'contraindication','genetic_marker','address'},
]
revealed_weight = lambda D: sum(weights[x] for x in D)
best = min(sufficient, key=revealed_weight)
assert best == {'contraindication'}

print('All dynamic weakness example checks passed.')
print('Sequential G*: P1-first -> (1,1); P2-first -> (1,0)')
print('Stag branch p*(0.99) =', stag_branch(0.99))
print('Punishment k*(0.9) =', kstar(0.9), '; k*(0.6) =', kstar(0.6))
