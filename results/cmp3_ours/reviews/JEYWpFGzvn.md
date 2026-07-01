Now I have all the information I need. Let me write the final review.

**Calibration bracket reasoning:** The ElasticTok paper (6.00) is the direct baseline — INFOToK presents a more principled method with theoretical grounding, stronger empirical results, and better efficiency. BSQ-ViT (5.75) and "How many tokens is an image worth?" (5.75) are also relevant anchors in the tokenization space. INFOToK is clearly stronger than ElasticTok in both theoretical contribution and empirical performance, so it should score above 6.0. However, the per-token ELBO underspecification and the unsupported 50% claim prevent it from reaching the 8+ tier. Initial bracket: 6.5–7.5. Final: 7.0.

---

## Summary

INFOToK is an adaptive discrete video tokenizer that uses an ELBO-based router to dynamically determine token sequence length per video and a transformer-based adaptive compressor to realize variable-length tokenization. The paper provides theoretical analysis (Theorems 2.2, 3.1) showing that fixed-rate and uniform-adaptive routers are suboptimal, and an ELBO-based router can approach the information-theoretic optimum. Empirically, INFOToK matches Cosmos-DV quality with ~20% fewer tokens and substantially outperforms ElasticTok across multiple metrics and compression levels, while requiring only 1 additional NFE vs. ElasticTok's 11.

## Strengths

1. **Principled theoretical motivation (Section 2.2–2.3).** Theorem 2.2 formally proves that uniform-adaptive routers (as used by ElasticTok) can be arbitrarily suboptimal in expected token length. The four-data example with probabilities {2⁻¹, 2⁻², 2⁻³, 2⁻³} provides clean intuition. This goes beyond the typical purely empirical tokenization literature and is a genuine theoretical contribution.

2. **Clean and efficient router design (Section 3.1).** The ELBO-based router (eq. 4) directly approximates the optimal token length via a quantity the model is already trained to maximize, requiring only one additional decoder pass vs. ElasticTok's 11 NFE binary search (Figure 4g). This is a substantial practical advantage.

3. **Strong empirical results (Table 1, Figure 4).** Against ElasticTok at the same BPP, INFOToK improves PSNR by ~1.6–1.9 dB, reduces LPIPS by ~0.1, and cuts FVD by 40–60%. Against Cosmos-DV (fixed-rate), INFOToK saves ~19% tokens (BPP 0.81 vs 1.00) while matching PSNR (30.08 vs 30.01).

4. **Well-designed oracle ablation (Table 2).** The ELBO-based router achieves within 0.06–0.17 PSNR of an exhaustive search-based "optimal" routing strategy across three compression levels, convincingly validating the theoretical prediction.

5. **Architecture-controlled ablation (Table 3, Right).** Comparing Uniform and ELBO mechanisms on the Cosmos backbone isolates the benefit of information-theoretic routing from architecture differences. The ELBO mechanism wins by a large margin (PSNR 29.30 vs 27.35 at BPP=0.56), confirming that the routing mechanism, not just extra transformer parameters, drives the improvement.

## Weaknesses

### Fatal
None.

### Major

- **Underspecified per-token ELBO computation (Section 3.2).** Equation (3) defines ELBO as a scalar per-video expectation. However, Section 3.2 uses "per-token log-likelihood, which is also approximated via the ELBO values" and computes a binary mask where "N_x tokens with the lowest ELBO values are 1." How a scalar ELBO is decomposed into per-token values for token ranking is never explained. Is the reconstruction loss attributed per spatial-temporal position? Is the KL term similarly per-token? This is the core mechanism driving the adaptive compressor, and without specifying it, a reader cannot reproduce the method. This is a genuine reproducibility gap that should be addressed in the rebuttal.

### Minor

- **Unsupported 50% token savings claim in the introduction.** The abstract correctly claims "saving 20% tokens without influence on performance" (supported: BPP 0.81 vs 1.00, PSNR 30.08 vs 30.01). The introduction claims "save approximately 50% tokens without loss of reconstruction quality compared to state-of-the-art fixed-length tokenizers." The closest evidence is INFOToK at BPP=0.56 vs Cosmos-DV at BPP=1.00 (~44% savings), but PSNR drops from 30.01 to 29.27 — a 0.74 dB reduction. The 50% claim overstates what Table 1 supports and should be qualified or removed. The 20% claim is strong enough on its own.

