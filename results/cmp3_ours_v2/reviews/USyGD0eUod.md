Now let me finalize my review incorporating the calibration insights.

**Calibration Bracket:**

Round 1 bracket: **5.5–6.5**. This paper is a solid empirical paper about an important negative result in mechanistic interpretability, but it has framing issues (overbroad title) and some methodological gaps (no uncertainty quantification). 

Comparing anchors:
- **"Sparse Autoencoders Do Not Find Canonical Units of Analysis"** (7.00): More novel methodology (stitching, meta-SAEs), more precise claims, stronger evidence. The current paper has less methodological novelty but addresses an equally important question with thorough experiments.
- **"Residual Stream Analysis with Multi-Layer SAEs"** (6.50): Clear contribution, well-executed. The current paper is comparable in execution but has framing issues the anchor does not.
- **"Compute Optimal Inference..."** (4.67, rejected): Had theory-practice gap and limited real LLM experiments. The current paper is empirically stronger.
- **"Sparse Autoencoders Find Highly Interpretable Features"** (4.80): Mixed reviews due to lack of novelty concerns. The current paper's negative finding is more novel.

Final score: **6.0** — borderline accept. The paper has a genuine, important contribution (systematic failure of auto-interpretability AUROC under randomization) but needs framing corrections and stronger uncertainty evidence.

Here is my final review:

---

## Summary

This paper applies the Adebayo et al. (2020) "randomization sanity check" to sparse autoencoders (SAEs), testing whether common SAE evaluation metrics can distinguish trained transformers from randomly initialized ones across Pythia models (70M–6.9B parameters). The authors find that fuzzing-based auto-interpretability AUROC and several reconstruction metrics show surprising similarity between SAEs trained on random vs. trained transformers, especially at larger scales, while token distribution entropy does reliably distinguish the two. The paper also provides toy models exploring why random networks may preserve superposition structure.

## Strengths

1. **Important and timely question** — The paper is the first systematic, large-scale test of whether commonly used SAE evaluation metrics pass the randomization sanity check. This has direct stakes for how the mechanistic interpretability community interprets auto-interpretability scores.

2. **Thorough experimental design** — The use of four distinct null conditions (Step-0, re-randomized excl. embeddings, re-randomized incl. embeddings, Gaussian control) is a strength. The finding that parameter-norm-matched re-randomized variants produce metrics more similar to the trained model than Step-0 is itself illuminating and would have been missed with a single random baseline.

3. **Scale analysis reveals a real trend** — Testing across Pythia 70M–6.9B and showing the trained-vs-random gap narrows at larger scales is a genuine finding. It explains the apparent contradiction with Bricken et al. (2023) (who found discrimination on one-layer transformers) and suggests the failure is scale-dependent.

4. **Token distribution entropy as a constructive alternative** — The paper does not merely critique existing metrics. The entropy analysis (Figure 2, last row) shows trained models trend upward with layer depth while randomized variants remain flat or lower, demonstrating that a targeted measure of feature *abstractness* succeeds where aggregate auto-interpretability fails. This points the field toward a productive direction.

## Weaknesses

### Major

1. **Title and headline claims overreach the evidence.** The title reads "AUTOMATED INTERPRETABILITY METRICS DO NOT DISTINGUISH TRAINED AND RANDOM TRANSFORMERS," but the paper's own results show a more nuanced picture. Token distribution entropy (Figure 2, row 7) *does* clearly distinguish trained from randomized models (trained entropy increases with depth; randomized variants remain flat or lower). The AUROC plots show trained and Step-0 "often achieving higher AUROC values" than other randomized variants (line 106). Reconstruction metrics show a mixed rather than uniformly null picture. The CE loss score cannot even be computed for randomized models. The paper's most precise finding concerns fuzzing/detection auto-interpretability AUROC specifically; the title should reflect this scope. While the entropy analysis is discussed in the text, its existence contradicts the blanket claim in the title.

2. **No uncertainty quantification for the central quantitative result.** Auto-interpretability scores are computed from 100 randomly sampled latents per SAE (line 77) — a tiny fraction of potentially ~640K latents for a large SAE (expansion factor 64 × ~10K-dimensional residual stream). The paper reports AUROC values (e.g., trained: 0.79 vs. randomized: 0.87 for Pythia-6.9B at layer 1) without confidence intervals, standard errors, or per-latent score distributions. The paper cites "Appendix E for multiple random seeds," but the main results lack any measure of within-SAE variance. If the 100 latents are sampled from a diverse set, the variance could be substantial, and the reader cannot assess whether the aggregate similarity is uniform across latents or driven by a specific subpopulation.

