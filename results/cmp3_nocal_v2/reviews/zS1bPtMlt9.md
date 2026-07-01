## Summary

REPL proposes a semi-supervised LiDAR semantic segmentation framework that refines pseudo-labels via error estimation and masked reconstruction, rather than filtering or reweighting them. The method uses a teacher-student architecture where a pseudo-label refiner identifies unreliable voxels via confidence-based agreement and corrects them through a masked reconstruction module. Experiments on nuScenes-lidarseg and SemanticKITTI show strong performance, particularly on nuScenes across all label ratios.

## Strengths

1. **Conceptually sensible departure from the dominant paradigm.** Most prior LiDAR semi-supervised methods accept teacher predictions as given and adjust post-hoc usage (filtering/reweighting). REPL instead attempts to correct the pseudo-labels themselves, which is a legitimate and under-explored direction.

2. **Ablation study cleanly isolates each component's contribution.** Tables 2, 3, and 5 progressively add loss terms (supervised refiner training, negative learning, mixed-scene training) and show consistent mIoU improvements. The ordering of contributions is plausible and gives confidence that the components are working as intended.

3. **Strong results on nuScenes-lidarseg.** REPL achieves the best results at 1%, 10%, 20%, and 50% labeled ratios, with gains of +2.3, +2.3, +1.5, and +1.7 mIoU over the next best method (IT2). These are non-trivial margins on a competitive benchmark.

4. **Computational overhead is quantified and moderate.** Table 7 shows the refiner adds 0.25s latency and 396MB memory for +9.1 mIoU gain, enabling a practical assessment of the cost-benefit trade-off.

## Weaknesses

### Fatal
None.

### Major

1. **Factual error in reporting: the paper claims best at 1% on SemanticKITTI, but its own table shows otherwise.** Line 166 states: *"On SemanticKITTI, REPL also showed strong results, achieving the best performance at 1% and 50%."* However, Table 1 shows REPL at 54.7 mIoU for SemanticKITTI 1%, while LaserMix++ achieves 56.2 and FrustrumMix achieves 55.7 — REPL is third. The bold formatting in the table is also inconsistent with the stated rule ("best results in each column are shown in bold"). This undermines confidence in the paper's central claim of state-of-the-art performance and must be corrected.

2. **Citation inconsistencies between text and table make it unclear which baselines were actually compared.** Three methods have mismatched citations:

   | Mentioned in text | Appearing in table | Discrepancy |
   |---|---|---|
   | "AIScene (Liu et al., 2025)" | "AScene (Xu et al., 2023)" | Different name, different authors, different year |
   | "FrustumMix (Xu et al., 2025)" | "FrustrumMix (Kong et al., 2023)" | Different spelling, different first author, different year |
   | "SLiDR (Sautier et al., 2022)" | "SLiDR (Santner et al., 2022)" | Author name mismatch |

   The reader cannot determine whether the correct methods were compared or whether the reported numbers come from properly configured re-implementations. This is an evidential problem that damages the comparison's credibility.

