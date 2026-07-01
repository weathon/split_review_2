## Summary

This paper applies a null-model sanity check (following Adebayo et al., 2020) to SAE evaluation metrics: it compares auto-interpretability scores (fuzzing AUROC, detection AUROC), reconstruction metrics, and token distribution entropy across SAEs trained on trained transformers versus several randomized variants (Step-0, re-randomized incl./excl. embeddings, and a Gaussian-embedding control). Across Pythia models from 70M to 6.9B parameters, the paper finds that aggregate auto-interpretability scores for random variants are often surprisingly similar to those of trained models, particularly at larger scales, and can even exceed them—suggesting that high aggregate scores alone do not guarantee that learned, computationally meaningful features have been recovered.

## Strengths

- **Systematic null-model evaluation across model scale.** The paper compares five well-motivated randomization variants (trained, Step-0, re-randomized incl./excl. embeddings, Gaussian-embedding control) across Pythia models spanning 70M–6.9B parameters and multiple layers per model. This sweep is thorough and directly tests whether findings depend on model scale.

- **A genuinely non-obvious finding.** The result that for Pythia-6.9b the randomized variants score *higher* (AUROC 0.87–0.88) than the trained model (AUROC 0.79) on fuzzing auto-interpretability is striking and worth reporting. It goes beyond a simple "metrics are insensitive" story and suggests a systematic bias toward simpler features at scale.

- **Honest and bounded conclusions.** The body (Section 5 limitations, Section 6 conclusion) carefully states what the paper does *not* claim—it does not assert that SAEs on trained models fail to learn meaningful features, only that the aggregate metrics are insufficient to prove they have done so. The limitations section acknowledges the restricted model family and metric suite.

## Weaknesses

### Fatal

None.

### Major

1. **The title and abstract overclaim relative to the paper's own results.** The title states that metrics "do not distinguish trained and random transformers," but the paper's own numbers contradict an absolute reading:
   - For Pythia-70m, the paper acknowledges metrics *do* discriminate (Section 2, line 49: "auto-interpretability scores for randomized models were relatively low for smaller models").
   - For Pythia-6.9b, the trained AUROC (0.79) and randomized AUROC (0.87–0.88) are *different* values; the problem is that random models score *higher*, not that the metrics produce indistinguishable numbers.
   - The abstract itself says "in many settings," which conflicts with the absolutist title.
   
   The actual finding is more nuanced and more interesting: the metrics do not distinguish *in a direction that signals learned computation*, and this failure becomes more pronounced at larger scales. The title should reflect this. The body is appropriately measured, but the headline framing is misleading.

2. **No uncertainty quantification in the main figures.** The paper's central claim is a *negative* one (metrics fail to distinguish), which places a higher burden on demonstrating that the observed trained–random similarity is robust. The main figures (Figures 1–2) are line plots without error bars, confidence intervals, or per-latent distribution information. The paper samples 100 latents per SAE, yet the reader cannot assess overlap between trained and random latent-wise AUROC distributions visually. Appendix E is referenced for multiple random seeds, but the main text does not report whether patterns replicate across seeds with any measure of variability. Adding bootstrap confidence intervals, violin plots, or a permutation test comparing trained vs. random latent-wise AUROC distributions would substantially strengthen the evidential basis for the negative claim.

### Minor

3. **Only one SAE architecture is tested.** The paper uses TopK SAEs (Gao et al., 2024) exclusively, with robustness checks limited to varying expansion factor and sparsity on Pythia-160m (Figure 18). Other popular architectures (Gated SAEs, JumpReLU SAEs, standard L1-penalty SAEs) are not tested. This limits generalizability of the finding that "SAE evaluation metrics do not distinguish" to the specific architecture studied.

