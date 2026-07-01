## Summary

This paper systematically evaluates whether common sparse autoencoder (SAE) quality metrics—especially aggregate auto-interpretability scores—can distinguish features learned by a trained transformer from those extracted from a randomly initialized one. Through extensive experiments across Pythia models (70M–7B parameters) and several randomization schemes, the authors find that SAE auto-interpretability scores and reconstruction metrics are often surprisingly similar for trained and random transformers, while only the trained model yields features that become more abstract in later layers. The results highlight that high aggregate interpretability scores are insufficient to guarantee discovery of complex, learned computational features, and the paper recommends routine randomized baselines and targeted measures like token distribution entropy.

## Strengths

- The paper performs a critical sanity check that is highly relevant to the mechanistic interpretability community. It systematically demonstrates that widely-used SAE evaluation metrics can fail to distinguish trained from random models, challenging assumptions underlying current interpretability pipelines.
- The experimental design is thorough: it covers five model sizes, multiple randomization variants (Step‑0, re‑randomized with/without embeddings, plus a Gaussian‑embedding control), and a range of standard metrics (explained variance, cosine similarity, AUROC for fuzzing/detection, CE loss score). The results are clearly presented and consistent across scales.
- The paper does not overclaim; it explicitly states that SAEs can still capture meaningful features in trained models, but that the metrics themselves are insufficient. The limitations are transparently discussed, including the focus on one model family and dataset.
- The toy model analysis (Section 4) provides plausible mechanistic explanations (preservation or amplification of superposition) for why random networks yield structured activations, grounding the empirical findings in a simplified formal framework.

## Weaknesses

### Major

- The paper identifies token distribution entropy as a promising additional metric that reveals differences in feature “abstractness,” but this idea is presented only as a preliminary proof‑of‑concept. It is not systematically validated (e.g., by showing that it generalizes across architectures, datasets, or SAE variants), and no concrete recommendation is given for how to combine it with existing metrics. This limits the actionable guidance for future work.
- The empirical study is restricted to a single model family (Pythia) and a single dataset (RedPajama). While this is a reasonable starting point, the claim that “high auto-interpretability scores do not distinguish trained from random” would be substantially stronger if demonstrated on other transformer families (e.g., Llama, GPT‑2) or on data from different domains. The paper acknowledges this limitation but does not mitigate it.
- The toy model (Section 4) illustrates how random MLPs can preserve or amplify superposition, but its direct connection to the language‑model results remains loose. The toy experiments use synthetic sparse features, not realistic word embeddings, and the “sparsification” effect is shown only on GloVe vectors (Figure 5b), not on the actual Pythia embeddings or residual stream activations. The explanatory value of the toy model for the main finding is therefore more suggestive than definitive.

### Minor

- The “CE Loss Score” row in Figure 2 only shows the trained variant. While the authors explain that this metric is meaningless for random models, showing it for completeness (even if uniformly poor) would help readers compare the overall landscape of metrics.
- The paper could have discussed why the “Re-randomized excl. embeddings” variant sometimes outperforms “Trained” on auto-interpretability AUROC (e.g., Figures 1 and 2). A brief speculation would strengthen the analysis.

### Trivial

- None.

## Nice-to-Haves

- A clear, synthesized recommendation for a “minimum‑reporting standard” for SAE papers (e.g., always include at least one randomized baseline and report token distribution entropy alongside auto-interpretability) would increase the paper’s immediate practical impact.
- Extending the analysis to a non‑Pythia model (e.g., a small Llama) or to a non‑language domain (e.g., images) would substantially strengthen the generalizability claim.

## Novel Insights

None beyond the paper’s own contributions.

## Suggestions

- Consider packaging the `token distribution entropy` metric into a reproducible evaluation script and releasing it as an open‑source tool, so that the community can easily adopt it as a sanity check.
- Provide guidance on what should be considered a “significant” gap between trained and random metrics. Currently the paper reports that metrics are “similar” but does not propose a threshold or effect size.

## Score and Decision

I assess this paper as a solid empirical contribution that exposes a real weakness in current SAE evaluation practices. The experiments are well‑designed, the results are clearly communicated, and the conclusions are measured. The main limitations are the incomplete validation of the proposed entropy metric and the restricted scope of models/datasets. These are not fatal, but they prevent the paper from being a fully comprehensive solution. The paper will be of significant value to the interpretability community by encouraging more rigorous baselines.

**Score:** 7.5  
**Decision:** Accept

MY FINAL SCORE: <score>7.5</score>  
MY FINAL DECISION: <decision>Accept</decision>