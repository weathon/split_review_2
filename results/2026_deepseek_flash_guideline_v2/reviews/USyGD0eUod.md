Now I have all the information I need. Let me produce the final consolidated review.

## Summary

This paper tests whether commonly used SAE interpretability metrics (auto-interpretability AUROC, reconstruction metrics) can distinguish trained transformers from randomly initialized ones across the Pythia model family (70M–6.9B parameters). The central finding is that aggregate auto-interpretability scores for trained and random models are both well above chance (e.g., Pythia-6.9b: trained AUROC=0.79, random variants AUROC=0.87–0.88, vs. Gaussian control AUROC=0.50), meaning high aggregate scores alone do not guarantee that learned, computationally relevant features have been identified. The paper also introduces token distribution entropy as a diagnostic that does reveal differences (trained models show increasing entropy across layers, random models do not), and provides toy-model evidence that random networks preserve or amplify superposition structure in their inputs.

## Strengths

1. **Systematic evaluation across model scales and multiple randomization schemes**: The paper tests five model sizes (70M–6.9B) and four distinct randomization variants (re-randomized incl./excl. embeddings, Step-0, Gaussian control). This goes substantially beyond prior work — Bricken et al. (2023) tested only one-layer transformers and found auto-interpretability *did* discriminate random from trained, while the paper here shows the gap narrows at larger scales (line 49: "auto-interpretability scores for randomized models were relatively low for smaller models... but the gap was narrowed for larger models").

2. **Token distribution entropy as a constructive diagnostic**: The paper proposes token distribution entropy (lines 91–96, Figure 2 last row) — measuring how concentrated latent activations are on individual token IDs. Unlike AUROC-based auto-interpretability, this metric *does* reveal differences: random models show flat, low entropy across layers (single-token features), while trained models show increasing entropy with layer depth (more abstract features). This provides an actionable alternative that partially recovers the signal missed by aggregate scores.

3. **Toy-model evidence for why random networks produce interpretable latents**: Section 4.2 uses Pareto frontiers of explained variance vs. sparsity to show that outputs of randomly initialized MLPs achieve greater sparsity at a given reconstruction quality than Gaussian controls, even when inputs are Gaussian. This provides mechanistic plausibility for the paper's central claim — that high interpretability scores from random models arise because random neural networks preserve or amplify superposed structure in their inputs (Section 4.1).

4. **Hyperparameter robustness checks**: The paper verifies its main findings across SAE expansion factors of 16–128 and sparsities of 16 and 32 (Pythia-160m, line 73), and with 1B-token training runs (line 71), showing the phenomenon is not an artifact of a specific SAE configuration.

5. **Direct engagement with contradictory prior results**: The paper explicitly addresses Bricken et al. (2023) (who found auto-interpretability did distinguish random from trained in one-layer transformers) and explains when the gap narrows (larger models). It also addresses Karvonen et al. (2024c) (chess data) and explains the discrepancy via different sparsity structure of language vs. board-game data.

## Weaknesses

### Fatal
None.

### Major

1. **Title/abstract overstate the claim relative to the paper's own data**: The title says metrics "do not distinguish" trained from random, and the abstract says scores are "similar." But the paper's own Figure 1 shows trained AUROC=0.79 vs. random=0.87–0.88 for Pythia-6.9b — a consistent 8–9 point gap with random models *outperforming* trained ones. While both are well above chance (0.50), a gap of this size with a uniform direction does not constitute "no distinction." The paper should either (a) provide an operational definition of what "do not distinguish" means (e.g., "both are well above chance" or "the gap is small relative to the gap to chance"), or (b) reframe the claim to "aggregate auto-interpretability scores are well above chance for both trained and random models, and do not cleanly separate them." The current framing risks overstating the finding. Additionally, the paper does not analyze or even acknowledge why random models consistently score *higher* — which is mechanistically interesting and could strengthen the paper's argument if discussed.

2. **No measures of variance or uncertainty for the central AUROC comparison**: The paper repeatedly states that trained and random results "overlap" and are "similar," but offers no confidence intervals, standard errors, or statistical tests for the AUROC comparisons. Appendix E is cited for "multiple random seeds," but the main text provides no basis to evaluate whether the trained (0.79) and random (0.87–0.88) values are statistically distinguishable or not. With 100 latents sampled per condition (line 77), bootstrap intervals or standard errors are feasible. Claims of "similarity" and "overlap" require uncertainty quantification to be substantive.

3. **Model-size dependency is under-foregrounded**: Line 49 acknowledges that "auto-interpretability scores for randomized models were relatively low for smaller models (e.g., Pythia-70m) but that the gap was narrowed for larger models (e.g., Pythia-6.9b)." This means the metrics *do* distinguish trained from random at smaller scales. The paper's title, abstract, and conclusion do not reflect this conditional nature of the finding. A reader walks away thinking the failure is general, when it is strongest at the largest model sizes.

### Minor

1. **Direction of the trained-random gap is unanalyzed**: Random models scoring *higher* than trained on fuzzing AUROC (0.87 vs. 0.79) is a surprising result that deserves discussion. Does the trained model learn more distributed features that are harder to characterize with single-sentence explanations, making its latents harder to classify? If so, this would actually *support* the paper's broader point about aggregate metrics missing complexity. The silence on this question weakens the analytical depth.

