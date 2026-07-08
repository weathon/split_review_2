Now let me finalize my assessment with the calibration analysis.

**Round 1 bracket: 5.5 – 7.5** (based on initial calibration search showing similar efficient-DiT papers in this range)

**Round 2 narrowing: 6.0 – 7.0** (based on comparisons with Qihoo-T2X at 6.40, UniCon at 7.00, LEGO bricks at 6.67)

**Final score placement: 6.5**

The paper's strengths (weights 7.63, 12.59, 9.92, 10.56) are comparable to or exceed those of Qihoo-T2X (6.40 avg, strengths up to 12.90) and UniCon (7.00 avg, strengths up to 9.78). The PAA module's weight of 12.59 is a very strong positive signal — it's as clean as Qihoo's best-rated contribution. The weaknesses are relatively mild: the lowest-weight weakness (-0.15, the baseline comparison ambiguity) is barely negative, unlike Qihoo's -3.87 (incremental novelty) or UniCon's -0.12. However, the paper's evaluation has more tangible reporting gaps (missing baseline fine-tuning clarification, no variance, F1 contradiction in description) than UniCon or Qihoo. On balance, this places it slightly above Qihoo-T2X (6.40) but below UniCon (7.00) due to the evaluation gaps.

Here is the final consolidated review.

## Summary

This paper addresses the computational bottleneck of multi-condition control in Diffusion Transformers (DiTs), where the "concatenate-and-attend" strategy leads to quadratic O(c²n²) attention cost. The authors propose Patch-wise and Keyword-Aware Attention (PKA), which decomposes full attention into two efficient modules — Position-Aligned Attention (PAA) for spatial conditions (O(N) one-to-one attention at aligned positions) and Keyword-Scoped Attention (KSA) for subject conditions (relevance-masked attention with temporal mask reuse) — complemented by a condition KV cache and an early-timestep sampling strategy. The method reports up to 10× inference speedup and 5.12× VRAM reduction on FLUX.1 while claiming maintained or improved generative quality.

## Strengths

1. **Well-motivated problem diagnosis (Section 1, Figures 2–3).** The paper identifies a genuine computational bottleneck in multi-condition DiTs and supports it with empirical analysis showing attention sparsity (diagonal-dominant for spatial conditions, locally activated for subject conditions). This provides a principled basis for the method's design.

2. **Clean, principled design of PAA (Section 3.2.1, Eq. 2).** Position-Aligned Attention is elegant: if the attention matrix is diagonal-dominant for spatial conditions, replace full O(N²) attention with O(N) one-to-one attention at each spatial position. The complexity reduction is well-characterized, and the ablation (Figure 9) confirms efficiency gains over sliding window attention baselines. **[strongest weighted item: 12.59]**

3. **Practical condition KV cache (Section 3.2, Figure 4a).** The insight that condition tokens only need self-attention (enabling one-time KV computation and caching across denoising steps) is a practical engineering contribution correctly motivated by the method's architecture.

4. **Impressive efficiency scaling (Figures 7–8).** The reported 10× speedup and 5.12× VRAM reduction at high condition counts (16 conditions, 1024 tokens each) show a clear growing advantage with more conditions, making the method increasingly attractive for complex multi-condition scenarios.

## Weaknesses

### Major

1. **Unfair or unstated comparison setup in quality evaluation (Table 1).** The paper states "To ensure a fair comparison, we fine-tune the FLUX.1 model using LoRA" but never clarifies whether the baselines (OminiControl2, UniCombine) were also fine-tuned under identical conditions (same LoRA, same data subset, same iterations). If baselines are used in default pretrained form while PKA benefits from task-specific fine-tuning, the quality comparison conflates method advantage with fine-tuning advantage. This is a structural reporting gap that makes the central "quality maintained or improved" claim uninterpretable as currently presented.

2. **Contradiction between claimed controllability and reported F1 score.** On Subject-Canny, UniCombine achieves F1=0.551 vs. PKA at 0.414 — a ~25% relative degradation. The paper dismisses this as "a minor exception of a narrow margin," which is factually inaccurate. While PKA does outperform on most other controllability metrics (e.g., MSE on Subject-Depth by ~49%, Canny-Depth by ~54%), this mischaracterization weakens trust in the paper's quantitative claims.

