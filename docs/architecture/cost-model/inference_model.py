"""Per-contribution LLM inference cost model (planning estimate).
Prices: Anthropic first-party list prices per million tokens: Opus 5.5 from the API reference (cached 2026-10-06), confirmed
on the pricing page on 2026-11-05 (evidence note R3); Sonnet 5.5 cache read per the pricing page (R3).
Cache: reads at the model's cache-read price; writes 1.25x base input (5-min TTL) or 2x (1-hour TTL).
"""
PRICES = {  # $ per million tokens
    "opus-5.5":   {"in": 4.00, "out": 20.00, "cache_read": 0.20},
    "sonnet-5.5": {"in": 2.00, "out": 10.00, "cache_read": 0.10},  # Anthropic pricing page read 2026-11-05 (R3); the 2026-10-06 API-reference cache listed $0.20
}
SCENARIOS = {
    # interview turns, avg cached prefix per turn, new tokens written per turn, output per turn (incl. thinking),
    # session (re)starts needing a full prefix write, agentic work (input tokens, output tokens, cached share),
    # pre-reading (input, output), fresh-context verification calls (n, input each, output each)
    "low":     dict(turns=60,  prefix=60_000,  write=2_000, out=1_000, restarts=2, ag_in=500_000,   ag_out=50_000,  ag_cached=0.90, pre_in=80_000,  pre_out=10_000, ver_n=5,  ver_in=15_000, ver_out=1_500),
    "central": dict(turns=100, prefix=100_000, write=3_000, out=2_000, restarts=3, ag_in=1_500_000, ag_out=150_000, ag_cached=0.90, pre_in=150_000, pre_out=20_000, ver_n=10, ver_in=20_000, ver_out=2_000),
    "high":    dict(turns=160, prefix=180_000, write=4_000, out=4_000, restarts=5, ag_in=4_000_000, ag_out=400_000, ag_cached=0.90, pre_in=250_000, pre_out=30_000, ver_n=20, ver_in=25_000, ver_out=2_500),
}
M = 1_000_000

def cost(model, s, caching=True):
    p = PRICES[model]
    out_cost = (s["turns"] * s["out"] + s["ag_out"] + s["pre_out"] + s["ver_n"] * s["ver_out"]) * p["out"] / M
    if caching:
        interview_in = s["turns"] * (s["prefix"] * p["cache_read"] + s["write"] * p["in"] * 2.0) / M  # 1-hour TTL writes
        restarts = s["restarts"] * s["prefix"] * p["in"] * 2.0 / M
        agentic_in = (s["ag_in"] * s["ag_cached"] * p["cache_read"] + s["ag_in"] * (1 - s["ag_cached"]) * p["in"] * 1.25) / M  # 5-min TTL
    else:
        interview_in = s["turns"] * (s["prefix"] + s["write"]) * p["in"] / M
        restarts = 0.0
        agentic_in = s["ag_in"] * p["in"] / M
    pre_in = s["pre_in"] * p["in"] / M
    ver_in = s["ver_n"] * s["ver_in"] * p["in"] / M
    total_in = interview_in + restarts + agentic_in + pre_in + ver_in
    parts = dict(interview_in=interview_in, restarts=restarts, agentic_in=agentic_in, pre_in=pre_in, ver_in=ver_in, output=out_cost)
    return total_in + out_cost, parts

def cost_without_agentic(model, s):
    """Option A with run kits or staff execution: no in-session agentic execution loops (fairness review, A-advocate #6)."""
    s2 = dict(s, ag_in=0, ag_out=0)
    return cost(model, s2)


if __name__ == "__main__":
    for name, s in SCENARIOS.items():
        c, _ = cost_without_agentic("opus-5.5", s)
        print(f"opus-5.5    {name:8s} without in-session agentic work (A1/staff): ${c:6.2f}")
    print()
    for model in PRICES:
        for name, s in SCENARIOS.items():
            c, parts = cost(model, s)
            u, _ = cost(model, s, caching=False)
            print(f"{model:11s} {name:8s} cached=${c:7.2f}  no-cache=${u:7.2f}  parts=" + ", ".join(f"{k}={v:.2f}" for k, v in parts.items()))
    print()
    for n in (10, 50, 200):
        row = []
        for name in ("low", "central", "high"):
            c, _ = cost("opus-5.5", SCENARIOS[name])
            row.append(f"{name}=${c*n:,.0f}")
        u, _ = cost("opus-5.5", SCENARIOS["high"], caching=False)
        print(f"N={n:3d} contributions, Opus 5.5: " + "  ".join(row) + f"  worst(no-cache,high)=${u*n:,.0f}")
