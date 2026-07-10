Now I'll produce the final consolidated review.

## Summary

This paper introduces PIRN, a prototype-driven reconstruction framework for few-shot multimodal anomaly detection. It uses three components—Balanced Prototype Assignment (BPA) via optimal transport to prevent codebook collapse, Adaptive Prototype Refinement (APR) to update prototypes at inference time for unseen normal variations, and Multimodal Normality Communication (MNC) for cross-modal knowledge exchange—to detect anomalies in RGB+surface-normal data from very few training samples. Experiments on MVTec-3D-AD, Eyecandies, and Real-IAD D3 show consistent improvements over baselines, and the method is substantially more computationally efficient than competing approaches.

## Strengths

- **Well-motivated problem with a clear diagnosis of failure modes (Section 1).** The paper identifies why cross-modal alignment methods fail with scarce data (unreliable correspondences) and why memory banks misclassify unseen normal variations. This specific diagnosis motivates the three components (BPA, APR, MNC) cleanly and non-trivially.

- **Consistent gains across all few-shot settings on two benchmarks (Table 1).** PIRN outperforms the strongest baseline on MVTec-3D-AD and Eyecandies at 5-shot, 10-shot, 50-shot, and all-shot, across all three metrics (AUROC_I, AUROC_P, AUPRO). The gains at the lowest-data regimes (5-shot: +3.9 and +3.6 AUROC_I) are the most practically relevant.

- **Computational efficiency is a genuine differentiator (Table 4).** PIRN achieves AUROC_I 0.922 while requiring 85% fewer FLOPs than FIND (103.36G vs. 728.46G) and running 4.35× faster. This is a concrete practical advantage for real-world deployment.

- **Clean, modular architecture with independently motivated components (Sections 3.2–3.4).** BPA's balanced OT formulation for prototype assignment is a principled solution to codebook collapse. Each component addresses a specific failure mode, and the ablation confirms each contributes.

## Weaknesses

### Fatal
None.

### Major

- **No variance reporting for few-shot experiments — the central empirical claim is uncalibrated.** The paper's core contribution is improved few-shot performance (5-shot, 10-shot, 50-shot in Table 1), yet there is no mention anywhere of multiple trials, random seeds, or statistical significance. In few-shot evaluation, the specific samples selected for the "shot" can dramatically affect results. Gains as small as +0.011 AUROC_I (all-shot MVTec) or +0.014 (all-shot Eyecandies) could be within the noise floor of a single draw. Without variance estimates, the reader cannot assess whether the reported gains are genuine improvements or artifacts of sample selection. This is the most significant weakness in the paper.

- **FIND is omitted from the main comparison table despite matching PIRN's performance.** FIND (Li et al., 2025) achieves AUROC_I 0.921 on 10-shot MVTec-3D-AD (Table 4), essentially tied with PIRN's 0.922. Yet FIND appears only in the computational efficiency comparison, not in the main results (Table 1). Even if FIND's results are only available for the 10-shot setting, it should appear in that column of Table 1, or the paper should explain its exclusion.

### Minor

- **Ablation table cannot be independently verified (Table 2).** All rows display identical checkmarks (a parsing artifact), making it impossible to tell which component combination each row represents. The numerical pattern also raises questions: one partial configuration achieves 0.967 AUROC_I versus the full model's 0.922 AUROC_I, which appears to contradict the textual claim that "removing each component results in a consistent performance drop." This needs clarification.

- **APR's GRU update mechanism is underspecified (Section 3.3).** The paper states prototypes are updated "via a GRU" (line 110) but does not provide the update equation, clarify how the prototype vector p_k and context vector c_k map to hidden state and input, or analyze the regime where OT-based context extraction might fail for subtle anomalies near the normal manifold.

- **Training epoch discrepancy unexplained (Section 4).** Few-shot settings use 60 epochs while the all-shot setting uses only 8 epochs — a 7.5× difference. The paper provides no rationale for this large gap or analysis of whether the few-shot training risks overfitting.

### Trivial

- **Loss function description is ambiguous.** Line 144 says the model uses "e.g., a soft mining loss" then states "In practice, we minimize the cosine distance" — the "e.g." hedges, and cosine distance minimization is a different loss from the cited soft mining loss. The exact loss should be stated unambiguously.

## Nice-to-Haves

- Include an analysis of the APR failure regime: controlled experiments with varying anomaly severity to validate when OT-based diffusion of anomalous tokens breaks down.
- Discuss the corner case where both modalities are anomalous in the same spatial region and how the current design handles it.
- Add a limitations section to candidly discuss failure modes and scope.

## Removed Points

These points from the input review were removed per filtering rules:

- "FIND should be in Table 1's 5-shot and 50-shot settings" — we cannot verify whether FIND reports results at those settings; the criticism about the 10-shot omission (where data exists) is retained.
- "The citation Huang et al., 2022 is missing from the main text" — factually incorrect; the citation appears in the introduction (line 13).
- Strongly speculative interpretation of Table 2's row-labels — the checkmarks are parser-garbled, so the specific row-to-configuration mapping the critic assumed is unverifiable.
- "No analysis of both-modalities-anomalous corner case" — speculative; APR's design with OT-based extraction and gated GRU partially addresses this.
- Pure formatting/style nitpicks and descriptive section-by-section notes without evaluative force.

## Novel Insights

None beyond the paper's own contributions. The single-reviewer input did not surface an analytical angle that the paper itself does not already articulate.

## Suggestions

1. **Address the variance gap:** Run the few-shot experiments (5-shot, 10-shot, 50-shot) with at least 5 different random splits and report means ± standard deviations. This is the single highest-leverage improvement for the paper.
2. **Complete the baseline comparison:** Include FIND in the main results table for the 10-shot setting where data is available, or clearly explain why it cannot be included.
3. **Provide the GRU update equation** for APR and clarify the arrangement of p_k and c_k relative to hidden state and input.
4. **Clarify the loss function** and the rationale for the 60 vs. 8 epoch discrepancy.
5. **Re-typeset Table 2** so component combinations are unambiguous.

## Score and Decision

The paper addresses a well-motivated problem with a clean, modular architecture and demonstrates consistent empirical gains alongside substantial efficiency improvements. However, the lack of variance reporting for the few-shot experiments (the paper's core contribution) is a significant evidential gap, and the omission of FIND from the main comparison table weakens the headline performance claims. These issues are fixable with additional experiments and presentation changes, and the underlying method is sound. On balance, the contributions merit acceptance conditional on addressing the rigor gaps.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>