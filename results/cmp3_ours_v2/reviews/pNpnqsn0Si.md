Now I have sufficient calibration context. Let me produce the final review.

## Summary

Thoughtbubbles proposes a transformer variant that learns to dynamically fork and delete residual streams during pretraining, enabling parallel adaptive computation without manual insertion of pause tokens. The method uses learnable cumulative scores to decide which tokens receive additional residual streams, with attention and residual updates attenuated by these scores. Experiments at 150M–772M scales on OpenWebText and peS2o show consistent perplexity improvements over standard transformers and a simple copy-multiple-residuals baseline.

## Strengths

- **A genuinely novel mechanism for adaptive parallel computation.** The idea of forking residual streams based on learned scores, with training signal coming from LM loss alone via attention/residual attenuation, is creative and well-motivated. The paper correctly identifies a gap in the pause-token literature — existing approaches insert computation tokens at fixed positions rather than learning *where* to allocate extra computation — and addresses it directly. This is not an incremental tweak.

- **Consistent perplexity improvements across all settings.** Every Thoughtbubbles variant beats every baseline (standard transformer and both copy baselines) on validation perplexity at every scale (150M, 319M, 772M) and on both datasets. The improvement is meaningful — e.g., 21.22 → 19.74 on OpenWebText at 772M (~7% relative). This consistency is the paper's strongest empirical result and separates it from many adaptive-computation proposals where gains are hit-or-miss.

- **The interpretability analysis (Figure 5) provides a genuine sanity check.** Showing that forking correlates positively with output entropy (for most of the entropy range) demonstrates that the model has learned to allocate computation where uncertainty is high, without any explicit supervision for this behavior. The attention analysis (Figure 4) further confirms that forked tokens substantively influence their parent's computation.

## Weaknesses

### Major

1. **Missing comparison against pause-token baselines.** The paper positions itself as addressing the limitations of pause-token methods (Goyal et al., 2024; Herel & Mikolov, 2024; Sun et al., 2025), which insert computation tokens at fixed positions. Yet none of these are included as baselines. The only parallel-computation baseline is Copy-3/Copy-5 — a "naive model" (Section 3.3) where input residuals are identically copied. The paper's central claim is that *adaptive* allocation beats *uniform* allocation of extra compute, but without comparing against the obvious uniform-allocation baselines from the pause-token literature — methods that are already known to work — the headline results do not demonstrate superiority over the relevant comparison class. This is the single most important gap in the paper.

2. **Imprecise and unsubstantiated FLOPs-matching claim.** Table 1 states that κ=4L is "roughly FLOPs-matched against copy-5 baseline," but no FLOPs numbers are reported anywhere. The two methods have substantially different computational profiles: Thoughtbubbles forks at only 3 layers (before layers 3, 7, 11), while Copy-5 extends sequence length at *every* layer. Without actual FLOPs, the reader cannot evaluate whether the comparison is fair. The paper's framing of "computation-matched" comparisons is weakened by this absence.

3. **Single-run results with no variance estimates.** All numbers in Table 1 come from a single run. For zero-shot evaluations like HellaSwag (differences of 1–2 percentage points) and PIQA (where all methods cluster with no clear trend), single-run results cannot be distinguished from noise. At 2.5B token pretraining with models up to 772M parameters, variance is likely non-trivial. This undermines the claim that Thoughtbubbles outperforms baselines on downstream tasks.

### Minor

4. **Gradient flow through the discrete top-k is acknowledged as a limitation but never explained.** The paper states in Section 8 that the hard top-k blocks gradients for dropped scores ("Top-K Gradient Bottleneck"). However, it never specifies whether any gradient estimator (straight-through, Gumbel-softmax, REINFORCE) is used, or whether training relies solely on the attention/residual-attenuation pathway (Eq. 8–10) for score learning. The mechanism demonstrably works — the scores learn useful behavior — but the exposition is incomplete. The authors should clarify the gradient path concretely.

5. **The "319M outperforms 772M baseline" framing conflates parameter count with compute.** The 319M Thoughtbubbles model uses substantially more computation per token than a standard 319M model (forking up to 4× sequence length at 3 layers). Claiming parameter-level efficiency while consuming more FLOPs is potentially misleading without a FLOPs-matched standard transformer for comparison. The 772M baseline is also substantially undertrained at 2.5B tokens (~3.2 tokens/parameter), making the comparison less informative.

6. **The entropy-computation analysis (Figure 5) lacks support for the hypothesized explanation.** The concave parabolic relationship (fewer forks at highest entropy) is attributed to "edges of clauses or coreferences where computation cannot help," but no examples or quantitative breakdown are provided. This is a plausible hypothesis, but it is presented as a finding without evidence.

