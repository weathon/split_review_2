Now let me write the final consolidated review.

## Summary

This paper performs a systematic empirical sanity check on whether common SAE evaluation metrics (auto-interpretability scores, reconstruction metrics) can distinguish features learned by trained transformers from those arising in randomly initialized ones. Evaluating Pythia models from 70M to 6.9B parameters across multiple randomization schemes and metrics, the authors find that aggregate auto-interpretability scores can be surprisingly similar between trained and randomized models — and in some cases, randomized models score *higher* than trained ones. The paper also introduces token distribution entropy as a diagnostic that captures differences in feature "abstractness" that aggregate metrics miss. The core insight — that high auto-interpretability scores are insufficient evidence for learned computational features — is important for the mechanistic interpretability community.

## Strengths

- **+9.4** Systematic evaluation across model scales (Pythia 70M to 6.9B), layers, four randomization schemes, and multiple metrics (explained variance, cosine similarity, L1 norm, fuzzing AUROC, detection AUROC, CE loss score, token distribution entropy). This breadth makes the empirical findings difficult to dismiss as coincidental.

- **+6.4** Token distribution entropy is a genuinely informative diagnostic. The finding that randomized models' latents stay concentrated on few token types while trained models' entropy increases with layer captures a qualitative difference that aggregate auto-interpretability scores miss, serving as a proof-of-concept for better evaluation.

- **+4.4** Important sanity-check question for the interpretability community, well-motivated by the Adebayo et al. (2020) precedent for saliency maps. The paper correctly identifies that the field needs stronger baselines for SAE evaluation.

## Weaknesses

### Fatal
None.

### Major

1. **No operational definition of "distinguish" (impact -8.2).** The paper never defines what it means for a metric to "distinguish" two conditions. No statistical criterion (effect size threshold, overlap coefficient, hypothesis test) is provided. For example, in Figure 1, trained AUROC=0.79 vs. randomized variants at 0.87–0.88 — a 0.08–0.09 gap on [0,1]. Is that "similar" or "distinguishable"? Without an operational definition, the paper's central claim is not falsifiable and the reader cannot assess whether the evidence supports it. This is the most consequential methodological gap.

2. **No error bars, confidence intervals, or variability measures in any main-text figure (impact -7.0).** Given the paper's claim is about similarity/overlap across conditions, the absence of variability information is a significant gap. The paper references Appendix E for multiple random seeds but does not display variance in the main results, making it impossible to judge whether the trained/randomized curves are statistically distinguishable or whether the observed differences are within noise.

3. **Title overclaims relative to the evidence (impact -6.7).** The title ("AUTOMATED INTERPRETABILITY METRICS DO NOT DISTINGUISH TRAINED AND RANDOM TRANSFORMERS") asserts a stronger claim than the data support. The paper's own results show that: (a) token distribution entropy *does* clearly separate trained from randomized models (Figure 2, last row), and (b) the trained model and randomized variants produce different AUROC values (randomized variants sometimes score *higher*, e.g., 0.87–0.88 vs. 0.79 in Figure 1). The abstract and conclusion use qualifying language ("in many settings," "under certain conditions") that the title lacks. The actual finding — that aggregate auto-interpretability scores are insufficient evidence for learned features — is valuable but the title asserts a stronger, less accurate claim.

### Minor

4. **Only one SAE architecture and one explanation LLM (impact -5.4).** Only TopK SAEs are evaluated in the main experiments. Hyperparameter variations are tested (Figure 18, appendix), but other SAE architectures (Gated SAEs, JumpReLU SAEs, standard L1-penalized SAEs) are not. Similarly, only Llama-3.1-70B is used for explanation generation. Both limitations are acknowledged, but the generalizability of the central finding to other architectures/models remains unclear.

5. **The toy model section (Section 4) is weakly connected and disproportionately long (impact -5.3).** It uses 2-layer MLPs with random weights while the main experiments use deep transformers with attention and residual connections. The section explicitly states (line 131) that it leaves the question of which mechanism predominates to future work. The ~38 lines plus 3 figures devoted to this speculative analysis are disproportionate to its contribution to the main empirical argument.

6. **The randomized-outperforming-trained finding is underexploited (impact -1.7).** The most striking result — that randomized variants can score substantially higher on auto-interpretability than the trained model (Figure 1: 0.87–0.88 vs. 0.79) — is mentioned but not centered or analyzed. This is a stronger indictment of the metrics than mere similarity (it shows the metric can be *systematically misleading*, not just insensitive) and deserves more discussion about what the metric actually captures.

### Trivial
None.

## Nice-to-Haves

- The finding that randomized models can *outperform* trained models on auto-interpretability could be made the centerpiece of the paper's argument, as it demonstrates the problem is not just overlap but systematic misleadingness.
- Adding an explicit positive-control condition (e.g., a synthetic model with known features where high AUROC is expected) would strengthen the argument that the pipeline can detect genuinely learned features when they exist.
- Statistical quantification (effect sizes, overlap coefficients between trained and randomized distributions for each metric-layer combination) would operationalize "distinguish" and strengthen reproducibility.

## Removed Points

- **"Positive control not properly established" (from the harsh critic):** Removed because the Gaussian control already demonstrates the pipeline can detect a very weak signal. The paper's claim is that even the trained model — the natural positive control — is not well-separated from random, which is the finding itself. Requesting an additional synthetic positive control is a strengthening suggestion, not a core weakness.
- **Sub-component breakdowns of the title-overclaim weakness:** The detailed sub-points about token distribution entropy separating conditions, AUROC differences, and abstract qualifying language were merged into a single MAJOR weakness (item 3 above) rather than treated as separate items.
- **Generic strength framing ("timely and important question" without specific grounding):** Kept in condensed form with specific reference to Adebayo et al. (2020) as grounding.

## Novel Insights

None beyond the paper's own contributions. The review confirms the paper's central empirical finding is sound but identifies a clear mismatch between the overclaimed title and the more nuanced evidence. The most useful observation from the review process is that the randomized-outperforming-trained finding (Figure 1) could be reframed as the paper's headline result — it is a stronger argument for improved evaluation than the "similarity" framing currently used.

## Suggestions

1. **Revise the title and headline claims** to match the evidence. A more accurate framing would foreground insufficiency rather than failure (e.g., "Aggregate Auto-Interpretability Scores Are Insufficient Evidence for Learned Features in SAEs").
2. **Add error bars or confidence bands** to all main figures. At minimum, show variability across SAE training seeds, latent samples, and explanation generation runs.
3. **Operationalize "distinguish"** with a clear statistical criterion (effect size, overlap coefficient, or ROC-based separation test) so readers can evaluate the claim.
4. **Either significantly condense the toy model section** into a brief speculative subsection of Section 3, or strengthen its empirical connection to the transformer experiments.
5. **Center the finding that randomized variants outperform trained models** on auto-interpretability — this is the paper's most striking result and deserves prominence.

## Score and Decision

The paper asks an important question and produces a broad, systematic empirical investigation. The core finding — that auto-interpretability metrics can give similar or even higher scores for randomized models than trained ones — is a meaningful contribution. However, the paper is held back by three significant weaknesses: (a) no operational definition of its central claim ("distinguish"), (b) absence of variability information in all main figures, and (c) a title that overclaims relative to the evidence. These are fixable issues — the underlying experiments appear sound — but they must be addressed before the paper's claims can be properly evaluated. I recommend **borderline accept** conditional on substantial revisions to framing and statistical presentation.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>