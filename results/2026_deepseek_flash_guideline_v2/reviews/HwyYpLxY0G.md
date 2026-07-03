Now I have all the information needed. Let me produce the final consolidated review.

## Summary

This paper proposes Aligned Scoring Rules (ASR) for textual information elicitation, combining the proper scoring rule framework of Wu & Hartline (2024) with convex optimization to align scoring rules with human preference scores (e.g., instructor scores of peer reviews). The key technical contribution is formulating alignment as a convex optimization over *separate scoring rules*—a weighted sum of single-dimensional proper rules—which preserves properness guarantees (truthfulness) while enabling efficient gradient-descent minimization of MSE with a reference score. Experiments on peer grading data (22 assignments, ~500 reviews) show that ASR achieves substantially lower MSE and higher correlation with reference scores than the non-aligned baselines from Wu & Hartline (2024).

## Strengths

1. **Principled convex formulation for aligning proper scoring rules.** Section 3.2 (Corollary 3.4) proves that restricting to separate scoring rules makes the alignment problem convex, enabling efficient optimization while preserving properness. This is a clean, theoretically sound advance beyond prior work: Wu & Hartline (2024) did not optimize for alignment, and Li et al. (2022) optimized for effort incentives rather than alignment with a reference score. The observation that the same formulation would *not* be convex for max-over-separate rules (line 252) is explicit and honest about the trade-off.

2. **Large empirical gains over non-aligned baselines across all metrics.** Table 1 (lines 348–353) reports that ASR reduces MSE from 9.541 (EGPT-AV) to 1.730 (an 82% reduction) and increases Pearson correlation from 0.294 to 0.717 when aligned to instructor scores, with similarly large improvements on the LLM-Judge reference. The gaps are far beyond what could be attributed to noise—notably, the non-aligned EGPT baselines are *worse* than a constant predictor, demonstrating that properness alone does not imply good alignment.

## Weaknesses

### Fatal

None.

### Major

1. **Evaluation does not clearly specify train/test separation.** The paper mentions "training data \(D\)" for computing the constant baseline mean (line 358), but it is never stated whether the MSE, Pearson, and Spearman metrics in Table 1 are reported on the same training set or on held-out data. If the numbers reflect training-set performance, they are optimistic and do not measure generalization. If they reflect a held-out test set, the paper should state this explicitly and describe the split protocol. This is a basic methodological requirement for any experimental paper.

2. **No uncertainty quantification.** The paper reports point estimates for MSE, Pearson correlation, and Spearman correlation without any confidence intervals, standard errors, or cross-validation. The dataset comprises roughly 500 reviews across 22 assignments (Section 5.1), which is modest in size; variance across assignments or folds could be substantial. Without a measure of stability, the reader cannot assess whether the observed improvements are reliable or driven by a few favorable partitions.

3. **No comparison against an optimized alternative, leaving the cost of properness unquantified.** ASR is optimized to minimize MSE with the reference score, while the baselines (EGPT-AV, EGPT-MV) are fixed-form rules *not* designed or optimized for alignment. This comparison demonstrates that optimization helps—a valid but weak finding. The paper's central thesis involves a trade-off between properness and alignment, yet it does not train an **unconstrained** version of the same model (same variables, same MSE objective, no properness constraints) to measure how much alignment is sacrificed for the properness guarantee. Without this comparison, the paper cannot support its implicit claim that the properness constraint does not meaningfully harm alignment. Similarly, optimizing within the V-shaped or max-over-separate families (even approximately) would clarify whether ASR's specific design choices (separate scoring rules, convexity-enforced properness) are what drive the improvement.

### Minor

4. **"Nearly-identity linear fit" is over-interpreted as a substantive finding.** Section 5.3 presents the near-identity regression of reference scores on ASR scores as "the first criterion for evaluating our approach." Since ASR was trained to minimize MSE directly with those reference scores, a good linear fit is a convergence check, not evidence of a novel property. The observation becomes more meaningful when contrasted with the EGPT baselines (which, per footnote 3, produce scores on a completely different scale), but the paper does not make this contrast.

5. **Scope of the "Know-it-or-not" assumption.** The paper is transparent that the ternary report space \( \{0,1,\perp\} \) is an empirical observation about the specific peer-grading dataset (line 110). However, Definition 2.3 and the formal machinery treat it as a general model, and the paper does not discuss how this assumption bounds the applicability of ASR to settings where agents express graded or probabilistic confidence. This limits the contribution's generality in a way that should be acknowledged more explicitly.

### Trivial

