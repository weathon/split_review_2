Now let me write the final consolidated review.

## Summary

This paper identifies and addresses the problem of high gradient variance when applying preference optimization (e.g., DPO) to Large Reasoning Models (LRMs) that generate intermediate reasoning traces before final answers. The authors propose Bias–Variance Optimized Preference Optimization (BVPO), which mixes the standard high-variance trace-based gradient with a low-variance "empty-trace" gradient (obtained by suppressing trace generation via `