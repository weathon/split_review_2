Now I have all the data I need for calibration. Let me finalize the review.

**Calibration Summary:**

| Anchor | Path | Avg Score | Round | Itemized | Comparison |
|--------|------|-----------|-------|----------|------------|
| EAC (Expand & Compress) | FRzCIlkM7I | 6.75 | 1,2 | Yes | Directly competing CSTF method. STBP uses more novel architecture (FreNet+DLGA+pattern bank) vs EAC's simpler prompt pool, achieves stronger traffic results (21-22% vs EAC), but has unexplained AIR-Stream disparity and missing ablation that EAC doesn't. |
| TFMoE (MoE for traffic) | vJGKYWC8j8 | 4.00 | 1 | Yes | Only one dataset, less novel. STBP is clearly stronger. |
| SKI-CL (continual MTS) | URCfZ2NgaR | 5.33 | 1 | Yes | Novelty concerns. STBP has more novel architecture and broader evaluation. |
| TESTAM (MoE traffic) | N0nTk5BSvO | 5.75 | 2 | Yes | Small improvements, standard techniques. STBP has larger improvements and more novel architecture. |

**Round-1 bracket:** 5.5 to 7.5 (above SKI-CL/TESTAM/TFMoE, comparable to EAC)

**Narrowing:** STBP is clearly above TESTAM (5.75) and SKI-CL (5.33) — both had much smaller improvements and weaker novelty. Compared to EAC (6.75), STBP has a more novel architecture and stronger traffic results, but the AIR-Stream heterogeneity and missing ablation are weaknesses EAC doesn't share. Placing at **6.0** — borderline accept.

Now producing the final review:

## Summary
...

## Strengths
1. Clean architecture with grounded design choices...
2. Strong results on two of three real-world datasets...
3. Comprehensive evaluation...
4. Few-shot experiment...

## Weaknesses
### Major
1. Improvement on AIR-Stream is marginal (2.35%) and unexplained...
2. Missing w/o FreNet ablation...

### Minor
3. Approximate ablation values...
4. Privacy/storage claim unsupported...
5. Pattern bank parameter trajectory not reported...
6. DLGA asymmetry lacks justification...

### Trivial
7. Terminology overlap...

## Nice-to-Haves
...

## Removed Points
...

Let me now write the full review.Now I have all the information needed. Let me produce the final consolidated review.

## Summary

This paper proposes STBP, a framework for continual spatio-temporal forecasting that combines a frozen backbone (FreNet for frequency-domain temporal modeling + DLGA for linear graph attention) with an expandable contextual pattern bank that handles node-level adaptation via prompt-based gating and attention. The backbone remains fixed after the first stage to preserve general knowledge, while the pattern bank incrementally expands to new nodes. On two traffic datasets (PEMS-Stream, CA-Stream), STBP achieves 21–22% relative MAE reduction over the best baseline. On a meteorological dataset (AIR-Stream), the improvement is 2.35%.

## Strengths

- **Clean, well-motivated architecture.** The division of labor is principled: the backbone (FreNet + DLGA) handles stable spatio-temporal patterns and distribution drift via frequency-domain analysis, while the contextual pattern bank captures evolving node-level heterogeneity. The dual-stream linear attention (Eq. 9) that incorporates **P**~τ~^(2)^ as an additional key is a clean bridge between the pattern bank and spatial modeling — not an ad-hoc coupling. **[impact=+9.41]**

- **Strong results on two of three datasets.** On PEMS-Stream (21.44% MAE reduction) and CA-Stream (21.93% MAE reduction), the gains over the best baseline are substantial and practically meaningful. The few-shot experiment (Table 2) further demonstrates robustness under data scarcity, with consistent outperformance across both traffic datasets. **[impact=+9.99]**

- **Comprehensive evaluation suite.** The paper covers main results, ablation studies, parameter sensitivity analysis, t-SNE case studies, and efficiency analysis spanning accuracy, training time, and memory. The breadth of evaluation is appropriate for a new-method paper in this area. **[impact=+8.13 / +8.87 combined]**

## Weaknesses

### Major

- **The improvement on AIR-Stream is marginal (2.35%) and the paper does not discuss why.** The paper frames STBP as a "general" spatio-temporal backbone, yet the results are dramatically different across domains: ~21–22% on traffic but only 2.35% on meteorology. The text at line 238 attributes the gain to "the bridge it establishes between STGNNs and CSTF methods" — if that bridge were the decisive factor, one would expect it to generalize consistently. The disparity suggests the frequency-domain backbone is particularly well-suited to traffic (which has strong periodicity) and less so to air-quality data, but the paper neither discusses this nor qualifies the claim of generality. Different temporal resolutions (5-min traffic vs. hourly air quality) and domain characteristics are mentioned in the experimental setup but are never connected to the heterogeneous results. **[impact=-2.52]**

- **The ablation study lacks a w/o FreNet variant.** The paper lists distributional drift as one of its four key challenges (Challenge ❶) and claims FreNet handles it (line 262: "The FreNet module also makes a notable contribution…"). However, the ablation includes only: (i) w/o Backbone (replaces *both* FreNet and DLGA with CNN+GCN simultaneously), (ii) w/o DLGA (removes only DLGA), and (iii) variants with the pattern bank removed. There is no variant that replaces FreNet with a standard temporal module (e.g., TCN, GRU) while keeping DLGA and the pattern bank. This means FreNet's contribution to handling distribution drift cannot be isolated from DLGA's contribution. The w/o Backbone vs. w/o DLGA comparison does not cleanly recover FreNet's effect because w/o Backbone replaces both the temporal and spatial modules with different architectures entirely. **[impact=-5.81]**

