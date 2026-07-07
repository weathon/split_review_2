Now I have sufficient calibration data. Let me compile the final review.

## Summary

This paper performs a necessary sanity check on SAE evaluation metrics by comparing auto-interpretability scores and reconstruction metrics between trained transformers and randomly initialized ones (Pythia 70M–6.9B). The central finding is that aggregate auto-interpretability metrics (AUROC for fuzzing/detection) produce similar scores for trained and random models — and in the case of AUROC, random models can score *higher* (0.87–0.88 vs. 0.79 for trained). The token distribution entropy analysis reveals a qualitative difference that these aggregate metrics miss: random-model features concentrate on single token IDs and do not become more abstract with depth, whereas trained-model features do. The paper recommends routine randomized baselines and targeted measures of feature abstractness.

## Strengths

- **The question is important and the answer is non-obvious.** The paper performs a necessary sanity check (in the tradition of Adebayo et al. 2020) for SAE evaluation that the mechanistic interpretability community has been relying on not having been done. The finding — that auto-interpretability AUROC for SAEs on random transformers can equal or exceed that on trained transformers — should give practitioners pause. [weight: +3.44]

- **The experimental design is well-structured.** The paper tests five model sizes (70M–6.9B), three randomization conditions (step-0, re-randomized with and without embeddings), a proper negative control (Gaussian token embeddings), and multiple metrics (explained variance, cosine similarity, L1 norm, AUROC for fuzzing and detection, CE loss score, token entropy). This breadth makes the core result credible. [weight: +3.08]

- **The token distribution entropy analysis (Section 3, last paragraph; Figure 2, bottom row) is a genuinely useful diagnostic.** It reveals a qualitative difference — randomized models produce features concentrated on single token IDs that do not become more abstract with depth — that aggregate auto-interpretability scores miss. This serves as a proof-of-concept for the kind of targeted metric the paper argues for. [weight: +3.84]

- **The paper is honest about its own limitations** (Section 5). It explicitly states it does not claim SAEs fail to capture meaningful features from trained models, only that aggregate metrics do not guarantee it. It acknowledges results may depend on the explanation-generating LLM and that the mechanism investigation (Section 4) is speculative. [weight: +1.47]

## Weaknesses

### Fatal
None.

### Major

- **AUROC inversion (random > trained) is undertreated, and the paper does not engage with the most interesting aspect of its own results.** From Figure 1, the trained model AUROC is 0.79 while randomized variants achieve 0.87–0.88. Randomized models do not merely score similarly to trained models — they score *strictly higher*. The paper's discussion (line 87) only speculates that AUROC increases with model size generally ("features become more specific as SAE size increases"), which does not explain why random models of the same size outperform trained ones. A plausible alternative explanation is that the Llama-3.1-70B explanation model finds it easier to describe simple token-level patterns (which dominate in random models, as the entropy analysis shows) than the more complex, distributed features of trained models — making the metric *inversely* sensitive rather than merely insensitive. The paper should engage with this inversion directly rather than treating it as a simple failure to distinguish. [weight: -1.75]

### Minor

- **The claim is scale-dependent in a way the title does not reflect.** The paper notes in Related Work (line 49) that "auto-interpretability scores for randomized models were relatively low for smaller models (e.g., Pythia-70m) but that the gap was narrowed for larger models (e.g., Pythia-6.9b)." This means that for Pythia-70m, the metrics partially work. The title and abstract should qualify the claim to reflect this boundary condition. [weight: -0.49]

- **Only 100 latents are sampled per SAE for auto-interpretability scoring** (line 77). For a 6.9B model with expansion factor 64 and d_model ~4096, the SAE has ~262,000 latents, meaning ~0.04% are evaluated. While Appendix E mentions multiple random seeds, the main text lacks variance estimates or bootstrapped confidence intervals for the AUROC values. Without these, it is unclear whether the similarity between trained and randomized AUROCs reflects genuine population similarity or noisy estimates from small samples. [weight: -0.23]

- **The paper relies on the claim that 'fuzzing' correlates with simulation scoring** (Paulo et al. 2024, line 77) to justify using only fuzzing. But the paper's central thesis is that these metrics can behave unexpectedly under null conditions. Whether the fuzzing–simulation correlation holds specifically on random models is not checked. If it does not, the paper may be evaluating a proxy that itself breaks under the null condition. [weight: -2.98]

- **The CE loss score does separate the trained from random conditions** (it is near 1 for trained models and effectively undefined/poor for random ones), but the paper's framing treats this as a definitional limitation ("only makes sense for the trained variant," line 89) rather than acknowledging it as one metric that successfully discriminates. While the paper is technically correct that the CE loss score cannot be meaningfully compared across conditions (random models have terrible baseline loss), a reader could come away thinking all common metrics fail the randomization test. The paper should more carefully delineate which metrics it is indicting and which it is not. [weight: -0.01]

