Now let me finalize my analysis. Let me compile the final review.

## Summary

The paper identifies an important problem—aligning Large Reasoning Models (LRMs) with human preferences is complicated by intractable marginalization over reasoning traces and high gradient variance from single-trace approximations—and proposes BVPO, which mixes a high-variance trace-based gradient with a low-variance "empty-trace" gradient (obtained by disabling reasoning). The paper provides theoretical guarantees (variance reduction, MSE-optimal mixing, tighter SGD bounds) and demonstrates consistent improvements of up to 7.8 points on alignment benchmarks without degrading—and in fact improving—math reasoning performance.

## Strengths

1. **Well-motivated and timely problem.** The paper correctly identifies that applying standard DPO to LRMs requires marginalizing over reasoning traces (intractable), and that single-trace approximations introduce gradient variance that hinders stable alignment. This gap in the literature is genuine (Section 1, Section 3.2).

2. **Simple, elegant, and non-obvious idea.** Exploiting the fact that LRMs can operate in a "no-thinking" mode (via `