4. **Section 4 (toy model) is exploratory and loosely coupled to the main result.** The toy analysis (matrix multiplication preserves superposition; random MLP outputs have high sparsity; GloVe embeddings exhibit superposition) is explicitly described as speculative (line 131: "we leave the question of which predominates… to future work"). While not incorrect, this section reads as preliminary mechanistic speculation that the paper does not need to make its main point. Shortening or moving it to the appendix would focus attention on the cleaner empirical finding in Section 3.

5. **The CE loss score result is noted but its diagnostic value is underplayed.** The paper states (line 89) that CE loss score "only makes sense for the trained variant" because random models have inherently poor loss. This is technically correct, but the fact that CE loss *cannot be meaningfully computed* for random models is itself a distinguishing property that practitioners could use as a quick check. Discussing this as a positive finding (a functionally grounded metric that automatically filters out null models) would make the paper more actionable.

### Trivial

None.

## Nice-to-Haves

- Add error bars, bootstrap confidence intervals, or per-latent distribution plots (violin plots, scatterplots) to the main figures, and report whether the observed trained–random similarity replicates across multiple random seeds with a quantitative test.
- Provide more specific practical guidance: how many random seeds? how many latents to sample? what threshold of similarity should trigger concern about a metric's informativeness?
- The qualitative examples in Appendices J/L are noted but could be brought into the main paper to strengthen the argument that random-model latents are qualitatively different despite similar aggregate scores.

## Removed Points

The following criticisms from the input review were removed after verification against the paper:

- **"Control condition is a weak comparator that inflates apparent informativeness"** — The paper uses the control as a floor (chance-level baseline) and explicitly defines it as such. The control serves a standard purpose in null-model testing. The meaningful comparison is between trained and non-control randomized variants, which the paper also provides. This criticism overstates the framing issue.
- **"No solution offered"** — The paper is scoped as an empirical sanity check, not a solution paper. The contribution is the finding itself and the recommendation for routine baselines. Criticizing the absence of a complete replacement metric is outside the paper's stated scope.
- **"No qualitative analysis of random-model latents"** — The paper explicitly references Appendix J ("a random sample of features and the corresponding maximally activating dataset examples for each variant") and Appendix L. The parser strips appendices, but the paper does address this.
- **"CE loss score distinguishes and should be a positive finding"** (strong version) — The paper correctly explains that CE loss is not meaningful for random models because their base loss is already at ceiling. The metric does not "cleanly separate" trained from random in the expected way (it simply cannot be computed). A weakened version of this point is retained as Minor weakness #5.
- **Section-by-section notes about framing and related work** that duplicate the major weakness about the title or are editorial in nature.

## Novel Insights

None beyond the paper's own contributions. The input review did not surface a genuinely novel observation that the paper itself misses.

## Suggestions

1. **Revise the title** to reflect the actual finding, e.g., "Aggregate Auto-Interpretability Metrics Do Not Reliably Distinguish Trained from Random Transformers" or "Automated Interpretability Metrics Fail as Evidence of Learned Computation at Scale."
2. **Add error quantification** to all main figures: bootstrap confidence intervals on AUROC values or per-latent scatterplots showing the distribution overlap between trained and randomized variants. Report a quantitative test (e.g., permutation test) comparing trained vs. random latent-wise AUROC distributions.
3. **Discuss the CE loss score more prominently** as a functionally grounded metric that automatically detects when the underlying model is not learned—this is useful practical guidance.
4. **Acknowledge the SAE architecture limitation** more explicitly and note that the findings may not generalize to other SAE variants.

## Score and Decision

The paper performs a useful and timely sanity check with a systematic experimental design. The core finding—that aggregate auto-interpretability metrics can give high scores to SAEs on random transformers, especially at scale—is real, non-obvious, and relevant to the community. However, the title overstates the finding (the metrics *do* produce numerically different values; the issue is more nuanced), and the main figures lack uncertainty quantification, which weakens the evidential basis for a negative claim. Neither issue is fatal, and both are addressable. The paper's contribution is solid but not exceptional.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>