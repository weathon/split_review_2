## Summary

This paper proposes STBP, a framework for continual spatio-temporal forecasting (CSTF) that combines (1) a spatio-temporal backbone with frequency-domain processing (FreNet) and dual-stream linear graph attention (DLGA) to handle distributional drift and dynamic correlations, and (2) a scalable contextual pattern bank of per-node trainable parameters that expands incrementally while the backbone stays frozen, to mitigate catastrophic forgetting. Experiments on three real-world datasets (traffic and air quality) show consistent improvements over existing CSTF methods, with particularly large margins on traffic data.

## Strengths

- **Few-shot experiment (Table 2) provides strong evidence of robustness.** With only 10% training data in later periods, STBP achieves MAE of 13.58 vs. EAC's 16.13 on PEMS-Stream (~16% improvement) and 17.11 vs. 20.94 on CA-Stream (~18% improvement). This is the cleanest apples-to-apples comparison in the paper and demonstrates that the continual learning mechanism genuinely extracts reusable knowledge across periods.

- **t-SNE visualization of the pattern bank (Figure 6) offers interpretable qualitative support for the architecture.** The pattern bank's learned embeddings cluster nodes with similar traffic patterns without explicit clustering supervision, validating the claim that the bank captures node-level heterogeneity and relevance.

- **The problem framing is clear and well-motivated.** The paper identifies a concrete gap — existing CSTF methods use weak backbones (stacks of graph+convolutional layers) poorly suited to long-term distributional drift — and enumerates four specific challenges (distributional drift, dynamic correlations, catastrophic forgetting, efficient incremental strategy) that the method is designed to address.

## Weaknesses

### Fatal

None.

### Major

None.

### Minor

- **Ablation study reports approximate values, reducing quantitative precision (Section 5.3, Figure 4 / lines 216–218).** The ablation table uses "~15", "~18", etc. rather than exact numbers with standard deviations, unlike the main results (Table 1) which report precise values. While the qualitative ordering of variants is unambiguous (Our < Retrain < Online < w/o Backbone < w/o DLGA < EAC), the lack of exact values makes it impossible to assess whether the differences between adjacent variants (e.g., w/o Backbone vs. w/o DLGA) are statistically meaningful or stable across seeds. This is the experiment designed to validate the paper's architectural claims, and it should meet the same precision standard as the main table.

- **The large improvement disparity between traffic datasets (~21% over best baseline) and the air quality dataset (2.35%) is not analyzed.** The paper reports these numbers (line 238) but offers no explanation for why AIR-Stream sees only a small gain. Possible factors worth discussing include: weaker periodic structure in hourly air quality data (reducing the advantage of FreNet), fewer incremental periods or smaller graph expansion (making the continual learning challenge easier), or domain-specific properties that differ from traffic. Without analysis, readers cannot assess whether STBP's strong traffic results are robust across modalities or depend on dataset-specific properties.

- **Differentiation from EAC — the most directly comparable method — is asserted but not experimentally isolated.** Both STBP and EAC use a frozen backbone with a dynamically expanding set of per-node learnable parameters (prompts/pattern bank) that adapt over time. The paper states its three-group gating mechanism is "distinct from existing work" (line 100), but the ablation "w/o Backbone" replaces the backbone (FreNet+DLGA) with CNN+GCN — it does not test whether the improvement over EAC comes from the stronger backbone or from the pattern bank interaction design. An ablation that keeps the same backbone but replaces STBP's three-group gating with a simpler interaction (e.g., additive prompt embeddings as in EAC) would isolate the claimed distinction. Currently, the improvement over EAC could stem entirely from the backbone architecture.

- **The evaluation protocol used for conventional STGNN baselines (GWNet, STID) retrains from scratch at each period (lines 187–188), which is the weakest possible adaptation and inflates the apparent performance gap.** The paper follows prior work (Chen & Liang, 2025) in this choice and acknowledges these models "are not designed for continual learning," so this does not affect the primary comparisons against CSTF methods. Still, including a fine-tuning variant of these backbones (analogous to how iTransformer is treated) would better isolate whether STBP's advantage comes from its backbone architecture or from its continual learning strategy.

- **The number of experimental runs underlying the standard deviations in Table 1 is not stated.** Values are reported with "±" notation but the paper does not specify whether these are over 3, 5, or 10 random seeds. This is a minor reproducibility omission.

### Trivial

None.

## Nice-to-Haves

- A sensitivity analysis showing the contribution of each of the three pattern bank groups (P^(0), P^(1), P^(2)) individually would strengthen the design justification for the three-group architecture in Equation (5).
- Reporting FLOPs or parameter counts for STBP vs. baselines would strengthen the scalability claims beyond the qualitative scatter plots in Figure 8.

## Removed Points

These points were identified by the reviewer but are removed or demoted from the final review for the following reasons:

- **"General" claim overstated** — REMOVED. The paper explicitly defines what "general" means (line 108: "the backbone is independent of the number of nodes and does not rely on any predefined adjacency matrix"). The critic conflated this technical definition with "universally superior across all domains," which the paper does not claim. The AIR-Stream disparity is addressed separately as a minor weakness about domain analysis, not about the "general" label.

- **Missing appendix content (dataset statistics, proofs)** — REMOVED per policy. The appendix is stripped by the parser; these materials exist in the original submission.

- **CA-Stream table garbled / unreadable** — REMOVED. Parser artifact, not a paper issue.

- **Efficiency study lacks precise numbers** — REMOVED. Scatter plots with visual indicators (marker size for GPU memory) are a standard presentation format for efficiency comparisons. The toy dataset experiment with bar charts provides the quantitative counterpart.

- **Section-by-section organizational notes** (Introduction doesn't map experiments to four challenges; methodology question about Eq. 5 groups) — REMOVED. These are suggestions for strengthening, not weaknesses. The methodological question about P^(0) vs. P^(1) collapsing is moved to Nice-to-Haves as a sensitivity analysis request.

## Novel Insights

The reviewer raises a genuinely useful connection: that STBP and EAC share the same high-level strategy (frozen backbone + dynamically expanding per-node parameters) and that the paper's reported improvement over EAC could be decomposed into backbone gains vs. interaction-mechanism gains. This decomposition — which the paper's ablations do not perform — is the most actionable insight for improving the paper. Additionally, the observation that the 10× gap between traffic and air-quality improvements may correlate with the strength of periodic structure in the data (which FreNet is designed to exploit) provides a concrete hypothesis for future analysis.

## Suggestions

1. Replace the approximate "~" values in the ablation table (Figure 4) with exact numbers and standard deviations, matching the precision standard of Table 1.
2. Add a short paragraph analyzing why AIR-Stream shows only 2.35% improvement — even a brief discussion of potential factors (periodicity, incremental periods, graph expansion rate) would significantly strengthen credibility for the "general" framing.
3. Add an ablation that keeps the same backbone architecture but replaces the three-group gating mechanism (Eq. 5) with a simpler pattern bank interaction (e.g., additive prompt embeddings), to directly test whether the claimed distinction from EAC drives the improvement.
4. State the number of random seeds used for the standard deviation estimates in Table 1.

## Score and Decision

<score>6</score>
<decision>Accept</decision>