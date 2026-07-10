Now I have all the information I need. Let me produce the final consolidated review.

**Analysis of the trained model signals:**
- Strengths are extremely strong (8.6-9.9), indicating a genuinely novel and well-executed paper.
- The Figure 3 correlation issue (-1.8) is the most impactful weakness, but the model agrees it doesn't sink the paper (especially since Table 3 ablations independently support the components' importance).
- The wall-clock/memory comparison (-0.4) and missing λ₁,λ₂ values (-0.3) are relatively minor.
- The "prompt perturbation distribution" trivial point has -2.0 which seems like noise (the paper does describe it qualitatively and defers full details to the appendix).

The balance strongly favors acceptance.

## Summary
2-3 sentence summary of the paper's contribution.

## Strengths
- strength 1 with evidence
- strength 2 with evidence

## Weaknesses
// List only reasonable points. Rank by severity.
// Not every paper has weaknesses at every tier. Leave a tier empty (or write "None") if nothing qualifies.

### Fatal
// Errors that invalidate the paper's core claims or results.
// Examples: fundamentally flawed methodology, unsupported central claim, incorrect proofs, data fabrication concerns.
// Most papers have none. Leave empty if none apply.

### Major
// Issues that a reviewer would weigh against acceptance, and that the authors should fully resolve in a rebuttal.
// Examples: missing critical baseline, overclaimed scope unsupported by experiments, significant methodological gap.
// Not every paper has major weaknesses. Do not invent them to fill this section.

- weakness 1 — why it matters
- weakness 2 — why it matters

### Minor
// Issues worth the authors' attention but unlikely to change an accept/reject decision.
// Examples: addressable in rebuttal, limited scope of one experiment, unclear phrasing of a claim, missing ablation that would strengthen but not invalidate.

- weakness 1 — why it matters

### Trivial
// Small issues the authors should fix but that carry no weight in evaluation.
// Examples: typos, minor notation inconsistencies, suboptimal figure choices, small presentation issues.

- weakness 1

## Nice-to-Haves
- suggestion that would improve but is not a core flaw

## Removed Points
Include something like this "These points are flagged to be removed, treat them with caution"
Weaknesses that are removed keep the details of the S/W just in case they are useful 

## Novel Insights
One paragraph synthesizing genuinely novel observations.
If no genuinely novel insight emerges from the reviews beyond the paper's own contributions, write
"None beyond the paper's own contributions."

## Suggestions
- specific actionable suggestion

## Score and Decision## Summary

This paper proposes Pi-CCA, a replay-free continual learning framework for vision-language models that directly preserves the cross-modal alignment geometry (canonical correlations and subspaces) using compact CCA certificates instead of regularizing proxy signals like logits or similarity distributions. The method uses random orthonormal sketches for constant-memory storage, prompt-invariant projector averaging, and exponential moving averages for streaming estimation. Across four VL-CL protocols (MTIL, X-TAIL, VLCL, ConStruct-VL), Pi-CCA achieves state-of-the-art results among replay-free methods, supported by thorough ablations.

## Strengths

- **Conceptually principled motivation.** The paper's core insight — that prior VL-CL methods regularize proxy quantities (logits, similarity distributions, parameters) rather than the cross-modal alignment geometry that actually drives zero-shot performance — is well-articulated and genuinely novel in the continual learning context (Section 1). This reframing of forgetting as "alignment-geometry drift" is the paper's strongest conceptual contribution.

- **Novel technical mechanism.** Using CCA certificates (top-k canonical correlations + sketched subspaces) as a compact summary of cross-modal alignment is genuinely new in continual learning. The sketching via random orthonormal projections (Eq. 4) for constant-memory storage and the prompt-invariance mechanism via projector averaging over perturbations (Eqs. 5–6, 11) are clean, thoughtful design choices.

- **Comprehensive evaluation scope.** The paper evaluates on four distinct VL-CL protocols covering classification (MTIL, X-TAIL), retrieval (VLCL), and structured-concept matching (ConStruct-VL). Results consistently place Pi-CCA at or near the top among replay-free methods (Tables 1 and 2), including surpassing a synthetic-replay method (GIFT) without storing or generating data.

- **Thorough ablations.** Table 3 is well-designed: each component (spectral term, subspace term, prompt invariance, certificate EMA, covariance EMA, spectral moments, pairing method, sketch type) is systematically removed or replaced with clear numerical deltas. This provides an honest, informative assessment of each design choice's contribution.

