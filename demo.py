"""Measure the Loop on seeds 7, 21, 42: joint overlap coupled (kappa=0.45,
the page default) vs alone (kappa=0), intact and with complementary
amnesia; ticks to resurrect a destroyed yang; and a kappa sweep."""
import sys
import yymembranes as y

SEEDS = [int(s) for s in sys.argv[1:]] or [7, 21, 42]
KAPPAS = [0.0, 0.15, 0.30, 0.45, 0.60, 0.90]


def fmt(v):
    return " none" if v is None else "%5d" % v


print("joint overlap = mean of (yin+yang)/2 over ticks 201-1200; "
      "resurrection = ticks until yang > 0.6 for 5 ticks (cap 1000)\n")
print("seed  damage   joint@0.45  joint@0   yin@0.45 yang@0.45  yin@0  yang@0   res@0.45 res@0")
for s in SEEDS:
    for d in (False, True):
        jc, yc, xc = y.joint_overlap(s, 0.45, d)
        ja, ya, xa = y.joint_overlap(s, 0.0, d)
        rc = y.resurrection_ticks(s, 0.45, d)
        ra = y.resurrection_ticks(s, 0.0, d)
        print("%4d  %-6s   %8.3f  %8.3f   %8.3f %8.3f  %6.3f %6.3f   %s  %s" % (
            s, "yes" if d else "no", jc, ja, yc, xc, ya, xa, fmt(rc), fmt(ra)))

print("\nkappa sweep, joint overlap (intact | damaged), seed %d" % SEEDS[0])
for k in KAPPAS:
    print("  kappa=%.2f  %.3f | %.3f" % (k, y.joint_overlap(SEEDS[0], k, False)[0],
                                         y.joint_overlap(SEEDS[0], k, True)[0]))
print("\nRESULT: read the table -- coupling is compared against kappa=0, not assumed to help.")