- **No variance or statistical reporting.** All results in Tables 1–3 are reported as single numbers without error bars, standard deviations, or confidence intervals. While single-run evaluation is common in this subfield, the absence of any uncertainty quantification makes it difficult to assess whether small differences (e.g., PSNR 29.86 vs 29.92 in Table 2) are meaningful or within noise. The paper would be strengthened by adding variance estimates or explicitly noting their absence as a limitation.

- **Theoretical guarantees assume idealized training conditions.** Theorems 2.2 and 3.1 assume the tokenizer minimizes the reconstruction loss (eq. 2), which SGD on neural networks does not guarantee. The paper acknowledges this (line 154: "ELBO values are believed to be close enough") but does not empirically verify the gap. The architecture-controlled ablation in Table 3 partially addresses this by showing the ELBO mechanism outperforms uniform masking on the same backbone, but the theoretical framing in the abstract and introduction could more carefully distinguish idealized guarantees from empirical demonstration.

### Trivial
None.

## Nice-to-Haves

- A wall-clock latency comparison (beyond NFEs) would strengthen the efficiency claim, though the paper notes this exists in Appendix D.
- A discussion of when the ELBO estimate might diverge from the true log-likelihood and cause poor routing decisions would be informative but is not a core flaw.

## Removed Points

- **ElasticTok reimplementation discrepancy claim (from Harsh Critic).** The reviewer claimed the Cosmos+Uniform reimplementation (PSNR 27.35, Table 3) is "substantially worse than the original ElasticTok (PSNR 28.26)." This is factually incorrect: ElasticTok's PSNR=28.26 is at BPP=0.81, while Table 3 results are all at BPP=0.56. At the same BPP=0.56, ElasticTok's PSNR is 27.34 — nearly identical to the reimplementation's 27.35. The reimplementation is faithful. **Removed as factually incorrect.**
- **Generic concerns about missing related works / formatting / reproducibility nitpicks.** Filtered per hard rules (missing related works cannot be verified, formatting artifacts are parser issues).

## Novel Insights

The most interesting observation across the reviews is that the ELBO-based router — a quantity the model is already trained to maximize — serves double duty as both a training objective and a routing criterion, eliminating the separate search procedure required by ElasticTok. The oracle ablation (Table 2) showing the ELBO router matches an exhaustive search-based optimal strategy within ~0.1 PSNR is particularly strong evidence that the theory transfers to practice, though neither reviewer deeply analyzed why this gap is so small.

## Suggestions

1. **Clarify the per-token ELBO computation.** Specify how the scalar ELBO from eq. (3) is decomposed into per-token values for ranking. This is the most critical issue for reproducibility.
2. **Reconcile or qualify the 50% claim** in the introduction to match the supported evidence. The 20% claim is strong enough on its own.
3. **Add variance estimates** (e.g., standard deviations across seeds) for the main experimental results, or explicitly state single-run evaluation as a limitation.

## Score and Decision

**Calibration anchors used:**
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/tFV5GrWOGm.md` — ElasticTok (6.00, Round 4). The direct baseline. INFOToK is clearly stronger on theoretical depth, empirical results, and efficiency.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/yGnsH3gQ6U.md` — BSQ-ViT (5.75, Round 4). Another video tokenization paper with strong reconstructions. Comparable empirical scope, but INFOToK's theoretical analysis is deeper.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/mb2ryuZ3wz.md` — "How many tokens is an image worth?" (5.75, Round 4). Adaptive image tokenization. Similar motivation but INFOToK has stronger theory and more comprehensive evaluation.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/IqGVIU4rvM.md` — VQ-VAE + Diffusion Tokenizers (2.50, Round 2). Not competitive — INFOToK is far more principled and better executed.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/1xG3MN1RRW.md` — SparseVLM (5.20, Round 3). Token sparsification for VLMs, related but different task. INFOToK has stronger theory and more convincing results.

**Round 1 bracket:** 6.5–7.5. **Final:** 7.0.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>