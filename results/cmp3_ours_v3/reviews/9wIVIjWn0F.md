Now I have all the information I need. Let me write the final review.

**Round 1 bracket**: After inspecting the paper, filtering the reviewer inputs, and comparing against calibration anchors in the 4–7 range, I initially place this paper between **4.0 and 5.5**. The paper has a clean practical idea and broad experimental coverage, but the core claim is unvalidated, gains are modest, and the framing overstates results. This is below the accepted papers at 6.0+, which tend to have clearer empirical validation and larger improvements.

**Narrowing**: Comparing against RLCF (6.67, accepted — stronger results and clearer contribution), DOTA (6.0, rejected despite interesting ideas), BAT-CLIP (5.5, mixed — had a fatal methodological concern), and InCPL (5.0, rejected — marginal improvements, terminology issues). The RTA paper is most comparable to papers in the 4.5–5.5 range — it has a practical contribution but the unvalidated mechanism prevents it from reaching accept territory. Final score: **5.0**.

---

## Summary

This paper proposes Regression-based Test-time Adaptation (RTA) for CLIP-based image classification. Instead of using entropy to select confident augmented views during test-time adaptation, RTA trains a LightGBM decision tree on pseudo-labeled data (ImageVal-12k, high-confidence CLIP predictions) to predict cross-entropy loss from logits. At test time, the regression model scores each augmented view and the lowest-predicted-loss views are selected for ensembling. The method is trained once offline and applied without per-instance optimization. Experiments span five ImageNet variants, ten cross-domain datasets, and three multi-label benchmarks using RN50 and ViT-B/16 backbones.

## Strengths

1. **The "Ceiling TTA" observation (Tables 1–2) is genuinely striking and well-documented.** Using true label cross-entropy for view selection yields dramatically higher accuracy than entropy-based selection (e.g., ViT-B/16 on ImageNet-A: 64.3% with entropy vs. 90.2% with LCE at 64 views). This finding is clearly presented and provides a strong empirical motivation for investigating regression-based view selection.

2. **Practical efficiency: the method is simple and computationally negligible at test time.** Training a LightGBM regressor once on 1,000 pseudo-labeled samples and using it for view selection without per-instance gradient updates or prompt tuning is genuinely appealing for deployment. The paper makes this practical advantage explicit.

3. **Broad experimental scope.** The paper evaluates on five ImageNet variants, ten cross-domain datasets, and three multi-label datasets with two backbones (RN50 and ViT-B/16). This coverage exceeds many TTA papers and gives reasonable confidence about where the method does and does not work.

## Weaknesses

### Major

1. **Motivation–execution gap: RTA does not meaningfully approach the ceiling that motivates the approach, and this is not discussed.** The paper opens by showing that true-label-CE view selection achieves overwhelming performance (e.g., ViT-B/16 on IN-A: 90.2%). This is framed as the motivation for learning the logits-to-CE mapping. However, RTA's actual performance (IN-A: 65.65%) is close to entropy (64.3%) and far from the ceiling (90.2%) — RTA captures only ~1.35 of the ~25.9 percentage-point gap. The paper never acknowledges or analyzes this discrepancy. Readers are left wondering why, if the regression model truly learns the logits-to-loss mapping, the gains are so marginal relative to the headroom. This weakens the paper's central narrative.

2. **The regression model's behavior is unvalidated against its stated objective.** The paper claims the core contribution is learning a "regression mapping relationship between augmented views and their corresponding cross-entropy loss" (Section 1). But the paper never directly tests whether the regression tree's predicted losses correlate with true cross-entropy loss on held-out test data. It also does not compare how the regression tree ranks views versus how entropy ranks them versus how true LCE ranks them. Without this validation, it is unclear whether the model is learning anything substantively different from a calibrated confidence score. The Spearman's correlation analysis (Figure 3) examines logit features vs. labels, not predicted vs. true loss. This is a significant evidential gap for a paper whose central mechanism is the regression mapping.

3. **Gains over baselines are modest on many benchmarks and unreplicated.** Several improvements are well under 1%:
   - ViT-B/16 on IN-1k: RTA 71.13% vs. Zero 70.89% (+0.24%)
   - ViT-B/16 on IN-R: RTA 81.05% vs. BCA 80.72% (+0.33%)
   - ViT-B/16 cross-domain average: RTA 68.70% vs. BCA 68.59% (+0.11%)
   
   On 6 of 10 cross-domain datasets (ViT-B/16), RTA does not match the best baseline (Pets, Flowers, DTD, EuroSAT, Food, SUN). No standard deviations, confidence intervals, or significance tests are reported anywhere in the paper. For sub-percentage-point differences, single-run results are insufficient to establish that improvements are meaningful rather than noise.

4. **No controlled ablation isolating the regression selector's contribution.** RTA is compared against full TTA methods that differ in many design dimensions (prompt updates, augmentation pipelines, ensembling strategies, entropy formulations). There is no experiment that holds everything constant and varies only the view-selection criterion (entropy vs. regression). The comparison against Zero is the closest, but Zero uses a different entropy formulation (bound entropy minimization) and its own hyperparameters. Without an equalized ablation, it is impossible to attribute the observed gains specifically to the regression-based selector rather than to pipeline differences.

### Minor

5. **Train-test distribution mismatch for the regression model.** The model is trained on logits from original (non-augmented) images but applied to logits from augmented views during TTA. The paper argues that "the original image itself can actually be regarded as a view" (Section 4.2), but provides no empirical analysis of whether the logit distributions differ between original and augmented views, or how this affects prediction quality.