3. **No variance reporting whatsoever.** Every number is a single point with no standard deviations, confidence intervals, or statement about number of runs or random seeds. Semi-supervised learning results are known to be sensitive to initialization, data splits, and training stochasticity, especially at low label ratios where variance is highest. Several margins on SemanticKITTI are small (e.g., average mIoU of 61.6 vs. AScene's 61.5 — a 0.1 point difference), and without variance information the reader cannot determine whether improvements are statistically meaningful.

### Minor

4. **The theoretical analysis is ornamental rather than substantive.** Proposition 1 (H(Y|X,T) ≤ H(Y|X)) is a direct consequence of the basic fact that conditioning reduces entropy — it tells us nothing specific about REPL or LiDAR segmentation. Proposition 2 formalizes the trade-off between error correction and error introduction but is a straightforward algebraic identity once variables are defined. The empirical verification (measuring q and r from REPL's own outputs and confirming they satisfy the condition) is circular: the condition is defined in terms of the method's own correction and error-introduction rates. The theory does not predict when REPL would fail or explain why it works beyond what an ablation study already shows.

5. **Large headroom between heuristic and oracle error detection.** Table 4 shows a 7.3 point gap (60.0 vs. 67.3 mIoU) between the paper's heuristic error mask and an oracle mask using ground truth. The paper acknowledges this but does not analyze what kinds of errors the heuristic misses (false negatives) or what correct predictions it incorrectly flags (false positives). This bottleneck is the single largest room for improvement and merits deeper analysis.

6. **The error detection relies on student predictions that are themselves evolving and potentially biased.** The unreliable voxel identification uses student-teacher agreement, but the student is trained on potentially noisy pseudo-labels, creating a feedback loop. The stop-gradient between student and refiner (line 125) mitigates but does not eliminate the concern that early student mistakes may bias what the refiner learns to treat as errors. The paper does not analyze this dependency.

7. **Limited hyperparameter search for the key confidence threshold κ.** Table 6 tests only three values (0.2, 0.4, 0.6), with a wide swing from 55.1 to 60.0 to 58.4. The same κ=0.4 was used across both datasets and all label ratios without demonstrating it is optimal across these conditions. The ablation is too coarse.

8. **The mixed-scene training introduces a distribution mismatch.** The refiner is trained on errors from mixed labeled+unlabeled scenes but during inference must handle errors on purely unlabeled scenes (Section 3.3, lines 99-101). The paper does not discuss whether this gap affects refinement quality.

### Trivial

9. **Novelty claim slightly overreaches.** The paper frames itself as the first to "improve pseudo-label quality" rather than adjust usage. Since related pseudo-label refinement ideas exist in 2D SSL (Noisy Student, masked image modeling approaches), the contribution is more precisely: applying masked-reconstruction-based pseudo-label refinement to *LiDAR* semantic segmentation. The claims could be scoped more carefully.

## Nice-to-Haves

- **Run main experiments with multiple seeds (3–5) and report mean ± std.** This is the single most impactful addition for verifying the claimed improvements.
- **Analyze correction and error-introduction rates (q, r) per class** to reveal which categories the refiner handles well and where it struggles.
- **Analyze the types of errors the heuristic mask misses** (false negatives) and those it incorrectly flags (false positives) to inform better error detection.
- **Consider whether the refiner could be disabled after the training midpoint** (Figure 5 shows declining improvement in the second half), potentially saving computation without harming performance.

## Removed Points

These points were raised in the input review but are removed for the reasons stated:
- *"No discussion of cross-dataset generalization"* — scope creep; in-domain semi-supervised evaluation is standard practice.
- *"Specific margin numbers (+0.8 at 10%, +1.1 at 20%) in the variance criticism"* — these numbers could not be verified from the paper's table; the general criticism about missing variance is retained.
- *"The average column is not particularly informative"* — this is a formatting preference with negligible impact on the paper's contributions.
- *"Declining improvement in Figure 5"* — the paper explicitly discusses this trend (line 277) as an expected consequence of the student becoming more accurate.
- *"The paper does not discuss whether the refiner could be disabled after the midpoint"* — this is a suggestion for future optimization, not a weakness of the presented method.

## Novel Insights

The reviewer's most useful observation is that the 7.3-point gap between the heuristic error mask and the oracle (Table 4) constitutes the primary bottleneck in the REPL pipeline — larger than any single loss component in the ablation study. This reframes the paper's contribution: the masked reconstruction refiner is shown to work well when given accurate error locations, but the current error detection heuristic is the limiting factor. The paper's framing (presenting this as validation of the heuristic) understates this finding's significance for future work.

## Suggestions

1. **Correct the factual error.** Either fix the claim about SemanticKITTI 1% results or correct the table numbers if they are wrong. The bold formatting in Table 1 also needs alignment with the stated rule.
2. **Reconcile all citation inconsistencies.** Ensure the text and table agree on method names, authors, and publication years for every baseline.
3. **Add multi-run statistics.** Report means and standard deviations over at least 3 seeds for all main results.
4. **Deepen the error mask analysis.** Characterize the types of errors the heuristic mask misses and falsely flags, and discuss how improved error detection could translate to better final performance.
5. **Tone down theoretical claims.** Either replace the current theoretical section with a genuine analysis of failure modes, or reframe it explicitly as a formalization of the correction-introduction trade-off rather than a "theoretical contribution."
6. **Consider broader hyperparameter search** for κ, or evaluate sensitivity across label ratios.

## Score and Decision

**Score:** The paper proposes a genuinely different approach to LiDAR semi-supervised learning with strong results on one of two benchmarks. However, the factual error in the paper's own results reporting, citation inconsistencies that prevent verification of the comparison, and complete absence of variance information are significant issues that prevent acceptance in the current form. The core idea is promising and could be acceptable after thorough revision.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>