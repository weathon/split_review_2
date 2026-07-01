Now I'll produce the final consolidated review.

## Summary

DND introduces a post-training method that retrofits pre-trained LLMs with a lightweight router to identify "hard" tokens and reprocess them through the same transformer layer (a nested pass). The method combines a router controlling loss (score dispersion + distribution preservation) with a dynamic threshold control scheme (buffer proportional control + EMA synchronization). Evaluated on three dense 1B-class models (Qwen3-1.7B, Llama3.2-1B, Gemma3-1B) and a 30B MoE model (Qwen3-30B-A3B), DND achieves consistent gains across 39 task benchmarks with ~6% extra FLOPs and 91.6–93.1% of vanilla throughput.

## Strengths

1. **Well-motivated architecture grounded in prior observations.** The design follows directly from the finding (Gloeckle et al., 2024) that token difficulty is uneven, and connects this to latent-space test-time scaling (Hao et al., 2024; Saunshi et al., 2025). The paper correctly identifies that reprocessing hard tokens through the same transformer layer is a clean instantiation of this principle (Sec. 1).

2. **Principled routing choice.** Token-choice routing is correctly motivated against expert-choice to avoid information leakage in auto-regressive decoding, supported by a clear architectural rationale and citations to Raposo et al. (2024) (Sec. 3.1.1).

3. **Consistent positive results across all tested models and benchmarks.** On Qwen3-1.7B: 11/11 benchmarks improve (avg +1.88); on Llama3.2-1B: 11/11 (+2.61); on Gemma3-1B: 11/11 (+2.50); on Qwen3-30B-A3B: 17/17 (+0.87). The across-the-board positive signal across 39 benchmarks is far more informative than a few cherry-picked wins (Tables 1, 2).

4. **Ablation confirms individual component contributions.** Table 4 disentangles the router controlling loss (+1.01) and threshold control (+1.05), showing each contributes independently and their combination (+1.88) outperforms either alone. Ablations on selection ratio (10%/20%/30%) and layer range further validate the architectural choices.

5. **Token selection analysis provides mechanistic evidence.** Figs. 4a and 4b show a positive correlation (r=0.34) between selection frequency and logit entropy, and a negative correlation (r=-0.58) between selection frequency and entropy change after DND, confirming that the router selects high-uncertainty tokens and the nested pass reduces that uncertainty.

## Weaknesses

### Fatal
None.

### Major

1. **No variance or statistical significance reporting.** Tables 1, 2, and 4 report single numbers without standard deviations, confidence intervals, or multi-seed experiments. Many individual gains on the 30B-A3B model are very small — BBH (+0.13), MATH (+0.15), MATH-500 (+0.20), DROP (+0.27), CMMLU (+0.37) — well within typical evaluation noise for these benchmarks. Without variance estimates, it is impossible to determine which of these small deltas represent real improvements versus measurement noise. The consistent positive direction across 17 benchmarks is suggestive, but the individual gains cannot be properly assessed. This is the paper's most significant evidential gap.

2. **Weak competitor baseline.** The only direct competitor (ITT, Chen et al., 2025) is evaluated on a single model (Qwen3-1.7B, Table 1) and achieves +0.05 average gain — essentially flat. The paper attributes this to a training-inference mismatch from Top-P selection, but does not report ITT hyperparameters or tuning effort, leaving open the possibility ITT was not properly configured for this setting. The closest prior work, MOR (Bae et al., 2025), is discussed at length (Sec. 2.2) but never compared empirically. While the authors give reasonable justification for not comparing to MOR (pretraining from scratch), the paper's core comparison is therefore SFT vs. SFT+DND, leaving the "better than existing post-training methods" claim largely untested.

### Minor

1. **Cost-benefit calibration is underdeveloped.** On the 30B-A3B model, the average gain is +0.87 points at a 7–9% throughput reduction (Table 3). The paper presents these numbers but does not discuss the practical trade-off or scenarios where the cost might or might not be justified. Throughput is measured under a narrow setting (single H100 GPU, single batch), and the 7–9% reduction exceeds the reported ~6% FLOPs increase, suggesting Pack/Unpack overhead that is not discussed.

2. **Training cost of DND relative to standard SFT is not quantified.** DND requires full-scale SFT with all parameters trainable. The additional overhead from the router loss computation, threshold control, and nested forward/backward pass relative to vanilla SFT is not reported in GPU-hours or wall-clock time.

3. **MoE-specific routing interactions are not examined.** For the Qwen3-30B-A3B MoE model, the nested pass routes selected tokens through the same transformer layer, including its MoE router. This could affect expert load balance or utilization patterns; the paper does not analyze this interaction.

