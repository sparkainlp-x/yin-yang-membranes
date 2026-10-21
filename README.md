# Yin-Yang Membranes

**Live demo:** [Holographic Thoughts, Loop view](https://sparkainlp-x.github.io/holographic-thoughts/) (interactive browser view; synthetic, classical simulation; measured numbers are in this repo)

**The Python reference model for the Loop view, and the measured finding that at the page's coupling (κ = 0.45) the loop makes both membranes worse.**

Two rings of 48 phase oscillators track conjugate traveling waves. Yin reads yang's *present* shape error; yang reads yin's *predicted next* state (the asymmetric "tic"). This is a line-by-line port of the page's JavaScript (`yymembranes.py`); only the random number generator differs (Python `random.Random(seed)`). Stdlib-only Python. AGPL-3.0-only.

> Synthetic toy simulation; classical software; not physical holography hardware. "Yin" and "yang" are names for the two rings only; no philosophical, spiritual or health claim is made.

## Verified (output of `python demo.py`, seeds 7 / 21 / 42)

Joint overlap = mean of (yin + yang)/2 over ticks 201–1200. Resurrection = ticks after destroying yang until its overlap stays above 0.6 for 5 ticks (cap 1000).

| seed | damage | joint, κ=0.45 | joint, alone (κ=0) | resurrect, κ=0.45 | resurrect, alone |
|---|---|---|---|---|---|
| 7 | no | 0.783 | 0.904 | 2 | 2 |
| 7 | amnesia | 0.456 | 0.724 | 658 | 4 |
| 21 | no | 0.788 | 0.904 | 3 | 3 |
| 21 | amnesia | 0.445 | 0.718 | 58 | 9 |
| 42 | no | 0.778 | 0.904 | 3 | 4 |
| 42 | amnesia | 0.463 | 0.723 | 83 | none by 1000 |

- **Negative result:** at κ = 0.45, coupling lowers joint overlap on every seed, intact (about 0.78 vs 0.90) and damaged (about 0.45 vs 0.72).
- **No resurrection through the loop is needed when intact:** a destroyed yang relocks in 2–4 ticks with or without coupling, from its own drive.
- **Under complementary amnesia, coupling slows resurrection** on all three seeds (58–658 ticks vs 4–9 alone). The one exception is seed 42 alone, which did not recover within 1000 ticks.
- **κ sweep, seed 7 only:** weak coupling (κ = 0.15) under amnesia raised joint overlap to 0.812 vs 0.724 alone. κ ≥ 0.30 collapses it to about 0.45. This is one seed and is not claimed as a general effect.
- 9/9 tests pass.

## Run it

```bash
python tests.py   # 9 tests
python demo.py    # seeds 7 21 42 table + kappa sweep (about 10 s)
```

## Honest limits

Toy scale (n = 48), one parameter set from the page (α 0.30, λ 0.25, σ 0.30, γ 1.0). Resurrection is a single destruction per seed, so those counts are noisy. The κ = 0.15 point is one seed. The 0.6 threshold is the page's own "locking again" cutoff. Earlier page figures (0.84 joint vs 0.70 alone, 14 ticks) were never reproduced by any model and are withdrawn. Details in `DESIGN.md`.

Author: Jean-François Brisson ([ORCID 0009-0000-9778-5374](https://orcid.org/0009-0000-9778-5374)). Licence: AGPL-3.0-only.
