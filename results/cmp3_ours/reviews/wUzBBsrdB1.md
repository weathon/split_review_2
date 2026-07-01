Now let me construct the final review.

## Summary

This paper studies the effect of L0 (average number of active features per token) on Sparse Autoencoders (SAEs) for LLM interpretability. Through carefully designed toy model experiments with known ground-truth features, it demonstrates that when L0 is set too low, SAEs mix correlated features to improve reconstruction at the cost of feature monosemanticity — a phenomenon it terms a manifestation of feature hedging. A key finding is that sparsity-reconstruction tradeoff plots, which are standard in the field, can be actively misleading: a ground-truth SAE scores *worse* on reconstruction than a corrupted low-L0 SAE that cheats by mixing features. The paper proposes a diagnostic metric, decoder pairwise cosine similarity (c_dec), that identifies the correct L0 in toy models and provides useful signal in LLMs, validated against sparse probing performance on Gemma-2-2b and Llama-3.2-1b.

## Strengths

- **Well-designed toy model experiments (Sections 3.1–3.4):** The setup is clean — orthogonal ground-truth features with controlled correlations, known "true L0," and the ability to construct a ground-truth SAE. The critical experiment in Section 3.3 (trained SAE achieves MSE 2.73 vs. ground-truth SAE's 4.88) cleanly isolates the problem and shows that MSE loss actively incentivizes incorrect features at low L0. The initialization of low-L0 SAEs to the ground-truth solution (Section 3.1) rules out local minima as an explanation.

- **Important critique of sparsity-reconstruction tradeoff plots (Section 3.4, Figure 4):** The demonstration that a ground-truth SAE scores *worse* on variance explained than a corrupted low-L0 SAE is a nontrivial finding with direct practical implications. The paper correctly argues that sparsity-reconstruction plots, as commonly used to compare SAE architectures, are not a sound evaluation method.

- **JumpReLU SAE results (Section 3.6):** The finding that JumpReLU SAEs "stick" near the correct L0 across a wide range of λ_s (Figure 7) is practically useful and empirically interesting. It suggests these SAEs have some robustness to misspecified sparsity coefficients.

## Weaknesses

### Fatal
None.

### Major

- **Framing gap between toy models and LLMs regarding "correct L0":** In toy models, "True L0" is well-defined because ground-truth features and their firing probabilities are known. The paper carries the "correct L0" / "incorrect L0" framing into LLM experiments (title, abstract, throughout), where no ground-truth features exist and no single L0 value is guaranteed to be correct for all latents. The paper partially acknowledges this in Section 4.2 ("There is no reason why every latent has the same firing threshold, so there is likely a range of L0s where some latents are firing more than they ideally should while other latents are firing less than they ideally should"), but the title and abstract do not reflect this nuance. The LLM validation against sparse probing shows small F1 differences (~0.04 range over 0.78–0.82 across Figure 8 and Figure 9), and no statistical significance is reported, making it unclear whether the observed patterns are meaningful.

### Minor

- **c_dec validation against sparse probing relies on qualitative judgment:** The paper uses the "elbow" of the c_dec curve (just before the jump due to low L0) rather than the global minimum to recommend L0 values, and validates this by stating it "seems to roughly correspond to peak k-sparse probing performance" (Section 4.1) based on visual inspection. No quantitative criterion is given for identifying the elbow, and no comparison is reported between the L0 at the c_dec elbow and the L0 that maximizes probing F1 across tasks. The sparse probing benchmark (Kantamneni et al., 2025) is used without discussion of what it measures or why it is a reliable proxy for feature quality.

- **Layer selection is not justified:** SAEs are trained on Gemma-2-2b Layer 5, Llama-3.2-1b Layer 7, and Gemma-2-2b Layer 12 without explanation of why these specific layers were chosen. Since the c_dec curves behave differently across layers (flat for Gemma Layer 5, U-shaped for Llama Layer 7), the reader cannot assess whether the results are representative or idiosyncratic.

### Trivial
None.

## Nice-to-Haves

- Provide a quantitative comparison: compute the L0 that maximizes sparse probing F1 across tasks and report its agreement with the c_dec elbow across multiple layers, models, and architectures.
- Include significance tests or confidence intervals on sparse probing F1 differences to establish that the ~0.04 range is meaningful.
- Show qualitative examples of latents from low-L0 and recommended-L0 SAEs to directly demonstrate improved interpretability.
- Lean into the per-latent L0 variation (Section 4.2) as a contribution rather than a complication, e.g., arguing that a single global L0 is fundamentally insufficient and motivating adaptive/ per-latent approaches.

## Removed Points

These points are flagged to be removed, treat them with caution:

- **"Most commonly used SAEs have too low L0" claim unsupported in main text:** Removed per policy — the evidence is referenced as Appendix A.13, which exists in the original submission but was stripped by the parser. The claim's placement in the abstract with supporting evidence deferred to the appendix is a presentation choice, not an absence of evidence.
- **c_dec inconsistency across architectures:** The reviewer argued that BatchTopK and JumpReLU SAEs give different minima on the same model. However, the paper explicitly discusses this difference (Section 4.1), uses the "elbow" rather than the global minimum, and offers a reasonable explanation (JumpReLU adjusts thresholds per latent). This is an addressed limitation, not an unacknowledged inconsistency.
- **"Correct L0 doesn't transfer to LLMs" as a fatal structural issue:** The paper acknowledges the per-latent variation explicitly in Section 4.2. The reviewer's characterization as a fatal structural flaw overstates the issue given the paper's own caveats; it is retained as a Major weakness above but not as a fatal one.

## Novel Insights

The reviewer identifies a useful framing tension: the paper's strongest contribution is diagnostic/cautionary (low L0 causes feature mixing; sparsity-reconstruction plots are misleading) rather than prescriptive (c_dec as a method for finding *the* correct L0). The toy model results are definitive, but the LLM evidence supports a more cautious reading. Reframing the contribution around what the toy models clearly demonstrate and presenting c_dec as a heuristic diagnostic tool — analogous to an elbow plot in PCA — rather than a method for identifying a single correct L0, would more accurately match the evidence and strengthen the paper.

## Suggestions

- Soften the framing around "correct L0" in the title and abstract to reflect that the concept applies cleanly to toy models and serves as a useful heuristic in LLMs rather than a precisely identifiable quantity.
- Add a quantitative comparison of c_dec elbow vs. optimal sparse probing L0 across layers and architectures.
- Include a brief justification for chosen layers and discuss whether the results are representative.

## Score and Decision

**Calibration anchors (all rounds):**

| Paper | Avg Score | Round | Comparison |
|-------|-----------|-------|------------|
| Scaling and evaluating sparse autoencoders (tcsZt9ZNKD) | 8.20 (outlier: 3) | R1 | Foundational SAE-scaling paper; substantially more comprehensive in scope. |
| Sparse Autoencoders Find Highly Interpretable Features in Language Models (F76bwRSLeK) | 4.80 | R1 | Foundational SAE paper; weaker novelty but broader scope. This paper has cleaner diagnostic experiments. |
| Sparse Autoencoders Do Not Find Canonical Units of Analysis (9ca9eHNrdH) | 7.00 | R1, R2 | Similar diagnostic/critique paper about SAEs; more novel experimental methodology (stitching, meta-SAEs) and stronger LLM evidence. |
| Towards Principled Evaluations of Sparse Autoencoders (1Njl73JKjB) | 7.00 | R2 | Evaluation-focused SAE paper; more rigorous evaluation framework. |
| Mechanistic Permutability (MDvecs7EvO) | 6.50 | R2 | SAE feature matching; comparable rigor but narrower scope. |
| Applying SAEs to Unlearn Knowledge (ZtvRqm6oBu) | 5.25 | R2 | Application paper with thinner evidence. |

**Round 1 bracket:** 5.0 – 7.0

**Narrowing:** The clean toy model experiments and the important critique of sparsity-reconstruction tradeoffs are genuine contributions that place this paper clearly above application-focused or thin-evidence papers (~5). However, the thinner LLM validation, framing issue, and reliance on qualitative judgment for c_dec validation prevent it from reaching the level of the stronger diagnostic papers (7.0). The paper sits comfortably at the lower end of the borderline-accept range.

**Final score: 6.0**

This reflects a paper with a real, solid contribution (the toy model demonstration of feature mixing at low L0 and the critique of sparsity-reconstruction plots) that is weakened by an overstated framing and limited LLM validation. The core findings are publishable, but the contributions are narrower than the title and abstract suggest.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>