7. **Several zero-shot evaluations show weak or inconsistent trends.** On BLiMP, copy baselines outperform Thoughtbubbles in most settings (which the paper acknowledges but does not explain). On PIQA, all methods perform similarly with no clear trend — the "winner" varies by row. These results weaken the downstream-task claims and suggest that the method's benefits are clearest on perplexity and certain tasks (LAMBADA, HellaSwag) but not universally applicable.

### Trivial

None.

## Nice-to-Haves

- Report actual FLOPs for all methods to substantiate the "computation-matched" framing.
- Report multiple seeds (at least 3) for the smaller scales with means and standard deviations.
- Wall-clock training time ratios (even acknowledging raw PyTorch overhead).
- Analyze what distinguishes kept vs. deleted forks at the same position, which would be the strongest test of whether the scores are meaningful.
- Ablate the RoPE partial rotation mechanism to establish whether it is important.

## Removed Points

These points are flagged to be removed, treat them with caution:

- *"The copy baseline is trivially weak because identical copies will attend to each other with near-perfect attention"* — The paper itself describes the baseline as "naive" (Section 3.3), and copies receive different RoPE positions, so this claimed flaw is overstated and not verified.
- *"Circularity concern about score training — scores may reflect which tokens happened to be highly scored at initialization"* — Speculative without supporting evidence; not a concrete identified problem.
- *"Autoregression complexity requires careful tuning"* — The paper already discusses this in Section 5.1 and Appendix E.1.
- *"No wall-clock time measurements"* — The paper acknowledges this in the Limitations section.
- *"BLiMP results show copy baselines outperform Thoughtbubbles"* — The paper already acknowledges this explicitly in the results text.
- *"LAMBADA variance at 150M κ=2L"* — This is raw data visible in the table, not a structural weakness.
- *"PIQA noise"* — Visible in the table; the paper honestly reports it.
- Various formatting and style nitpicks that are parser artifacts, not author errors.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Replace the copy baselines or supplement them with pause-token baselines.** The most important experiment for this paper is to compare against a non-adaptive version of your own architecture (fixed forking positions for all tokens) and/or against the pause-token methods you cite as related work (Goyal et al., Herel & Mikolov). This directly tests your central claim: adaptive allocation beats uniform allocation.

2. **Report FLOPs.** Provide actual FLOPs for all methods (standard transformer, Copy-3/5, Thoughtbubbles κ=2L/4L) so readers can evaluate the "computation-matched" claim.

3. **Report multiple seeds.** At minimum 3 seeds for the smaller scales, with means and standard deviations, to establish that the observed differences are statistically meaningful.

4. **Clarify the gradient flow.** Even a brief statement — "gradients flow only through the attenuation pathway; the top-k selection itself is not differentiated" — would resolve the ambiguity.

5. **Avoid the "lower parameter count beats higher parameter count" framing** without also acknowledging the increased FLOPs used.

---

## Score and Decision

**Round 1 bracket:** After initial review draft and before calibration search, I estimated the paper sits between 4.5 and 5.5 based on comparison with anchors:

| Anchor Paper | Path | Avg Score | Round | Comparison |
|---|---|---|---|---|
| Stutter makes LLMs smarter | UvYrFbKj8j.md | 4.50 | R1 | Similar topic (selective extra compute for hard tokens), rejected. Thoughtbubbles has more novel mechanism and more consistent results. |
| Pause Tokens (Goyal et al.) | ph04CRkPdC.md | 5.50 | R2 | Most directly relevant baseline. Simpler method but more thorough evaluation with multiple seeds and downstream reasoning tasks. Thoughtbubbles is more novel but less rigorously evaluated. |
| CoTFormer | 7igPXQFupX.md | 5.75 | R1 | Similar concerns about baselines and compute-matching. Accepted. Thoughtbubbles is slightly weaker due to no variance reporting and missing relevant baselines. |
| Seq-VCR (pause tokens + regularization) | 30oIfmrcFO.md | 6.25 | R1 | Stronger results on specific reasoning tasks but narrower evaluation. |
| FiRST (router layer skipping) | ulGwcj1egv.md | 3.00 | R2 | Lower quality, different domain. Not directly comparable. |

**Final score:** 5.0. The paper's core idea is genuinely novel and the perplexity results are consistently positive. However, the evaluation has three interlocking weaknesses — missing pause-token baselines, unsubstantiated FLOPs-matching, and single-run results — that collectively prevent the paper from making a fully convincing case. A strengthened version with proper baselines and statistical rigor could be a strong contribution.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>