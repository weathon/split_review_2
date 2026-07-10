Now let me compose the final review.

## Summary

This paper introduces TNT (Two-stage Non-linear Training), a training paradigm for deep memory modules (non-linear RNNs with test-time memorization, e.g., Titans, TTT). TNT proposes a hierarchical memory architecture where multiple parallel local memory modules with periodic state resets handle fine-grained context while a global memory captures long-range dependencies, enabling context parallelism for non-linear recurrences. A two-stage process decouples training efficiency (large chunks, Stage 1) from inference performance (small-chunk fine-tuning, Stage 2), and a Q-K Projection mechanism resolves a domain mismatch between memory compression (key-space) and retrieval (query-space). Experiments on the Titans architecture demonstrate up to 17× training speedups with improved perplexity over baseline Titans.

## Strengths

- **The periodic state reset mechanism (Section 4.1.1, Eq. 6) is a genuinely clever solution to a hard problem**: breaking sequential dependencies in non-linear RNNs to enable context parallelism. The idea of resetting local memory to a shared learned initial state while compensating with a global memory module is simple, well-motivated, and demonstrably effective.

- **The Q-K Projection (Section 4.1.2, Eq. 7) insightfully addresses a subtle but real mismatch**: memory compression optimizes the sub-network in key-space, while retrieval queries in query-space. The running-sum implementation avoids storing all past keys, and the ablation (Table 3) confirms it provides meaningful gains (PPL 22.01 vs 21.04 without it).

- **Speedups at long sequences are real and significant**. Figure 4 shows TNT achieving near-constant runtime (~400–550ms) across 2K–32K sequence lengths, while Titans (C=16) grows from ~400ms to ~4000ms. At 32K, TNT is 5.1× faster than Titans with the same chunk size and 1.3× faster than FlashAttention.

- **The problem is well-motivated** (Section 3): deep memory modules face a genuine scalability bottleneck requiring small chunk sizes (16–64 tokens) for accuracy, leading to 5–10% FLOP utilization. The paper clearly articulates why linear-memory parallelization techniques (parallel scans) do not apply to non-linear recurrences.

## Weaknesses

### Major

- **Overclaimed evaluation scope and generality.** The abstract states "Evaluated on Titans and TTT models," and the paper frames TNT as a "general training paradigm applicable to any deep memory module" (Section 1, line 35). However, **all TNT experiments use only Titans** as the base architecture. TTT appears only as a baseline in Table 2 (PPL 27.62), not as an instantiation of the TNT framework. This discrepancy between the claimed breadth and the actual evidence undermines the paper's central generality claim. At minimum, the abstract should be corrected; ideally, the paper should demonstrate TNT on at least one other deep memory architecture (TTT, Atlas, etc.). *(Favorability: 0.00 — the most significant weakness.)*

### Minor

- **Stage 2 fine-tuning improvements lack statistical support.** Table 2 shows PPL reductions of 0.03–0.11 across configurations (e.g., best configuration: 23.13→23.09). These differences are very small, and the paper reports no variance estimates, error bars, or multiple-seed results anywhere. While Stage 1 results alone are already strong and Stage 2 improvements are directionally consistent, the claim that Stage 2 "consistently lowers" perplexity (line 239) would be significantly strengthened by significance testing or replication. *(Favorability: 0.00 — the model views this as a serious weakness in rigor, though the underlying Stage 1 contribution is unaffected.)*

- **Parameter counts across compared models are not clearly accounted for.** The paper trains "150M parameter models" (line 207), but TNT with N local memory modules adds multiple deep sub-networks (fast weights) beyond the single module in baseline Titans. It is unclear whether total parameter count (slow weights + all fast-weight sub-networks) is held constant across comparisons. The ablation in Table 3 shows perplexity improving monotonically as local modules are added (23.53→20.15), which is consistent with a capacity explanation, but the paper does not discuss this confound. *(Favorability: 0.50)*