- Footnote 1 notes that when the ground truth contains \(\perp\), the agent is scored by an expected score where the binary state is drawn from the prior. This introduces Monte Carlo noise into the scoring process. A brief discussion of how this affects score informativeness would be helpful.

## Nice-to-Haves

- **Quantify the cost of properness** by training an unconstrained version of the scoring rule (same hypothesis class, same MSE objective, no properness constraints) and comparing its test-set MSE to ASR's.
- **Report variance** using bootstrap or cross-validation to provide confidence intervals for the metrics in Table 1.
- **Test generalization** across assignments (e.g., train on one class, test on the other) to see whether ASR captures general patterns of review quality.
- **Compare against a simple calibration baseline**: e.g., take EGPT(AV) and apply an affine transformation to match the reference score's mean and variance, to isolate whether fine-grained optimization buys anything over re-scaling.
- The paper notes (but does not discuss) that EGPT baselines achieve MSE *worse than the constant* (e.g., 9.541 vs. 3.741 for Instructor). This asymmetry is interesting—it shows that un-optimized proper scoring rules can be *negatively* correlated with human preference—and warrants explicit commentary.

## Removed Points

These points were raised by the reviewers but are removed from the main evaluation for the following reasons:

- **"The experimental comparison is staged / not informative"** (Harsh Critic #1): Removed as overstatement. Comparing an optimized method against state-of-the-art prior methods that were not designed for alignment is a standard and informative evaluation. The finding that properness alone (EGPT) does not produce good alignment is itself meaningful. However, the narrower concern about missing optimized baselines is preserved in Major #3 above.
- **"Nearly-identity linear fit is circular / not evidence"**: Removed the "circular" framing. It is not circular—the optimization could fail—but it is over-interpreted. A weakened version is preserved as Minor #4.
- **"Know-it-or-not assumption is more restrictive than the paper acknowledges"**: Removed the "more restrictive" framing because the paper explicitly acknowledges this is dataset-specific (line 110). A milder version is preserved as Minor #5.
- **"Best constant baseline is surprisingly effective"**: Moved to Nice-to-Haves as an observation worth discussing, not a weakness.
- **"Grounding truth can contain ⟂ introduces noise"**: Moved to Trivial/Nice-to-Have.
- **Interpretability (Strength Finder strength #4)**: Removed as a strength because the paper *claims* interpretability (lines 33-36, 231) but provides only a case study in the removed appendix; there is no empirical evaluation of interpretability in the main text.
- **Nearly-identity linear fit (Strength Finder strength #3)**: Removed as a strength since it is over-interpreted; preserved as a minor observation.

## Novel Insights

None beyond the paper's own contributions. The reviews do surface a useful meta-point: this paper sits at an awkward intersection of theory (mechanism design) and empirics (NLP/LLM evaluation), and the evaluation standards of both communities should be met. The theoretical side is well-executed (convex properness-preserving optimization), but the empirical side (baseline choices, uncertainty quantification, train/test separation) does not meet the bar for a systems-type contribution. This tension is the core reason the paper is borderline—not because the theoretical idea is weak, but because the empirical execution is incomplete.

## Suggestions

1. **Clarify the evaluation protocol.** State explicitly whether Table 1 reports training-set or held-out metrics. If the former, add a held-out evaluation. If the latter, describe the split procedure.
2. **Add uncertainty quantification.** At minimum, provide bootstrap confidence intervals or per-assignment error bars for the three metrics.
3. **Add an unconstrained baseline.** Train the same model without properness constraints and report the gap in MSE. This directly addresses the paper's core trade-off and would substantially strengthen the contribution.
4. **Acknowledge the evaluation limitations more candidly in the paper.** The current text ("outperforms previous methods") is too strong given the gaps; a more measured claim would better match the evidence.

## Score and Decision

I assign a score of **4.5** (borderline reject).

**Reasoning**: The paper addresses a well-motivated problem and makes a clean theoretical contribution (convex optimization of separate scoring rules for alignment while preserving properness). The empirical results are suggestive and directionally correct. However, the evaluation has three significant gaps that prevent certification of the main claims: (1) it is unclear whether the reported metrics reflect training or held-out data; (2) point estimates are reported without any measure of uncertainty; and (3) the paper does not quantify the cost of the properness constraint by comparing against an unconstrained optimized baseline. These gaps are addressable and do not invalidate the theoretical contribution, but in their current form they leave the paper's central empirical claim inadequately supported. With substantial revisions to the evaluation (particularly points 1-3 above), this could become a solid paper.

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>