6. **Selective training data.** The regression model is trained only on samples where CLIP's predicted confidence ≥ 0.8 (discarding potentially the majority of ImageVal-12k). The potential selection bias from training only on CLIP's own high-confidence predictions is not analyzed. If the model only learns from cases where CLIP is already confident, its ability to identify truly informative views from uncertain predictions is unclear.

7. **No empirical comparison against the most closely related prior work (Kim et al., 2020).** The paper correctly identifies Kim et al. (Learning Loss for Test-Time Augmentation) as the most related work and describes differences in approach, but provides no experimental comparison. Given the closely related setup, this omission makes it hard to assess RTA's relative contribution.

8. **Overstated claims.** The abstract and conclusion state that RTA "significantly outperforms existing entropy-based TTA methods." Sub-percentage-point gains on several benchmarks do not support the adverb "significantly" without statistical testing. The "overwhelming performance" descriptor is used for the ceiling (which is fair) but the phrasing could mislead readers about RTA's own results.

### Trivial

9. **Equation (8) notation error.** Equation (8) uses `x_i^reg` where it should use `x_i^test` to denote test-time augmented views (line 312). The same issue propagates to Equations (9) and (10). This does not affect comprehension but should be corrected.

## Nice-to-Haves

- Direct analysis of the regression tree's predicted vs. true CE loss on held-out test data, and comparison of view rankings (regression vs. entropy vs. true LCE).
- A controlled ablation that replaces the regression selector with entropy in the exact same augmentation + ensembling pipeline.
- Candid discussion of why RTA does not approach the ceiling performance, and what would be needed to close that gap.

## Removed Points

These points from the input review were removed; included here for completeness:

- *"The paper never formally defines what 'confident views' are"* — The paper defines confident views as those with low entropy/loss in Section 3 (Preliminaries). This is clearly addressed.
- *"Figure 4/5 analysis adds limited insight"* — Subjective opinion about the value of scaling analysis, not a verifiable weakness.
- *"Spearman's correlation doesn't report numerical values in text"* — Values are presented in Figure 3 (a figure). This is a figure-vs-text formatting choice, not a substantive omission.
- *Critique about missing related works* — Cannot be independently verified per policy.
- *Pure formatting/style nitpicks* — Parser artifacts, not author errors.
- *Reproducibility complaints about missing appendix content* — Appendix is stripped by the parser; assumed present in original submission.

## Novel Insights

The harsh critique surfaces one genuinely novel observation not present in the paper itself: the regression model trained on pseudo-label CE from high-confidence CLIP predictions is effectively a *learned confidence score* — a learned function that maps logits to a scalar measure of how "CLIP-confident" a view looks. The paper presents this as fundamentally different from entropy, but the critic's reframing — that it may simply be a better-calibrated version of the same quantity — is a useful lens. The paper would benefit from engaging with this interpretation directly and running the controlled experiments needed to distinguish between these explanations.

## Suggestions

1. **Validate the central mechanism.** Add a section analyzing the regression model's predictions against true LCE on a held-out labeled set. Report the correlation between predicted loss and true loss, and compare how top-k view selections from the regression model overlap with those from entropy and true LCE.
2. **Run a controlled ablation.** Same augmentation pipeline, same ensembling, same k — but compare entropy-based view selection vs. regression-based view selection to isolate the selector's contribution.
3. **Report uncertainty.** Provide means and standard deviations over multiple runs (or at minimum bootstrapped confidence intervals) for key comparisons, especially where margins are <1%.
4. **Acknowledge the gap.** Candidly discuss the gap between the ceiling motivation and RTA's actual performance, explaining why it exists (pseudo-labels vs. true labels, training on original vs. augmented views, etc.).
5. **Tone down claims.** Replace "significantly outperforms" with specific, quantified descriptions of improvement, especially where margins are below 1% and no significance testing is provided.

## Score and Decision

**Round 1 bracket**: 4.0–5.5 (determined by comparison to calibration anchors).

**Calibration anchors consulted** (all from deepreview_13k_calibration):

| Paper | Avg Score | Round | Comparison to RTA |
|-------|-----------|-------|-------------------|
| RLCF (kIP0duasBb.md) | 6.67 | Bracket | Stronger empirical results and clearer novel contribution; accepted |
| ML-TTA (75PhjtbBdr.md) | 6.25 | Bracket | Novel multi-label TTA framing with well-supported results; accepted |
| DOTA (yD2JMeKumt.md) | 6.00 | Bracket | Interesting distributional TTA idea but rejected due to methodological concerns — similar situation to RTA |
| BAT-CLIP (z7PhIgVmZU.md) | 5.50 | Narrow | Had a fatal methodological flaw (alleged label leakage); RTA is cleaner methodologically |
| InCPL (Rc3RP9OoEJ.md) | 5.00 | Bracket | Marginal improvements and terminology issues; rejected — comparable to RTA's situation |
| ROSITA (lF9QXpfNHm.md) | 4.67 | Narrow | Incremental contribution, missing baselines; rejected — RTA has broader experiments |
| TTAAux (PxL35zAxvT.md) | 4.67 | Narrow | Methodological concerns; RTA is cleaner |
| TUI (LGIhipNvCQ.md) | 4.25 | Narrow | Conformal prediction for CTTA; RTA has broader experiments |

**Final score determination**: RTA has a clean, practical idea and broad experimental coverage that places it above rejected papers with fatal flaws or trivial contributions (scores 1–4). However, the central mechanism is unvalidated, gains are modest (often <1%), and no controlled ablation isolates the contribution — issues that prevent it from reaching the 6+ band where accepted papers in this area sit. The paper is comparable to InCPL (5.0, rejected) in terms of the gap between claims and evidence. Score: **5.0** — borderline reject.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>