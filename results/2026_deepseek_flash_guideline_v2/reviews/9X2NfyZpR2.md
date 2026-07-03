I was unable to access the calibration corpus due to a file system error. I will proceed with my best judgmental calibration based on the paper content and review synthesis.

Here is the final consolidated review:

---

## Summary

The paper introduces TbLTA, the first weakly-supervised framework for dense Long-Term Action Anticipation (LTA) trained exclusively from video transcripts (ordered action lists without timing or duration). The method uses a temporal alignment module (ATBA) to generate pseudo-labels from transcripts, which supervise both a segmentation head and an anticipation decoder. Transcripts are also leveraged via cross-modal attention with a local binary mask to enrich video features. Despite using no frame-level annotations, TbLTA achieves competitive results on Breakfast (29.03 avg MoC, matching/beating supervised FUTR/ActFusion), demonstrates feasibility on 50Salads and EGTEA, and shows particular strength on rare classes on EGTEA.

## Strengths

1. **Novel problem formulation and first transcript-only LTA method.** The paper correctly identifies an underexplored gap—dense LTA under weak supervision—and proposes the first framework that operates without any frame-level boundary annotations. This opens a genuinely new direction for scalable LTA research.

2. **Strong results on the Breakfast dataset.** TbLTA's deterministic variant (29.03% avg MoC) outperforms fully-supervised FUTR (26.59%) and matches ActFusion (28.45%). At 30% observation, TbLTA achieves the highest scores across all prediction horizons. This is the paper's strongest empirical result and validates that transcript-only supervision can be viable for dense LTA.

3. **Superior rare-class performance on EGTEA.** Table 2 shows TbLTA achieves 60.11% mAP on Rare classes, surpassing fully-supervised Timeception (59.70%) and Anticipatr (55.10%). This suggests transcript-level semantic supervision can mitigate data imbalance—a concrete advantage over frame-label-based methods.

4. **Ablation studies validate individual architectural components.** The ablation hierarchy (*w/o cross-att* < *cross-att simplex* < *TbLTA*) holds consistently across datasets. The CTC loss, cross-modal attention mask, and CRF each show non-trivial contributions, with the structured cross-modal design outperforming unconstrained cross-attention by ~1.9 points on Breakfast. The progressive three-stage training scheme (Section 4.1) is a practical design that addresses the cold-start problem of pseudo-labels.

5. **Self-supervised duration prediction.** The momentum-based duration buffer (Eq. 7) is a clever mechanism that provides temporal regularization without any boundary annotations, contributing ~0.2–3.3 points in the ablation study.

## Weaknesses

### Fatal
None.

### Major

1. **Missing analysis of pseudo-label quality.** The entire framework hinges on ATBA-generated pseudo-labels—they supervise the TAS head, the anticipation decoder, and construct the cross-modal attention mask. Yet the paper provides no analysis of how accurate these pseudo-labels are, no comparison to ground-truth frame labels (even on a held-out subset), and no study of how alignment errors propagate to anticipation errors. This is a foundational gap in the evidence chain. Since pseudo-label noise cascades to every downstream component, the reader cannot assess whether the performance gap on 50Salads (trailing supervised methods by ~26%) stems from alignment difficulty, anticipation difficulty, or both.

2. **The "competitive with fully supervised" claim is overstated in the abstract and conclusion.** On Breakfast the claim holds (TbLTA beats supervised methods on average). But on 50Salads, TbLTA deterministic (20.92 avg MoC) trails ActFusion (28.39 avg) by ~26% relative. On EGTEA, TbLTA (65.37 mAP) trails Anticipatr (76.80 mAP) by ~15%. The paper's body text acknowledges this for 50Salads, but the abstract asserts transcript supervision is a "robust and less costly alternative" to full supervision—a claim that the three-dataset average does not support. The conclusion similarly claims results are "competitive with, and in certain settings even superior to, fully supervised methods" without qualifying the substantial variation. A reader skimming these sections gets a misleadingly uniform impression.

3. **Inconsistent evaluation regime between main results and ablations.** The main comparison (Table 1) reports deterministic TbLTA results separately from stochastic (Top1) results, with Top1 substantially higher (e.g., 37.15 vs 29.03 on Breakfast avg). However, the ablation study (Table 4) uses the stochastic Top1 protocol as the default metric. The ablation baseline values (28.5 on 50Salads, 37.2 on Breakfast) match the Top1 stochastic results, not the deterministic results (20.92, 29.03). While the paper states "we report results using the Top-1 MoC metric" for ablations, it does not explain why the stochastic protocol was chosen as the ablation baseline or whether the component contributions hold under deterministic evaluation. This makes it hard to interpret whether ablation findings generalize to the deterministic setting reported in the main comparison.

### Minor

1. **No statistical significance or variance reporting.** All results are single point estimates. Given the small dataset sizes (50Salads: 50 videos across 5 splits), standard deviations would help assess whether observed differences between ablations are meaningful.

2. **Weakly-supervised baseline comparison is thin.** WS-DA (Zhang et al., 2021) is the only weakly-supervised comparison, with only two numbers across both datasets (both at Obs30% only). The paper correctly notes this limitation (the field is nascent), but the framing "consistently surpasses prior weakly-supervised baselines" is technically true yet minimally informative.

