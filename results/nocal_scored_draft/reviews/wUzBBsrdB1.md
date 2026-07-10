Now I'll compose the final consolidated review.

## Summary

This paper studies the effect of the L0 sparsity hyperparameter on Sparse Autoencoders (SAEs) for LLM interpretability. Using synthetic toy models with ground-truth features, it demonstrates that when SAE L0 is set lower than the true feature sparsity, the SAE "cheats" by mixing correlated features to improve MSE at the cost of monosemanticity — and that the standard sparsity-reconstruction tradeoff plot is misleading because a ground-truth SAE scores worse than a cheating one. The paper proposes a decoder pairwise cosine similarity metric (c_dec) as a heuristic to detect the correct L0, validates it on toy models, and presents suggestive but limited validation on real LLMs (Gemma-2-2b, Llama-3.2-1b).

## Strengths

- **Compelling toy-model demonstration (Section 3).** The ground-truth SAE comparison (Section 3.3) is the strongest piece of evidence: MSE of the trained (incorrect) SAE is 2.73 vs 4.88 for the ground-truth SAE, confirming the MSE loss function *actively incentivizes* incorrect features when L0 is too low. This is a clean, falsifiable demonstration.
- **Novel critique of sparsity-reconstruction tradeoff plots (Section 3.4, Figure 4).** Showing that a ground-truth SAE achieves *worse* reconstruction than a cheating SAE at low L0 exposes a genuine flaw in how the field evaluates SAE quality. This conceptual contribution has clear practical implications for practitioners.
- **c_dec metric is intuitive and well-validated in toy models (Section 3.5, Equation 4, Figure 6).** The idea that decoder latents become less orthogonal when they mix correlated features follows from the paper's mechanism analysis. In toy models, c_dec is minimized at the true L0 with low variance across 5 seeds.
- **JumpReLU experiments (Section 3.6, Figure 7) provide a useful architecture sanity check.** The phenomenon is not specific to BatchTopK SAEs. The observation that L0 "sticks" near the correct value for a wide range of λ_s in JumpReLU SAEs is an interesting practical finding.

## Weaknesses

### Fatal
None.

### Major
- **LLM validation is thin and correlational.** Only one SAE width (h=32768) is tested across only 3 layer-model combinations (Gemma-2-2b layers 5 and 12; Llama-3.2-1b layer 7). The sparse probing F1 improvements are modest (~0.78→0.82, Figure 8) with no confidence intervals or statistical significance tests, even though the paper mentions 3 seeds. The connection between c_dec and feature quality in real LLMs is entirely correlational — the paper shows c_dec's elbow coincides with peak sparse probing performance, but does not demonstrate the same causal mechanism (correlation-based feature mixing) as in the toy models. This gap between the strong causal demonstration in toy models and the weak correlational evidence in real models is the paper's most significant limitation.

### Minor
- **The "elbow" criterion for c_dec is post-hoc and lacks an algorithmic rule.** For Gemma-2-2b Layer 5 (Figure 8), c_dec has a long flat region with the global minimum in that shallow region; the paper defaults to a visually defined "elbow" just before the low-L0 jump. The paper acknowledges this (Discussion: "we do not view this as a perfect guide") but does not provide a principled, repeatable rule for identification. If one needs to already know roughly the correct L0 to identify the elbow, the metric risks circularity.
- **The claim that "most commonly used SAEs have an L0 that is too low" is not adequately substantiated in the main text.** This appears in the Abstract, Introduction, and Discussion, but the only support is a reference to "a cursory search of open source SAEs on Neuronpedia" (Discussion, line 240, referencing Appendix A.13) without quantitative characterization (e.g., distribution of L0 values, fraction below a threshold) in the main body.
- **Feature splitting is a confound that the paper does not address.** Related Work mentions feature splitting (where a general interpretable feature splits into more specific sub-features in wider SAEs), but the paper does not discuss how c_dec behaves in this regime. If an SAE has higher L0 because features have legitimately split into more specific sub-features firing on different inputs, c_dec's ability to distinguish this from genuinely too-high L0 is unclear.
- **The paper's framing assumes a single "correct" L0 via the Linear Representation Hypothesis but does not discuss cases where features may not follow sparse linear superposition.** The paper cites Engels et al. (2025) on circular embeddings that violate linearity, but does not engage with how this might affect the claims about L0.

### Trivial
- No discussion of the computational cost of training a sweep over L0, which is a significant practical barrier for practitioners training a single SAE.

## Nice-to-Haves
- An algorithmic rule for identifying the c_dec elbow (e.g., "the smallest L0 such that c_dec is within 1 std of its minimum in the low-L0 regime") would make the metric more actionable.
- Discussion of how the toy model results depend on feature correlation strength would strengthen the mechanistic understanding.
- Additional validation on real SAEs (e.g., human evaluation of interpretability, or downstream task performance beyond sparse probing) would strengthen the claim that c_dec detects genuinely better features.
- Mentioning the computational cost of sweeping L0 would help calibrate practitioner expectations.

## Removed Points

- Criticism about "formal theoretical justification in Appendix A.6 being unverifiable" — removed per guidelines (appendix stripped by parser; treat as existing in original submission).
- Request for more discussion of how correlation strength affects results — moved to Nice-to-Haves above.

## Novel Insights

The key structural observation from the review process is that this paper's two contributions operate at different evidential levels: the toy-model demonstration (that misspecified L0 actively corrupts features) is rigorous and causal, while the c_dec heuristic for real LLMs is correlational with unaddressed confounds. The paper is honest about this asymmetry, but it means different readers may reasonably weigh the contributions very differently.

## Suggestions

- Provide concrete numbers (e.g., distribution of L0 values on Neuronpedia) in the main text to substantiate the "most SAEs have too low L0" claim.
- Explicitly discuss how feature splitting interacts with c_dec, including what the metric would show when features genuinely split.
- Visualize the variance across seeds in the sparse probing results (the 3 seeds are mentioned but not shown as intervals).
- Consider defining an automated rule for c_dec's elbow to replace the post-hoc visual criterion.

MY FINAL SCORE: <score>7</score>
MY FINAL DECISION: <decision>Accept</decision>