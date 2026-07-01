Now I have sufficient calibration information. Let me write the final consolidated review.

**Bracket Analysis (Round 1):**
Based on calibration, the paper is most comparable to:
- "Towards Best Practices of Activation Patching" (6.67, accepted) - similar empirical evaluation of interpretability methodology
- "Interpretability Illusions in Generalization of Simplified Models" (5.60, rejected) - similar negative finding about interpretability
- "Is This the Subspace You Are Looking For?" (6.33, accepted) - similar "sanity check" revealing illusion
- "Don't trust your eyes" (7.00, rejected) - similar reliability check on interpretability methods

Initial bracket: **5.5–7.0**

After narrowing against these anchors, I place this paper at **6.0** — slightly below the activation patching paper due to the absence of error bars on central similarity claims and the overclaiming title, but slightly above the "Interpretability Illusions" paper due to broader experimental coverage.

Here is the final review:

## Summary
This paper applies Adebayo et al.'s null-model sanity check to SAE evaluation metrics. By training SAEs on trained vs. randomly initialized Pythia transformers (70M–6.9B parameters) and comparing auto-interpretability scores and reconstruction metrics, the authors find that several aggregate metrics produce surprisingly similar results across trained and randomized models, especially for larger models. The paper also explores potential explanations through toy models and proposes token distribution entropy as a preliminary alternative measure.

## Strengths
1. **Important and timely question.** SAE-based interpretability has become a major subfield, and the field relies heavily on aggregate auto-interpretability scores without systematic null-model validation. This paper performs exactly that missing check.

2. **Well-designed experimental sweep.** The paper covers five model variants (trained, step-0, re-randomized incl./excl. embeddings, Gaussian control), five model sizes (70M–6.9B), multiple layers per model, and multiple evaluation metrics (AUROC fuzzing/detection, explained variance, cosine similarity, L1 norm, CE loss score, token entropy). This breadth supports the conclusions.

3. **Gaussian control condition is well-chosen.** It confirms the evaluation pipeline is not broken: metrics correctly show chance-level performance (AUC ≈ 0.50) when all structure is removed from inputs, isolating the problem to metrics failing to distinguish trained vs. randomized models.

4. **Honest about limitations.** Section 5 explicitly states the paper does not claim SAEs fail to learn meaningful features. The conclusion is measured: "High aggregate auto-interpretability scores are insufficient proof for the discovery of complex, learned computations."

5. **Token distribution entropy analysis is a useful proof-of-concept.** It reveals differences in feature abstractness that aggregate auto-interpretability scores miss, pointing toward a concrete direction for better metrics.

## Weaknesses

### Fatal
None.

### Major
1. **Title overclaims relative to evidence.** The title states metrics "DO NOT DISTINGUISH trained and random transformers," but the paper's own results show that for smaller models (Pythia-70m) "auto-interpretability scores for randomized models were relatively low" (line 49), token distribution entropy does distinguish, and the Gaussian control is clearly separated. The abstract appropriately qualifies with "in many settings," but the title is an unqualified absolute that contradicts parts of the paper's evidence.

2. **No error bars, confidence intervals, or variance measures on central results.** The paper's core claim is that trained and randomized models produce *similar* scores. Establishing similarity (near-equivalence) requires showing the difference is small relative to measurement variability. The main figures (Figures 1, 2) are single lines without any indication of variance. Appendix E is referenced for "multiple random seeds" but the primary visual evidence lacks measures of variability. Without this, the reader cannot assess whether the apparent similarity would replicate across random seeds, data subsets, or SAE training runs. This is a structural evidential gap for a paper whose conclusion rests on establishing similarity.

### Minor
3. **The randomized models *outscoring* the trained model on auto-interpretability is under-discussed.** For Pythia-6.9b, randomized variants achieve AUROC of 0.87–0.88 while the trained model achieves 0.79 (line 63–65). The paper mentions this in the figure caption but does not analyze why random-model latents score *higher* on auto-interpretability than trained-model latents. This is arguably the most provocative finding and deserves deeper analysis — it suggests the metrics may be biased toward simpler features.

4. **CE loss score is dismissed without supporting evidence.** The paper states CE loss "only makes sense for the trained variant" (line 89) and does not plot it for randomized models. The authors may be correct that the CE loss ratio is not meaningful when the base loss is extremely high for random models, but this is asserted without supporting data. The paper would be stronger by either showing the CE loss for random models or explaining concretely why it cannot meaningfully be computed.

5. **No analysis of individual latent score distributions.** The paper relies on aggregate AUROC but does not examine the distribution of individual latent interpretability scores. Trained models may produce a mix of high- and low-scoring latents that average to the same mean as random models, but with very different structure (e.g., a long tail of abstract features). Examining this would strengthen the argument.

