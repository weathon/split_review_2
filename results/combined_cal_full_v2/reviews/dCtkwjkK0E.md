## Summary

This paper presents a pilot study on active learning for flow matching models in the context of conditional shape design. The authors propose a piecewise-linear analysis framework to derive how data composition affects generation diversity and accuracy, leading to two query strategies: Q_D (for diversity, selecting labels similar to existing data) and Q_A (for accuracy, selecting labels farthest from existing data). The paper demonstrates that Q_D consistently improves diversity over standard active learning baselines across four datasets. The key practical strength is that both strategies operate directly on the dataset via an RBF label predictor, avoiding expensive retraining of the flow matching model.

## Strengths

- **Addresses a genuinely under-explored problem.** Active learning for generative models — especially flow matching — has received far less attention than active learning for discriminative models. The paper correctly identifies and scopes this gap, and the framing as a pilot study is appropriate. (weight=7.89)

- **Practical decoupling of query from model training.** Q_D and Q_A operate directly on the dataset via an RBF label predictor rather than requiring repeated training of the expensive flow matching model. This is a concrete practical advantage stated clearly in Section 2.4. (weight=9.96)

- **The core insight is clearly articulated.** The idea that data sharing labels with existing data enhances diversity while data with novel labels improves accuracy is intuitive and grounded in the piecewise-linear analysis. The paper formalizes the diversity-accuracy trade-off from a data-centric perspective. (weight=9.28)

- **Well-matched application domain.** The shape design datasets (airfoil, flying wing, starship) with continuous performance-requirement labels and expensive numerical-simulation ground truth are exactly the setting where active learning can provide meaningful savings. (weight=8.94)

## Weaknesses

### Major

- **Q_A excluded from the main quantitative comparison (Figure 4).** The paper claims (line 163) that "Q_A yields the highest accuracy," but Figure 4 — the primary quantitative comparison across all four datasets — compares only Random, Coreset, Committee, Anchor, and Q_D. Q_A's accuracy is only supported by qualitative visual comparisons (Figures 5–8) showing per-condition accuracy numbers, not by aggregate metrics against baselines. This omission makes the central accuracy claim unverifiable from the paper's main experiment. (weight=1.40)

- **Gap between theoretical derivation and the actual Q_D method.** The theoretical analysis (Section 2.3) is worked out for c∈R¹ with exact label matching, showing that adding data with identical labels increases interpolation pairs from *mn* to *(m+1)n*. However, Q_D (Eq. 4) is a three-term heuristic: (i) `-distance(y, 𝒴)` uses approximate label similarity (the paper acknowledges exact matches are "infeasible," line 89), (ii) `Δentropy` is a clustering-based heuristic with an unspecified threshold, and (iii) `distance(x, 𝒳)` is explicitly coresets-inspired. Two of the three terms and the label-similarity relaxation have no formal grounding in the presented analysis. The paper overstates what the theory delivers, claiming it "precisely elucidates" (line 208) the behavior of individual data points. (weight=0.09)

### Minor

- **No statistical uncertainty reported.** Results are reported over 5 iterations with a single run per method — no error bars, confidence intervals, or mention of random seeds. Given that the initial round is random, differences between methods could be driven by seed-dependent initialization effects rather than the query strategy. (weight=2.47)

- **Key hyperparameters unspecified.** The weighting coefficients α, β, γ in Q_D (Eq. 4) are not reported anywhere in the paper. The clustering threshold for the Δentropy term is also unspecified. Without these values the method cannot be reproduced, and it is unclear whether results depend on careful per-dataset tuning. (weight=3.22)

- **Ablation (Figure 9) shows the coresets-inspired term is the most important for Q_D.** Removing `distance(x, 𝒳)` — the term with no theoretical grounding from the paper's analysis — causes the largest diversity drop across all datasets. This raises the question of how much of Q_D's performance is attributable to the paper's theoretical insight (label-consistent data) versus an existing coresets criterion. (weight=4.23)

- **Q_D outperforming the full dataset on diversity (line 159) is noted without explanation.** Since a model trained on all available data should have access to strictly more information, this finding is counterintuitive. The paper does not discuss whether this reflects a property of the diversity metric (Eq. 8) or a genuine phenomenon. (weight=3.08)

- **The piecewise-linear interpolation assumption (Eq. 2) lacks empirical validation.** The assumption is presented as a hypothesis citing condensation literature on two-layer ReLU networks. The paper does not validate whether this holds for the actual deep flow matching model (8-layer, 512-unit, LeakyReLU) used in experiments. The theoretical counting argument is also restricted to c∈R¹ and d=1; the extension to higher-dimensional label spaces (the real datasets use R³ and R⁴) is not provided. (weight=1.91)

### Trivial

None.

## Nice-to-Haves

- Include the full-dataset model as a reference line in Figure 4 to contextualize how much of the upper-bound performance each active learning method recovers.
- Conduct an ablation testing Q_D with only the theory-derived term (`-distance(y, 𝒴)`, with β=γ=0) to directly test whether the theoretical insight drives diversity improvement.
- Validate the piecewise-linear interpolation assumption empirically by measuring whether the trained flow matching model's vector field interpolates approximately linearly between conditioned outputs.

## Removed Points

