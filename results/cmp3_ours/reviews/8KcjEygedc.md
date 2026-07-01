Now I'll write the final consolidated review.

## Summary

This paper develops a theoretical framework for data curation in high-dimensional binary classification, where a pruning oracle selects training examples based on difficulty and correctness. Using random matrix theory, the authors derive exact test error formulas (Theorem 1) for ridge regression under label-agnostic and label-aware pruning. The core result (Theorem 2) identifies a non-obvious phase transition: optimal pruning flips from "keep hard" to "keep easy" as generator quality drops, and this transition interacts with data scale. The theory is validated on synthetic data and ImageNet, and connected to recent LLM reasoning results (LIMO, s1).

## Strengths

- **Clean geometric framing.** Parameterizing data curation via cosines of angles between the generator, pruner, and ground-truth vectors (ρ, ρ₊, ρ_g in Eqn 7) is an elegant abstraction that subsumes prior work (Sorscher et al., Feng et al., Firdoussi et al.) as special cases (Remark 1, Section 3). The quantities map directly to interpretable test error rates via the simple relation E_test = (1/π) arccos(ρ).

- **Non-obvious phase transition.** Theorem 2 — showing that optimal pruning switches from "keep hard" when the generator is strong (ρ → 1) to "keep easy" when the generator is weak (ρ < 1) — is the paper's strongest result. The finding that this transition depends on the interaction of generator quality *and* data scale (Figure 1, bottom-left quadrant: large n + strong generator → aggressive pruning is optimal) is genuinely informative and non-trivial.

- **Unified treatment of both curation settings.** Extending the same framework to label-agnostic (Theorem 1) and label-aware (Theorem 3) curation using the same test-error formula demonstrates genuine generality. The model collapse connection (Figure 3), showing that "keep hard" pruning stabilizes iterative retraining while full-data training degrades, is a revealing additional application.

## Weaknesses

### Fatal

None.

### Major

- **Scope gap between theory and claimed implications.** The theory studies binary classification with squared loss on isotropic Gaussian features in the proportional asymptotics limit. The abstract and introduction claim to provide "a rigorous justification for why methods like LIMO and s1 succeed" (line 27) and that the results demonstrate that "the striking results from systems like LIMO and s1 are not coincidences but follow from fundamental properties" (line 281). The gap between ridge regression on Gaussian features and autoregressive LLM training on text is wide, and the limitations section (line 285) does not explain why readers should believe the connection is more than a loose analogy. The theory is a well-motivated toy model, but the claims about "rigorous justification" for LLM methods overstate what the analysis supports.

- **LLM "reconciliation" is post-hoc interpretation, not validation.** Section 4.2 assigns ρ (generator quality) differently for average vs. hard AIME questions without independent measurement: "the base LLM is a strong generator (high ρ) for the majority of problems" (line 206) vs. "the same LLM is a weak generator (low ρ) relative to this difficult data slice" (line 230). Since ρ is assigned post-hoc to match the observed outcome in each case, the theory cannot make falsifiable predictions about these data. Moreover, Tables 1 and 2 compare datasets differing in source, curation method, and training protocol (1k curated from a pool, 59k s1, 114k OpenThinker, 1M OpenThinker2) — the theory's prediction is about *pruning a fixed data source*, not comparing datasets from different pipelines. The section is rhetorically appealing but does not constitute evidence supporting the theory.

- **ImageNet and model collapse experiments lack sufficient methodological detail.** Section 4.3 does not specify: (i) what architecture was used (the MMPreTrain/OpenMMLab reference is too broad — ResNet? ViT?), (ii) how the 1000-class ImageNet was reduced to binary classification, (iii) how "keep easy" and "keep hard" were operationalized for images (margin? confidence? loss?), (iv) training hyperparameters (learning rate, batch size, optimizer, epochs, regularization λ), or (v) number of seeds / error bars (error bars are mentioned for synthetic experiments but not ImageNet). The model collapse experiment (Figure 3) similarly lacks details about architecture, per-round data construction, and the definition of "hard valid examples." While the theory is the paper's main contribution, these empirical experiments are relied on to validate the central claims, and the methodology is too vaguely described to be independently assessed.

### Minor

- **Synthetic experiments compare "keep hard" vs. "random" pruning** (Figure 1) rather than "keep hard" vs. "keep easy." Theorem 2 predicts the optimal strategy switches between these two extremes — comparing against uninformative random pruning tests a weaker claim. (The ImageNet experiments in Figure 2 do compare "keep hard" vs. "keep easy," partially addressing this.)

