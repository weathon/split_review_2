Now I have all the calibration data I need. Let me write the final consolidated review.

## Summary

This paper applies the Adebayo et al. randomization sanity check to sparse autoencoder (SAE) evaluation. The authors train TopK SAEs on Pythia models (70M–6.9B parameters) across five model variants (trained, Step-0 initialization, re-randomized with/without embeddings, and a noise control) and find that aggregate auto-interpretability metrics (primarily fuzzing AUROC) and reconstruction metrics can be surprisingly similar between trained and randomly initialized transformers, particularly at larger model scales. The paper also proposes token distribution entropy as a complementary measure that does reveal qualitative differences between trained and random models.

## Strengths

1. **Well-motivated and timely sanity check.** Applying the randomization test (Adebayo et al., 2020) to SAE evaluation is a natural and overdue methodological contribution. The paper frames this clearly (Section 1) and connects it to a concrete gap in current practice.

2. **Carefully designed null variants.** The paper uses three distinct randomization schemes (Step-0, re-randomized including embeddings, re-randomized excluding embeddings) plus a noise control. The "re-randomized including embeddings" variant (matching weight distribution statistics of the trained model) is a particularly strong null that rules out trivial explanations (Section 3, lines 53–60).

3. **Multiple model scales reveal an important interaction with model size.** Testing five Pythia sizes (70M–6.9B) shows that the metrics distinguish trained from random at smaller scales but the gap narrows at larger scales (line 49; Figure 2). This is more informative than a single-model study and gives the negative result a precise scope.

4. **Token distribution entropy analysis is a genuine positive contribution.** The entropy analysis (Section 3, lines 91–127) identifies a dimension—feature abstractness as measured by token-specificity—that aggregate AUROC misses, and successfully shows that trained models develop more abstract features in later layers while random models do not. This provides a concrete starting point for better evaluation, not just a critique.

5. **Measured and honest conclusions.** The paper carefully states (line 179): "This result does not imply that SAEs trained on real models fail to learn meaningful computational features." The recommendations (routine randomized baselines, measures of abstractness) follow from the evidence.

## Weaknesses

### Fatal
None.

### Major

1. **The title overclaims the scope of the negative result.** The title states categorically that metrics "Do Not Distinguish" trained from random transformers. However, the paper's own text (line 49) says: "we found that auto-interpretability scores for randomized models were relatively low for smaller models (e.g., Pythia-70m) but that the gap was narrowed for larger models (e.g., Pythia-6.9b)." This means the metrics *do* distinguish trained from random at the 70M scale. The evidence supports a more nuanced claim: metrics distinguish at smaller scales but fail at larger ones. The title should reflect this scale-dependency. The abstract's "in many settings" partially mitigates this, but the categorical title is not matched to the paper's own data.

2. **Only classification-based auto-interpretability (fuzzing/detection) is tested; simulation scoring is not examined.** The paper uses fuzzing scoring (Paulo et al., 2024) as its primary auto-interpretability measure, justified by its correlation with simulation scoring (line 77). But the paper's scope claims are about "auto-interpretability metrics" broadly. If simulation scoring (Bills et al., 2023)—the gold standard that fuzzing was designed to approximate—were to distinguish trained from random models, the paper's recommendation would change from "auto-interpretability metrics are insufficient" to "use the more expensive simulation scoring." The paper does not test this possibility or sufficiently limit its claims to classification-based proxies. Since fuzzing is explicitly a cheaper approximation of simulation scoring, this gap weakens the generality of the conclusion.

### Minor

1. **Single SAE architecture (TopK) tested.** The paper uses only TopK SAEs with expansion factor 64 and sparsity k=32 (line 73). No other SAE architectures are tested (e.g., Gated SAEs, JumpReLU SAEs, standard L1-penalized SAEs), which are known to learn qualitatively different latent spaces. The paper acknowledges this indirectly in Limitations (line 173) but the title and abstract do not reflect this scope constraint.

2. **No confidence intervals or error bars on the main AUROC results.** The paper samples 100 features per SAE (line 77) and reports point estimates without variance measures in the main figures. For a negative-result paper where the argument depends on the *similarity* of values between trained and random models, uncertainty quantification is especially important. The paper mentions "Appendix E for multiple random seeds" (line 67), but the main text does not establish whether the observed patterns are statistically reliable.

3. **Randomized variants scoring *higher* than trained on AUROC is not discussed.** Figure 1 shows randomized variants achieving AUROC of 0.87–0.88 compared to 0.79 for the trained model. This is arguably stronger evidence that the metric is broken than mere similarity, but the paper reports this without analysis or discussion.

### Trivial
None.

## Nice-to-Haves

