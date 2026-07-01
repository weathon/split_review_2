Now let me produce the final review with all filtering and calibration applied.

## Summary

This paper proposes Medix, a framework for OOD detection that uses element-wise median (EWM) filtering on gradients of unlabeled wild data to identify outliers, then trains a binary OOD detector on the identified outliers and labeled InD data. The paper provides theoretical bounds on inlier/outlier misclassification rates for median-based filtering and demonstrates strong empirical results on CIFAR-10 and CIFAR-100 benchmarks.

## Strengths

1. **Novel median-based filtering approach with clear empirical motivation.** The preliminary experiment (Figure 1) showing a monotonic increase in L2 deviation between the InD mean gradient and the EWM of wild gradients as OOD samples are added provides intuitive grounding for the method. The use of element-wise median — which is robust to up to 50% contamination — is a genuine methodological innovation in the wild-data OOD setting.

2. **Strong empirical results, especially on CIFAR-10.** Medix achieves an average FPR95 of 0.80% (vs. 3.40% for WOODS) and AUROC of 99.74% (vs. 98.92%) on CIFAR-10 across five OOD datasets, with consistent improvements on every individual dataset. Results include standard deviations from 5 runs.

3. **Two-sided theoretical framing.** The paper provides formal bounds for both inlier misclassification (Theorem 4.1) and outlier misclassification (Theorem 4.2), organized around a clear conceptual framework of contamination, concentration, and separation effects. The sub-Gaussian assumption is empirically validated (Figure 4, Remark 4.3), and a looser bounded-moments version is also provided (Theorem C.3).

4. **Broad comparison.** The paper compares against 20 baselines across 11 InD-OOD pairs, covering both InD-only methods and methods that use wild data.

## Weaknesses

### Major

1. **The "EWM filtering rule" in the theorems is not specified, and its connection to Algorithm 1 is unclear.** Theorems 4.1 and 4.2 bound "the inlier/outlier misclassification rate of the EWM filtering rule" but never define what this rule is operationally — i.e., how one goes from computing an element-wise median to a classification decision for individual wild samples. The actual method (Algorithm 1) is a greedy, iterative leave-one-out procedure that removes the top-*k* samples with the largest L2-distance drop at each iteration. The theoretical analysis appears to analyze a single-shot median computation, but this is never specified. The paper claims "these results provide rigorous theoretical assurance that Medix minimizes both types of errors under mild assumptions" (end of Section 4), but the logical connection between the theorems and Algorithm 1 is not established. The theorems may be correct for some median-based filtering procedure, but it is unclear that procedure is Algorithm 1. **This does not invalidate the empirical contribution but weakens the paper's central claim of having "theoretical guarantees for Medix."**

### Minor

2. **Theoretical bounds are loose in the tested regime.** At the paper's default setting of π=0.5 (equal InD/OOD proportions, used in all main experiments), the contamination term in Theorem 4.1 is π/[2(1-π)] = 0.5, so the bound on inlier misclassification rate is at least 50% before concentration terms. While bounds can be loose, the presentation ("provable bounds," "low error rate") creates a stronger impression than the mathematics delivers at the tested contamination level.

3. **Baseline standard deviations not reported.** Tables 1 and 2 report standard deviations only for Medix (5 runs) but none of the 20 baselines have variance information. This makes it difficult to assess statistical significance, particularly on CIFAR-100 where improvements over WOODS are modest (5.42% vs 6.74% average FPR95) and on individual OOD pairs where gaps are small (e.g., 0.16% vs 0.17% on SVHN).

4. **CONJ and DRL baseline results are absent from the main tables.** These methods are listed as baselines (Section 5.1) and the conclusion claims superiority over DRL, but their results do not appear in the main tables. (If they appear in the appendix, the main text should clearly reference this.)

5. **Hyperparameter selection description is ambiguous.** The paper states ε and k are selected "with the objective of maximizing OOD performance" but does not specify whether this was done using a validation split or directly on test OOD data. The appendix (A.2) is referenced for sensitivity analysis but the selection protocol itself should be stated in the main text.

### Trivial

6. **Notation m_min in Theorem 4.1 is undefined.** The bound uses m_min in the ε definition and concentration term without defining it; it appears to denote min(m_in, m_out), which is an unusual choice for an inlier misclassification bound. This should be clarified.

