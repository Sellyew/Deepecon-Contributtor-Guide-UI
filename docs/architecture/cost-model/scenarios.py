"""Scenario table for 10 / 50 / 200 contributions (planning estimates, not quotes).

Human effort is reported in hours; convert with your institution's fully loaded rates.
Inference uses inference_model.py (Anthropic list prices; see that file for sources).
Ranges combine all low or all high values, so they are crude bounds, not intervals.
Every assumption below is [U]: to be calibrated in the pilot (Deliverable 8, PQ5).
"""
from inference_model import SCENARIOS, cost, cost_without_agentic

# (central, low, high)
TASKS_PER_CONTRIBUTION = (1.0, 0.2, 1.5)        # admitted tasks per contribution; TBS merged 70 of 386 pull requests [S]
SHEPHERD_SCREENING_H_PER_CONTRIBUTION = (10, 5, 20)  # Stages 0-4 on every candidate, including those later dropped
SHEPHERD_H_PER_ADMITTED_TASK = (30, 15, 60)     # Stages 5-8 incl. clean-room witness, hidden variants, ladder L0-L12;
                                                # Good Benchmarks §10: "well over forty hours" for hard tasks [P-full]
REVIEWER_H_PER_TASK = (8, 4, 12)                # domain reviewer + benchmark reviewer
ECONOMIST_H_PER_TASK = (15, 5, 35)              # outside economists: blind SP-1 solves, GT-2 classification, V3 raters, calibration
TRIAL_COMPUTE_USD_PER_TASK = (500, 250, 750)    # validation trials (L8, L10, L11): ~50-150 trials at ~$5 each (methodology review)
STAFF_S5_H_PER_CONTRIBUTION = (4, 2, 6)         # extra shepherd hours per contribution routed to staff execution (A's staff route or B-staff)
SUPPORT_H_A = (0.75, 0.25, 1.5)                 # per contributor: web platform plus run-kit questions
SUPPORT_H_B = (1.0, 0.5, 2.0)                   # per contributor: local installation and environments

# Evaluation inference: regression suite of simulated contributors (interview protocol §15: 5 personas x >= 3 replicates)
SUITE_SIZE = 15
PASSES_PER_YEAR_A = (6, 4, 8)                   # protocol or pinned-model changes
PASSES_PER_YEAR_B = (12, 12, 52)                # certified stable client releases: monthly by default, weekly at most


def triple(n, per):
    c, lo, hi = per
    return n * c, n * lo, n * hi


def per_task(n, per):
    t = triple(n, TASKS_PER_CONTRIBUTION)
    return t[0] * per[0], t[1] * per[1], t[2] * per[2]


def shepherd(n):
    t = triple(n, TASKS_PER_CONTRIBUTION)
    s = SHEPHERD_SCREENING_H_PER_CONTRIBUTION
    a = SHEPHERD_H_PER_ADMITTED_TASK
    return n * s[0] + t[0] * a[0], n * s[1] + t[1] * a[1], n * s[2] + t[2] * a[2]


def suite_cost():
    c = [cost("opus-5.5", SCENARIOS[k])[0] * SUITE_SIZE for k in ("central", "low", "high")]
    return tuple(c)


if __name__ == "__main__":
    f = lambda t, d="": f"{d}{t[0]:,.0f} [{d}{t[1]:,.0f}-{d}{t[2]:,.0f}]"
    print("Per-contribution interview inference, Opus 5.5 (central [low-high]):")
    b = [cost("opus-5.5", SCENARIOS[k])[0] for k in ("central", "low", "high")]
    a = [cost_without_agentic("opus-5.5", SCENARIOS[k])[0] for k in ("central", "low", "high")]
    print(f"  with in-session agentic work (B, A2): ${b[0]:.2f} [${b[1]:.2f}-${b[2]:.2f}]")
    print(f"  without (A1, staff execution):        ${a[0]:.2f} [${a[1]:.2f}-${a[2]:.2f}]")
    print()
    cols = ["N", "tasks", "inference $", "shepherd h", "reviewer h", "economist h", "trial compute $", "staff-S5 h (if all; A staff or B-staff)", "support h A", "support h B"]
    print(" | ".join(cols))
    for n in (10, 50, 200):
        inf = tuple(cost("opus-5.5", SCENARIOS[k])[0] * n for k in ("central", "low", "high"))
        row = [
            f"{n}",
            f(triple(n, TASKS_PER_CONTRIBUTION)),
            f(inf, "$"),
            f(shepherd(n)),
            f(per_task(n, REVIEWER_H_PER_TASK)),
            f(per_task(n, ECONOMIST_H_PER_TASK)),
            f(per_task(n, TRIAL_COMPUTE_USD_PER_TASK), "$"),
            f(triple(n, STAFF_S5_H_PER_CONTRIBUTION)),
            f(triple(n, SUPPORT_H_A)),
            f(triple(n, SUPPORT_H_B)),
        ]
        print(" | ".join(row))
    print()
    s = suite_cost()
    print(f"Evaluation suite pass ({SUITE_SIZE} simulated contributions): ${s[0]:,.0f} [${s[1]:,.0f}-${s[2]:,.0f}]")
    ya = (s[0] * PASSES_PER_YEAR_A[0], s[1] * PASSES_PER_YEAR_A[1], s[2] * PASSES_PER_YEAR_A[2])
    yb = (s[0] * PASSES_PER_YEAR_B[0], s[1] * PASSES_PER_YEAR_B[1], s[2] * PASSES_PER_YEAR_B[2])
    print(f"Evaluation inference per year, A: {f(ya, '$')}  (passes {PASSES_PER_YEAR_A})")
    print(f"Evaluation inference per year, B: {f(yb, '$')}  (passes {PASSES_PER_YEAR_B})")
