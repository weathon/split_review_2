Now I have all the information needed. Let me write the final consolidated review.

## Summary

This paper introduces TNT, a two-stage training framework for deep memory modules (e.g., Titans, TTT). Stage 1 uses a hierarchical memory architecture — a global module processing large, hardware-friendly chunks for long-range context, and parallel local modules with periodic state resets that break sequential dependencies to enable context parallelism. Stage 2 is a brief fine-tuning phase that adapts local modules to smaller chunk sizes for optimal inference. The paper demonstrates up to 17× training speedup over baseline Titans while maintaining or improving quality at 150M parameter scale trained on 10B tokens.

## Strengths

1. **Periodic reset of local memory states is a clean, practical contribution.** Non-linear recurrences in deep memory modules have been hard to parallelize because each state depends on its predecessor. Resetting local memory to a learned initial state at regular intervals (Eq. 6, Section 4.1.1) breaks this dependency and enables context parallelism. The speedup is verified empirically: at C_L={8}, TNT trains 7.68× faster than the Titans baseline (C=8) (Table 1), which is directly attributable to the parallelism enabled by the reset mechanism.

2. **Substantial and well-measured speedups.** The paper reports up to 17.37× time-to-quality improvement (Table 1), 5.1× faster single-step runtime at 32K sequence length (Figure 4), and linear scaling with sequence length versus quadratic for standard attention. These numbers are concrete, practically meaningful, and honestly contextualized (the paper acknowledges TNT does not yet match FlashAttention-optimized Transformers for all configurations).

3. **Two-stage decoupling of training efficiency from inference performance is well-motivated.** Challenge 3 (Figure 2) convincingly shows that a model trained with chunk size C performs optimally only at C at inference. The idea of using large chunks for pre-training and then briefly fine-tuning at smaller chunks is sensible, and Stage 2 requires only 5% additional compute.

4. **Ablation studies validate key design choices.** Removing global memory (PPL increases from 21.04 to 25.60), removing Q-K Projection (21.04 → 22.01), and the incremental benefit of adding multiple local modules (23.53 → 20.15) are all cleanly demonstrated in Table 3.

## Weaknesses

### Fatal
None.

### Major

1. **Central framing conflates an architectural change with a "training paradigm," and the controlled experiment to disentangle them is missing.** The paper states "TNT is a general training paradigm applicable to any deep memory module rather than a specific architecture" (Section 4). But the hierarchical memory with global + N parallel local modules and periodic resets is an architectural modification — the resulting model processes information through different pathways than a single-memory Titans model. The experiments compare TNT's hierarchical architecture against Titans' single-memory architecture. A controlled experiment is absent: apply the same two-stage training approach (large-chunk pre-training → small-chunk fine-tuning) to a non-hierarchical deep memory module. Without this, it is unclear whether the quality improvements (e.g., PPL 23.13 vs. 25.07) come from the architectural change, the two-stage training, or both. The paper's empirical contributions (speedup, quality) are real regardless, but the framing needs to be adjusted to match what is actually demonstrated. This is the most significant weakness and the authors should address it by either adding the controlled experiment or clearly reframing TNT as an architectural contribution with an associated training procedure.

2. **No statistical uncertainty reported anywhere, despite fine-grained comparisons.** No error bars, confidence intervals, or significance tests are reported for any result in Table 2 or Table 3. The Stage 2 fine-tuning improvement in average perplexity is 23.13 → 23.09 (Table 2) — a difference of 0.04. Without variance estimates, the reader cannot assess whether this is a real improvement or run-to-run noise. The paper acknowledges "downstream task accuracy can be subject to higher variance" (Section 5.3) but does not report variance for perplexity either. While single-run evaluation is common at this training scale, the Stage 2 claim specifically requires statistical support.

### Minor

3. **Q-K Projection does not compute what the paper claims it computes.** The paper states: "projecting the query q_t onto the subspace spanned by previously observed keys" (Section 4.1.2). The formula in Eq. 7 computes Σ_τ (k_τ k_τ^⊤ / ‖k_τ‖²) q_t, which is the *sum of individual rank-1 projections* of q onto each key direction — not the orthogonal projection onto the joint subspace spanned by all keys (which would require K(K^⊤K)⁺K^⊤). Unless the keys are orthonormal (which they generally are not), these differ. The operation is closer to a linear attention mechanism. This mathematical imprecision should be corrected: either characterize it as an approximation/heuristic, or correct the formula to a true orthogonal projection. The ablation (Table 3) confirms the component is empirically valuable (PPL 21.04 → 22.01 when removed), so this is a description issue, not a validity issue.

4. **Abstract overstates experimental scope.** The abstract states "Evaluated on Titans and TTT models," but TTT only appears as a baseline (Table 2, PPL 27.62). TNT is instantiated on Titans only. The paper should either add TNT-on-TTT results or correct the abstract.

### Trivial

