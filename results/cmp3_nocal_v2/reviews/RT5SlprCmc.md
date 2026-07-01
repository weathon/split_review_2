## Summary

This paper proposes a self-supervised framework for learning the Minimum Action Distance (MAD)—the minimum number of actions required to transition between states—from state-only trajectories (no rewards or actions needed). The contributions are: (1) two algorithms (MadDist and TDMadDist) that combine a scale-invariant regression loss, a contrastive separation term, and an upper-bound constraint loss; (2) a simple quasimetric distance function (`d_simple`); and (3) a benchmark suite of environments with known ground-truth MAD covering deterministic/stochastic dynamics, discrete/continuous states, and noisy observations. Empirical results show MadDist learns accurate MAD approximations and achieves strong downstream planning performance across diverse settings.

## Strengths

1. **Clean problem framing with ground-truth evaluation.** The paper correctly identifies that prior work on MAD approximation has not been systematically evaluated on the accuracy of the MAD function itself, and builds evaluation environments with *known ground truth* MAD. This is a genuine methodological improvement over work that evaluates approximations only indirectly through downstream RL performance.

2. **Scale-invariant loss (Equation 5).** The modification `(d_θ/(j-i) - 1)^2` versus the unnormalized `(d_θ - (j-i))^2` in prior work (Steccanella & Jonsson, 2022) is well-motivated: long-range pairs would otherwise dominate the loss simply due to larger error magnitudes. The experimental results (Figure 3) support its effectiveness.

3. **Strong empirical results on a diverse benchmark suite.** The evaluation covers discrete and continuous state spaces, deterministic and stochastic dynamics, noisy observations, and asymmetric transitions. The downstream planning results (Table 1) are clean: MadDist achieves near-perfect or perfect success rates across all OGBench PointMaze variants, while baselines (especially Hilbert) degrade substantially.

4. **Honest reporting of the TD variant's underperformance.** TDMadDist (Equation 8) is clearly described and its inferior performance relative to MadDist is reported without overclaiming, providing an informative negative result for future work.

## Weaknesses

### Fatal

None.

### Major

1. **Inconsistent seed count between text and figures.** The empirical setup (line 220) states: "All reported results are means over five independent runs (random seeds)." Yet the Figure 3 caption (lines 232, 238, 240) repeatedly states: "Shaded regions indicate minimum and maximum values across three random seeds." This is a concrete inconsistency in a critical experimental detail that must be resolved. If only 3 seeds were used, the statistical robustness is weaker than claimed; if 5 were used, the figure is mislabeled.

2. **The claim that `d_simple` outperforms other quasimetrics is unsubstantiated in the main paper.** The introduction (lines 19–20) lists as a contribution: "we define a novel quasimetric distance function that is computationally efficient and that, in spite of its simplicity, outperforms more elaborate quasimetrics in the existing literature." However, the main text's only description of the relevant ablation (line 222–223) says the method is "robust to... the choice of quasimetric"—a claim about *robustness*, not *superiority*. The paper presents no head-to-head comparison in the main text showing `d_simple` outperforming Wide Norm or IQE within the same MadDist framework. Since this is listed as one of three main contributions, the evidence gap between the claim and what is substantiated in the main paper needs to be addressed (either by providing the evidence or by revising the claim).

### Minor

1. **No ablation of the three loss components.** MadDist's composite loss (Equation 4) combines L_o (scale-invariant regression), L_r (contrastive separation), and L_c (upper-bound constraint). It is unclear whether all three terms are necessary, whether the contrastive term L_r might hurt in densely connected environments (by penalizing small predicted distances even when they are correct), and whether the scale-invariant formulation is the key driver of improvement. An ablation isolating each component on at least one environment would significantly strengthen the paper.

2. **Self-loop edge case in Equation 1 not acknowledged.** The paper states (line 76): "d_MAD satisfies the second constraint with equality, i.e. d(s,s')=1 for all (s,s')∈R." If R contains self-loops (an action that leaves the state unchanged, implying (s,s)∈R), then this would force d(s,s)=1, contradicting the first constraint d(s,s)=0. This edge case is minor but should be acknowledged.