2. **Modest sampling of features**: Only 100 features are sampled per SAE for auto-interpretability scoring (line 77). With thousands of latents per SAE and multiple layers, 100 is a modest sample. The paper does not discuss sampling variability or whether this is sufficient to characterize the distribution of latent interpretability scores.

3. **Token distribution entropy is promising but under-validated**: The entropy metric is presented as a "proof-of-concept" (line 179). While this is honestly scoped, the paper would be strengthened by showing that it correlates with downstream measures of computational significance or can predict, at the individual latent level, whether a feature came from a trained or random model. Currently it is shown only at the aggregate level.

### Trivial
None.

## Nice-to-Haves

- A direct comparison of individual latent-level score distributions (e.g., histograms or violin plots of per-latent AUROC) would let readers see whether the similarity in means hides bimodal distributions or whether the entire distributions genuinely overlap.
- Discussion of whether results depend on the choice of explanation model (Llama-3.1-70B). Could a more capable model distinguish trained from random features? This is noted as a limitation (line 173) but not explored.
- Stating the key caveat — "we do not claim that SAEs fail to capture information from trained Transformers above and beyond randomly initialized transformers" (line 173) — earlier in the paper, e.g., in the abstract or introduction.

## Removed Points

These points from the inputs were removed with justifications:

1. **"The headline claim is contradicted by the paper's own data"** (Harsh Critic #1) — The claim is that metrics "do not distinguish" in the sense of providing reliable evidence of learned computation. Both trained (0.79) and random (0.87) produce well-above-chance scores, and the gap (0.79 vs 0.87) does not *contradict* the central finding that high scores don't guarantee learned features. A gap of 0.08 where random scores *higher* actually reinforces the paper's cautionary message. This is reframed as a Major weakness about overstatement rather than a contradiction.

2. **"The entropy metric gets almost no analytical weight"** (Harsh Critic #4) — The paper explicitly describes the entropy analysis as preliminary/a proof-of-concept (line 179). This is a scope limitation honestly stated, not a weakness. Demoted to Minor weakness #3 (under-validated).

3. **"Missing appendix, proofs, or references"** — Removed per instructions. The parser strips these sections; they exist in the original submission.

4. **"Figure 2 is dense and hard to parse"** — Removed as a presentation nitpick. The figure description shows a well-organized 7×5 grid, which is standard for multi-metric comparisons.

5. **"The CE loss score provides no comparison"** — The paper explicitly states (line 89) that this metric only makes sense for the trained variant and provides it for calibration with literature.

6. **Generic or weak strengths from Strength Finder** — Strengths about "addressing an important problem" and "timely contribution" are generic and removed. Only concrete, paper-specific strengths retained.

## Novel Insights

None beyond the paper's own contributions. The intersection of the two reviews does not surface any observation about the paper that is not already present in the paper itself.

## Suggestions

1. **Reframe the headline claim** to be more precise: e.g., "Aggregate Auto-Interpretability Scores Are Well Above Chance for Both Trained and Random Transformers" or "Auto-Interpretability Scores Fail to Reliably Distinguish Trained from Random Transformers at Scale." Make clear in the abstract that the gap narrows at larger model sizes.

2. **Add confidence intervals or bootstrap estimates** for the AUROC comparisons in the main text (not just Appendix E) so that claims of "overlap" and "similarity" are backed by uncertainty quantification.

3. **Analyze the direction of the trained-random gap**: Why do random models score *higher* than trained on fuzzing AUROC? At minimum, add a paragraph of speculation or analysis in the Results section.

4. **Include individual latent-level score distributions** (e.g., violin plots or histograms of per-latent AUROC for trained vs. random) to complement the aggregate ROC curves.

5. **Move the model-size qualification** into the abstract so readers immediately understand that the effect is strongest at large scales.

6. **Consider validating the entropy metric** more thoroughly — show that it predicts which individual latents are likely to be "meaningful features" rather than token-level artifacts.

## Score and Decision

**Calibration note**: The calibration search tool encountered a path error and could not retrieve anchor papers. The following score is based on direct analysis of the paper against ICLR review standards.

This paper presents an important, timely, and methodologically sound empirical finding: aggregate SAE auto-interpretability metrics produce well-above-chance scores for both trained and random transformers, meaning high scores alone do not constitute evidence of learned computational features. The experimental design is thorough (multiple model scales, multiple randomization schemes, robustness checks), the writeup is clear, and the limitations are honestly stated. The paper also contributes a constructive diagnostic (token distribution entropy) and a mechanistic explanation via toy models, going beyond merely reporting a negative result.

The primary weaknesses are presentational/analytical rather than methodological: the title/abstract slightly overstate the claim (0.79 vs 0.87 is a systematic gap, not pure overlap), variance is not quantified for the central comparison, and the model-size dependency is under-foregrounded. These are addressable in revision and do not threaten the core finding.

On the ICLR scale (1=strong reject, 3=reject, 4=borderline reject, 6=borderline accept, 8=accept, 10=strong accept), this paper sits above borderline accept due to its clear contribution and solid execution, but below a strong accept due to the presentational issues identified above.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>