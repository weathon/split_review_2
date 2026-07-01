## Summary

This paper applies a standard sanity check from interpretability research—comparing method outputs on a trained model versus a randomly initialized null model—to sparse autoencoder (SAE) evaluation. The authors train SAEs on residual stream activations of Pythia models (70M–6.9B parameters) and find that commonly used auto-interpretability scores (fuzzing AUROC) and several reconstruction metrics yield surprisingly similar aggregate values for SAEs trained on fully trained transformers versus those trained on randomly initialized ones, especially for larger models. The paper proposes token distribution entropy as a preliminary alternative that better captures the difference in feature “abstractness” between the two settings, and provides toy experiments suggesting that random neural networks can preserve or amplify superposition already present in the input data.

## Strengths

* **Important sanity check for a widely used methodology.** The paper addresses a fundamental question that the mechanistic interpretability community should be asking: do current SAE evaluation metrics actually indicate that learned, computationally relevant features have been discovered, or could they be driven by simpler artifacts of data or architecture? The answer has direct implications for how results from thousands of SAE-trained features are interpreted.
* **Comprehensive experimental design.** The study spans five model scales (70M to 6.9B parameters), multiple randomization schemes (step-0, re-randomized with/without embeddings, Gaussian embedding control), several metrics (auto-interpretability AUROC, reconstruction metrics, cross-entropy loss score, token distribution entropy), and checks robustness across expansion factors and sparsity levels. This breadth strengthens the generalizability of the main claim.
* **Clear documentation of a non-obvious failure mode.** The finding that auto-interpretability scores for random models *exceed* those for trained models in some settings (e.g., Pythia-6.9b) is striking and counterintuitive. It powerfully demonstrates that high aggregate auto-interpretability does not guarantee that the SAE has recovered learned, abstract features.
* **Constructive suggestion for improvement.** The token distribution entropy analysis, while preliminary, provides a concrete example of a metric that does reveal differences between trained and random models, pointing toward a more meaningful evaluation axis (feature abstractness/complexity).

## Weaknesses

### Fatal
None.

### Major
1. **Title overstates the empirical scope.** The paper’s title claims that *automated interpretability metrics* (plural, presumably all) *do not distinguish* trained and random transformers. The evidence actually shows that *some* metrics (auto-interpretability AUROC and certain reconstruction metrics) do not distinguish them, while *other* metrics do (e.g., cross-entropy loss score is only well-defined for the trained model; token distribution entropy shows clear separation; the Gaussian embedding control is always distinguishable). The paper itself acknowledges this nuance, but the title could mislead readers into thinking no metric works.

2. **No uncertainty quantification on the main auto-interpretability results.** The paper reports AUROC values for fuzzing scoring using 100 randomly sampled latents per SAE, but provides no error bars, confidence intervals, or statistical tests comparing the trained and randomized variants across layers or across random seeds. Without knowing the variability of these scores, it is difficult to assess whether the observed similarity is statistically meaningful or might arise from sampling noise. The appendix mentions “multiple random seeds” but does not bring that uncertainty into the main figures.

3. **Reliance on a single auto-interpretability method (“fuzzing”) for the primary claim.** While detection scoring is briefly shown in the appendix, the paper’s central argument rests almost entirely on fuzzing AUROC. Simulation-based scoring (Bills et al., 2023) is acknowledged as expensive but not included. Different auto-interpretability pipelines could potentially be more or less discriminative; the paper would be stronger if it either used multiple methods or systematically argued why fuzzing is representative.

### Minor
1. **The toy model (Section 4) is only loosely connected to the main experiments.** The toy results show that random MLPs can preserve/amplify superposition in synthetic data and that token embeddings may exhibit some superposition, but the paper does not directly test whether this mechanism explains the transformer results (and states that it defers this to future work). This makes Section 4 a plausibility argument rather than a core part of the evidence.

2. **Token distribution entropy is an imperfect proxy for “abstractness.”** The paper uses entropy of token IDs among maximally activating examples to quantify feature complexity, but this measure conflates several properties (e.g., a latent that fires on a few *different* tokens that happen to be semantically unrelated would have high entropy but not necessarily represent an “abstract” concept in the intended sense). The paper appropriately calls this preliminary, but more careful validation would strengthen the proposal.

### Trivial
- The captions of Figures 1 and 2 are partially redundant with the main text; the text does a good job summarizing the takeaway, but the figures would benefit from slightly more self-contained captions.

## Nice-to-Haves
- Include error bars (e.g., bootstrapped confidence intervals) on the main AUROC and reconstruction metric plots to quantify sampling variability.
- Add a comparison with simulation-based auto-interpretability (even on a subset of layers or latents) to verify that the finding is not specific to the “fuzzing” protocol.
- Make the toy model section more directly predictive of the transformer results (e.g., test whether random transformer activations are “more superposed” than trained ones using the Pareto frontier analysis on actual transformer activations).

## Novel Insights
None beyond the paper’s own contributions.

## Suggestions
- Moderate the title to something like “*Aggregate Auto-Interpretability Metrics for SAEs Fail to Distinguish Trained from Random Transformers*” to accurately reflect the empirical scope.
- Add statistical tests (e.g., whether the difference in AUROC between trained and randomized variants is significant given the sample of 100 latents) and report variability in the main figures.
- Include the detection AUROC results in the main paper rather than only the appendix, since the paper’s claim is about “automated interpretability metrics” broadly.

## Score and Decision
The paper makes a timely and empirically sound contribution that should influence how SAE evaluation results are reported and interpreted. The weaknesses (title overreach, lack of uncertainty quantification, reliance on one auto-interpretability method) are real but do not invalidate the core finding. The paper is an important cautionary study that merits acceptance.

MY FINAL SCORE: 7.0</score>
MY FINAL DECISION: Accept</decision>