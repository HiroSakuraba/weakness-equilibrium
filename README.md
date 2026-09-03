# Weakness Equilibrium and the Failure of Exact Correctness

Source for the September 2026 paper by Benjamin John Schulz.

**Repository:** https://github.com/HiroSakuraba/weakness-equilibrium

## Abstract

We study an abstract economy in which each player first has to satisfy a binding correctness requirement and, among the strategies that satisfy it, prefers the strategy retaining the greatest measure of requirements. Under a strict-feasibility condition, equilibrium exists for any threshold α < 1; in particular, this holds for uniformly correct games. At the endpoint α = 1, however, feasibility becomes support-sensitive and equilibrium can fail.

The central phenomenon is narrow: an almost-sure hard constraint can make zero probability qualitatively different from arbitrarily small positive probability.

## Files

- [`weakness_equilibrium_revised.tex`](weakness_equilibrium_revised.tex) — LaTeX source

## Build

```bash
pdflatex weakness_equilibrium_revised.tex
```

A second `pdflatex` pass resolves cross-references.

## Results at a glance

- Existence for every α < 1 under strict feasibility (Theorem 4).
- In a restricted 2×2 class: 33,856 uniformly correct games, 336 with no exact-correctness equilibrium.
- Witness game G*: unique equilibrium p* = 2(1-α), q* = 1/2 for α ∈ (3/4, 1); the limit (0, 1/2) is feasible at α = 1 but is not an equilibrium.
- Correlation under conditional exact admissibility does not repair G*.
- Finite-chain games with increasing differences and ascending exact-feasible correspondences have a pure exact equilibrium (Theorem 13).