- **The toy model section (Section 4), while transparently speculative, occupies significant space without directly supporting the main empirical claim.** The paper acknowledges (line 131) that it "leave[s] the question of which predominates... to future work." The connection to transformer-scale language models is tenuous, and this section could be condensed or moved to an appendix without weakening the core empirical finding. [weight: +0.98]

### Trivial
None.

## Nice-to-Haves
- Bootstrapped confidence intervals for AUROC estimates from the 100-latent samples would substantially strengthen the evidential status of the main claim.
- A check on whether the fuzzing–simulation correlation (Paulo et al., 2024) holds specifically on random-model SAE latents.
- A brief robustness check varying the TopK sparsity parameter k across model sizes.

## Removed Points
None.

## Novel Insights
The most novel insight emerging from the reviews is that the paper's strongest empirical finding — randomized models scoring *higher* on AUROC than trained models — points to a more damning problem than mere indistinguishability: the auto-interpretability pipeline may be inversely sensitive, scoring higher for simple token-level patterns (which dominate in random models) than for genuinely complex features. This inversion suggests the field should focus not just on developing metrics that separate conditions, but on ensuring metrics are sensitive to the *right kind* of structure (i.e., computational relevance / abstractness rather than token-level specificity). The token entropy analysis provides an initial proof-of-concept for this direction.

## Suggestions
1. Qualify the title to reflect the scale dependence (metrics do work for smaller models) and the fact that some metrics (CE loss score) do separate conditions.
2. Report bootstrapped confidence intervals or variance estimates for the AUROC estimates.
3. Engage directly with the AUROC inversion: an additional analysis showing that the AUROC gap correlates with token entropy would both explain the inversion and reinforce the paper's call for "abstractness" metrics.
4. Check whether the fuzzing–simulation correlation holds on random-model SAE latents.
5. Move the scale-dependence caveat (smaller models show clearer separation) from Related Work into the Results section and abstract.

## Score Calibration

**Round 1 bracket:** 6.0–7.0.

**Anchors retrieved (all rounds):**

| Path | Avg Score | Round | Itemized | Comparison |
|------|-----------|-------|----------|------------|
| 9ca9eHNrdH.md — "SAEs Do Not Find Canonical Units of Analysis" | 7.00 | R1 | Yes | Proposes novel methodology (stitching, meta-SAEs) for SAE analysis; stronger positive weights (+7.45, +6.25) but also heavier negatives (-6.55). My paper is a cleaner sanity check with less formal contribution. |
| 1Njl73JKjB.md — "Towards Principled Evaluations of SAEs" | 7.00 | R1 | Yes | Proposes a supervised-dictionary evaluation framework; strong positive weights (+5.52) but heavy negatives (-8.01 on fundamental limitation). My paper is more empirically focused. |
| OZWHYyfPwY.md — "Don't trust your eyes: on the (un)reliability of feature visualizations" | 7.00 | R2 | Yes | Closest in spirit — a sanity-check paper revealing interpretability method limitations. Stronger positive weights (+5.29) but also heavier negatives (-5.09 on unclear definitions). My paper is cleaner but lacks formal/theoretical contribution. |
| Ebt7JgMHv1.md — "Interpretability Illusion for Subspace Activation Patching" | 6.33 | R2 | Yes | Another interpretability sanity-check paper. Very strong positives (+7.07) but heavy negatives (-7.87). My paper has fewer controversial aspects. |
| ghH6YYDs15.md — "Compute Optimal Inference in SAEs" | 4.67 | R1 | Yes | Had major theoretical gaps and limited real-model experiments. My paper is empirically much stronger. |
| v675Iyu0ta.md — "Interpretability Illusions in Generalization" | 5.60 | R2 | Yes | Limited to toy Dyck language task; my paper studies realistic models. |
| Wxl0JMgDoU.md — "Understanding Skill Adaptation in Transformers Using SAEs" | 2.50 | R1 | Yes | Poorly presented with limited novelty; my paper is in a different tier. |

**Weighted-item comparison:** My draft's positive weights (+3.84 max) are lower than the top-tier anchors' positives (+5.29 to +7.45), reflecting that the paper is a purely empirical contribution without new methodology or formal results. My draft's negative weights (-2.98 max) are milder than the top anchors' negatives (-5.09 to -8.01), reflecting that the paper is cleanly executed and honest about its scope. The paper falls between the 5.60 anchor (limited to toy tasks) and the 7.00 anchors (more novel/formal contributions). Given that the paper's weaknesses are all addressable framing and minor methodological gaps rather than fatal flaws, and given its clean execution and important finding, **6.5** is the appropriate score — a solid borderline-accept.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>