## Nice-to-Haves

- Add standard deviations for the main baselines (WOODS, OE, KNN+) to enable readers to assess statistical significance.
- Include computational cost information (wall-clock time or FLOPs) for the filtering stage in the main paper.
- Tighten the theory-algorithm connection by either (a) defining the "EWM filtering rule" that the theorems analyze and showing how Algorithm 1 implements it, or (b) explicitly characterizing the gap.

## Removed Points

*These points were flagged for removal from the harsh critic input; treat with caution.*

- "Within-distribution OOD detection" scope limitation: The protocol follows the community standard (Katz-Samuels et al., 2022a) and the paper addresses unseen OOD in Appendix A.4. Not a valid weakness.
- Suspicion about identical InD ACC for post-hoc methods (94.84 on CIFAR-10): These methods all use the same pre-trained base classifier, so identical InD accuracy is expected and standard. The reviewer's suspicion was a misunderstanding.
- Missing algorithm complexity analysis in main paper: Referenced to Appendix A.6.
- Gap between Eq. 4 and Algorithm 1 being too large: The paper explicitly acknowledges this ("Solving… can be computationally prohibitive… we propose a greedy approximation") and frames Algorithm 1 as motivated by Eq. 4 rather than derived from it. This is a reasonable level of transparency.
- Various formatting/presentation nitpicks, including the "ReaT" label (parser artifact — the original paper reads "ReAct") and questions about parser artifacts. These are not author errors.

## Novel Insights

The harsh critic's most valuable insight is the unrecognized gap between the theorem's unspecified "EWM filtering rule" and the actual Algorithm 1. This is a structural issue in how the paper presents its theoretical contribution: the paper conflates "median-based filtering" (a broad class) with "Medix's specific algorithm" (a greedy iterative procedure). The critic correctly identifies that the theorems bound error rates for some rule that is never operationalized, creating an impression of rigor that does not survive scrutiny of the details. The analysis of bound looseness at π=0.5 is a secondary but valid concern about presentation. The missing baseline standard deviations and ambiguous hyperparameter tuning description are standard reviewer observations, not novel per se, but worth foregrounding.

## Suggestions

1. Most importantly, define the "EWM filtering rule" explicitly in Section 4 — what decision rule maps from the element-wise median to a per-sample classification? Then discuss how Algorithm 1 relates to this rule (e.g., is it an implementation, an approximation, or a different procedure altogether?).
2. Report standard deviations for the main competing baselines (WOODS, OE, KNN+) in the tables.
3. Clarify the hyperparameter selection protocol — specify whether a validation split was used or not.
4. Either include CONJ/DRL results in the main tables or clearly state in the main text that they appear in the appendix and summarize their relative performance.

## Score and Decision

**Calibration Summary.** I retrieved 24 anchor papers across score bands via `calibration_search`. The most directly comparable anchor is "How Does Unlabeled Data Provably Help Out-of-Distribution Detection?" (Du et al., SAL; avg score 6.50, decision Accept). SAL addresses the same problem with a similar filter-train structure and direct theory-method connection. Medix has stronger per-dataset empirical margins on CIFAR-10 but a weaker theory-method connection, placing it slightly below SAL. The MetaOOD paper (5.25, Accept) provides a lower anchor — it was accepted despite conceptual simplicity and evaluation limitations. The NAP paper (4.75, Reject) and Normalizing Flows paper (3.40, Reject) provide reject anchors for comparison: both were rejected primarily for insufficient novelty or weak experimental methodology, which does not describe Medix. **Round-1 bracket:** 4.5–6.5. **Narrowing:** On re-reading the SAL reviews, most criticisms were about missing experiments and baseline breadth, not about structural theory-method disconnection. Medix's theory-algorithm gap is a more significant structural weakness than anything raised against SAL, so Medix should score below 6.5. At the same time, Medix's empirical results are strong across all 11 InD-OOD pairs (especially CIFAR-10), the method is novel, and the theory provides useful conceptual framing even if the algorithmic connection needs tightening — unlike the 3.40–4.75 anchors which had fundamental novelty or rigor problems. **Final score:** 5.5.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Accept</decision>