5. **No analysis of what the periodic reset costs in modeling capacity.** The local memory window S_L = 2048 means the fine-grained memory cannot capture dependencies across reset boundaries. The global memory (C_G = 2048) compensates, but whether this coarse resolution preserves long-range dependencies as well as a full fine-grained memory is not analyzed.

6. **"Q-K Projection" naming is imprecise.** Since the operation is not a true orthogonal projection, "key-weighted query remapping" or similar would be more accurate.

## Nice-to-Haves

- A controlled experiment applying Stage 2 fine-tuning to a standard (non-hierarchical) Titans model would strengthen the claim that TNT is a general training paradigm rather than tied to the specific architecture.
- Reporting variances (even a brief "results averaged over 3 seeds, std ≤ X") would substantially increase credibility, particularly for the Stage 2 improvements.
- Wall-clock time for Stage 2 fine-tuning would help contextualize the "5% of pre-training compute" claim.

## Removed Points

These points were flagged by reviewers but are removed with justification:

- **"No evaluation on TTT despite abstract claiming so"** — This is kept as a Minor weakness (see weakness #4 above). The reviewer's version overstated the severity; the abstract discrepancy is real but minor.
- **"The speedup comparisons face the same issue [as the framing issue]" (Issue 1 second paragraph)** — The speedup comparison in Table 1 compares TNT vs. Titans at the same chunk size (C_L={8} vs C=8 gives 7.68×). The speedup is primarily attributable to the parallelism enabled by the reset mechanism, which is the paper's core contribution. This is a fair comparison, not an uninterpretable one.
- **"Challenge 2 (domain mismatch)" as a weakness** — The harsh critic actually praised this as a genuine insight. Not a weakness.
- **Stage 2 gain marginality merged into the statistical uncertainty weakness** — The 0.04 PPL gain is small, but without error bars the extent of the concern is unclear. This is now properly covered under weakness #2 (no statistical uncertainty).
- **"Section 4.1.1 doesn't discuss what is lost by resetting"** — Kept as trivial weakness #5.
- **"Table 1 17× should be contextualized"** — The paper does contextualize this: it also reports 7.68× at equal chunk size. This is reasonable presentation.

## Novel Insights

None beyond the paper's own contributions. The reviewer analysis confirmed the core contributions (periodic resets for parallelism, hierarchical memory design) are novel and the speedup numbers are substantial. The primary novel insight from the review process is the identification of the framing mismatch between "training paradigm" and actual architectural changes, which the authors should resolve.

## Suggestions

1. **Reframe the contribution.** Either add a controlled experiment where two-stage training is applied to a non-hierarchical deep memory module, or clearly present TNT as an architectural contribution (hierarchical memory with periodic resets + associated two-stage training procedure) rather than a "general training paradigm." The latter framing is more honest to what the paper demonstrates and still constitutes a strong contribution.

2. **Correct the Q-K Projection description.** Acknowledge that Eq. 7 computes a sum of individual rank-1 projections rather than a true orthogonal projection, and explain why this heuristic is effective (or replace it with the correct formulation).

3. **Report variances for key results.** Even a concise statement like "results averaged over 3 seeds with standard deviations ≤ 0.1 for perplexity" would significantly improve credibility.

4. **Adjust the abstract** to accurately reflect the experimental scope (TNT instantiated on Titans; TTT used as baseline only).

5. **Analyze the tradeoff introduced by periodic resets.** Report how varying S_L (local memory window) affects both quality and speed, to give practitioners a clear understanding of the cost.

## Score and Decision

**Round 1 bracket:** 5.5–7.0 (based on initial comparison with anchors)

**Calibration anchors (all rounds):**
- *Parallelizing non-linear sequential models* (6.0, Accept) — parallelization of non-linear RNNs via fixed-point iteration; comparable contribution, similar evaluation rigor, accepted.
- *FlashRNN* (6.5, Accept) — hardware-optimized kernels for traditional RNNs; focused on low-level optimization rather than architectural innovation.
- *MELODI* (6.25, Accept) — hierarchical memory compression for long contexts; similar hierarchical design, accepted with comparable scrutiny.
- *Memory Mosaics* (6.25, Accept) — novel associative memory architecture; mixed reviews (3, 8, 8, 6) but accepted on strength of core idea.
- *Were RNNs All We Needed?* (5.0, Reject) — simplified RNNs for parallel training; weaker evaluation, rejected despite similar topic.
- *Retentive Network* (4.75, Reject) — chunkwise recurrent training; strong results but novelty concerns led to rejection.

The TNT paper is clearly stronger than the reject-range anchors (Were RNNs, RetNet) — it has better-grounded novelty (periodic resets are genuinely new) and more thorough evaluation (10B tokens, multiple benchmarks, ablations). It is comparable to the accept-range anchors (6.0–6.5), with a similar balance of a solid core contribution and some presentation/evidential weaknesses. The framing issue is the primary weakness that prevents a higher score.

**Final score: 6.0**

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>