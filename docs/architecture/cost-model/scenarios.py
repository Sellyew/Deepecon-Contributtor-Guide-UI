"""Scenario table for 10 / 50 / 200 contributions (planning estimates, not quotes).

Human effort is reported in hours; convert with your institution's fully loaded rates.
Inference uses inference_model.py (Anthropic list prices, cached 2026-10-06).
"""
from inference_model import SCENARIOS, cost

# Assumptions (central value, low, high) -- all [U]: to be calibrated in the pilot.
TASKS_PER_CONTRIBUTION = (1.0, 0.5, 1.5)      # admitted tasks per contribution (many candidates fail)
SHEPHERD_HOURS_PER_TASK = (20, 10, 40)        # Good Benchmarks §10 reports >40 h for hard tasks
REVIEWER_HOURS_PER_TASK = (8, 4, 12)          # two independent reviewers x 2-6 h
SUPPORT_HOURS_A = (0.5, 0.25, 1.0)            # per contributor, hosted platform
SUPPORT_HOURS_B = (1.0, 0.5, 2.0)             # per contributor, local plugin (environment heterogeneity)

def triple(n, per):
    c, lo, hi = per
    return n * c, n * lo, n * hi

if __name__ == "__main__":
    print(f"{'N':>4} | {'inference $ (central [low-high])':>34} | {'shepherd h':>22} | {'reviewer h':>20} | {'support h A':>17} | {'support h B':>17}")
    for n in (10, 50, 200):
        inf = [cost('opus-5.5', SCENARIOS[k])[0] * n for k in ('central', 'low', 'high')]
        tasks = triple(n, TASKS_PER_CONTRIBUTION)
        sh = (tasks[0] * SHEPHERD_HOURS_PER_TASK[0], tasks[1] * SHEPHERD_HOURS_PER_TASK[1], tasks[2] * SHEPHERD_HOURS_PER_TASK[2])
        rv = (tasks[0] * REVIEWER_HOURS_PER_TASK[0], tasks[1] * REVIEWER_HOURS_PER_TASK[1], tasks[2] * REVIEWER_HOURS_PER_TASK[2])
        sa = triple(n, SUPPORT_HOURS_A)
        sb = triple(n, SUPPORT_HOURS_B)
        f = lambda t: f"{t[0]:,.0f} [{t[1]:,.0f}-{t[2]:,.0f}]"
        print(f"{n:>4} | ${inf[0]:>9,.0f} [${inf[1]:,.0f}-${inf[2]:,.0f}]{'':>9} | {f(sh):>22} | {f(rv):>20} | {f(sa):>17} | {f(sb):>17}")
