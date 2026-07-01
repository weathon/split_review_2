Now I have a solid calibration. Let me construct the final review.

## Summary

The paper addresses the alignment of Large Reasoning Models (LRMs) that generate intermediate reasoning traces. It identifies that standard preference optimization applied to LRMs suffers from high gradient variance introduced by stochastic trace sampling, since the correct marginal objective requires summing over all traces and is intractable. The authors propose BVPO, which mixes a high-variance trace-based gradient with a low-variance "empty-trace" gradient (obtained by disabling trace generation) via a convex combination. Theoretical analysis shows variance reduction, MSE-optimal mixing, and tighter SGD convergence bounds. Empirically, BVPO outperforms DPO and SimPO on AlpacaEval 2 and Arena-Hard across three model sizes (1.5B, 7B, 8B) by up to 7.8 and 6.8 points respectively.

## Strengths

1. **Novel and timely problem framing.** The paper is the first to systematically identify and formalize the trace-sampling-induced gradient variance problem in LRM alignment. Section 3.2 clearly contrasts the intractable marginal objective $\mathcal{L}_m$ with the practical trace-based proxy $\mathcal{L}_t$, articulating a gap that prior alignment work on conventional LLMs does not face.

2. **Simple, practical method.** BVPO requires only appending `