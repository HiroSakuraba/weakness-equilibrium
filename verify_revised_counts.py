from itertools import product
from fractions import Fraction

# Cell state = (retained measure m, binding-correctness bit a).
STATES = [(0,0),(1,0),(2,0),(1,1),(2,1)]
SUPPORTS = [(0,), (1,), (0,1)]


def strong_leq(A, B):
    """Strong set order on nonempty subsets of the chain 0<1."""
    return all(min(a,b) in A and max(a,b) in B for a in A for b in B)


def uniform_correct(a1, a2):
    p1 = any(all(a1[r][c] for c in (0,1)) for r in (0,1))
    p2 = any(all(a2[r][c] for r in (0,1)) for c in (0,1))
    return p1 and p2


def support_domain_has_solution(supp, relation):
    """Does x in the probability domain determined by supp satisfy A*x+B rel 0?"""
    rel, A, B = relation
    if supp == (0,):
        x = Fraction(1)
        v = A*x + B
        return {'ge': v >= 0, 'le': v <= 0, 'eq': v == 0}[rel]
    if supp == (1,):
        x = Fraction(0)
        v = A*x + B
        return {'ge': v >= 0, 'le': v <= 0, 'eq': v == 0}[rel]

    # Full support means x is strictly inside (0,1).
    if rel == 'eq':
        if A == 0:
            return B == 0
        root = -Fraction(B, A)
        return 0 < root < 1
    if A == 0:
        return B >= 0 if rel == 'ge' else B <= 0

    root = -Fraction(B, A)
    if rel == 'ge':
        return max(B, A+B) > 0 or 0 < root < 1
    return min(B, A+B) < 0 or 0 < root < 1


def has_exact_equilibrium(m1, a1, m2, a2):
    """Exact support enumeration for a 2x2 alpha=1 weakness game."""
    for row_supp in SUPPORTS:
        for col_supp in SUPPORTS:
            T1 = [r for r in (0,1) if all(a1[r][c] for c in col_supp)]
            T2 = [c for c in (0,1) if all(a2[r][c] for r in row_supp)]
            if not set(row_supp).issubset(T1) or not set(col_supp).issubset(T2):
                continue

            # D1(q) = payoff(row0)-payoff(row1) = A1*q+B1.
            d10 = m1[0][0] - m1[1][0]
            d11 = m1[0][1] - m1[1][1]
            A1, B1 = d10-d11, d11
            if len(T1) == 1:
                if row_supp != (T1[0],):
                    continue
                cond1 = ('eq', 0, 0)
            elif row_supp == (0,):
                cond1 = ('ge', A1, B1)
            elif row_supp == (1,):
                cond1 = ('le', A1, B1)
            else:
                cond1 = ('eq', A1, B1)

            # D2(p) = payoff(col0)-payoff(col1) = A2*p+B2.
            d20 = m2[0][0] - m2[0][1]
            d21 = m2[1][0] - m2[1][1]
            A2, B2 = d20-d21, d21
            if len(T2) == 1:
                if col_supp != (T2[0],):
                    continue
                cond2 = ('eq', 0, 0)
            elif col_supp == (0,):
                cond2 = ('ge', A2, B2)
            elif col_supp == (1,):
                cond2 = ('le', A2, B2)
            else:
                cond2 = ('eq', A2, B2)

            if (support_domain_has_solution(col_supp, cond1)
                    and support_domain_has_solution(row_supp, cond2)):
                return True
    return False


def main():
    counts = dict(uniform=0, fail=0, inc=0, inc_fail=0,
                  asc=0, asc_fail=0, both=0, both_fail=0)

    for vals in product(STATES, repeat=8):
        v1, v2 = vals[:4], vals[4:]
        # Cell order: (0,0),(0,1),(1,0),(1,1).
        m1 = [[v1[0][0],v1[1][0]],[v1[2][0],v1[3][0]]]
        a1 = [[v1[0][1],v1[1][1]],[v1[2][1],v1[3][1]]]
        m2 = [[v2[0][0],v2[1][0]],[v2[2][0],v2[3][0]]]
        a2 = [[v2[0][1],v2[1][1]],[v2[2][1],v2[3][1]]]

        if not uniform_correct(a1, a2):
            continue
        counts['uniform'] += 1
        eq = has_exact_equilibrium(m1, a1, m2, a2)
        counts['fail'] += int(not eq)

        increasing = (
            m1[1][1]-m1[0][1] >= m1[1][0]-m1[0][0]
            and m2[1][1]-m2[1][0] >= m2[0][1]-m2[0][0]
        )
        T10 = {r for r in (0,1) if a1[r][0]}
        T11 = {r for r in (0,1) if a1[r][1]}
        T20 = {c for c in (0,1) if a2[0][c]}
        T21 = {c for c in (0,1) if a2[1][c]}
        ascending = strong_leq(T10, T11) and strong_leq(T20, T21)

        if increasing:
            counts['inc'] += 1
            counts['inc_fail'] += int(not eq)
        if ascending:
            counts['asc'] += 1
            counts['asc_fail'] += int(not eq)
        if increasing and ascending:
            counts['both'] += 1
            counts['both_fail'] += int(not eq)

    expected = {
        'uniform': 33856, 'fail': 336,
        'inc': 14161, 'inc_fail': 52,
        'asc': 18496, 'asc_fail': 24,
        'both': 9025, 'both_fail': 0,
    }
    print(counts)
    assert counts == expected, (counts, expected)
    print('All revised enumeration counts verified exactly.')


if __name__ == '__main__':
    main()
