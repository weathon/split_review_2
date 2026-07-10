Now let me produce the final consolidated review.

## Summary

This paper introduces a theoretical framework for data curation in high-dimensional binary classification. Using angular alignments (ρ, ρ₍, ρ_g) between generator, pruner, and ground-truth, the authors derive exact scaling laws for test error under label-agnostic and label-aware pruning rules, and identify generator quality as the key determinant of whether "keep hard" or "keep easy" is optimal. The theory is validated on synthetic data and ImageNet, and qualitatively connected to recent LLM reasoning results (LIMO, s1) and model collapse mitigation.

## Strengths

1. **Clean geometric parametrization.** The framing in terms of angular alignments (ρ, ρ₍, ρ_g) between generator, pruner, and ground truth elegantly reduces the messy question of "when to prune" to a tractable comparison of cosines. This is a genuine conceptual contribution independent of the specific calculations.

2. **Synthetic validation matches theory convincingly.** The match between theoretical curves and empirical simulations in Figure 1 (solid vs. dashed lines) is visually compelling, and the crossover pattern — where less-is-more emerges only with abundant data and a strong generator — is clean and interpretable.

3. **Theorem 2 provides a crisp theoretical result.** It establishes that generator quality (ρ) determines the optimal pruning strategy: keep-hard when the generator is excellent (ρ → 1) and keep-easy when the generator is poor (ρ < 1), given an excellent pruner. This directly explains the intuition behind methods like LIMO/s1.

## Weaknesses

### Fatal
None.

### Major

1. **Overclaimed connection to LLM reasoning (LIMO/s1).** The abstract claims the framework "provides a principled explanation for the contradictory curation strategies recently observed in LLM mathematical reasoning." However, the paper does not measure ρ for any LLM, make quantitative predictions, or derive the observed scaling exponents. Section 4.2 labels existing results (Tables 1-2, aggregated from prior work) with the theory's categories post-hoc — the base LLM is called a "strong generator" when evaluating average AIME performance but a "weak generator" when evaluating only the hardest questions. This is a qualitative analogy, not a validated explanation, and no evidential bridge is established between the Gaussian linear model and LLM reasoning. The framing in the abstract and introduction overstates what the evidence supports.

2. **Model collapse mitigation claim is stronger than the evidence delivered.** The contributions list states: "We show analytically that data curation can avert model collapse under label shift, establishing phase boundaries where uncurated training diverges while curated training remains stable." In the main text, however, there is no analytical treatment of iterative dynamics or phase boundaries for model collapse. Theorem 2(B) is about single-round pruning (not iterative retraining), and Figure 3 is entirely empirical. The claimed analytical result is not present in the submitted text.

### Minor

3. **Theorem 1 defers key quantities to the appendix.** The test error formula in Theorem 1 is expressed in terms of functions *m*, *\tilde{m}*, and *r* that are said to be "explicitly determined by the constants in Eqn (8)" with "Details in appendix," but their functional forms are not given in the main text. While deferred derivations are common, the paper's claim to "derive exact scaling law curves" is partially deferred, and a reader cannot evaluate what the theorem actually computes from the main text alone.

4. **Theorem 2 addresses only extreme cases.** The theorem requires an excellent pruner (ρ₍ → 1) in both regimes and only varies generator quality between perfect (ρ → 1) and imperfect (ρ < 1). The practically relevant middle of the parameter space — where the pruner is mediocre, or both generator and pruner have intermediate quality — is not covered. The claimed phase transitions are shown only at the corners of the parameter space.

5. **ImageNet experiments validate qualitative spirit but not quantitative predictions.** The theory is derived for binary classification with Gaussian features and identity covariance; ImageNet is 1000-class with real images. No mapping of the theoretical quantities (ρ, ρ₍, ρ_g) to the experimental setting is attempted. The paper acknowledges these limitations but presents the results as confirmation of the theory, when they are at best a consistency check.

## Nice-to-Haves

- Include at least one closed-form special case of Theorem 1 in the main text (e.g., test error for "keep easy" or "keep hard" with a given retention fraction) so readers can see the machinery in action.
- Derive or state the full phase diagram in ρ-ρ₍ space (even for a special case) to make the practical decision rule more usable for practitioners.
- Clarify what the error bars in Figure 1 represent (standard deviation? 95% CI?) and add variance information to the ImageNet results.

## Removed Points

These points were flagged in the input but are removed with justification:

- **"Baseline comparison in Figure 1 is stacked":** Comparing informed keep-hard pruning against random (uninformative) selection is a natural and valid baseline for demonstrating that strategic curation outperforms uninformative selection. The comparison is appropriate for the claim being made.
- **"Sun et al. (2025) characterization question":** Removed per hard rules — cited references are assumed to exist and be accurately characterized.
- **"Squared loss is unusual for classification":** The paper is transparent about using squared L2 loss; this is a standard modeling choice in high-dimensional learning theory and not a weakness.
- **"Tables 1-2 cross-paper comparison differences":** The paper transparently states these results are "aggregated from existing literature" and uses them only to illustrate the qualitative pattern. Not a flaw.
- **Strength about "Timely and well-motivated problem":** Generic; lacks a specific, grounded anchor in the paper's content.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- Reframe Section 4.2 explicitly as a qualitative analogy or conceptual illustration rather than a "principled explanation." The paper is strongest when it presents what it directly derives.
- Either deliver the analytical model collapse result claimed in the contributions, or remove that claim and reframe the model collapse discussion as an empirical demonstration with a conceptual link to Theorem 2.
- Strengthen the main text by including at least one special case where readers can see the closed-form test error expression in terms of known quantities — this would make Theorem 1 less opaque without requiring the appendix.

## Score and Decision

The paper presents a genuinely novel and elegant theoretical contribution — the geometric parametrization of data curation via angular alignments and the identification of generator quality as the key determinant of optimal pruning strategy. The synthetic validation is convincing. However, the paper's framing overstates its reach in two significant ways: claiming a "principled explanation" for LLM reasoning results that is actually a post-hoc qualitative analogy, and claiming an analytical result for model collapse mitigation that the main text does not deliver. These overclaims are fixable through more measured framing, and the underlying theoretical contribution is worth publishing. With adjustments to align the claims with the evidence, this would be a solid paper.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>