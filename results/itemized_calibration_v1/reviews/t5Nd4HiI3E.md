## Summary

This paper studies preference optimization for Large Reasoning Models (LRMs), where standard DPO objectives must marginalize over stochastic reasoning traces — intractable in practice. The authors propose BVPO, which mixes a high-variance trace-based gradient (g_t) with a low-variance "empty-trace" gradient (g_e, computed by disabling reasoning trace generation) via convex combination g_c = α·g_t + (1−α)·g_e. The paper provides theoretical analysis (variance reduction, MSE-optimal mixing weight, SGD convergence bounds) and reports empirical gains over DPO and SimPO on AlpacaEval 2 and Arena-Hard across three model scales, alongside improved math reasoning.

## Strengths

1. **Well-motivated and genuinely novel problem.** The paper clearly articulates (Sections 1 and 3.2) why standard DPO is unstable for LRMs: the intractable marginal over reasoning traces forces a single-trace Monte Carlo estimate, producing high-variance gradients. This source of instability is underexplored, with only brief mentions in technical reports (DeepSeek-R1, GPT-o1). The identification of trace-induced gradient variance as a distinct bottleneck is the paper's strongest original contribution.

2. **Clean, simple, practically adoptable method.** BVPO is a drop-in modification requiring no architectural changes — it changes only the gradient estimate (convex combination). The empty-trace estimator is straightforward to implement by appending "