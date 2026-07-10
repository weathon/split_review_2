Now I have all the calibration data I need. Let me compile the final review.

## Summary

This paper proposes PIRN, a prototype-driven reconstruction framework for few-shot multimodal anomaly detection. It introduces three components: Balanced Prototype Assignment (BPA) using optimal transport to prevent codebook collapse, Adaptive Prototype Refinement (APR) with GRU-based prototype updates during inference to handle novel normal variations, and Multimodal Normality Communication (MNC) for cross-modal knowledge exchange. The method is evaluated on MVTec 3D-AD, Eyecandies, and Real-IAD D3 benchmarks, consistently outperforming baselines in few-shot settings while being substantially more computationally efficient than prior work.

## Strengths

- **Well-motivated problem with clean structure.** The paper identifies three specific failure modes of existing MAD methods in few-shot scenarios (codebook collapse, static prototypes, lack of cross-modal interaction) and maps each to a corresponding module (BPA, APR, MNC). This architecture-level alignment between diagnosed problems and proposed solutions gives the paper strong internal coherence.

- **Principled technical design.** Using balanced optimal transport for uniform prototype utilization is mathematically well-grounded. The APR module's use of OT-weighted context vectors combined with GRU gating to avoid contamination by anomalous tokens during inference is clever and well-motivated. MNC's two-stage design (GAT-based prototype alignment followed by gated cross-attention injection) provides a sensible mechanism for cross-modal communication that avoids unreliable dense patch-to-patch alignment.

- **Strong and consistent empirical results across multiple settings.** PIRN consistently outperforms the best baselines on MVTec 3D-AD and Eyecandies at 5-shot, 10-shot, 50-shot, and full-shot settings. The gains are meaningful in absolute terms (e.g., +3.9 AUROC_I on MVTec 3D-AD 5-shot, +3.7 on 10-shot, +2.4 on 50-shot over the strongest baseline) and hold across both datasets. The pattern of improvement is consistent rather than sporadic, lending credibility to the core claim.

- **Computational efficiency is a genuine practical contribution.** PIRN achieves 85% fewer FLOPs than FIND (103G vs. 728G, Table 4) while matching or exceeding its accuracy. This is a meaningful practical advantage for deployment and is rarely demonstrated in the MAD literature.

- **Thorough ablations validate design choices.** The paper ablates prototype count K (Table 5), decoder depth L (Table 6), token aggregation methods for APR (Table 7), individual component contributions (Table 2), and modality availability (Table 3). The sensitivity analysis on K is particularly informative — showing that too few (K=5) or too many (K=50/100) prototypes both hurt performance, which directly validates the information-bottleneck intuition.

## Weaknesses

### Major

- **No statistical significance or variance reporting for few-shot results.** Few-shot experiments are inherently high-variance — drawing different 5-shot subsets from the same training set can produce substantially different results. The paper reports a single number per metric per shot setting with no standard deviations, confidence intervals, or any statement about how many random seeds/trials were averaged. Given that the few-shot improvements (3-4 AUROC_I points) are modest in absolute terms, the reader cannot assess whether the reported gains are robust or could flip under a different data split. This is the primary evidential gap in the paper. The authors should report means and standard deviations over at least 3-5 random seeds for each few-shot setting.

### Minor

- **GRU update specification in APR is underspecified.** Section 3.3 states "update each prototype p_k to p'_k by incorporating its context c_k via a GRU" but does not clarify which quantity serves as the GRU input and which as the hidden state (e.g., is the current prototype p_k the hidden state and context c_k the input, or vice versa?). This is a reproducibility concern that should be clarified.

### Trivial

- **Sinkhorn entropic regularization parameters not reported.** The paper states the OT problem is solved "using the Sinkhorn algorithm with entropic regularization" but does not report the entropic regularization strength (ε) or the number of Sinkhorn iterations, both of which affect the sharpness of the assignment.

## Nice-to-Haves

- The INP-Former baseline is adapted via a two-stream architecture with independent RGB and surface-normal branches fused at the output level. While the paper acknowledges this adaptation and PIRN also outperforms proper MAD baselines (M3DM, CFM, 3D-ADNAS) that were designed for multimodal input, the paper could be strengthened by experimenting with a version that shares prototypes across streams to more directly isolate whether cross-modal communication drives the improvement.
- On Real-IAD D3 (full-shot setting), PIRN achieves best localization (AUROC_P 0.961) but second-best detection (AUROC_J 0.873, behind D3M at 0.890). The paper accurately reports this. A brief discussion of why the detection gap exists for this particular dataset would be informative.