### Minor

3. **The toy model analysis (Section 4) does not cleanly connect to the central empirical puzzle.** The paper shows that random NNs can preserve or amplify superposition, which provides a plausible high-level mechanism. However, this does not explain the paper's most striking specific result: auto-interpretability AUROC is *higher* for random models (0.87) than trained (0.79) at the 6.9B scale. If random networks merely preserve superposition, metrics should be similar, not higher. The entropy analysis suggests a mechanism (random models produce more token-specific, narrowly-activating features that are easier to explain), but this is not carried through the toy models. The paper acknowledges this gap (line 131: "we leave the question of which predominates… to future work"), which is honest but leaves a key question unresolved.

4. **Limited discussion of how randomization procedure affects results.** The re-randomized variants preserve first and second moments of the trained weight matrices but not higher-order structure (e.g., correlations between weights, low-rank structure). A close match between trained and randomized metrics is partly expected if metrics are sensitive primarily to activation scale and variance rather than learned structure. The paper could strengthen its argument by discussing whether alternative procedures (e.g., weight permutation, which preserves the full empirical distribution) would produce similar results.

5. **Only TopK SAEs (k=32, expansion factor 64) used in the main experiments.** Robustness checks are limited to Pythia-160m (Figure 18). It is unclear whether the findings generalize to other widely-used SAE variants (Gated SAEs, JumpReLU SAEs, etc.).

### Trivial

6. The phrasing "a randomly initialized network still performs a basic form of computation" (line 17) is somewhat tautological — every network performs computation regardless of initialization. The language could more precisely specify what kind of computation is relevant for interpretability (e.g., "preserving or amplifying the sparse structure of its inputs," which the paper already provides in the same sentence).

## Nice-to-Haves

- Showing per-latent AUROC score distributions (histograms or violin plots) rather than only the aggregate AUROC would allow readers to directly assess the degree of overlap between trained and random distributions.
- Bootstrap confidence intervals for the AUROC values would considerably strengthen the quantitative claims.
- The paper could discuss whether weight permutation (preserving the full joint distribution of weights) would produce different results from the Gaussian-moment-matched randomization used here.
- A discussion of whether the 100-latent sample is large enough to be representative, and any checks on sampling stability, would help address the uncertainty concern.

## Novel Insights

The most striking finding not fully foregrounded by the paper's framing is the *asymmetry* in the 6.9B results: auto-interpretability AUROC is higher for random models (0.87) than trained (0.79). Together with the entropy analysis, this suggests that the failure mode is not just "metrics can't tell the difference" but rather "random models produce more token-specific, narrowly-scoped features that are *easier* to explain" — a subtly different and more interesting conclusion than simple indistinguishability.

## Suggestions

1. Reframe the title and abstract to precisely match the evidence, e.g., "Fuzzing-Based Auto-Interpretability AUROC Does Not Distinguish Trained from Random Transformers at Scale."
2. Add confidence intervals (even simple bootstrap over the 100 sampled latents) to the AUROC values in Figure 2.
3. Discuss whether alternative randomization procedures (weight permutation) would produce similar results to the Gaussian-moment-matched approach used here.
4. Explicitly connect the entropy finding to the toy models: why do random models produce more token-specific features, and can the toy models reproduce or explain this asymmetry?

## Removed Points (from input, filtered per guidelines)

- **"Parameter norm matching confound underplayed"** — The paper explicitly discusses this mechanism at line 87, noting that randomized variants (norm-matched) are more similar to trained than Step-0 and speculating on the reason. This is presented as an observation and plausible explanation, not a confound that invalidates the core claim. Moved to nice-to-have about presentation emphasis.
- **"Related work lacks critical engagement"** — Generic criticism without specific evidence. The paper critically engages with Bricken et al. (2023), Karvonen et al. (2024c), and Zhong and Andreas (2024).
- **Various formatting/style nitpicks** — Removed per filtering rules (parser artifacts, not author errors).
- **"Step-0 shows higher AUROC than trained models"** — This is already acknowledged in the paper's description (line 106: "Trained and Step-0 variants often achieving higher AUROC values").

## Score and Decision

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>