### Minor

- **The ablation table (Figure 4) reports only approximate values** (~15, ~20, etc.) without standard deviations, unlike the main results (Table 1) which include them. This makes it harder to assess the magnitude and reliability of each component's contribution. The trends are clear but exact numbers with confidence bounds would be more informative. **[impact=-0.00]**

- **The paper claims privacy protection and storage efficiency advantages** (line 104: "offering advantages in privacy protection and storage efficiency") for the pattern bank over raw-data replay, but provides no experimental measurement of storage footprint and no privacy analysis. This claim is a qualitative extrapolation, not evidence. It should either be supported or scoped more carefully. **[impact=-9.91]**

- **The pattern bank parameter trajectory is not documented.** The pattern bank uses 3×N~τ~×d parameters (three prompt groups **P**~τ~^(0)^, **P**~τ~^(1)^, **P**~τ~^(2)^) and grows linearly with nodes. The efficiency analysis reports training time and memory, but total parameter counts per stage are not reported, making it harder to assess scalability as the graph expands. **[impact=-0.00]**

- **The DLGA attention asymmetry lacks justification.** In Eq. 9, **P**~τ~^(2)^ provides keys but no corresponding values — the values come from the input. The approximation uses φ(**P**~τ~^(2)^)^⊤^**V**, which is asymmetric. This design is plausible but a brief justification would help readers understand why the pattern bank provides keys but not values. **[impact=-0.00]**

### Trivial

- **Terminology overlap.** The term "contextual pattern bank" is also used to describe components in prior methods (STID, HimNet) in the related work (line 32–33), which could cause confusion with STBP's central component of the same name. A clarifying remark distinguishing the paper's design from prior uses would help. **[impact=-0.05]**

## Nice-to-Haves

- A w/o FreNet ablation (swap FreNet for a standard temporal module while keeping DLGA and the pattern bank) to directly isolate FreNet's contribution to handling distribution drift.
- A domain-level analysis of why the method works well on traffic data (strong periodicity) but only marginally on air-quality data, clarifying the method's scope conditions.
- Documenting parameter counts of the pattern bank across stages as the node count grows.
- The paper could systematically map its four stated challenges (distributional drift, dynamic correlations, catastrophic forgetting, backbone collaboration) to specific experiments to help readers assess each one.

## Removed Points (excluded from evaluation)

- *"Comparison with GWNet/STID conflates continual learning strategy and model architecture"*: The paper follows standard practice from prior work (Chen & Liang, 2025), acknowledged as reasonable even by the critic.
- *"Efficiency study lacks quantified training time/memory differences"*: Figure 8 plots MAE vs. Average Training Time with scatter size encoding GPU memory — the quantified data is in the figure.
- *"AIR-Stream improvement could be within noise"*: The paper reports standard deviations (e.g., STBP 23.64±0.23 vs. EAC 24.21±0.43), and the gap exceeds the combined uncertainty; the improvement is small but not within noise.
- *"Clarify Table 1 column alignment"*: Parser artifact.
- *"Paper should return to four challenges in evaluation section"*: A presentation suggestion, not a substantive flaw.
- *All formatting/style nitpicks* (typos, table alignment, figure rendering): These are parser artifacts, not author errors.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Add a w/o FreNet ablation** where FreNet is replaced by a standard temporal module (e.g., TCN or GRU) while keeping DLGA and the pattern bank. This would directly quantify FreNet's contribution to handling distribution drift.
2. **Discuss the heterogeneous results** across traffic vs. air-quality domains. Explain whether FreNet's frequency-domain design is particularly suited to data with strong periodicity, and scope the generality claim accordingly.
3. **Replace approximate ablation values** with exact numbers and standard deviations, as is done for the main results.
4. **Either provide storage measurements** for the privacy/storage claim or rephrase it as a qualitative observation (e.g., "our method avoids storing raw historical data, which is a necessary but not sufficient condition for privacy").
5. **Report parameter counts** of the pattern bank at each incremental stage to clarify scalability.

## Score and Decision

**Calibration details:** Round-1 bracketing placed this paper in the 5.5–7.5 range, above TFMoE (4.00), SKI-CL (5.33), and TESTAM (5.75), and comparable to EAC (6.75). Compared to EAC — the closest anchor — STBP has a more novel architecture (FreNet + DLGA + pattern bank vs. simple prompt pool), stronger reported traffic results (21–22% vs. a few percent), and better-documented methodological details. However, STBP has two weaknesses EAC does not: the unexplained AIR-Stream disparity (2.35% vs. 21–22%) and the missing w/o FreNet ablation. The impact scores confirm this trade-off: STBP's strengths in architecture (+9.41) and traffic results (+9.99) rival EAC's strongest items, while EAC's decisive weaknesses (missing baseline details -9.97, missing recent baselines -9.58) are absent from STBP. The AIR-Stream gap (-2.52) and missing ablation (-5.81) pull the score down, placing STBP between TESTAM (5.75) and EAC (6.75).

**Final score:** The paper makes a real contribution — the backbone + pattern bank framework is well-designed and strongly validated on traffic data — but the unexplained domain heterogeneity and incomplete ablation keep it from being a clear accept.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>