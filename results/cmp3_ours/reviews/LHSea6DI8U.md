Now I have sufficient calibration data. Let me write the final authoritative review.

## Summary

This paper proposes STBP, a framework for continual spatio-temporal forecasting (CSTF). It combines a spatio-temporal backbone (frequency-domain processing via FreNet + dual-stream linear graph attention DLGA) with an expandable contextual pattern bank. The backbone is frozen after the first incremental period; only the pattern bank expands and updates to handle new nodes and distribution shifts. Evaluated on three streaming datasets (PEMS-Stream, CA-Stream, AIR-Stream), STBP achieves substantial MAE reductions on traffic datasets and a modest 2.35% improvement on the air-quality dataset.

## Strengths

1. **Strong empirical performance on traffic datasets.** On PEMS-Stream and CA-Stream, STBP achieves 21.44% and 21.93% average MAE reduction over the best CSTF baseline (STKEC). These margins are meaningful and consistently reported across horizons.

2. **Well-motivated architectural separation.** Freezing the backbone after the first period and only updating the expandable pattern bank is a clean design that directly addresses the stability-plasticity tradeoff in continual learning. The paper states this clearly in Section 4.1 and Algorithm 1 (in appendix).

3. **Informative few-shot validation (Table 2).** When subsequent periods are reduced to 10% of training data, STBP maintains a clear edge (MAE 13.58 vs. next-best 16.13 on PEMS-Stream; 17.11 vs. 20.94 on CA-Stream). This provides evidence that the method's continual-learning effectiveness goes beyond merely having more capacity.

4. **t-SNE visualization of the pattern bank (Figures 3/6).** The clustering analysis provides qualitative evidence that the learned parameters correspond to meaningful behavioral groups, supporting the paper's claim about node relevance and heterogeneity.

## Weaknesses

### Major

1. **Ablation study reporting is opaque and appears inconsistent with main results.** The ablation table (lines 214–218) reports approximate values (e.g., "Our ~15", "EAC ~26" on PEMS-Stream) without specifying which metric (MAE, RMSE, or MAPE) these correspond to. The figure caption states three metrics are shown, but the transcribed table collapses them into a single row per dataset. As a result, the reader cannot verify whether the ablation uses the same experimental protocol as the main evaluation. For instance, if these are MAE values, EAC at ~26 is far above the CSTF methods in the main table (~15–17), suggesting either a different setup or a different metric. The paper must clarify which metric is reported and reconcile any discrepancies.

2. **Overclaiming "outperforms all competing models" without discussing AIR-Stream RMSE at longer horizons.** On AIR-Stream, STBP is worse than the best baseline (STKEC) on RMSE at horizons 6 (39.81 vs. 39.63) and 12 (44.97 vs. 44.65). While the average MAE improvement (2.35%) is positive and honestly reported in the numbers, the blanket statement "STBP outperforms all competing models" (line 238) is too broad. The paper should either qualify this claim (e.g., "on average MAE") or discuss the RMSE trade-off explicitly. This is particularly relevant because the paper markets STBP as a "general" backbone for CSTF, yet its advantage on the only non-traffic dataset is marginal on the primary metric and negative on some RMSE horizons.

3. **No ablation that isolates the pattern bank's contribution from the backbone's.** The "w/o Backbone" ablation replaces FreNet+DLGA with CNN+GCN — a change that simultaneously removes the backbone architecture, frequency-domain processing, and linear attention mechanism. This makes it impossible to determine whether STBP's gains over EAC come from (a) the three-group pattern bank design, (b) the stronger backbone, or (c) both. An ablation that keeps the backbone identical and varies only the continual-learning mechanism (pattern bank vs. EAC-style prompt pool) would directly address this.

### Minor

4. **Efficiency comparison (Section 5.5) lacks numerical values in the text.** The efficiency study is described only qualitatively ("minimal overhead," "negligible cost increase"). No training time (seconds/period) or GPU memory (GB) figures are given for any model in the main paper. Figure 8 contains scatter plots, but the reader must visually estimate values.

5. **Equation 5 notation is ambiguous.** The operation "·" in H'_τ = P_τ^(1) · h_θ(H_τ · (1 + P_τ^(0))) is not explicitly defined as element-wise multiplication, and the dimensionality of "1" (broadcast scalar vs. all-ones matrix) is not clarified. The output dimension of h_θ(·) is also unspecified, making the equation difficult to verify without reading the appendix.

