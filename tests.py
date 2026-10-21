import math
import yymembranes as y


def test_wrap_range():
    for a in (-10, -math.pi, 0, math.pi, 3 * math.pi, 7.5):
        w = y.wrap(a)
        assert -math.pi < w <= math.pi
        assert abs(math.cos(w) - math.cos(a)) < 1e-9


def test_patterns_conjugate():
    for k in range(y.N):
        assert abs(y.wrap(y.pat_yin(k, 5) + y.pat_yang(k, 5))) < 1e-9


def test_overlap_perfect_and_random():
    P = [y.pat_yin(k, 0) for k in range(y.N)]
    assert abs(y.overlap(P, P) - 1) < 1e-12
    shifted = [p + 0.7 for p in P]
    assert abs(y.overlap(shifted, P) - 1) < 1e-12  # global phase invariant


def test_drive_zero_mask():
    assert y.drive([0.0] * 4, [0.0] * 4, [0] * 4) == (0.0, 0.0)


def test_determinism():
    assert y.joint_overlap(7, 0.45, False, 20, 30) == y.joint_overlap(7, 0.45, False, 20, 30)


def test_kappa_zero_decouples():
    # with kappa=0 yin's trajectory does not depend on yang's state
    a, b = y.Loop(3, 0.0), y.Loop(3, 0.0)
    b.psi = [0.0] * y.N  # perturb yang only (no rng draw)
    for _ in range(10):
        a.tick(); b.tick()
    assert a.phi == b.phi


def test_destroy_scrambles_yang():
    L = y.Loop(7, 0.45)
    for _ in range(100):
        L.tick()
    L.destroy_yang()
    assert L.overlaps()[1] < 0.5


def test_damage_masks_complementary():
    L = y.Loop(1, 0.45, damage=True)
    assert all(a + b == 1 for a, b in zip(L.mask_yin, L.mask_yang))


def test_solo_locks_intact():
    j, _, _ = y.joint_overlap(7, 0.0, False, 100, 100)
    assert j > 0.8


if __name__ == "__main__":
    n = 0
    for name, f in sorted(globals().items()):
        if name.startswith("test_"):
            f(); print("PASS", name); n += 1
    print("all tests passed (%d)" % n)
