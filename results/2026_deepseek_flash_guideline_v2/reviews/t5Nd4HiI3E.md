I've confirmed the calibration corpus is inaccessible. I'll proceed with my best judgment calibrated against known ICLR standards.

---

## Summary

This paper studies preference optimization for Large Reasoning Models (LRMs), where the statistically correct marginal objective (summing over all possible reasoning traces) is intractable and practical single-trace surrogates introduce high gradient variance. The authors propose BVPO, which mixes a trace-based gradient estimator \(g_t\) with an "empty-trace" estimator \(g_e\) (obtained by disabling trace generation via `"