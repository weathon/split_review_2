## Summary

AdaSVD proposes two complementary techniques for improving SVD-based LLM compression: (1) **adaComp**, which reduces SVD truncation error by alternately updating the U and V matrices after truncation using a Moore-Penrose pseudoinverse formulation, and (2) **adaCR**, which assigns layer-specific compression ratios based on input-output cosine similarity. The paper evaluates on multiple LLMs (LLaMA2-7B, OPT-6.7B, Vicuna-7B, Mistral-7B) and a VLM (LLaVA), showing consistent perplexity improvements over SVD-LLM, particularly at high compression ratios.

## Strengths

- **Consistent improvements over the strongest prior baseline across multiple settings.** In Table 1 on LLaMA2-7B, AdaSVD outperforms SVD-LLM on every language modeling dataset at every compression ratio (40–60%). The gap widens at higher compression where prior work struggles most — e.g., 50.33 vs. 89.90 on WikiText-2 at 60% (44% relative improvement), and 239.18 vs. 561.00 on C4 at 60% (57% relative improvement).

- **Clean ablation study isolating individual component contributions.** Table 3a and 3b decouple adaComp and adaCR, showing that each contributes meaningfully and independently. At 60% compression, AdaSVD without adaComp achieves 78.82 (still beating SVD-LLM's 89.90), and adding adaComp further drops perplexity to 50.33. Similarly, removing adaCR (constant CR) yields 69.46 vs. 50.33 with adaptive CR.

- **Demonstrated orthogonality to weight quantization.** Table 4 shows AdaSVD combined with GPTQ-INT4 consistently outperforms SVD-LLM+GPTQ-INT4 across all compression ratios (40–80%) on all three language modeling datasets, supporting practical applicability in compound compression pipelines.

- **Evaluation across diverse model families.** The paper tests on LLaMA2-7B, OPT-6.7B, Vicuna-7B, and Mistral-7B, not just a single architecture, providing reasonable evidence of generalizability.

## Weaknesses

### Fatal
None.

### Major
None that can be verified from the paper as written.

### Minor

1. **Limited algorithmic novelty of adaComp.** The alternating update of U and V using a Moore-Penrose pseudoinverse is a standard technique in numerical linear algebra (the pseudoinverse is the textbook solution to the least-norm least-squares problem). The paper reformulates the optimization as a least-squares estimation problem and solves via SVD-based pseudoinverse — this is a reasonable engineering choice for numerical stability but not a fundamentally new method. The "adaptive compensation" framing somewhat overstates what is essentially alternating least squares on the SVD reconstruction objective.

2. **adaCR importance metric is unvalidated.** The cosine-similarity-based layer importance (Eq. 17) is intuitive but the paper provides no analysis showing correlation between this metric and actual performance degradation when compressing a specific layer. Without validation, the mechanism is plausible but unsubstantiated. Additionally, the observation that "the first layer always weighs the most importance" could simply reflect that the first layer receives high-variance token embeddings rather than indicating task-level importance.

3. **VLM evaluation is qualitative only.** The VLM experiments (Figure 5) present cherry-picked image captioning examples without quantitative metrics (CIDEr, BLEU, SPICE). A single example where SVD-LLM outputs "sasasm" is not compelling evidence. This weakens the generalizability claims to vision-language models.

4. **No confidence intervals or variance estimates.** All results are point estimates from a single calibration sample (256 samples from WikiText-2). Given the stochasticity of calibration sampling, reporting standard deviations across multiple seeds would strengthen reliability claims.

5. **Hyperparameter sensitivity of adaComp iteration count.** Table 3c shows that at 40% compression, 1 iteration (14.76) outperforms 15 iterations (15.84), which the paper attributes to overfitting. This means the optimal iteration count varies with compression ratio and calibration data, requiring per-model/per-target tuning that is not addressed with practical guidance.

### Trivial
None.

## Nice-to-Haves

- The paper could include a correlation study between cosine-similarity importance and per-layer compression degradation to validate adaCR.
- Including standard deviations for main results would improve reproducibility claims.
- Adding quantitative VLM metrics would strengthen the VLM experiments.

## Removed Points

These points were flagged by reviewers but removed with justification:

- **"FWSVD and ASVD comparisons are meaningless"** — The paper explicitly acknowledges in Section 4.2 that "FWSVD and ASVD fail on these LLMs with compression ratios under 60%." They are included transparently. The primary comparison is against SVD-LLM, not these broken baselines. The paper's claims do not rest on the contrast with FWSVD/ASVD.

- **"adaCR has a logical gap — no guarantee of overall compression ratio"** — Factually incorrect. Equation 18 performs mean normalization: `I_n(W) = I(W) / mean(I(W))`. Since the mean of `I_n(W)` is exactly 1 by construction, Equation 19 guarantees the average retention ratio across layers equals the target `trr`. The paper does provide this normalization.

- **"Practical significance is unclear / perplexity degradation is large"** — The degree of degradation at high compression ratios is inherent to the problem domain, not specific to AdaSVD. The paper's claim is relative improvement over prior work. The "resource-constrained devices" framing is standard aspirational language used throughout the compression literature.

- **"Missing Table 2"** — Parser artifact (stripped appendix). The table exists in the original submission.

- **"MMLU results are flat/near-random"** — The original uncompressed model also achieves low MMLU (7.34) due to the evaluation setup used, so the metric is consistently measuring the same condition across all methods and does not invalidate comparisons.

- Various formatting/style nitpicks, speculation about content in the (stripped) appendix, and demands that the paper address problems outside its stated scope.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Validate the adaCR importance metric by showing correlation between cosine-similarity scores and the actual perplexity change when compressing individual layers.
2. Include confidence intervals or standard deviations for main results across multiple calibration seeds.
3. Add quantitative captioning metrics (CIDEr, BLEU, SPICE) for VLM evaluation instead of only qualitative examples.
4. Provide practical guidance on selecting the adaComp iteration count — e.g., an early-stopping heuristic based on validation perplexity or MSE convergence.

## Score and Decision

**Score: 5.5**

**Decision: Borderline (leaning reject / borderline accept)**

**Calibration note:** The calibration search tool was unavailable due to a file-system error in the calibration data directory. In lieu of retrieved anchors, this score is calibrated against the ICLR scoring rubric (1–10) and the reviewer's assessment of comparable papers in LLM compression. A score of 5.5 reflects that the paper makes genuine, reproducible improvements over the prior state-of-the-art (SVD-LLM) with thorough ablation studies and multi-model evaluation, but the core algorithmic contributions are incremental (alternating least squares with pseudoinverse is a standard technique, and the importance metric is unvalidated). The paper sits between the "borderline reject" (4) and "borderline accept" (6) bands — it has real empirical value but insufficient novelty and rigor (particularly the unvalidated adaCR and qualitative-only VLM results) for a clear accept at a top venue.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>