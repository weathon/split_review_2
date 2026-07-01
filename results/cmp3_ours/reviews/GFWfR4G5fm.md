Now I have all the information I need. Let me write the final consolidated review.

## Summary
2-3 sentence summary of the paper's contribution.

This paper identifies three fundamental limitations of static supervised causal learning (SCL) — distribution-shift fragility, compositional generalization failure, and synthetic-to-real performance collapse — and proposes TTT-SCL, a framework that dynamically generates causally-aligned training data at test time. The instantiation, TACTIC, combines a likelihood-based Alignment of Distribution (AD) metric with sparsity constraints, performs stochastic graph refinement, and trains an SCL model on data generated from the refined graphs. Experiments on synthetic, pseudo-real (SynTReN), and real-world (Sachs) benchmarks show consistent improvements over static pre-trained SCL baselines.

## Strengths

1. **Well-executed problem diagnosis (Section 3).** The paper systematically demonstrates three real limitations of static SCL through clean experiments (Figure 2, Table 1). The "Component-mixed" condition (Section 3.1) is a particularly effective diagnostic that isolates compositional failure from mere component novelty. The finding that SCL models fail on novel combinations of seen components — revealing memorization rather than modular learning — is a valuable empirical contribution independent of any proposed method.

2. **Novel core idea.** Moving from static pre-training to test-time generation of causally-aligned training data is a genuinely new direction for SCL. The paper correctly identifies that diversity-only strategies of prior work are insufficient, and the concentration framing provides a useful conceptual lens. The distinction between diversity and concentration (Section 1, paragraph 3) is well-drawn.

3. **Informative two-stage analysis (Table 4).** Showing that the final SCL output beats both the seed graph AND the highest-score graph from the AD search cleanly demonstrates that the SCL training phase adds value beyond what score-based search alone achieves. This two-stage improvement (seed: 61.8 → highest-score: 66.6 → final: 78.9 on Sachs) is the paper's most compelling evidence for the TTT-SCL pipeline and effectively addresses the concern that the method reduces to standard score-based discovery.

## Weaknesses

### Fatal
None.

### Major

1. **Scalability is unaddressed.** All evaluations are on 10–20 variable problems (Sachs: 11, SynTReN: 20). The paper claims "real-world applicability" throughout (abstract, conclusion, Section 4.3) but does not demonstrate TACTIC on any larger benchmark, despite noting that the AVICI baseline was trained on graphs "with up to 100 nodes" (Section 3.1). The TACTIC pipeline — stochastic DAG search (combinatorial space) + per-instance neural network training — has clear scaling challenges that are not discussed in the main text. This creates a significant gap between the claims and the evidence.

2. **Missing recent SCL baselines.** The paper cites Zhang et al. (2025) and Froehlich & Koeppel (2024) as SCL methods in the related work (Section 5) but does not compare against them in Table 2. If these methods have available implementations or pre-trained models, their absence from the main experimental table weakens the claim that TACTIC "achieves state-of-the-art performance."

### Minor

3. **SIM regression method is unspecified.** The AD metric (Equation 3) requires fitting mechanisms f_i^k from D_test given a candidate graph, but the paper only states "we regress the corresponding mechanisms from the observed D_test" (Section 4.1). The specific regression technique (linear regression, kernel regression, neural network?) is not stated in the main text, which affects reproducibility of the core AD computation. While Appendix A (stripped from this version) may contain these details, the main text should at least identify the function class used.

4. **No compute or runtime comparison.** TACTIC trains a neural network from scratch per test instance — orders of magnitude more compute than the static AVICI baseline — but no runtime, FLOP, or cost comparisons are provided. This makes it difficult to assess the practical trade-off between the improved accuracy and the computational overhead.

5. **No ablation of the AD component.** The sparsity term is ablated (Table 3), confirming it matters. However, there is no complementary ablation where AD is removed (e.g., optimizing sparsity alone) or replaced with a simpler baseline. The claim that "both AD and sparsity are indispensable" (Section 4.4) is only partially supported without this control.

6. **λ hyperparameter value and sensitivity not reported.** The sparsity penalty coefficient λ (Equation 5) controls the core trade-off between distributional alignment and causal minimality. Its value, selection method, and sensitivity are not provided. Since this directly determines which graphs are found during search, its absence is a nontrivial gap.

7. **Missing variance for real/pseudo-real datasets.** Table 2 reports standard deviations for synthetic datasets but not for Sachs and SynTReN, making it difficult to assess the stability of TACTIC on non-synthetic data.

