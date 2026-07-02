Now let me write the final consolidated review.

## Summary

This paper proves that decoder-only Transformer language models are almost-surely injective: distinct prompts map to distinct last-token hidden states. It establishes this property at initialization (Theorem 2.2), shows it is preserved under GD/SGD training (Theorem 2.3, Corollary 2.3.1), and introduces SIFT/SIPIT, an algorithm that exactly recovers input prompts from hidden states with an O(T·|V|) worst-case bound. Experiments on six model families find zero collisions across ~5B pairwise comparisons, and the inversion algorithm achieves 100% accuracy on tested prompts.

## Strengths

1. **Rigorous proof of a non-obvious property (Theorems 2.1–2.3).** The proof strategy—establishing real-analyticity of the architecture (Thm 2.1), using the real-analytic function dichotomy to bound collision sets to measure zero (Thm 2.2), and showing gradient descent preserves absolute continuity of the parameter distribution (Thm 2.3)—is conceptually clean and technically non-trivial. The construction of a separating parameter configuration in Theorem 2.2, particularly for prompts that differ at early positions, requires careful reasoning about attention mechanisms under causal masking.

2. **Training-preservation argument (Thm 2.3 and Corollary 2.3.1).** Extending injectivity from initialization (Sutter et al., 2025) to trained models is a genuine advance. The argument using Jacobian determinants and absolute continuity preservation is elegant and represents the strongest technical contribution. The extension to SGD and mini-batch GD is also well-conceived.

3. **Clear framing of the discrete-to-continuous map (§2, footnote 2).** The paper correctly distinguishes its object of study—the map from discrete prompts s ∈ 𝒱^{≤K} to continuous hidden states in ℝ^d—from the more commonly studied map from ℝ^d to ℝ^d. This reframing is what makes the injectivity claim plausible (a large but finite set mapped into high-dimensional space with structured functions) and separates the result from intuitions about individual components being many-to-one.

4. **Empirical validation at scale.** The collision search across 100k prompts (~5B pairwise comparisons) across six model families (GPT-2, Gemma-3, Llama-3.1, Mistral-7B, Phi-4, TinyStories) provides credible support. Finding zero collisions with minimum L2 distances far above the 10^{-6} threshold is consistent with the measure-zero prediction. The quantized-model and large-model (70B) extensions test conditions the theory does not cover and demonstrate empirical robustness.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

1. **Naming inconsistency across the paper.** The algorithm is introduced as "SIFT" (lines 9, 17), then "SIPIT" (lines 45, 139), then "SIpIT" (Algorithm 1 header, Theorem 3.1), then "SIpT" (Section 4 header), then "SiPT" (Tables 4–5, several lines in Section 4.2). At least four distinct capitalizations appear. This is confusing and should be unified.

2. **The "adversarial batch selection" claim in Corollary 2.3.1 is imprecisely supported.** The corollary states that injectivity is preserved under SGD with "arbitrary (possibly random or adversarial) batch selections ℬ_t." The proof argues that each fixed batch ℬ defines a real-analytic update map φ_ℬ with non-zero Jacobian determinant. For random batches this works via the law of total probability. For adversarially chosen batches where ℬ_t depends on θ_t, the proof would need an additional argument (e.g., finiteness of the batch space for a fixed finite dataset) to ensure that the union of measure-zero preimages across adaptively selected batches does not accumulate into a positive-measure set. The gap is small and fixable, but the current proof sketch does not address it.

3. **The O(T·|V|) worst-case bound is called "linear time" without clarifying the role of |V|.** Theorem 3.1 states a bound of T·|V| steps. Calling this "linear-time guarantees" (abstract, intro, discussion) is defensible if |V| is treated as a model-specific constant, but a casual reader may expect scaling only with T. The paper should state "O(T·|V|) time" and explain the practical dependence on vocabulary size.

4. **No description of the computational method for 5B pairwise comparisons.** The paper reports ~5B pairwise comparisons across 100k prompts but does not describe whether hashing, approximate nearest neighbors, exact GPU computation, or some other method was used. This affects reproducibility and the interpretability of the "no collisions" finding.

5. **Small inversion experiment scale.** The inversion experiments use 100 prompts (20 tokens) for GPT-2 Small and 50 prompts (10 tokens) for quantized models. While 100% accuracy is consistent with theory, these sample sizes are modest. Scaling to at least 500–1000 prompts would provide stronger evidence.