- Testing at least one alternative SAE architecture (e.g., Gated SAE or JumpReLU SAE) would strengthen the claim that the phenomenon is not specific to TopK.
- A systematic qualitative comparison of features from trained vs. random models beyond anecdotal examples (entropy is a coarse proxy; direct categorization would strengthen the claim that random-model features are simpler).
- The toy model section (Section 4) is somewhat disconnected from the main empirical contribution and could be condensed.

## Removed Points

The following points from the input review were filtered out:

- **"Fuzzing scoring vs. auto-interpretability broadly" as a fatal issue**: Downgraded from a critical issue to Major weakness #2. The paper is transparent about using fuzzing (line 77) and justifies the choice by correlation with simulation scoring. However, the scope overclaim in the title is real, and the failure to test simulation scoring is a gap — hence Major, not Fatal.

- **"Only 100 latents sampled" as a major concern**: Downgraded to Minor (weakness #2 under Minor). The paper checks multiple random seeds in the appendix, partially addressing this concern. The lack of confidence intervals in the main text is the real issue.

- **"No quantitative comparison beyond entropy"**: Removed. The entropy analysis IS the quantitative comparison the paper provides. A categorization of feature types would be a nice-to-have, not a required analysis.

- **"SAE quality on random models not discussed"**: Removed. The CE loss score is reported (line 89) and the paper explicitly notes it only makes sense for the trained variant.

- **Missing related works**: Removed per instructions (cannot confirm existence of external references).

- **Formatting/style nitpicks and reproducibility complaints about undisclosed hyperparameters**: Removed per instructions.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Revise the title to reflect the scale-dependency of the finding, e.g., "At Scale, Automated Interpretability Metrics Do Not Distinguish Trained and Random Transformers" or add a qualifying subtitle.

2. Add confidence intervals or error bars to the main AUROC figures, or move the multiple-seed analysis from the appendix into the main text.

3. Discuss why randomized variants score *higher* than trained models on AUROC (Figure 1). This is a striking result that strengthens the indictment and deserves analysis.

4. Either test simulation scoring on a subset of latents, or explicitly scope the title/abstract to "classification-based auto-interpretability proxies (fuzzing, detection)."

5. Consider foregrounding the token distribution entropy finding more prominently, as it is the paper's most constructive and actionable contribution.

## Score and Decision

**Round 1 bracket (initial):** Based on the anchors retrieved and inspected, the plausible score range for this paper is **5.5–6.5**.

**Calibration anchors used (all rounds):**

| Anchor Paper | Path | Avg Score | Round | Comparison |
|---|---|---|---|---|
| *Why Sanity Check for Saliency Metrics Fails?* | Pev2ufTzMv.md | 3.75 | R1 | Similar theme (sanity check for interpretability metrics) but weaker experiments; tested on image classifiers with Gaussian blur, not LLMs or SAEs. Our paper is substantially stronger. |
| *Examining Why Perturbation-Based Fidelity Metrics are Inconsistent* | HNJJEWfo0Z.md | 3.75 | R1 | Similar theme, rejected for weak methodology. Our paper has far better experimental design. |
| *Interpretable Patterns in Random Initialization* | bWT6OBJ71x.md | 4.40 | R1 | Related topic (random initialization patterns) but limited to algorithmic toy tasks. Our paper tests on real LLMs at scale. |
| *Metric-Driven Attributions for Vision Transformers* | rGP2jbWt0l.md | 5.25 | R1 | Accepted paper with mixed reviews (3,6,6,6). Comparable score range. |
| *Benchmarking Deletion Metrics* | bXeSwrVgjN.md | 6.00 | R2 | Similar approach (benchmarking existing metrics). Rejected despite 6.0 due to polarized reviews. Our paper has less polarization risk. |
| *Towards Principled Evaluations of SAEs* | 1Njl73JKjB.md | 7.00 | R1 | Strong SAE evaluation paper with novel framework. Our paper has weaker positive contribution but similarly rigorous experiments. |
| *SAEs Do Not Find Canonical Units* | 9ca9eHNrdH.md | 7.00 | R1 | Negative-result SAE paper with novel techniques (stitching, meta-SAEs). Our paper has less methodological novelty. |
| *Scaling and Evaluating Sparse Autoencoders* | tcsZt9ZNKD.md | 8.20 | R2 | Major positive contribution (scaling laws, new SAE variant). Far stronger than our paper. |

**Narrowing:** The paper is clearly stronger than the 3.75–4.40 papers (real LLMs vs. image perturbations or toy tasks), placing it above the reject range. It is weaker than the 7.0–8.2 papers (less methodological novelty, overbroad title, narrower SAE scope). Within the 5–7 band, the paper's main weaknesses (overclaimed title, single SAE architecture, no simulation scoring test) are significant but fixable, while its strengths (careful null design, multiple scales, entropy analysis) are genuine. This places it at **6.0** — borderline accept.

**Final score:**
MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>