6. **The introduction presents the toy model explanation with more confidence than the evidence supports.** Section 4 is appropriately framed as exploratory ("we leave the question... to future work," line 131). However, the introduction states that "a randomly initialized network still performs a basic form of computation, such as preserving or amplifying the sparse structure of its inputs (Section 4)" (line 17) with more confidence than the speculative toy experiments in Section 4 warrant.

7. **Limited SAE architectural scope.** Only TopK SAEs (expansion factor 64, k=32) are tested. While hyperparameter variations are explored (Figure 18), the findings are not validated on Gated SAEs, JumpReLU SAEs, or other commonly used SAE variants.

### Trivial
8. **Section 4.1's claim that matrix multiplication preserves superposition is a straightforward linear algebra observation.** The paper presents this as a "simplified model" when it is simply the observation that a linear transformation of a superposed representation remains superposed. This does not affect the paper's main contribution.

## Nice-to-Haves
- Validate the token distribution entropy measure against human judgments of feature abstractness or against known examples from the literature.
- Provide a systematic categorization of feature types learned by each model variant (beyond qualitative examples).
- Show CE loss score for all model variants to concretely demonstrate why the metric is not meaningful in the random setting.

## Removed Points
- **"Toy model section does not explain the main results" (Harsh Critic #5):** The paper consistently frames this section as speculative and explicitly defers conclusions to future work (line 131). This is a scope choice honestly acknowledged by the authors, not a flaw.
- **"Should mention model-size dependence in abstract":** The abstract already says "in many settings," which captures the nuance. The title is the real problem.
- **Criticism that CE loss "clearly separates" trained from random:** The critic assumes a result not shown in the paper. The paper does not compute CE loss for random models; it merely states the base loss is very poor. This is a weakness in the paper's evidence, not a factual error.
- **"Missing related works":** Excluded per protocol — cannot verify existence of cited works.

## Novel Insights
The reviews' key insight beyond the paper itself is that the finding where random models *outscore* trained models on auto-interpretability (Figure 1, Pythia-6.9b: 0.87–0.88 vs. 0.79) is the paper's most provocative result but is under-analyzed. The paper treats this as "similarity" when the direction of the gap (random > trained) raises fundamentally different questions than simple failure to distinguish. Understanding why auto-interpretability favors simpler, random-model latents — perhaps because the LLM judge finds them easier to classify — could be more informative than the paper's focus on aggregate score similarity.

## Suggestions
1. Add error bars, confidence intervals, or bootstrapped variance to Figures 1 and 2.
2. Revise the title to match the evidence (e.g., "Aggregate Auto-Interpretability Metrics May Not Reliably Distinguish Trained and Random Transformers").
3. Deeply analyze why random models achieve *higher* AUROC than trained models in Figure 1 — this could be the paper's most impactful finding.
4. Either show CE loss scores for all model variants or explain concretely why the metric is not meaningful for random models.
5. Include a distributional analysis of individual latent scores rather than only aggregate AUROC.

## Calibration Anchors
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/Hf17y6u9BC.md` — 6.67 — "Towards Best Practices of Activation Patching" — accepted; similar systematic empirical evaluation of interpretability methods, but has clearer recommendations and better statistical rigor
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/9ca9eHNrdH.md` — 7.00 — "Sparse Autoencoders Do Not Find Canonical Units" — accepted; more methodologically novel with SAE stitching/meta-SAEs
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/v675Iyu0ta.md` — 5.60 — "Interpretability Illusions" — rejected; similar negative finding about interpretability but narrower scope
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/OZWHYyfPwY.md` — 7.00 — "Don't trust your eyes" — rejected despite high scores; similar sanity check on visualizations
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/Ebt7JgMHv1.md` — 6.33 — "Is This the Subspace You Are Looking For?" — accepted; similar "illusion" paper
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/1Njl73JKjB.md` — 7.00 — "Towards Principled Evaluations of SAEs" — accepted; more methodologically refined SAE evaluation framework
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/tcsZt9ZNKD.md` — 8.20 — "Scaling and evaluating sparse autoencoders" — accepted; landmark paper with architectural contributions
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/F76bwRSLeK.md` — 4.80 — "Sparse Autoencoders Find Highly Interpretable Features" — accepted but controversial
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/ZtvRqm6oBu.md` — 5.25 — "Applying SAEs to Unlearn Knowledge" — rejected; narrower applied contribution
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/bXeSwrVgjN.md` — 6.00 — "Benchmarking Deletion Metrics" — rejected; similar evaluation-focused paper
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/4ikjWBs3tE.md` — 6.75 — "Transformers Learn Low Sensitivity Functions" — accepted; similar empirical characterization

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>