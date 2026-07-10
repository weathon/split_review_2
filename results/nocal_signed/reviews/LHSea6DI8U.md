Now I have all the information needed. Let me compile the final authoritative review.

## Summary

This paper proposes STBP, a framework for continual spatio-temporal forecasting (CSTF) that combines a frequency-domain spatio-temporal backbone with an expanding "contextual pattern bank" for prompt-based adaptation. The backbone (FreNet for temporal stability, DLGA for linear-complexity spatial attention) handles distributional drift and dynamic correlations, while the pattern bank provides node-specific adaptation through parameter expansion with a frozen backbone to mitigate catastrophic forgetting.

## Strengths

- **Well-motivated architectural design (Section 4).** The paper decomposes CSTF into four specific challenges and assigns each a corresponding component (FreNet for distributional drift, DLGA for dynamic spatial correlations, pattern bank for forgetting, freeze-expand for stability). This clean mapping from problem to mechanism is principled and rare in CSTF papers.

- **Non-trivial dual-stream linear attention with pattern bank integration (Eq. 7–9, Section 4.3).** DLGA incorporates the pattern bank as an additional key stream *within* the attention computation itself rather than through standard prompt concatenation. This is a genuine architectural innovation, and the O(N) complexity is a practical advantage for growing graphs.

- **Substantial improvements on traffic datasets (Table 1).** On PEMS-Stream and CA-Stream, STBP achieves MAE reductions of 21.44% and 21.93% over the best baseline, with confidence intervals suggesting statistical significance. Gains are consistent across all three forecasting horizons (3, 6, 12).

## Weaknesses

### Fatal
None.

### Major

- **AIR-Stream results are substantially weaker and inadequately discussed.** The paper reports only 2.35% MAE improvement on AIR-Stream (vs. 21%+ on traffic datasets), and the RMSE values at individual horizons are marginal or negative relative to baselines. The paper states "STBP outperforms all competing models" as a global claim without qualifying this domain discrepancy, and it does not analyze why the method underperforms on meteorological data relative to traffic data (e.g., coarser temporal resolution, different spatial correlation structure, different distribution shift patterns). This is not a fatal flaw — a method can work well on some domains — but the claims should be scoped and the discrepancy discussed.

- **Conventional baselines (GWNet, STID) are evaluated in a weak setup.** Section 5.2 states these models are "retrained from scratch at each incremental stage using only data from the current period," meaning they receive no historical data and no weight initialization. This design choice, while following prior work (Chen & Liang, 2025), inflates STBP's apparent advantage. iTransformer is given a fairer online fine-tuning setup, but GWNet and STID are the primary STGNN representatives. A cumulative-training variant (or at least fine-tuning from the previous checkpoint) would provide a more informative comparison.

### Minor

- **The w/o Backbone ablation conflates multiple changes (Section 5.3).** It replaces both FreNet and DLGA simultaneously with "CNN and GCN" from unspecified architectures ("the ones used in TrafficStream, STKEC, and EAC"). This makes it impossible to attribute the performance drop to the temporal or spatial module individually. Having a separate w/o DLGA ablation helps partially, but the combined swap remains ambiguous.

- **Equation 5 dimension compatibility is unclear.** The operation $\mathbf{P}_\tau^{(1)} \cdot h_\theta(\dots)$ implies matrix multiplication, but the dimensions of $\mathbf{P}_\tau^{(1)} \in \mathbb{R}^{N_\tau \times d}$ and the output of $h_\theta$ are not specified, making it unclear whether the operation is valid.

- **Train/val/test split not specified as temporal or random (Section 5.1).** The paper states a 6:2:2 fixed ratio but does not clarify whether this split respects temporal ordering (first 60% of time steps for training, last 20% for test). In a streaming setting, a random split could violate temporal ordering assumptions.

- **No per-task forgetting metric reported.** In continual learning, standard evaluation reports how performance on earlier stages changes as later stages are added (e.g., average accuracy on previous tasks). The paper only reports aggregate metrics averaged over all incremental periods, which does not directly answer the forgetting question.

- **t-SNE visualization lacks quantitative validation (Section 5.4, Figure 6).** The clusters are presented as evidence that the pattern bank "autonomously distinguishes heterogeneous and relevant nodes," but no quantitative metric (silhouette score, NMI) is provided, and there is no comparison to clustering raw input features.

- **Parameter sensitivity analysis is limited (Section 5.3).** Only the channel dimension $d$ is varied, which is the least informative hyperparameter. Sensitivity to the number of prompt groups (3), the expansion strategy, or the frequency threshold would be more revealing.

### Trivial
None.

## Nice-to-Haves

- Statistical significance tests (e.g., Diebold-Mariano) comparing STBP against the best baseline on AIR-Stream to clarify the ambiguity.
- Reporting pattern bank growth ($N_\tau$ over periods) and the corresponding memory footprint, relevant for long-running deployments.
- A cumulative-training variant of GWNet/STID as a stronger comparison baseline.
- Per-task forgetting metrics (accuracy on earlier nodes after later nodes are added).

## Removed Points

The following points from the input review were removed per the filtering rules:

- **Table formatting garbled**: Parser artifact — the PDF-to-text extraction mangled the table alignment. The paper's actual submission has a properly rendered table. (Rule: formatting artifact.)
- **Softmax as random feature mapping**: The paper explicitly states $\phi$ is a random feature mapping "with Softmax used for approximation" (Section 4.3), which is a standard approach for linear attention. The reviewer misread this as using Softmax directly as the feature map. (Rule: factually wrong.)
- **Related work "reads as a list"**: Subjective presentation criticism. (Rule: style nitpick.)
- **FreNet phase information**: Minor implementation detail about complex-valued embedding parameterization; not critical to evaluating the contribution. (Rule: scope-creep; standard for FFT-based methods.)
- **Abstract claim about "limited modeling capacity" not substantiated**: General motivation framing, not a technical claim requiring formal substantiation. (Rule: scope-creep.)
- **Efficiency study toy comparison is "self-evident"**: Validating O(N) vs O(N²) empirically in the paper's own setup is standard practice, not a weakness. (Rule: not a genuine weakness.)
- **Conclusion missing certain limitations**: The paper acknowledges one limitation (single-task setting). Calling for more self-criticism is not a genuine weakness. (Rule: nice-to-have, not a weakness.)

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Add a discussion section analyzing why STBP works well on traffic data but less so on meteorological data (AIR-Stream). Address the RMSE regressions explicitly.
2. Add a cumulative-training baseline for GWNet/STID as a fairer comparison point.
3. Clarify the dimension compatibility in Eq. 5 and specify whether the 6:2:2 split is temporal or random.
4. Add per-task forgetting metrics to directly evaluate catastrophic forgetting.

## Score and Decision

The paper proposes a well-structured, novel method for a genuine problem. The core architectural design is principled, the dual-stream linear attention is a non-trivial innovation, and the results on traffic datasets are strong and convincing. The two main weaknesses — the unqualified domain generalization claim (AIR-Stream is marginal) and the weak conventional baselines — are real but not fatal: they reduce the strength of the evidence rather than invalidating the method. The method clearly works well on traffic data, and the architectural ideas are sound. With proper qualification and additional analysis, these issues would be substantially mitigated. The paper makes a solid contribution to CSTF.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>