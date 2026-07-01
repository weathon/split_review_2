Now I have all the verification I need. Let me write the final consolidated review.

## Summary

This paper tests whether common sparse autoencoder (SAE) quality metrics and automatic explanation pipelines can distinguish trained transformers from randomly initialized ones (parameters sampled i.i.d. from a Gaussian). Over Pythia models ranging from 70M to 6.9B parameters, with multiple randomization schemes, the authors find that auto-interpretability AUROC scores and reconstruction metrics from SAEs trained on random transformers are often surprisingly similar to those from trained models. The paper also proposes token distribution entropy as a metric that does reveal differences in feature "abstractness." The core finding — that aggregate auto-interpretability scores are insufficient to guarantee that learned, computationally relevant features have been recovered — is timely and important for the mechanistic interpretability community.

## Strengths

- **Well-motivated and timely question (line 15).** The paper applies the established "randomized model as null" sanity check from interpretability (Adebayo et al., 2020) to SAE evaluation metrics. This is exactly the kind of scrutiny the field needs given the rapid adoption of auto-interpretability pipelines.

- **Systematic experimental design (Section 3).** The paper covers 5 model sizes (70M–6.9B), multiple layers, 5 carefully chosen variants (trained, step-0, re-randomized incl./excl. embeddings, control), and multiple metrics (fuzzing AUROC, detection AUROC, explained variance, cosine similarity, L1 norm, CE loss score, token entropy). The "control" condition (Gaussian token embeddings producing chance-level AUROC, lines 59, 69) is a useful sanity check showing the pipeline requires some structure in the activations.

- **Token distribution entropy as a promising alternative (lines 125–127).** The entropy analysis reveals genuine differences between trained and randomized models that aggregate auto-interpretability scores miss: trained models show increasing entropy (more abstract features) with layer depth, while randomized models stay at low entropy. This is the paper's most constructive finding and points toward what a better metric might look like.

- **Honest framing of limitations (Section 5, line 173).** The paper explicitly states: "We do not claim that SAEs fail to capture information from trained Transformers above and beyond randomly initialized transformers; only that aggregate auto-interpretability measures do not necessarily indicate the existence of interesting underlying features." This is appropriately measured.

## Weaknesses

### Major

- **Title and framing overstate the central claim relative to the evidence.** The title states that metrics "Do Not Distinguish" trained from random transformers, but the body presents a more nuanced picture that partially undermines this absolute framing. Specifically: (a) the CE loss score cleanly separates trained from random — the paper notes it "only makes sense for the trained variant" (line 89); (b) token distribution entropy distinguishes trained from random, with trained models showing increasing entropy across layers while random models stay flat (lines 125–127); (c) for Pythia-6.9b, the randomized variants score *higher* on auto-interpretability AUROC (0.87–0.88) than the trained model (0.79) — a reversal, not a failure to distinguish (Figure 1, line 63–65). The paper's caption itself says "All variants save for control achieve comparable performance" (line 115), which is a weaker claim than "do not distinguish." The actual contribution — that auto-interpretability AUROC overlaps substantially between trained and random models, making it unreliable as a standalone diagnostic — is real and important, but the title and framing should be recalibrated to match the evidence.

- **No statistical uncertainty quantification on main results.** The paper samples 100 latents per SAE (line 77) but reports no error bars, confidence intervals, or significance tests on any of the main figures (Figures 1, 2). The central argument is about the *similarity* of score distributions between trained and random models, which requires quantifying the variance of those distributions. Without uncertainty quantification, the reader cannot assess whether the observed overlap is robust or an artifact of the 100-latent sample. Appendix E is mentioned (line 67) for multiple random seeds, but the main figures are presented as single deterministic curves. For a paper whose core claim is a negative one about metric distinguishability, this is a significant evidential gap.

### Minor

- **The toy model (Section 4) is loosely connected to the main experiments.** Section 4 shows that random neural networks can preserve or amplify superposition in toy data, but the connection to the auto-interpretability results is never made explicit. The toy model uses synthetic data with reconstruction-based metrics (explained variance vs. sparsity), not auto-interpretability scores. The paper is transparent about this — line 131 states "we leave the question of which predominates in the case of randomized transformers... to future work" — but as a result, Sections 3 and 4 feel like two separate papers rather than a unified argument. The paper would be stronger either by establishing a tighter link or by clearly separating the two contributions.