- **Theorem 2 assumes ρ_g > 0** (positive alignment between pruner and generator). The misaligned case (ρ_g ≤ 0) is not discussed, which could lead to different optimal strategies. This assumption is stated (line 151) but its implications are not explored.

### Trivial

None.

## Nice-to-Haves

- Including a "keep hard" vs. "keep easy" comparison in the synthetic experiments (Figure 1) would directly test the phase transition prediction of Theorem 2.
- Providing an independent estimate of ρ from LLM performance on held-out data (rather than post-hoc assignment) would strengthen the LLM connection.
- For completeness, discussing the ρ_g ≤ 0 case (e.g., when the pruner and generator disagree on what is "hard") would round out the theoretical analysis.

## Removed Points

- **Issue about Theorem 1 being incomplete (missing functional forms of m, m̃, r).** The paper states "Details in appendix" for these functions. The hard rules require removing weaknesses about missing appendix content since the parser strips the appendix. The theorem states the explicit equations (9)–(11) and describes m as "the Stieltjes transform of a Marchenko-Pastur law, 'deformed' by pruning" — a standard RMT formulation whose fixed-point equations are deferred to the appendix in this literature.

- **Claim that the proof sketch is uninformative.** Proof sketches in theory papers of this nature (see "An Effective Theory of Bias Amplification," "Strong Model Collapse" in the calibration corpus) are typically brief and defer to the appendix. This is standard practice, not a weakness.

- **Strength that was generic/superficial:** None of the three listed strengths were generic — each is specific and evidence-backed.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Tone down the claims about "rigorous justification" for LLM methods.** The theory applies directly to the Gaussian feature model; the LLM connection should be framed as qualitative analogy or interpretive lens, not as "justification." The conclusion (line 281) and contribution list (line 27) should be revised to match what the evidence supports.

2. **Add a brief experimental methodology paragraph** to Section 4.3 specifying architecture, class-reduction procedure, operationalization of "easy"/"hard" (margin threshold vs. loss vs. confidence), and training hyperparameters.

3. **Either run a controlled LLM experiment** where ρ is manipulated and the theory's predictions are tested prospectively, or **clearly re-label Section 4.2** as qualitative analogy/interpretation (removing the language of "reconciling" or "resolving" the paradox).

## Score and Decision

**Calibration anchors consulted:**
| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| EOPLy80bBm (Data Pruning for Fine-Tuning) | 3.00 | R1 | Weaker theory, more empirical; current paper is clearly stronger theoretically |
| e2F0mJJeN0 (Geometric Median Matching) | 3.00 | R1 | Similar, empirical pruning paper |
| zxqdVo9FjY (Least Squares with Spiked Covs) | 4.80 | R1 | RMT generalization paper; comparable depth but rejected for novelty concerns |
| nxnbPPVvOG (Flat Minima Linear Est.) | 5.67 | R2 | RMT+ridge theory, accepted; current paper has more interesting phase transition |
| Jc0FssXh2R (Optimal Criterion for Feature Learning) | 6.25 | R1/R2 | RMT theory, accepted; comparable depth, current paper has cleaner framing |
| FT4gAPFsQd (How Sparse Can We Prune) | 6.00 | R2 | Pruning+phase transition, rejected; current paper has similar strengths/weaknesses balance |
| VoI4d6uhdr (Effective Theory of Bias Amplification) | 7.00 | R1 | Ridge+RMT theory, accepted; more thorough validation, less overclaiming |
| et5l9qPUhm (Strong Model Collapse) | 8.00 | R1 | Directly related (model collapse+RMT), very strong, scored higher |

**Round-1 bracket:** 5.5–6.5. **Narrowing:** Compared to the 6.25 "Optimal Criterion" paper (accepted) and the 6.0 "How Sparse Can We Prune" paper (rejected), the current paper has a comparably interesting theoretical core but weaker empirical validation and more overclaimed scope. The 7.0 "Bias Amplification" paper is a ceiling: similar methodology but better validated. **Final score:** 6.0.

The paper makes a genuine theoretical contribution with a clean framing and a non-obvious phase transition result. However, the empirical validation is under-specified, the LLM connection is post-hoc interpretation rather than rigorous evidence, and the scope claims outrun what the theory supports. With revisions to the claims, experimental details, and framing of the LLM section, this would be a solid accept.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>