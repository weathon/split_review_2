Now let me produce the final consolidated review.

---

## Summary

This paper provides the first theoretical analysis of the training dynamics of a one-layer Mamba-style model for in-context learning (ICL) on binary classification tasks where prompts may contain additive outliers. The key analytical insight is that a one-layer Mamba (with the simplification $\mathbf{A}=-\mathbf{I}_m$) decomposes into linear attention followed by a multiplicative gating function. The paper proves convergence guarantees for SGD training, characterizes how the gating mechanism suppresses outliers and enforces a locality bias, and compares these results against linear Transformers to show Mamba's superior robustness when the outlier fraction exceeds $1/2$. The theoretical findings are supported by synthetic experiments, including an honest report of a discovered vulnerability (Mamba's performance degrades when outliers are placed closest to the query, due to the exponential-decay property).

## Strengths

- **First theoretical analysis of Mamba training dynamics for ICL (Section 3.3).** Prior theoretical work on Mamba/SSM-based models (Li et al., 2024b; 2025b) studied global minima, not training dynamics. This paper provides SGD convergence guarantees — a meaningful step forward. The characterization of how the outlier fraction $p_a$ scales the required iterations and context length is genuinely informative.

- **Clean decomposition of the Mamba mechanism (Equation 3).** The derivation showing that a one-layer Mamba (with $\mathbf{A}=-\mathbf{I}_m$) decomposes into a linear attention layer followed by a multiplicative gating layer $G_{i,l+1}(\mathbf{w})$ — a product of sigmoids over future positions — is a genuinely useful analytical insight. It makes the architecture tractable while retaining the distinguishing gating component.

- **Corollaries 1 and 2 provide concrete, interpretable mechanism claims.** These results characterize *how* the trained model works: attention scores concentrate on same-pattern examples (Corollary 1); gating suppresses outlier examples and enforces an exponential decay in importance with index distance from the query (Corollary 2). These go beyond "the model generalizes" to characterize the learned computation. The experimental validation in Figures 3 and 4 adds credibility.

- **Honest treatment of a discovered vulnerability (Table 1, CQ setting).** The paper reports that when outliers are placed closest to the query, Mamba's accuracy drops to 82.73% vs. the linear Transformer's 93.96%. This is a real vulnerability that follows directly from the exponential-decay property in Corollary 2, and the paper does not hide it. This is the kind of finding that makes a theoretical paper useful — it predicts a failure mode.

## Weaknesses

### Fatal
None.

### Major

- **The analyzed model is a substantial simplification of the full Mamba architecture, and the framing outstrips the technical scope.** The derivation (Equation 3) sets $\mathbf{A} = -\mathbf{I}_m$ and simplifies the selective scan mechanism, reducing the model to linear attention + a specific gating function. The paper acknowledges this assumption (Section 2) but frames its contribution throughout the title, abstract, and conclusions as being about "Mamba" without clearly delineating which components of the real architecture are retained and which are abstracted away. A reader familiar with Mamba (Gu & Dao, 2023) would reasonably ask whether the results reflect properties of the selective scan mechanism itself or the simpler gating that remains after the simplification. The paper should more clearly scope its claims to the specific simplified architecture analyzed and add a dedicated discussion of what is lost in the simplification.

### Minor

- **The comparison is against linear attention, not the softmax attention used in practice.** The paper is transparent about this (Remark 6 clarifies that the comparison isolates the effect of gating and notes that large Transformers with proper design can achieve robustness). However, the title's framing ("Can Mamba Learn in Context with Outliers?") sets up a general Mamba-vs-Transformer contrast that the linear-attention comparison alone does not fully support. The experiments also use only the linear-attention variant. A more explicit upfront caveat would prevent over-interpretation.

- **The comparison of sufficient conditions (Theorems 1 vs. 3) is informative but over-relied upon in the narrative.** The paper compares sufficient (not necessary) conditions for convergence, finding that the linear Transformer requires smaller batch sizes and fewer iterations. Since these are upper bounds whose tightness is not established, it is possible Mamba converges faster or Transformers slower than the bounds suggest. The paper acknowledges this is "common practice" and uses hedged language, but Contribution 2 and Section 3.1 (P2) lean on this comparison heavily. The experiments do show a clear empirical robustness gap, so the empirical claim is well-supported; the issue is how much weight the theoretical comparison of sufficient conditions should carry.

### Trivial
None.

## Nice-to-Haves

- Add an experiment where test outliers are orthogonal to the training outlier subspace to test the boundary of Theorem 2's Condition (a).
- Report how well the $\Theta(1/2^{j-1})$ bound fits the actual gating values in Figure 4 (e.g., a fitted decay rate).

## Removed Points

These points are flagged to be removed; treat them with caution.

- **"Test-time outlier condition is too restrictive"**: Removed because the paper explicitly states (Section 3.1, line 93) that test outliers must be "positive linear combinations" and discusses this in Remark 3. The condition is transparently presented; the restriction is inherent to the theoretical analysis.
- **"Experiments are entirely on synthetic data with the same data model"**: Removed because this is standard practice for theory papers in this area. The model's item weighting (−6.43) indicates this is not a valid weakness against a theory paper testing its own predictions.
- **"Missing proof sketches in main text"**: Removed because the paper explicitly states proof sketches exist in Appendix A. The parser strips appendices; the proofs exist in the original submission.
- **"Sensitivity to p_a = 0.6 choice" / "Gating decay quantification"**: Removed because these are nice-to-have ablations/suggestions, not actual weaknesses.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- Add a dedicated paragraph early in the paper listing which Mamba components are retained and which are abstracted away, explaining why the retained components are the ones responsible for outlier robustness. This would preempt the inevitable reader skepticism about whether the results apply to the actual Mamba architecture.
- State upfront in the introduction that the Transformer comparison is specifically against linear attention because it isolates the effect of gating, and that results for softmax-attention Transformers may differ.
- Add an experiment where test outliers are orthogonal to the training outlier subspace to test the boundary of Theorem 2's Condition (a).

## Score and Decision

The paper sits between the 4.00 anchor (52XG8eexal, SSM+ICL theory, Reject) and the 6.00–6.50 anchors (jwsPS8yRe4, n7n8McETXw, ikwEDva1JZ, clean ICL theory papers, Accept). Compared to the 4.00 anchor — which was criticized for limited novelty and disconnect from practice — our paper avoids the novelty concern (it provides the *first* training-dynamics analysis of Mamba for ICL) and has a cleaner theoretical contribution. Compared to the 6.00 anchor (jwsPS8yRe4, linear transformer ICL theory, Accept), our paper has comparable theoretical rigor and strength magnitude (heavy positives +5.40/+5.55 vs. +5.72; heaviest negatives −2.25/−2.71 vs. −2.70/−3.53), but has a more significant architecture simplification concern that prevents it from reaching the 6.5 level. The paper makes a genuine contribution — first training dynamics analysis for Mamba-style ICL, clean mechanism characterization, honest vulnerability reporting — but the framing gap between "Mamba" and the simplified model analyzed, combined with the linear-attention comparison scope, keep it at a borderline-accept level requiring framing revisions.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>