- **The choice of fuzzing as the primary auto-interpretability metric is not validated for the trained-vs-random distinction.** The paper uses fuzzing scores because they "correlate with simulation scoring" (line 76). However, correlation in absolute scores does not guarantee that the *difference between trained and random* is preserved under both scoring methods. If fuzzing and simulation scores correlate overall but differ in their sensitivity to training status, the choice of metric could drive the results. This concern should be acknowledged or addressed (detection scores are deferred to Appendix B).

- **The control condition, while useful as a sanity check, is set to an extreme (Gaussian token noise) that makes the trained-vs-random comparison look more binary than it is.** The control produces chance-level AUROC (~0.5), creating a dichotomous framing (chance vs. above-chance) that de-emphasizes the systematic differences between trained and random variants. A null that preserved activation statistics (e.g., by matching activation moments) would provide a more informative baseline for quantifying the *degree* of similarity between trained and random.

### Trivial

None.

## Nice-to-Haves

- **Quantify distinguishability directly.** The paper could report how well a simple classifier (or the overlap coefficient/Wasserstein distance) can discriminate trained-from-random based on each metric. This would directly quantify the "distinguishability" the title discusses, rather than relying on qualitative overlap claims.
- **Investigate why scores are similar.** The paper observes overlap but does not probe whether the LLM generates similar explanations for trained and random latents, whether activation patterns are similar, or whether features themselves overlap. Some qualitative analysis appears in appendices, but a brief discussion in the main text would strengthen the paper.
- **Match activation statistics for a stronger null.** Instead of pure noise, a null where activations are matched to the trained model's moments (mean, variance) would isolate whether metric differences are driven by activation statistics or learned weight structure.

## Removed Points

These points were flagged by the harsh critic but are removed for the following reasons:

- **Claim that the "language is sparser than board games" assertion is made without evidence (line 47–48).** This is a speculative remark in a related-work discussion, not a core empirical claim. It is an opinion about a possible explanation for a prior result, not an assertion the paper depends on.

- **"Connection to existing literature on random networks" as a missing piece.** This is a suggestion, not a weakness. The paper's scope is empirical evaluation of SAE metrics; requiring a theoretical treatment of random feature maps (NTK, etc.) is outside scope.

- **"Investigation of why scores are similar" as a missing piece.** The paper does discuss this via the superposition hypothesis (Section 4) and explicitly frames it as open. The critic's remaining concern is more of a "would be nice to have."

- **Criticism that the qualitative analysis is presented as "exploratory" (lines 91–93).** This describes the paper's own framing, not a flaw; presenting exploratory analyses as exploratory is correct practice.

## Novel Insights

The harsh critic's review surfaces a key tension that the paper itself does not fully resolve: the metrics *do* distinguish trained from random in some settings (CE loss, token entropy, and even AUROC direction-reversal for Pythia-6.9b), yet the paper's title claims they do not. This is not merely a presentation problem — it reflects a genuine ambiguity in what "distinguish" means. The paper's strongest evidence is that AUROC overlap is substantial enough to make the metric unreliable as a *sole* diagnostic, not that the metrics are completely uninformative. This distinction — between "insufficient as a standalone criterion" and "fails to detect any difference" — is the paper's actual finding, and framing it as the former rather than the latter would make the contribution both more precise and more actionable for practitioners.

## Suggestions

1. **Recalibrate the title and abstract** to reflect the nuanced finding (e.g., "Aggregate Auto-Interpretability Metrics Are Insufficient to Reliably Distinguish Trained from Random Transformers").
2. **Add error bars or confidence bands** to Figures 1 and 2, at minimum showing the variance across sampled latents (or across random seeds from Appendix E).
3. **Either tighten the toy-model connection** (e.g., by showing that SAEs on random-model toy data also receive high auto-interpretability scores) **or separate it clearly** into a standalone section that does not claim to explain the main results.
4. **Acknowledge the fuzzing-metric concern** explicitly: note that correlation with simulation scoring was demonstrated on trained models, and the sensitivity of this correlation to training status is unknown.

## Score and Decision

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>