## Removed Points

These points from the input review were removed after verification:
- **"INP-Former baseline comparison may underestimate the competitor"**: The paper acknowledges the adaptation. More importantly, PIRN consistently outperforms proper MAD baselines (M3DM, CFM, 3D-ADNAS) that were designed for multimodal input, so the core claim does not rest on the INP-Former comparison. The reviewer themselves concedes this.
- **"Real-IAD D3 results presented as stronger than they are"**: The paper's language ("highly competitive performance," "second-best anomaly detection") is measured and accurately reports both the best localization and the detection shortfall. The modality difference with D3M is also noted. The language is fair.
- **"Ablation Table 2 formatting garbled"** and **"BFA vs BPA typo"**: These are text-extraction artifacts, not author errors. The original PDF would display correctly.

## Novel Insights

The input review's most useful observation is that the missing variance reporting is the single point of evidential uncertainty in an otherwise well-supported paper. The consistency of gains across shot settings, datasets, and baselines partially mitigates this gap, but it remains the key issue the authors should address. The calibration comparison with accepted papers at similar anomaly detection venues (6.17–6.50) confirms that PIRN's method coherence, ablation depth, and efficiency analysis are above the typical accepted paper in this area, with the variance gap being the main factor preventing a cleaner accept.

## Suggestions

1. Report means and standard deviations over at least 3 random seeds for the 5-shot and 10-shot settings on MVTec 3D-AD and Eyecandies. This directly addresses the primary evidential gap.
2. Clarify the GRU input/hidden state configuration in APR (Section 3.3).
3. Report the entropic regularization strength (ε) and number of Sinkhorn iterations used in the BPA and APR modules.
4. For the Real-IAD D3 results, consider adding a brief discussion of why the detection metric lags behind D3M despite superior localization.

## Score and Decision

**Calibration anchor comparison:**

| Anchor Paper | Path | Avg Score | Round | Itemized | Comparison |
|---|---|---|---|---|---|
| One-for-All Few-Shot AD | Zzs3JwknAY.md | 6.40 | 1,2 | Yes | Lower method coherence ("too many modules"), worse ablations, less clean exposition. PIRN stronger across all dimensions. |
| Prototype-based OT for OOD | J2we1sVd9m.md | 4.60 | 1 | Yes | OOD detection (different task); major methodological concern about using test data. PIRN clearly superior. |
| PTAD Tabular AD | Vi6p2TeujL.md | 4.25 | 1 | Yes | Tabular domain; severe reproducibility issues (no code, no hyperparams). PIRN much stronger. |
| AnomalyCLIP | buC4E91xZE.md | 6.17 | 2 | Yes | Zero-shot setting; DPAM module poorly justified. PIRN has more principled design. |
| MMAD Benchmark | JDiER86r8v.md | 6.50 | 2 | Yes | Benchmark paper, different contribution type. Some reviewers found contribution weak. PIRN has stronger technical contribution. |
| Deep Orthogonal Hypersphere | cJs4oE4m9Q.md | 8.00 | 1 | No | Clean accept with no major weaknesses. PIRN's variance gap prevents reaching this level. |

**Bracket reasoning (Round 1 → Round 2):** Round 1 bracketing placed PIRN above the 4.25–4.60 anchors (weaker papers with significant problems) and above the 6.17–6.50 anomaly detection papers (which have worse method coherence, weaker ablations, or reliance on less principled techniques). The 8.00 anchor represents a paper with no significant weaknesses, which PIRN does not match due to the missing variance reporting. **Round 1 bracket: 6.5–7.5.** Round 2 narrowed this by comparing itemized impact scores: PIRN's strengths (empirical results +10.00, ablations +10.00, efficiency +9.85, design +9.59) are decisively higher than the 6.17–6.50 anchors' strengths, but the single -9.99 weakness on missing variance prevents the paper from reaching the 8.00 level. The paper sits comfortably above the middle of the accept range but below the clean-accept threshold.

**Final score: 7.0** — clearly above borderline accept (6). The paper has a well-motivated, principled method, strong empirical results across multiple datasets, impressive computational efficiency, and thorough ablations. The primary weakness (missing variance reporting) is real but fixable and does not threaten the paper's core claims given the consistency of gains across settings. The minor and trivial concerns are easily addressable. This is a solid accept.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>