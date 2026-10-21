# DESIGN: Yin-Yang Membranes

## Source
A faithful port of the Loop view's `tick()` in sparkainlp-x/holographic-thoughts `index.html`: same constants (n 48, ω 0.06, α 0.30, λ 0.25, σ 0.30, γ 1.0), same mask-weighted drive, same 3-tap same-parity deviation smoothing, same trust terms (drive magnitude² × partner stability), same yang prediction (yin advanced by one global velocity step and read through yang's mask), and the same uniform-random destruction. `wrap` copies `wrapA`, with JS `%` as `math.fmod`. The only change is the RNG: seeded `random.Random` instead of `Math.random`, so runs are reproducible.

## Protocol
- **Alone** means κ = 0. Each ring is then driven only by its own pattern; a test proves yin is independent of yang.
- **Joint overlap:** 200 burn-in ticks, then the mean of (yin + yang)/2 over 1000 ticks.
- **Resurrection:** 200 burn-in ticks, destroy yang, then count ticks to the first of 5 consecutive ticks with yang overlap > 0.6 (the page's "locking again" cutoff). Cap 1000.
- **Damage:** the page's complementary amnesia. Yin keeps even k and yang keeps odd k in their own drive.

## Finding
Coupling at the page default (κ = 0.45) hurts. Joint overlap falls from 0.904 to about 0.78 intact and from about 0.72 to about 0.45 damaged, on all three seeds. Intact rings recover from destruction in 2–4 ticks on their own, so the loop isn't needed for resurrection. Under amnesia, coupling slowed recovery. A plausible mechanism, not proven here: the cross term pulls each ring toward the partner's noisy shape error, which adds noise once the ring's own drive already locks it. On seed 7, weak coupling (0.15) helped under amnesia (0.812 vs 0.724). That one data point suggests a window worth sweeping across seeds; it is not a claim.

## Limits
One parameter set, three seeds, one destruction per seed, toy scale. The browser runs at an unseeded frame rate, so its live readout will differ from these numbers.