- **Q-K Projection computational cost is not analyzed.** The projection mechanism (Eq. 7) maintains a running d×d matrix Σ(kτ kτ^⊤ / ‖kτ‖²), an O(d²) per-chunk operation (for d=768, ~589K elements per local module). The paper describes this as "updated efficiently" (line 166) but provides no FLOP analysis, runtime overhead measurement, or ablation isolating its computational cost. Given that the paper's core motivation is training efficiency, quantifying this overhead would strengthen the analysis. *(Favorability: 0.49)*

- **Headline 17× speedup is selectively aggressive.** The 17× figure (abstract, Table 1) compares the fastest TNT configuration (C_L=64, 1.12 hrs) against the slowest Titans configuration (C=8, 19.48 hrs). The equal-chunksize comparison (TNT C_L=8 vs Titans C=8) gives 7.7× — still a meaningful speedup. The paper does transparently report this number (Section 5.2), but leads with the more aggressive figure in the abstract and conclusion. *(Favorability: 0.51)*

### Trivial

None.

## Nice-to-Haves

- Demonstrate TNT on at least one other deep memory architecture (e.g., TTT or Atlas) to substantiate the generality claim.
- Report variance (e.g., 3–5 seeds with mean±std) for key perplexity results, especially Stage 2 fine-tuning.
- Provide a FLOP utilization analysis or runtime breakdown for the Q-K Projection to quantify its overhead.
- Include an ablation of the reset window hyperparameter S_L (currently fixed at 2048 or 4096 with no study of sensitivity).
- Add inference-time speed benchmarks for models fine-tuned to C′=1 to validate the claimed inference benefit.

## Removed Points

These points from the input review were removed after verification:

- **"No TTT experiment at all"** — Kept but reclassified from "fatal" to "major" (see above). The core method (periodic resets) is architecture-agnostic and the paper frames it as validated on Titans, but the abstract's claim of TTT evaluation is overstepping.
- **"Appendix E was stripped"** — Removed per rule: appendix content is a parser artifact, not an author omission; the generalized formulation exists in the original submission.
- **"Stage 2 {1} has worse PPL than Stage 1 with 4 modules"** — Removed as it compares different configurations (different N of local modules); the valid comparison (Stage 2 {1} vs Stage 1 {8}) shows improvement (24.10→23.99).
- **"Figure 2 uses 550M but experiments use 150M"** — Removed; motivating the problem at larger scale then ablating at smaller scale is standard practice.
- **"Transformer baselines use FlashAttention but TNT uses JAX"** — Removed because the paper explicitly acknowledges this limitation and states it as future work (Section 5.2).
- **Formatting/style nitpicks, missing related works, and speculative concerns** — Removed per rules.

## Novel Insights

None beyond the paper's own contributions. The reviewer feedback confirms the paper's core technical claims (periodic resets enabling context parallelism, Q-K Projection) are sound and the speed results are impressive, while raising valid concerns about evaluation scope and statistical rigor that the authors should address.

## Suggestions

1. **Correct the abstract** to accurately reflect that TNT was validated on the Titans architecture (not on TTT), or add a TTT experiment.
2. **Add multiple-seed experiments** with variance reporting for Stage 2 fine-tuning results.
3. **Clarify parameter accounting** — explicitly state whether total parameter counts are held constant across compared configurations, and if not, discuss the capacity confound.
4. **Include FLOP analysis** or a profiling table showing the computational cost breakdown of TNT components (including Q-K Projection).

## Score and Decision

The paper makes a genuine contribution: the periodic reset mechanism is a simple yet effective solution to a real bottleneck in non-linear RNN training, and the speedup evidence is compelling. The weaknesses are real but addressable — the core claims about context parallelism and training speed are well-supported. The main concern (overclaimed generality on TTT) does not invalidate the method but should be corrected. The Stage 2 rigor concern is notable but the Stage 1 results alone already demonstrate the method's value.

MY FINAL SCORE: 7

MY FINAL DECISION: Accept