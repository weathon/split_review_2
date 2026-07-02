## Summary

This paper proposes REPL, a semi-supervised LiDAR semantic segmentation framework that refines pseudo-labels through a two-stage process: detecting potentially erroneous voxels via confidence-based teacher-student agreement, and then correcting them via masked reconstruction with a learnable refiner. The approach directly addresses pseudo-label quality at the point of generation rather than applying post-hoc filtering or reweighting. The method is evaluated on nuScenes-lidarseg and SemanticKITTI across varying label ratios.

## Strengths

- **Well-motivated problem framing.** The paper clearly articulates the limitation of existing "post-hoc" pseudo-label strategies (filtering, reweighting) and proposes a principled alternative: improve pseudo-labels directly via error estimation + masked reconstruction. This framing meaningfully distinguishes REPL from prior work (Section 1, paragraphs 3–4).

- **Substantial and consistent gains on nuScenes-lidarseg.** REPL outperforms the second-best method (IT2) by an average of +2.0 mIoU across all label ratios on nuScenes, with the largest margin at 10% labeled data (74.4 vs. 72.1). At 50% labeled data, REPL achieves 75.8 vs. IT2's 74.1 (Table 1). These are practically meaningful improvements.

- **Comprehensive ablation study.** The paper decomposes the contribution of each loss term for both the refiner (Table 2) and the segmentation network (Table 3), showing incremental gains from each component. The analysis of error mask quality (Table 4, oracle at 67.3 vs. heuristic at 60.0) is informative and honestly acknowledges the gap to the upper bound.

- **Computational cost reporting.** Table 7 quantifies latency (+0.25s) and memory (+396MB) overhead from the refiner alongside the +9.1 mIoU gain, enabling readers to assess the practical trade-off.

- **Honest failure case analysis.** Figure 4 shows examples where refinement over-corrects, and the text acknowledges that "successful corrections outweigh these localized failures." This transparency strengthens the paper.

## Weaknesses

### Fatal
None.

### Major

- **Factually incorrect claim about SemanticKITTI 1% results.** Section 4.2 states that REPL "achiev[es] the best performance at 1% and 50%" on SemanticKITTI. Table 1 contradicts this: at SemanticKITTI 1%, LaserMix++ achieves 56.2, FrustrumMix achieves 55.7, and REPL achieves 54.7 — third place, not first. This is not a subtle discrepancy; it is a direct factual error in a headline result statement. The abstract's claim that the method "achieves the state of the art" and the third contribution bullet must be qualified accordingly. The error is fixable but must be corrected.

### Minor

- **Overclaimed theoretical analysis.** Proposition 1 states H(Y|X,T) ≤ H(Y|X), which is a textbook property of conditional entropy — it carries no practical content about generalization or sample efficiency under limited supervision. Proposition 2 provides a correct algebraic condition (ζ = π − r/(q+r) > 0) but is essentially an accounting identity that follows from definitions. The paper frames this as "rigorous analysis" that "establishes the condition under which... refinement is beneficial" (contribution bullet 2), which overstates the depth of the theoretical content. The ζ condition itself is useful as a diagnostic, and the empirical measurement of REPL's ζ values is informative; the issue is one of framing.

- **No variance or statistical significance reported.** All results in Table 1 are single numbers without standard deviations or multiple runs. For SemanticKITTI, the average improvement over the second-best method (AScene/FrustrumMix both at 61.5) is only 0.1 mIoU — within the noise floor of a single-run evaluation. Even for nuScenes where gains are larger, the absence of any uncertainty quantification makes it difficult to assess whether the reported differences reflect genuine improvement or run-to-run variation.

- **Citation and name inconsistencies between text and table.** The text (Section 4.2) refers to "AIScene (Liu et al., 2025)" and "FrustumMix (Xu et al., 2025)," but Table 1 lists "AScene (Xu et al., 2023)" and "FrustrumMix (Kong et al., 2023)." These are different names with different citations. The authors must clarify which methods are actually being compared and resolve the inconsistencies.

- **Missing semi-supervised baseline without refinement in ablation.** Table 2 compares the refiner with various loss combinations against a supervised-only baseline (50.9 mIoU). This does not isolate the refiner's contribution from the teacher-student framework's contribution. A natural baseline would be training the student with raw teacher pseudo-labels (teacher-student without the refiner), which would directly quantify the value added specifically by refinement.

### Trivial
None.

## Nice-to-Haves

- Clarify the data split (labeled, unlabeled, or validation set) used to measure π, q, and r in the empirical analysis of the improvement condition (Section 3.5, Figure 2). These quantities require ground-truth labels, and the measurement protocol is not stated.
- Discuss why the gap between the heuristic error mask and the oracle (7.3 mIoU, Table 4) exists — what kinds of errors does the heuristic systematically miss vs. catch?
- The error detection heuristic flags ~60% of voxels for potential refinement (κ=40th percentile). A brief discussion of this design choice and its implications would be helpful.

## Removed Points

The following points from the input review were removed per the filtering rubric:
- **60% of voxels flagged as unreliable:** This was an observation, not a framed weakness against the paper's claims.
- **Bold formatting concern in Table 1:** Parser artifact issue; the paper's caption states "best results in bold" and parser-extracted formatting may not match the original.
- **"Eleven times" arithmetic:** Folded into the overclaimed-theory weakness above; not a separate point.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Correct the factual error regarding SemanticKITTI 1% results — revise the text in Section 4.2 and the bolding in Table 1 so they match the actual numbers.
2. Add variance estimates (standard deviations over ≥3 runs) for the main results, or at minimum acknowledge the limitation of single-run reporting and justify it.
3. Add a row to the ablation (Table 2) showing teacher-student without the refiner, to isolate the refiner's contribution from the student-teacher framework's contribution.
4. Resolve the citation inconsistencies (AIScene/AScene, FrustumMix/FrustrumMix) between text and Table 1.
5. Tone down the "rigorous analysis" framing of the theoretical section — present Propositions 1–2 as useful diagnostics rather than deep theoretical guarantees.

## Score and Decision

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>