3. **Efficiency improvements not disentangled across components.** The headline 10× speedup and 5.12× VRAM reduction (Figures 7–8) are the combined effect of PAA, KSA, the condition KV cache, and the condition self-attention-only design. Ablations (Figures 9–10) evaluate PAA and KSA in isolation but do not isolate the KV cache contribution or show what PAA+KSA alone achieve without caching. The attribution of efficiency gains to the novel attention mechanisms vs. the caching optimization is unclear.

### Minor

4. **No variance or significance reported in Table 1.** Every metric is a single number with no standard deviation, confidence interval, or statistical test. For generative evaluation, this limits interpretability of numerical differences.

5. **Missing experimental details for reproducibility.** The paper does not report: training subset size, train/test split ratio, number of denoising steps, image resolution, condition token encoding, or the keyword selection procedure for KSA.

6. **KSA mask computation overhead not quantified.** KSA uses a two-step mechanism: compute mask M^t at timestep t (O(N × |𝕂|) with |𝕂|=1–2), reuse at t+1. For T-step generation, roughly T/2 steps incur this cost. The paper neither reports T nor quantifies this overhead relative to savings, making it hard to assess true end-to-end KSA efficiency.

7. **Initial mask M^0 for KSA is undefined.** KSA reuses M^t from step t at step t+1 (Eqs. 3–4), but step 0 has no prior mask. The paper does not specify how the first step handles subject attention.

8. **Early-timestep sampling lacks quantitative validation.** The evidence (Figure 11) is purely qualitative (one example, no metric). No controlled experiment separates its contribution from PKA's main results.

9. **PAA assumes spatial alignment.** The paper does not discuss what happens when spatial conditions are at different resolutions or aspect ratios from the latent.

10. **Alternative interpretation of perturbation analysis not discussed.** "High-to-Low" perturbations degrading SSIM faster may simply reflect longer error propagation rather than specifically indicating when conditioning is learned.

### Trivial

None.

## Nice-to-Haves

- Include a controlled ablation of PKA with vs. without the condition KV cache to separate caching's contribution from the novel attention mechanisms.
- Provide a controlled quantitative experiment for early-timestep sampling (e.g., convergence curves of a relevant metric with/without it, holding PKA fixed).
- Report variance/confidence intervals for all metrics in Table 1.
- Discuss failure modes: when might PAA's alignment assumption break (different resolutions), and when might KSA's keyword extraction fail?
- Report the number of denoising steps used for inference.

## Removed Points

These points were flagged to be removed from the harsh critic's input; treat them with caution:

1. **"Figures 2–3 not independently accessible"** — Removed. This is a parser/formatting artifact; the original PDF contains these figures.
2. **"FID scores anomalously high (52–80 vs. expected 20–40)"** — Removed as a standalone weakness. The comparison to standard text-to-image FID on COCO is not a valid reference for multi-condition control on a Subject200K subset. The underlying concern about missing calibration context is folded into Minor points 4–5.
3. **"Early-timestep sampling is a standard technique"** — Removed. The paper provides perturbation analysis as motivation; novelty judgment is better addressed by the request for quantitative validation (Minor point 8).
4. **"Related work too thin"** — Removed as scope creep. The paper adequately cites relevant prior work.

## Novel Insights

None beyond the paper's own contributions. The harsh critic's observations about the F1 contradiction and the missing baseline fine-tuning clarification are the most actionable insights not already surfaced by the paper.

## Suggestions

1. Clarify in the evaluation setup whether baselines were fine-tuned under identical conditions. If they were, state this explicitly; if not, either perform the fair comparison or acknowledge the confound and adjust the quality-maintenance claim accordingly.
2. Correct the characterization of the Subject-Canny F1 result — a 25% relative drop is not "a minor exception of a narrow margin."
3. Add an ablation isolating the condition KV cache from PAA+KSA to show how much each component contributes to the reported speedup/VRAM reduction.
4. Report the number of denoising steps and quantify KSA mask computation overhead vs. savings for a full generation run.
5. Add standard deviations or confidence intervals to Table 1.
6. Provide a quantitative ablation of early-timestep sampling (e.g., FID convergence curves with/without it).

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>