## Weaknesses

### Fatal
None.

### Major

1. **Figure 3 reports correlation values that strain credibility.** The figure caption states Pearson r=1.00 in two panels and Spearman ρ=1.00 in all four panels for the relationship between geometry drift and performance drop across a sweep of hyperparameter settings. With real experimental data involving multiple independent measurements (covering certificate size, EMAs, invariance strength, whitening, pairing, LoRA capacity/LR, sketch type), even a near-perfect relationship should produce r=0.999 or 0.998, not 1.00. Spearman ρ=1.00 in every panel is especially difficult to explain as a rounding artifact and requires clarification. The paper's claim that "stability of the canonical subspace/spectrum reliably predicts downstream performance" leans on this evidence. The authors should report the number of data points, provide unrounded correlation values, and explain how these perfect values arise. That said, the ablation results in Table 3 independently demonstrate the importance of the spectral and subspace components, so this issue does not invalidate the core contribution.

2. **No wall-clock or memory comparison against any baseline method.** The efficiency analysis (Figure 2) only sweeps Pi-CCA's own (k, h) configurations. Since Pi-CCA's per-step computation is substantially heavier than baselines (EMA covariances, whitening via eigendecomposition or Newton–Schulz, SVD, sketching, M perturbed SVDs for prompt-invariance), the reader cannot judge whether the performance gains (e.g., 76.8 vs 75.2 on MTIL Avg, 48.6 vs 46.1 on VLCL I2T R@1) come at a reasonable computational cost. A comparison against 2-3 top baselines is needed to assess practical viability.

### Minor

3. **The certificate is a moving target, not a fixed invariant.** The certificate is updated every step via a slow EMA (Eq. 13), making it a progressively drifting reference rather than a snapshot of the original pre-continual alignment. The paper does not quantify how much the certificate drifts over a task sequence. The ablation showing that freezing the certificate (α=0) only drops MTIL by 1.2-1.4 points suggests the initial certificate does provide meaningful anchoring, but the "invariant preservation" framing would be strengthened by directly measuring and reporting drift magnitude.

4. **Default values of λ₁ and λ₂ are not reported in the main text.** Only λ₃=0.2 is given (line 224). While these likely appear in the appendix, the main text should state them for reproducibility.

5. **Table 1 reports point estimates without confidence intervals or standard deviations**, while Table 2 includes ± values. This inconsistency makes it difficult to assess whether Pi-CCA's lead over the second-best method (e.g., 76.8 vs 75.2 on MTIL Avg) is statistically significant.

### Trivial

6. **The prompt perturbation distribution 𝒫 is described only qualitatively** ("synonym/template variation," "token-level synonym swap/back-translation/template jitter") without a precise formal specification in the main text.

7. **The time-continual study on TiC-YFCC/RedCaps** mentioned in §4.1 is not presented in the main results section.

## Nice-to-Haves

- Provide a brief summary of the theoretical explanation (currently in Appendix §A.4) in the main text.
- Show the within-order seed variation in Figure 5 (the dots are per-order means, but the spread across seeds within each order is not shown).

## Removed Points

These points were removed from the harsh critic's review with justification:

- **"Streaming CCA under distribution shift is theoretically problematic"** — Removed because it is a speculative theoretical concern without evidence that it degrades performance. The paper demonstrates strong empirical results across diverse benchmarks, and many continual learning methods use EMA-based statistics as practical approximations.
- **"The main text claims theoretical explanation (§A.4) but this is in the appendix"** — Removed as standard practice; deferred details to appendix are normal.
- **Various formatting/nitpick comments** — Removed per hard rules (parser artifacts, not author errors).
- **"Missing related works"** — Removed per hard rules (cannot confirm existence of unmentioned works).
- **"Cannot release code during review"** — Removed per hard rules (code release is not required during review; the paper commits to open-sourcing upon acceptance).

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Recompute the geometry-performance correlations, report actual unrounded r/ρ values, show the number of data points, and display the scatter plot so readers can visually assess the relationship.
2. Add wall-clock time and peak memory benchmarks against the top 2-3 baselines (e.g., C-CLIP, ZSCL) on at least one dataset.
3. Add confidence intervals or standard deviations to Table 1 (MTIL/X-TAIL).
4. Quantify certificate drift over a representative task sequence to clarify whether the method preserves invariants or primarily acts as temporal smoothness regularization.
5. Specify default λ₁ and λ₂ values explicitly in the main text.

## Score and Decision

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>