4. **Sensitivity to loss-balance hyperparameters not explored.** The router controlling loss combines L_sd (score dispersion) and L_dp (distribution preservation) with weights λ_sd and λ_dp. The ablation (Table 4) tests only presence/absence, not the balance between these terms, despite the conceptual description of a "push-pull" dynamic that depends on proper balancing (Sec. 3.2.1).

5. **Selection ratio in Fig. 7a needs clarification.** The paper states DND is applied only to intermediate layers (Sec. 3.1), yet Fig. 7a reports selection ratios across all 42 layers, with elevated selection in "shallowest and deepest" layers where DND should not be active. The paper should clarify what is being measured in these layers.

6. **Qualitative analysis rests on a single example.** Fig. 7b's interpretation (nouns selected by shallower layers, mathematical expressions by deeper layers) is based on one GPQA example. The paper's language is appropriately cautious, but the generalizability of this hierarchical interpretation is unsubstantiated.

### Trivial

1. **Ambiguous "%" notation in abstract.** The stated gains "1.88%, 2.61%, and 2.50% ... and 0.87%" are absolute percentage-point gains (clear from the Δ rows in tables), but the "%" notation could mislead readers into interpreting them as relative improvements.

## Nice-to-Haves

- Multi-seed experiments (≥3) with mean ± std for the dense models to establish robustness of the reported gains.
- A properly tuned ITT comparison or an adapted MOR-style baseline (e.g., z-loss only routing) to strengthen the competitor comparison.
- GPU-hour breakdown of DND training overhead vs. standard SFT.
- Sensitivity analysis on λ_sd / λ_dp ratio.
- MoE expert utilization analysis comparing vanilla vs. nested pass routing patterns.
- Clarification of the Pack/Unpack overhead causing the gap between 6% FLOPs and 7–9% throughput reduction.

## Removed Points

These points are flagged to be removed; treat them with caution.

- **Threshold control hyperparameters not reported (α, γ, buffer size N_b):** The paper states that detailed hyperparameters are in Appendix Sec. B (line 199), which is stripped by the parser. Per guidelines, criticisms about appendix content that cannot be verified are removed.
- **ITT hyperparameters not reported:** Similarly may be in the stripped appendix.
- **Training GPU-hours not quantified:** May be in the appendix.
- **MOR scale limitation claim:** The paper states MOR "is limited to 1B-parameter" as a factual observation about the published scope of prior work, not a claim about inherent scalability. This is a description of prior work, not an overclaim.
- **Expert-choice routing mismatch lacks empirical demonstration:** The paper provides a theoretical argument backed by citations (Raposo et al., 2024). Requesting empirical validation of this specific point is scope creep beyond what is standard for an architectural design decision.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Add multi-seed experiments (at least 3 runs) for the dense models and report mean ± std. This is the single highest-priority improvement — it would directly address the main evidential weakness.
2. Either tune ITT more carefully and document the setup, or add a controlled ablation using z-loss only routing (mirroring MOR's approach) to strengthen the competitor baseline.
3. Report the GPU-hour overhead of DND training relative to standard SFT to help readers assess cost-effectiveness.
4. Add an analysis of expert utilization patterns in the MoE model with and without DND.
5. Clarify what Fig. 7a measures in non-DND layers.
6. Report the λ_sd and λ_dp values used and discuss sensitivity to their balance.

## Calibration Anchors

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| UvYrFbKj8j.md (Stutter) | 4.50 | 1 | Similar selective-additional-computation approach but on smaller models (Pythia up to 1B) with less consistent results and no MoE scaling. DND is clearly stronger. |
| 7DY2DFDT0T.md (EfficientSkip) | 2.50 | 1 | Significantly weaker: single model, single benchmark, poor presentation. DND is far stronger. |
| diKRhKs5yl.md (FEEDER) | 5.25 | 1 | Different topic (demonstration selection for ICL) but similar score band. DND has more extensive evaluation. |
| 7igPXQFupX.md (CoTFormer) | 5.75 | 2 | Highly related — adaptive token-level depth via repeated processing. DND has more comprehensive evaluation (39 benchmarks, 4 models including 30B MoE) and works as post-training. Comparable overall quality. |
| 6qUUgw9bAZ.md (Learning How Hard to Think) | 6.50 | 1 | Different approach (input-level allocation of decoding compute) but strong execution with clean evaluation. DND is slightly weaker on evidential rigor (variance, baselines). |

**Round 1 bracket**: 5.5–6.5. **Round 2 anchor comparison**: DND compares favorably to Stutter (4.50) and on par with CoTFormer (5.75), but does not match the evidential rigor of the 6.50 anchor. **Final score**: 6.0.

## Score and Decision

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>