6. **"General" claim is oversold relative to the evidence.** The paper defines "general" architecturally (node-count independence, no fixed adjacency matrix), which is justified. However, the method is evaluated on only three datasets from two domains (traffic, air quality). The modest AIR-Stream results and absence of non-spatial domains (e.g., energy, crowd flows, epidemiology) mean the claim of generality is not strongly supported.

### Trivial

7. The paper does not state how many incremental periods each dataset has or how many new nodes arrive per period — information that would help the reader assess the difficulty of the continual learning setting. (This may be in the appendix, but a summary in the main text would help.)

## Nice-to-Haves

- **Isolate pattern bank vs. prompt pool design.** The most informative single experiment would be: keep the backbone (FreNet+DLGA) fixed, and compare STBP's three-group pattern bank against EAC's single-group prompt pool. This would clarify whether the three-group design is the source of the gains.
- **Add datasets from more domains** (energy, crowd flow, wind) to substantiate the "general" claim, or scope it to traffic/meteorology CSTF.
- **Report exact numerical values** for the ablation and efficiency experiments, not approximate chart readings.

## Removed Points

These points from the input review are removed with brief justification:

- **"Distinction from EAC is too thin"**: The paper explicitly states the three-group design and its different interaction roles (gating, attention key). Whether the gains come from the pattern bank vs. backbone is a valid question (captured in Weakness 3 above), but the distinction itself is stated. The harsh critic's framing overstates this as a "methodological gap."
- **"General claim oversold" on novelty of linear attention**: The paper accurately cites Katharopoulos et al. (2020) for linear attention. The contribution is in adapting it for CSTF with the dual-stream key from the pattern bank, not in inventing linear attention. This is standard practice.
- **Missing related works**: Cannot be verified without external sources.
- **Formatting/stylistic nitpicks**: Parser artifacts, not author errors.
- **Speculation about appendix content**: The parser strips appendices; assuming missing content there is improper.

## Novel Insights

None beyond the paper's own contributions. The harsh critic and strength analysis largely agree on the paper's strengths and weaknesses; no unexpected pattern emerged.

## Suggestions

1. Clarify which metric the ablation table reports and ensure consistency with the main experimental setup.
2. Qualify the "outperforms all competing models" statement to acknowledge the RMSE underperformance on AIR-Stream at horizons 6 and 12.
3. Add an ablation that keeps the backbone fixed and varies only the continual-learning mechanism (pattern bank vs. prompt pool) to isolate the source of gains over EAC.
4. Report exact numerical values for training time and GPU memory in the efficiency study.

## Score and Decision

**Calibration report:**

Round 1 bracket: 5.5–7.5 (anchored by the EAC paper at 6.75, TESTAM at 5.75, FreeDyG at 6.75, and STDM at 3.0).

Anchors used:
- **Expand and Compress (EAC)** (FRzCIlkM7I, 6.75, accepted) — Most directly comparable: same CSTF task, same prompt-tuning paradigm, similar datasets. STBP has stronger backbone design and better traffic results but weaker reporting clarity. STBP is slightly below EAC's overall quality due to ablation and overclaiming issues.
- **TESTAM** (N0nTk5BSvO, 5.75, accepted) — Traffic forecasting with mixture-of-experts, no continual learning focus. STBP is a stronger method paper in a harder setting.
- **FreeDyG** (82Mc5ilInM, 6.75, accepted) — Frequency-enhanced dynamic graph model. Similar use of frequency-domain techniques. Comparable quality but different task.
- **Structural Knowledge Informed CL** (URCfZ2NgaR, 5.33, rejected) — Continual MTS forecasting. Criticized for limited novelty; STBP has stronger architectural contribution.
- **Online Continual Graph Learning** (4sJJixGIZX, 5.00, rejected) — Benchmarking paper. STBP has stronger methodological contribution.

Narrowing: STBP is clearly above the 5.0–5.4 anchor papers (rejected) due to its well-designed architecture and strong traffic results. It is below the EAC paper (6.75) because of the ablation reporting opacity and overclaiming issues. The most appropriate score is 6.0 — a solid paper with genuine contributions that needs to fix reporting issues before it reaches the level of its strongest comparator.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>