6. **No discussion of floating-point precision.** The theory concerns exact equality in ℝ^d. Practical implementations use floating-point arithmetic. Could two mathematically distinct representations be indistinguishable due to rounding? The observed minimum distances are orders of magnitude above the 10^{-6} threshold, so this is not a practical concern, but a brief discussion would strengthen the paper.

7. **Inconsistent framing of quantization results.** The paper correctly lists quantization as a failure case of the analyticity assumption (§2), yet the experimental section (§4.1) states quantization "preserves the integrity of the representation space" in a way that could be read as confirming the theory. Since the theory makes no prediction about quantized models, these results should be more clearly framed as demonstrating empirical robustness beyond the theoretical guarantees.

### Trivial

- The privacy/legal discussion in Section 6 makes a plausible argument but overstates the logical chain: injectivity shows hidden states *determine* the input, not that they are legally equivalent to the input. This is an opinion in the discussion section and does not affect the technical contribution.
- The proof sketch for Theorem 2.2's "differing earlier" construction is brief; the full proof is deferred to the appendix (standard practice). A slightly expanded example in the main text would improve readability.

## Nice-to-Haves

- Extend the training-preservation proof boundary to Adam/AdamW, which use adaptive step sizes and square-root operations that may not be real-analytic. The paper covers GD/SGD theoretically and validates empirically on Adam-trained models, but stating this boundary condition explicitly would strengthen the contribution.
- Expand the separating construction in Theorem 2.2 with a concrete worked example for a minimal transformer (1 layer, 1 head) to improve reader confidence without requiring appendix access.

## Removed Points

These points from the input review were removed with justification:
- **"Adversarial batch selection as a fatal flaw"**: Removed because the criticism that adversarial selection invalidates the proof is incorrect. Since the set of possible mini-batches is finite for any finite dataset, the union of φ_ℬ^{-1}(collision set) over all ℬ still has measure zero, so absolute continuity is preserved even under adaptive selection. The issue is merely one of missing precision in the proof sketch, not a conceptual flaw.
- **"Under-specified construction in Theorem 2.2 as a serious weakness"**: The paper explicitly labels this a "Sketch of proof" and directs readers to "Appendix C, Theorem C.2." This is standard practice; the main-text sketch is adequate for evaluation.
- **Generic strengths** (e.g., "Connect-theory-to-practice demonstration") were dropped as they lacked specific content beyond what is already listed.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Unify the algorithm name to a single consistent capitalization throughout.
2. Add a brief remark in Corollary 2.3.1 clarifying that the adversarial claim relies on the batch space being finite for a fixed finite dataset.
3. Describe the computational method used for the 5B pairwise comparisons in the collision search.
4. Increase the inversion experiment sample sizes in a revision or appendix.
5. Clarify the "linear time" phrasing to explicitly note the O(T·|V|) dependence.
6. Add a note on floating-point precision and why the 10^{-6} threshold is safe given the observed margins.

---

**Calibration Anchors (all rounds):**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| 6S4WQD1LZR (Transformers are Universal ICL) | 6.67 | R1, R2 | Similar theoretical contribution; accepted; comparable proof quality but less empirical support |
| STUGfUz8ob (When can transformers reason) | 7.60 | R1, R2 | Stronger empirical component with architectural modifications; accepted; similar theory+experiment balance |
| NHhjczmJjo (Learn-to-Optimize Transformers) | 7.00 | R1, R2 | Comparable theoretical depth with convergence proofs; accepted |
| hwSmPOAmhk (Factual Recall via Assoc. Memories) | 7.33 | R1, R2 | Similar structure (proofs + empirical); accepted |
| 4ikjWBs3tE (Transformers Learn Low Sensitivity) | 6.75 | R1, R2 | Similar theoretical+empirical profile; accepted |

**Round 1 bracket:** 6.5–8.0 (based on comparison with similar theoretical Transformer papers scoring 6.67–7.60)

**Final score rationale:** The paper's core theoretical contribution is solid and comparable to accepted theoretical papers in the calibration set (6.67–7.60). The training-preservation argument is a genuine advance over prior work. The weaknesses are predominantly presentation-level (naming, missing methodological detail, small experiment scales) rather than conceptual. The paper sits at the lower end of the 6.5–8.0 bracket because the empirical evaluation has clear gaps (inversion sample sizes, missing collision-search methodology), but the theory is strong enough to justify acceptance.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>