- **"Q_A is not a novel contribution — it is explicitly coresets in label space."** Removed because the paper itself states this clearly (line 99: "Essentially, Q_A performs the coresets algorithm in the label space"). The contribution is the insight that label-space coverage drives accuracy, which follows from the analysis; the paper does not claim algorithm-level novelty for Q_A.
- **"Figure 4 caption contradicts text (Random highest accuracy vs Q_A highest accuracy)."** Removed because no contradiction exists. The caption describes what is in the figure (among Random, Coreset, Committee, Anchor, Q_D, Random has highest accuracy); the text refers to Q_A (not shown). These statements are compatible.
- **"Missing proof for Lemma 2 / appendix content."** Removed because the parser strips appendix content; this cannot be verified.
- **"Missing related works."** Per meta-reviewer rules, missing related works should not be noted.
- **Formatting/style nitpicks.** Removed per meta-reviewer rules.
- **Several minor points from section-by-section notes** (e.g., more GALISP discussion, specifics of RBF architecture) that are generic scope-expansion requests without a concrete anchor in the paper.

## Novel Insights

None beyond the paper's own contributions. The reviews surface the structural tension between the paper's theoretical framing and its algorithmic instantiation, but this is already implicit in the paper's own self-aware acknowledgments (the exact-match requirement, the coresets inspiration). The key gap — Q_A's omission from the main quantitative comparison — is an experimental omission rather than a novel analytical finding.

## Suggestions

1. Include Q_A in the main quantitative comparison (Figure 4) alongside Random, Coreset, Committee, and Anchor, so the accuracy claim can be directly verified against baselines.
2. Report α, β, γ values and the clustering threshold for reproducibility.
3. Add error bars or confidence intervals from multiple random seeds.
4. Include the full-dataset model as a reference line in Figure 4.
5. Conduct an ablation testing Q_D with only the theory-derived term (`-distance(y, 𝒴)`, with β=γ=0) to isolate the contribution of the theoretical insight.

## Score and Decision

### Calibration Details

**All retrieved anchors (across rounds):**

| Path | Avg Score | Round | Itemized | Comparison |
|------|-----------|-------|----------|------------|
| Uj0h13lVrR (KL GFlowNets) | 1.00 | R1 | No | Much more poorly executed; unserious work |
| u1cQYxRI1H (IC-Light) | 10.00 | R1 | No | Strong accept; not comparable topic |
| 5lUdTogEL3 (Lifelong ReID) | 1.00 | R1 | No | Unrelated; unserious work |
| P49gSPmrvN (UMAP discourse) | 1.00 | R1 | No | Unrelated |
| WxLwXyBJLw (FM one-step) | 3.25 | R1 | Yes | Similar theory-method gap but much weaker experiments; our paper is stronger |
| 2whSvqwemU (FM-TS) | 3.00 | R1 | No | Flow matching for time series; lower relevance |
| SEvJfuCtPY (Phase-aware FM) | 3.00 | R1 | No | Theoretical FM analysis; different contribution type |
| YiyG1tHDxq (BALSA) | 3.40 | R1 | Yes | Most topically similar; our paper has stronger presentation and framing but similar empirical gaps. BALSA has severely negative-weighted weaknesses (-4.75, -4.92); our paper has none this severe |
| DoDNJdDntB (FM+SBI) | 4.20 | R1/R2 | Yes | Interesting idea, incomplete validation — similar pattern; mixed reviewer scores (3,3,3,6,6) |
| 8ZJAdSVHS1 (Cond Prior FM) | 4.25 | R2 | No | Flow matching conditional prior; lower relevance |
| MM197t8WlM (Local FM) | 4.25 | R2 | No | Flow matching architecture contribution |
| B5IuILRdAX (One-step FM Gen) | 5.00 | R1 | No | Stronger flow matching contribution |
| ndCJeysCPe (Analysis FM limited) | 6.33 | R2 | No | Theoretical FM analysis; higher-scoring but different contribution type |
| THUBTfSAS2 (LDM Active Learning) | 5.25 | R2 | Yes | Strong theory + empirics; clearly above our paper's bar |
| yZBpnKpBCw (FALCUN) | 4.50 | R2 | Yes | Similar heuristic combination critique, but stronger empirics; our paper has more novel problem |
| lgmCGI2IpI (AQOT) | 4.50 | R2 | Yes | Also criticized for heuristic score combination; our paper has weaker empirics |

**Round 1 bracket:** 3.5–5.5 (borderline range). The paper's problems are real but not as severe as strong-reject papers (score <1.5 band), and it has genuine contributions that place it above the simple-reject band (1.5–3.5).

**Round 2 narrowing:** Comparing weighted items, our paper's strengths (7.89–9.96) are comparable to FALCUN (4.50) and AQOT (4.50). However, our paper's major weaknesses have near-neutral weights (0.09, 1.40) while the 4.50-range anchors have severely negative-weighted weaknesses (FALCUN: -5.84; AQOT: -5.42). This suggests the calibrating model sees our weaknesses as less severe. However, from a substantive meta-review perspective, the Q_A omission from Figure 4 is a material gap that undermines a core claim, and the theory-method gap is significant for a paper framing itself as theoretically grounded. Taking these together, the paper sits below the 4.50 anchors but above the 3.40 BALSA anchor.

**Final calibrated score: 4.0.** This reflects a borderline-reject paper with genuine insight and a well-posed problem, held back by a material experimental omission and a theory that is narrower than advertised.

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>