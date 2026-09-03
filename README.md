# Weakness games

Companion papers by Benjamin John Schulz, September 2026.

**Repository:** https://github.com/HiroSakuraba/weakness-equilibrium

1. *Weakness Equilibrium and the Failure of Exact Correctness* (static)
2. *Weakest Viable Continuations: Dynamic Weakness in Sequential Games* (dynamic)

The static paper studies simultaneous weakness games: meet a binding correctness requirement, then maximise retained requirement measure. Exact correctness can fail to have an equilibrium. The dynamic paper ranks viable continuations in sequential games and proves pure subgame-perfect existence under recursive viability in finite deterministic perfect-information trees.

## Files

- [`weakness_equilibrium_revised.tex`](weakness_equilibrium_revised.tex) — static paper
- [`weakest_viable_continuations.tex`](weakest_viable_continuations.tex) — dynamic companion
- [`verify_revised_counts.py`](verify_revised_counts.py) — exact-rational verifier for the static 2×2 enumeration
- [`verify_dynamic_weakness_examples.py`](verify_dynamic_weakness_examples.py) — checks sequential \(G^*\), the Stag Hunt branch, punishment lengths, and a disclosure toy

## Build

```bash
pdflatex weakness_equilibrium_revised.tex
pdflatex weakest_viable_continuations.tex
```

A second `pdflatex` pass resolves cross-references.

## Reproduce the checks

```bash
python3 verify_revised_counts.py
python3 verify_dynamic_weakness_examples.py
```

Static enumeration targets:

- 33,856 uniformly correct games, 336 with no exact equilibrium
- 14,161 with increasing differences, 52 failures
- 18,496 with ascending exact-feasible sets, 24 failures
- 9,025 satisfying both conditions, 0 failures

Dynamic example targets:

- sequential \(G^*\): player 1 first gives (1,1); player 2 first gives (1,0)
- Stag Hunt slack branch collapses to (S,S) as \(\alpha \to 1^-\)
- repeated PD with \((T,R,P,S)=(5,3,1,0)\): \(k^*(0.9)=2\), \(k^*(0.6)=3\)
