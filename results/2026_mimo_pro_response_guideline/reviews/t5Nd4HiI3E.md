Now I have enough calibration data. Let me finalize the review. Here is my synthesis:

---

## Summary

This paper proposes BVPO (Bias-Variance Optimized Preference Optimization) for aligning Large Reasoning Models (LRMs). It identifies trace-induced gradient variance as a systematic bottleneck in applying DPO to LRMs (since the correct marginal objective over all traces is intractable) and addresses it by mixing a high-variance trace-based gradient estimator with a low-variance "empty-trace" estimator obtained by conditioning on an empty reasoning trace. The paper proves variance reduction, MSE-optimality of the convex combination, and tightened SGD convergence bounds. Empirically, BVPO improves alignment over DPO and SimPO on AlpacaEval 2 and Arena-Hard across three model scales, and preserves/improves math reasoning performance.

## Strengths

- **Novel and well-scoped problem formalization**: The paper precisely identifies trace-induced gradient variance as a systematic bottleneck for LRM alignment and provides the first principled treatment of this issue (Section 3.2, Equations 1 and surrounding text). While technical reports mention this in passing, this is the first systematic analysis.

- **Elegant, practical method with minimal overhead**: The empty-trace trick—appending "