3. **Duration loss ablation shows inconsistent benefit on 50Salads.** At Obs30%/Pred20% on 50Salads, "w/o duration" (33.8) outperforms the full TbLTA (33.3). The overall average (28.5 vs 26.3) supports the claim that duration loss helps, but the benefit is not uniform across settings, and the paper's claim that it "serves as a temporal regularizer that stabilizes long-horizon predictions" is not fully supported by the per-setting breakdown.

### Trivial
- The stochastic "Top1" protocol is relegated to the supplement without a brief explanation in the main text (number of samples, selection criterion).
- No computational cost comparison (training time, inference time, model size) despite motivating transcript supervision as "less costly."

## Nice-to-Haves
- Pseudo-label quality analysis (alignment accuracy vs. ground-truth frame labels, correlation of alignment errors with anticipation errors).
- Comparison with a simple weakly-supervised baseline (e.g., training a supervised LTA model on pseudo-labels from an off-the-shelf TAS aligner).
- Variance/confidence intervals for main results and key ablations.

## Removed Points
The following points raised by reviewers were filtered out as they do not constitute valid or substantive weaknesses:

1. **Circular dependency concern (confirmation bias in cross-attention).** The generic concern about pseudo-labels and cross-attention creating a self-reinforcing loop is common to self-training approaches. The paper's three-stage progressive training scheme (Section 4.1) is explicitly designed to address this. *Removed as insufficiently specific.*

2. **Training uses future frames (training-inference mismatch).** This is standard practice in the LTA literature ("following Gong et al., 2024"). All supervised baselines use the same strategy. *Removed as strawman.*

3. **Conflation of transcript-level vs frame-level prediction in related works.** This is a minor organizational observation that does not affect the paper's contributions or evaluation. *Removed as a formatting/organizational nitpick.*

4. **Generic strengths from Strength Finder** (e.g., "paper addresses an important problem," "method is clearly described"). These lack specific empirical grounding. *Removed per filtering rules.*

5. **Request for more weakly-supervised baselines beyond what exists in the literature.** The paper cannot create baselines that do not exist. The only existing weakly-supervised LTA method (WS-DA) is compared. *Removed as scope creep.*

6. **Request for momentum buffer stability analysis.** This is an implementation detail; the ablation already validates the duration loss's overall contribution. *Removed as nice-to-have, not a weakness.*

## Novel Insights
None beyond the paper's own contributions. Both reviewers converge on the paper's genuine novelty (first transcript-only LTA method) and its main gaps (missing pseudo-label analysis, overclaimed framing, evaluation regime inconsistency). The harsh critic's framing of the paper as "establishing a baseline rather than outperforming" is a useful reframing that the authors should adopt.

## Suggestions
1. **Add pseudo-label quality analysis**: Report alignment accuracy of ATBA against ground-truth frame labels (even on a held-out subset of a single split) and show how alignment errors correlate with anticipation errors. This single addition would address the biggest gap in the evidence chain.
2. **Reframe the contribution**: Position the paper as establishing the first transcript-only LTA baseline and demonstrating feasibility, rather than as a "robust alternative" to full supervision. Qualify dataset-specific competitiveness in the abstract and conclusion.
3. **Explain the stochastic protocol in the main text**: State the number of samples used during stochastic inference and whether selection uses a validation set. Clarify why ablations use this protocol rather than the deterministic one.
4. **Report standard deviations** for main results and key ablations, especially given the small dataset sizes.
5. **Add a simple weakly-supervised baseline**: Train a supervised LTA model (e.g., ActFusion or FUTR) on pseudo-labels from an off-the-shelf TAS alignment method to provide a more informative weak-supervision comparison.

## Score and Decision

**Calibration note:** The calibration search tool was unable to access the human-review corpus due to a file system error. The following assessment is based on direct judgment of the paper's content against ICLR standards.

**Score reasoning:** The paper has genuine novelty (first transcript-only LTA method) and one strong empirical result (Breakfast), supported by informative ablations. However, there are three major weaknesses: (1) no analysis of the pseudo-label quality that the entire framework depends on, (2) overclaimed framing in the abstract/conclusion relative to the actual three-dataset results, and (3) an unexplained shift between deterministic and stochastic evaluation regimes between the main table and the ablations. These are not fatal—the method is sound and the contribution is real—but they prevent the paper from being fully accepted in its current form. The paper sits at the borderline: with pseudo-label analysis, reframed claims, and clarified evaluation protocol, it would be a solid accept. In its current form, the gap between what is claimed and what is demonstrated is too wide.

**Score:** 5.5

**Decision:** Reject

The paper has a valuable core contribution and the strongest results (Breakfast) are genuinely impressive for a weakly-supervised method. However, the missing pseudo-label analysis, overclaimed framing, and inconsistent evaluation protocol collectively weaken the evidence chain enough that substantial revision is needed. The paper is close to the acceptance threshold and the authors are encouraged to resubmit with the suggested improvements.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>