3. **Hyperparameter α for d_simple not discussed.** The quasimetric `d_simple` (Equation 3) has a hyperparameter α ∈ [0,1]. The paper does not discuss how α is chosen in experiments (e.g., tuned per environment or fixed), nor its sensitivity. This affects reproducibility.

4. **Encoder architecture not described in the main text.** The paper does not describe the encoder φ_θ architecture (MLP width/depth, CNN structure, etc.) in the main text, making it harder for readers to assess the method without consulting the appendix.

5. **Large standard deviations and potential ceiling effects in Table 1.** Several entries have large standard deviations relative to means (e.g., QRL on PM Giant Navigate: 0.87±0.21; TDMadDist on PM Large Navigate: 0.70±0.30). Meanwhile, MadDist hitting 1.00±0.00 on multiple environments raises the question of whether the planning task is at ceiling for any reasonably accurate distance metric. A more discriminative evaluation (e.g., varying the planning budget or measuring suboptimality gap) would strengthen the evidence.

6. **Ratio CV metric and same-state pairs.** The Ratio Coefficient of Variation (Equation 11) is defined for d_i > 0. It is not clarified whether same-state pairs (where d_i = 0) are explicitly excluded from the computation.

### Trivial

- Terminology inconsistency: The conclusion (line 263) mentions "Shortest Path Distance (SPD)" while the background (line 78) uses "Stochastic Shortest Path (SSP)." The terminology should be consistent.

## Nice-to-Haves

- **Ablation of the three loss components** (L_o, L_r, L_c) on at least one environment would clarify which design choices drive the improvement.
- **Planning with the true MAD as an oracle comparison** would confirm that the downstream benefit comes from accurate MAD approximation specifically, not just from any learned representation.
- **Hyperparameter sensitivity analysis** for the most critical hyperparameters (especially H_c and w_r) would strengthen reproducibility claims.

## Removed Points

These points are flagged to be removed; treat them with caution.

1. **Equation 9 corruption (line 171):** The critic noted a garbled term in the PDF-extracted text. This is a parser artifact, not an author error, and is removed per the formatting-artifact rule.
2. **"Core methodological novelty is modest":** The reviewer's framing conflates a subjective assessment with a weakness. The paper clearly states it builds on Steccanella & Jonsson (2022) and lists its specific modifications (quasimetric support, scale-invariant loss, contrastive term). The degree of novelty is an editorial judgment, and the paper is transparent about its inheritance. Removed because the paper reasonably delineates what is new vs. inherited.
3. **Missing appendix content / proofs:** The critic noted missing appendix details (ablation results, proofs). The appendix is stripped by the PDF parser; these exist in the original submission. Removed per the missing-appendix rule.
4. **"Strengthening the Paper on Its Own Terms" section:** These suggestions (oracle comparison, loss ablation) are preserved in the Nice-to-Haves section above; the framing as a separate weakness category is redundant.

## Novel Insights

None beyond the paper's own contributions. The reviews surface a concrete inconsistency (seed count) and a claim-evidence gap (d_simple outperformance) that the authors should address, but do not add fundamentally new analytical insights beyond what the paper itself presents.

## Suggestions

- Resolve the seed-count inconsistency in the text (line 220) and Figure 3 captions. Ensure consistency throughout.
- Either provide head-to-head evidence that `d_simple` outperforms Wide Norm and IQE within MadDist, or revise the introduction's claim to reflect that `d_simple` provides a computationally efficient alternative with comparable robustness.
- Add an ablation study (on at least one environment) isolating the contribution of each loss term (L_o, L_r, L_c) to validate the design choices.
- Acknowledge the self-loop edge case in the constrained optimization formulation of MAD (Equation 1).
- Report how α is chosen for `d_simple` and, ideally, its sensitivity.
- Describe the encoder architecture in the main text.

## Score and Decision

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>