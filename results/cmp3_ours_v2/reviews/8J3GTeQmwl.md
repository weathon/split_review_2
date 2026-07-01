## Summary

This paper introduces CV-imputation, a novel K-fold cross-validation procedure for tuning parameter selection and model selection in graphon models. The key innovation is replacing held-out edges with random Bernoulli draws rather than costly matrix completion (as in the existing ECV method), then applying an affine correction (Equation 6) to recover the original probability matrix estimate. The method is supported by an asymptotic consistency result (Theorem 1) and demonstrated on both synthetic and real networks, showing substantial speedups (4×–25×) over ECV.

## Strengths

- **Novel and conceptually elegant core idea.** Replacing held-out edges with random imputation rather than costly matrix completion is an original approach. The linear correction in Equation (6) follows cleanly from Lemma 1, and the resulting procedure avoids the low-rank assumption that limits ECV.

- **Clear and well-demonstrated computational advantage.** Table 2 shows dramatic speedups on real networks (e.g., 56.9s vs. 258.7s for PolBlog, 51.0s vs. 771.2s for NetSci, 240.9s vs. 6021.1s for Yeast). The complexity analysis in Section 3 correctly identifies the source (eliminating O(n³) matrix completion per fold). This is the paper's strongest concrete contribution.

- **Reasonable evaluation scope for a methods paper.** Four graphon types varying in density and rank, four estimation methods (NS, USVT, SAS, ICE), multiple network sizes (n=50–200), and four real networks. The COVID-19 ledipasvir case study provides an interesting real-world validation, including a link prediction later corroborated by clinical research.

- **Theoretical support for consistency.** Theorem 1 shows that the CV-imputation score is asymptotically parallel to the estimation error up to a constant, establishing that model selection via CV-imputation is consistent.

## Weaknesses

### Fatal

None.

### Major

None.

### Minor

- **Overstated claim about default selection, contradicted by Table 1.** The paper states that "our method and ECV select M resulting in lower MSE values compared to the default selection" (line 155). However, Table 1 shows a counterexample: on Graphon 3 with NS, the default (M=1) achieves MSE 0.74 ± 0.04, while CV-imputation (NS) achieves 0.79 ± 0.07 — the default outperforms CV-imputation. While this is one of many comparisons, the blanket assertion is inaccurate and should be qualified.

- **Conditional theoretical result with limited instantiation.** Theorem 1 requires Condition 1 (Q_K(M) = O_p(K^{-α}) for some α > 0), which is verified only for the trivial Erdős–Rényi case (α = 1) with a simple averaging estimator — not for NS, SAS, USVT, or ICE on the four graphon types used in experiments. The paper notes that Q_K(M) "can be verified computationally" and defers to Figure S.3 in the appendix, but the main text does not establish this condition for the actual settings where the method is applied. This weakens the theoretical contribution from a guarantee to a conditional statement.

- **Choice of the imputation parameter θ is deferred entirely to the appendix.** The paper states that "the selection of θ is discussed in Section S.4" (line 63) without stating the default value or any sensitivity analysis in the main text. Since θ controls the distribution of imputed values and is a tunable parameter of the method itself, this is a notable gap.

- **ECV comparison raises unanswered questions.** Several results in Table 1 warrant discussion that the paper does not provide: ECV(NS) on Graphon 1 has MSE 9.15 ± 19.25 (standard deviation more than double the mean, suggesting extreme instability or implementation issues); ECV(USVT) on Graphon 1 produces exactly the same MSE as Default USVT (0.60 ± 0.09), suggesting it may be selecting the same hyperparameter rather than a different one via CV. The paper does not clarify whether the ECV implementation is original code from Li et al. (2020a) or a reimplementation, making it difficult to assess comparison fairness.

- **Text says "five estimation methods" (line 155) but only four (NS, USVT, SAS, ICE) are listed.** This is a minor but noticeable inconsistency.

### Trivial

- **Figure 3 caption contains "In all cases, ECV is faster than CV-imputation"** — this directly contradicts the body text (line 173) and Table 2 data. This appears to be a parser artifact from the figure image caption rather than an author error, but it creates confusion.

## Nice-to-Haves

- **Sensitivity analysis for θ in the main text.** Even a short paragraph showing results are stable for θ in a reasonable range (e.g., global edge density ± some offset) would address a key methodological concern.
- **Uncertainty quantification for the 100% accuracy claim** in model selection (Figure 5). Reporting confidence intervals or variance across replications would strengthen this result.
- **An "oracle" baseline** showing the gap between what CV-imputation achieves and the theoretically optimal M (the one minimizing MSE on the true P) would help calibrate the method's performance ceiling.
- **A brief discussion of why CV-imputation can outperform ECV despite using random noise imputation** — this is counterintuitive and warrants explicit intuition.

## Removed Points

These points are flagged to be removed; treat them with caution:

1. **Issue about estimators failing on noise-corrupted training data (Harsh Critic Issue 1).** REMOVED because it misunderstands the math. Lemma 1 establishes that A^{[-k]} has entries ~ Bernoulli(P^{[-k]}_{ij}), where P^{[-k]} = w_kθ11^T + (1−w_k)P. Since P is a smooth graphon, the affine-transformed P^{[-k]} is also a smooth graphon — the training matrix IS generated from a valid graphon model. Standard graphon estimators designed for graphon-structured data apply directly to A^{[-k]} because it comes from the same model class (just a different graphon). This is not a structural gap.

2. **"No comparison to AIC/BIC variants or other model selection approaches."** REMOVED as scope creep. The paper targets CV methods for graphon tuning; ECV is the direct and natural competitor. Demanding comparisons to AIC/BIC variants for network models goes beyond the paper's stated scope.

3. **"Default baselines are weak."** REMOVED. The defaults (NS M=1, USVT M=0.01, SAS M=⌊n/log n⌋) are standard choices from the respective methods' literature. Using them as baselines is standard practice, not a weakness.

4. **"Table 1 MSE×100 inflates small differences."** REMOVED — this is a presentation choice; all comparisons use the same scaling and are directly comparable.

5. **"CV-imputation uniformly beating ECV is suspicious/counterintuitive."** REMOVED as speculative. The paper demonstrates the results; the fact that CV-imputation outperforms ECV is an empirical finding, not a weakness. The reviewer's suspicion does not constitute evidence of a problem.

## Novel Insights

The harsh critic raises a genuinely interesting methodological question about whether the training matrix after random imputation preserves the structural properties that graphon estimators rely on. While this particular concern turns out to be unfounded (as analyzed above — the training matrix IS a valid graphon model), the question of how different imputation distributions (θ) interact with different estimators' finite-sample behavior is a potentially fruitful direction that the paper does not explore. Additionally, the observation that CV-imputation can outperform ECV despite using a seemingly cruder imputation strategy is counterintuitive on its face; an explanation rooted in the mismatch between ECV's low-rank assumptions and the actual graphon rank would strengthen the paper's narrative.

## Suggestions

- Correct the blanket claim on line 155 to acknowledge that default selection occasionally matches or outperforms CV-imputation (e.g., Graphon 3 with NS).
- Add 1–2 sentences in Section 3 stating the default choice of θ (presumably the global edge density) and noting that results are robust to reasonable variations.
- Provide more detail on the ECV implementation: is it the original authors' code or a reimplementation? How were hyperparameter grids matched?
- Fix the "five estimation methods" → "four estimation methods" inconsistency on line 155 and the Figure 3 caption error.
- Add error bars or confidence intervals to the 100% accuracy claim for model selection (Figure 5).

## Score and Decision

**Initial bracket (Round 1):** Based on comparison with calibration anchors — papers scoring 5.5–6.0 typically have a clear novel contribution but some overclaimed results, limited theoretical instantiation, or presentation gaps. The current paper fits this profile: the core idea is genuinely novel and the computational advantage is strong, but the theoretical result is conditional, one empirical claim is contradicted by the paper's own data, and several presentation issues remain.

**Round 2 narrow:** Comparing against the 6.0 paper (Causal Graph Transformer, avg score 6.0, all scores 6) and the 5.25 paper (Hyperparameter Selection in Graph SSL, avg 5.25, mixed scores): the current paper has a stronger empirical component than the 5.25 paper (which was criticized for limited experiments), and its core methodological contribution is clearer than the 5.25 paper's contribution. However, it has one direct empirical inaccuracy (the default-beating claim) that the 6.0 paper did not have. The paper sits most naturally at the boundary between these two anchors.

**Anchors considered:**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| Uj0h13lVrR (GFlowNets) | 1.00 | 1 | Far weaker; fundamentally flawed methodology |
| Aku2I3z4aV (Intra-fused GW) | 2.60 | 1 | Weaker; lacks empirical validation |
| Ivk2j3uRYh (Random Graph Asymptotics) | 4.50 | 1 | Comparable novelty but weaker empirical scope |
| gqC0egRfWq (Hyperparam Selection in Graph SSL) | 5.25 | 1 | Stronger theory but much weaker experiments; unclear positioning |
| **Current paper** | **6.0** | — | Clear novel method, good experiments, minor overstatements |
| xljPZuprBA (Edge Probability Graph Models) | 5.75 | 1+2 | Similar score; had validation/comparison gaps, rejected |
| foQ4AeEGG7 (Causal Graph Transformer) | 6.00 | 2 | Similar quality; accepted with minor concerns about scope |
| SjufxrSOYd (Invariant Graphon Networks) | 8.00 | 1 | Stronger; fully rigorous theoretical paper, no experiments |
| uwzyMFwyOO (Latent Graph Structures) | 5.60 | 1+2 | Weaker; oversimplified graph structures, limited practicality |

**Final score:** 6.0 — a solid methods paper with a genuinely novel contribution and clear computational advantages, held back from a higher score by (a) an overclaimed result contradicted by the paper's own data, (b) a conditional theoretical result whose key rate condition is only instantiated for a trivial case, and (c) several presentation gaps (θ selection, ECV implementation detail). These issues are addressable and do not undermine the core contribution.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>