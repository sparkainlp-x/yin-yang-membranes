"""Yin-yang membranes: a stdlib-only Python port of the Loop view of
Holographic Thoughts (sparkainlp-x/holographic-thoughts, index.html).

Two rings of n=48 phase oscillators track conjugate traveling waves.
Yin reads yang's *present* shape error; yang reads yin's *predicted
next* state (one global velocity step). Coupling strength kappa.
Synthetic toy, classical simulation.
"""
import math
import random

TWO_PI = 2 * math.pi
N = 48
OMEGA = 0.06
ALPHA, LAMBDA, SIGMA, GAMMA = 0.30, 0.25, 0.30, 1.0


def wrap(a):
    """Fold an angle to (-pi, pi], same as the page's wrapA (JS % = fmod)."""
    a = math.fmod(a, TWO_PI)
    if a > math.pi:
        a -= TWO_PI
    if a <= -math.pi:
        a += TWO_PI
    return a


def pat_yin(k, t, n=N):
    return wrap(TWO_PI * k / n - OMEGA * t)


def pat_yang(k, t, n=N):
    return wrap(-TWO_PI * k / n + OMEGA * t)


def drive(A, P, mask):
    re = im = ws = 0.0
    for k in range(len(A)):
        m = mask[k]
        if m == 0:
            continue
        d = P[k] - A[k]
        re += m * math.cos(d)
        im += m * math.sin(d)
        ws += m
    if ws == 0:
        return 0.0, 0.0
    re /= ws
    im /= ws
    return math.hypot(re, im), math.atan2(im, re)


def deviation(A, P, mask):
    n = len(A)
    mag, ang = drive(A, P, mask)
    dev = [wrap(A[k] - (P[k] + ang)) for k in range(n)]
    sm = [0.0] * n
    for k in range(n):
        sre = sim = ws = 0.0
        for idx, w in (((k - 2) % n, 1), (k, 2), ((k + 2) % n, 1)):
            wg = w * mask[idx]
            sre += wg * math.cos(dev[idx])
            sim += wg * math.sin(dev[idx])
            ws += wg
        sm[k] = math.atan2(sim, sre) if ws > 0 else dev[k]
    return sm, mag, ang


def stability(cur, prev):
    n = len(cur)
    re = sum(math.cos(wrap(c - p)) for c, p in zip(cur, prev)) / n
    im = sum(math.sin(wrap(c - p)) for c, p in zip(cur, prev)) / n
    return math.hypot(re, im)


def overlap(A, P):
    n = len(A)
    re = sum(math.cos(p - a) for a, p in zip(A, P)) / n
    im = sum(math.sin(p - a) for a, p in zip(A, P)) / n
    return math.hypot(re, im)


class Loop:
    """One coupled pair. kappa=0 means each membrane runs alone."""

    def __init__(self, seed, kappa=0.45, damage=False, n=N):
        self.rng = random.Random(seed)
        self.n, self.kappa, self.damage, self.t = n, kappa, damage, 0
        g = self.rng.gauss
        self.phi = [wrap(pat_yin(k, 0, n) + g(0, 1) * 0.35) for k in range(n)]
        self.psi = [wrap(pat_yang(k, 0, n) + g(0, 1) * 0.35) for k in range(n)]
        self.phi_prev, self.psi_prev = self.phi[:], self.psi[:]

    @property
    def mask_yin(self):
        return [1 if (not self.damage or k % 2 == 0) else 0 for k in range(self.n)]

    @property
    def mask_yang(self):
        return [1 if (not self.damage or k % 2 == 1) else 0 for k in range(self.n)]

    def tick(self):
        n, t, g = self.n, self.t, self.rng.gauss
        my, mx = self.mask_yin, self.mask_yang
        Py = [pat_yin(k, t, n) for k in range(n)]
        Qx = [pat_yang(k, t, n) for k in range(n)]
        PyN = [pat_yin(k, t + 1, n) for k in range(n)]
        QxN = [pat_yang(k, t + 1, n) for k in range(n)]
        dY, mY, aY = deviation(self.phi, Py, my)
        dX, mX, aX = deviation(self.psi, Qx, mx)
        vre = sum(math.cos(wrap(a - b)) for a, b in zip(self.phi, self.phi_prev)) / n
        vim = sum(math.sin(wrap(a - b)) for a, b in zip(self.phi, self.phi_prev)) / n
        v = math.atan2(vim, vre)
        pred = [wrap(a + GAMMA * v) for a in self.phi]
        dP, _, _ = deviation(pred, PyN, mx)
        trust_yin = mX * mX * stability(self.psi, self.psi_prev)
        trust_yang = mY * mY * stability(self.phi, self.phi_prev)
        kap = self.kappa
        new_phi, new_psi = [0.0] * n, [0.0] * n
        for j in range(n):
            c = Py[j] - dX[j]
            tx = ALPHA * my[j] * mY * math.cos(Py[j] + aY) + kap * trust_yin * math.cos(c)
            ty = ALPHA * my[j] * mY * math.sin(Py[j] + aY) + kap * trust_yin * math.sin(c)
            new_phi[j] = wrap(self.phi[j] + LAMBDA * wrap(math.atan2(ty, tx) - self.phi[j]) + g(0, 1) * SIGMA)
            c = QxN[j] - dP[j]
            tx = ALPHA * mx[j] * mX * math.cos(Qx[j] + aX) + kap * trust_yang * math.cos(c)
            ty = ALPHA * mx[j] * mX * math.sin(Qx[j] + aX) + kap * trust_yang * math.sin(c)
            new_psi[j] = wrap(self.psi[j] + LAMBDA * wrap(math.atan2(ty, tx) - self.psi[j]) + g(0, 1) * SIGMA)
        self.phi_prev, self.psi_prev = self.phi, self.psi
        self.phi, self.psi = new_phi, new_psi
        self.t += 1
        return self.overlaps()

    def overlaps(self):
        n, t = self.n, self.t
        oy = overlap(self.phi, [pat_yin(k, t, n) for k in range(n)])
        ox = overlap(self.psi, [pat_yang(k, t, n) for k in range(n)])
        return oy, ox

    def destroy_yang(self):
        self.psi = [self.rng.random() * TWO_PI - math.pi for _ in range(self.n)]
        self.psi_prev = self.psi[:]


def joint_overlap(seed, kappa, damage, burn=200, ticks=1000):
    """Mean (yin+yang)/2 overlap over `ticks` after `burn`; also per membrane."""
    L = Loop(seed, kappa, damage)
    for _ in range(burn):
        L.tick()
    sy = sx = 0.0
    for _ in range(ticks):
        oy, ox = L.tick()
        sy += oy
        sx += ox
    return (sy + sx) / (2 * ticks), sy / ticks, sx / ticks


def resurrection_ticks(seed, kappa, damage, burn=200, threshold=0.6, hold=5, cap=1000):
    """Destroy yang after `burn`; ticks until yang overlap > threshold for
    `hold` consecutive ticks (first tick of that run). None if not by `cap`."""
    L = Loop(seed, kappa, damage)
    for _ in range(burn):
        L.tick()
    L.destroy_yang()
    run = 0
    for i in range(1, cap + 1):
        _, ox = L.tick()
        run = run + 1 if ox > threshold else 0
        if run == hold:
            return i - hold + 1
    return None