8. **Noise distribution mismatch not discussed.** The paper sets noise to N(0,1) by default for generating training data (Section 4.2, step 3) but evaluates on Linear_U where the true noise is Uniform (Section 3.1). The paper does not discuss how this misspecification affects the AD likelihood computation or why the method remains robust despite it. While the good results (86.3 AUROC) suggest robustness, the issue deserves explicit discussion.

### Trivial
None.

## Nice-to-Haves
- Compare TACTIC against an AVICI model fine-tuned on TACTIC-generated data to control for the compute advantage of per-instance training.
- Report what happens when the seed graph is set to the true graph, to clarify whether the search or the SCL training contributes more to the improvement.
- Add runtime comparisons to help readers evaluate the practical cost of per-instance training.

## Removed Points

These points are flagged to be removed, treat them with caution:

- **"The AD metric and search procedure amount to standard score-based discovery."** — The paper explicitly addresses this through Table 4 and the two-stage analysis in Section 4.4, demonstrating that the SCL training phase adds substantial value beyond the search. The core contribution is the two-stage pipeline, not the AD metric in isolation. The paper separates the stages clearly.

- **"The evaluation does not control for compute."** — This is partially captured in Minor weakness 4 (compute comparison), but the framing as "unfair comparison" is too harsh. Comparing against the publicly available static AVICI is standard practice; the paper acknowledges the compute trade-off would be useful to quantify.

- **"Overclaiming ('paradigm shift')."** — Subjective framing criticism, not a technical weakness.

- **"Complexity analysis in Appendix F is missing."** — The parser strips appendices; this information exists in the original submission.

- **"The paper never compares against a version where the search result is used directly as the output."** — Table 4 does exactly this (the "Highest-score graph" column). The paper does compare against this.

- **"Lacks comparison against fine-tuned AVICI."** — Captured in Nice-to-Haves.

## Novel Insights

Beyond the paper's own contributions, the main insight from synthesizing the reviews is that the two-stage improvement shown in Table 4 (seed → highest-score graph → final SCL output) is the cleanest evidence for the paper's central claim. The paper would benefit from foregrounding this analysis even more prominently, as it directly addresses the natural concern that TACTIC might reduce to standard score-based discovery. The other key observation is that the missing SIM regression detail creates a reproducibility gap that should be straightforward to close — the paper is not fundamentally flawed, just incomplete in its current presentation on this point.

## Suggestions
1. Specify the regression method used for SIM (the AD computation) in the main text, or ensure the appendix is available.
2. Add results on at least one benchmark with 50+ variables, or explicitly discuss the scalability limitations of the method.
3. Add runtime/cost comparisons against baselines.
4. Include or justify the absence of recent SCL methods cited in related work (Zhang et al., 2025; Froehlich & Koeppel, 2024) as baselines.
5. Report λ value, selection method, and sensitivity analysis.
6. Add standard deviations for Sachs and SynTReN results.
7. Add an ablation that removes AD (optimizing sparsity alone) to fully support the claim that both components are indispensable.

**Calibration anchors used (all rounds):**
| Path | Avg Score | Round | Comparison |
|---|---|---|---|
| lQYi2zeDyh.md (Demystifying amortized CD) | 5.0 | 1 | Analysis-only, bivariate, no real data → our paper is stronger |
| x3F8oPxKV2.md (Zero-Shot Learning of Causal Models) | 6.25 | 1 | Novel amortized SCM inference, similar scalability issues → our paper is comparable but slightly weaker |
| AvXrppAS2o.md (Best of both worlds) | 3.0 | 2 | Weak marginal improvements → our paper is much stronger |
| Q0s6kgrUMr.md (Robust Causal/Anticausal) | 6.67 | 2 | Cleaner theory + experiments → our paper is weaker, less rigorous |

Round-1 bracket: [5.0, 6.25]. Final score 5.5: The Section 3 diagnosis and TTT-SCL framework represent a genuine contribution, and the two-stage improvement (Table 4) is compelling. However, the unaddressed scalability (≤20 variables), missing SIM regression details, absent recent SCL baselines, and lack of compute/runtime analysis prevent the paper from reaching a stronger acceptance tier. The paper falls between the 5.0 anchor (weaker analysis paper) and 6.25 anchor (cleaner method paper) — closer to the latter but with more gaps in presentation.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>