## Summary

This paper introduces Content-Aware Mamba (CAM) for learned image compression, addressing two key limitations of standard Mamba when applied to images: (1) the fixed content-agnostic raster scan, which processes tokens by spatial proximity rather than feature similarity, and (2) strict causality, which prevents tokens from accessing global context. The authors propose Content-Adaptive Token Permutation (CTP), which clusters tokens by feature similarity and reorders the scan sequence accordingly, and Global-Prior Prompting (GPP), which conditions the SSM output on cluster-derived global prompts to expand the effective receptive field. The resulting CMIC model achieves strong BD-rate savings (−15.91%, −21.34%, −17.58% on Kodak, Tecnick, CLIC vs. VTM-21.0) with competitive efficiency (69.11M params, 2.39 TFLOPs, 4.44 GB peak memory).

## Strengths

1. **Well-motivated problem formulation.** The paper identifies two genuine, non-trivial limitations of Mamba for image compression: (a) the rigid raster scan ignores feature-space proximity, and (b) strict causality prevents global context. Both are real issues that prior Mamba-based compression work (MambaVC, MambaIC) does not address.

2. **Elegant, complementary solution design.** CTP (content-adaptive reordering) and GPP (global-prior prompting) target the two limitations respectively and are empirically complementary. Table 2 shows that together they achieve 2.7–3.6% BD-rate reduction, with each contributing 1–2% individually, confirming non-redundancy.

3. **Strong empirical results.** CMIC achieves SOTA BD-rate savings, substantially outperforming prior Mamba-based models (MambaVC: 6.8–10.09%; MambaIC: 2.17–6.48%). The RD curves (Figures 4–6) show consistent separation across the full bitrate range, not just at isolated operating points.

4. **Convincing ERF visualizations.** Figure 9 provides unusually direct evidence for the mechanism-level claims: (b) vanilla raster scan produces strictly causal ERF; (c) GPP alone yields non-zero activations beyond the causal boundary; (d–e) CTP reshapes the ERF toward semantically meaningful regions. This standard of evidence is stronger than most LIC papers provide.

5. **Favorable efficiency.** With 69.11M parameters, CMIC achieves better RD performance than larger models (MLICv2: 84.30M, MLIC++: 116.48M) while using less compute. The 78% memory reduction over MambaIC (20.32 GB → 4.44 GB) is a significant practical advantage.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

1. **Overclaimed "consistently outperforming" statement (Section 4.3).** The paper states: "The proposed CMIC model consistently outperforms leading methods across all evaluated datasets" (line 224). In Table 1, MLICv2 achieves −16.16% on Kodak, which is strictly better than CMIC's −15.91%. While CMIC leads on Tecnick (−21.34 vs −20.13) and CLIC (−17.58 vs −15.79), it loses on Kodak by 0.25 percentage points. The "consistently outperforms... across all datasets" framing is inaccurate for this specific comparison. The text should acknowledge MLICv2's better Kodak result and frame the advantage as "competitive or superior" rather than "consistently superior across all datasets."

2. **Imprecise characterization of GPP's causality mitigation (Sections 1, 3.4).** The paper claims GPP "effectively mitigates the strict causal chain" and "overcomes the sequential dependency." The mechanism conditions the **output** on global prompts: **O_i = (C + P)h_i + Dx_i**. However, the **state recurrence** remains strictly causal: **h_i = Āh_{i-1} + B̄x_i**. The prompt does not enter the state update; it augments only the output projection. The ERF evidence (Figure 9) does show genuine broadening of the effective context, so the effect is real — but the framing should be more precise: "global conditioning of the output" rather than "mitigating strict causality" in the state. The paper correctly describes the equations (lines 130, 181), so the issue is confined to the high-level characterization.

3. **Confounded contributions from entropy model improvements (Table 1 vs. Table 2).** The comparison against prior methods (Table 1) uses the full CMIC system, which includes both CAM components (CTP + GPP) in the transform network *and* an enhanced entropy model (SCTX with added depthwise convolutions and gated MLPs). The ablation in Table 2 isolates CTP and GPP contributions but holds the enhanced entropy model fixed throughout, so readers cannot determine what portion of the observed gains over, say, MambaVC or FTIC comes from the CAM mechanism versus the entropy model improvements. The paper notes that "adding CAM yields negligible performance gains" in the entropy model (Appendix A.3.2), but this addresses a different question. A controlled ablation — the full CAM transform paired with a baseline SCTX entropy model — would cleanly attribute the gains.

### Trivial

4. **Discretization method unspecified (Section 3.4).** The ZOH equation for **B̄** is written as **(ΔA)⁻¹(exp(ΔA) − I) · ΔB**, which involves a matrix inverse. The Mamba codebase often uses a simplified first-order Taylor approximation (**B̄ ≈ ΔB**). The paper should state which variant is used, as this affects numerical behavior and efficiency.

5. **Imprecise "quadratic 2D scans" phrasing (Section 4.4).** The paper attributes memory reduction to "efficient single selective scan rather than the quadratic 2D scans" (line 244). Multi-directional scanning (as in MambaIC) uses four *linear* scans, not quadratic-in-resolution scans. The 78% memory reduction comes from having 1 scan vs 4 scans, not from avoiding quadratic complexity.

6. **Missing training duration details (Section 4.1).** Total training steps/epochs and batch size are not reported. This is a minor omission for reproducibility.

## Nice-to-Haves

- **Quantify ERF improvement numerically.** The ERF visualizations (Figure 9) are currently qualitative. A metric such as "ERF area" (fraction of input pixels with gradient above a threshold) or "ERF dispersion" would allow mechanism-level claims to be independently verified from the RD numbers.
- **Clarify centroid initialization.** The initialization of centroids by dividing the first batch's tokens into consecutive segments (line 116) is described but not justified. While EMA updates likely stabilize over training, a brief explanation or evidence of robustness would strengthen the method description.

## Removed Points

- **"Missing baseline BD-rate in Table 2."** The reviewer claimed the baseline row (both components disabled) is missing BD-rate numbers. This is incorrect — the baseline values (−13.26, −17.74, −14.87) are present in the first row of Table 2. The checkmark rendering confusion is a parser artifact, not a paper deficiency. **Removed** (factually wrong).
- **"Quadruples computational complexity" clarification.** The paper's claim that multi-directional scanning quadruples complexity is correct (4 independent scans = 4× cost). The reviewer's clarification is not a criticism. **Removed** (not a weakness).
- **"Non-Euclidean clustering" terminological point.** The paper describes its clustering as "non-Euclidean" while using cosine similarity on normalized vectors. This is a matter of convention and does not affect the method's validity or contribution. **Removed** (stylistic, not substantive).
- **"Centroid initialization" concern.** The consecutive-segment initialization is arbitrary but stabilized by EMA updates over training. This is a design detail, not a demonstrated flaw. **Moved to Nice-to-Haves.**
- **Missing MS-SSIM table.** The paper mentions MS-SSIM results in text and provides two comparison points; requesting a full table is a presentation suggestion, not a weakness. **Removed** (nice-to-have).

## Novel Insights

None beyond the paper's own contributions. The reviewer's observation about the precise mechanism of GPP (output conditioning vs. state modification) is worth noting as it refines how the contribution should be described, but this is already evident from the equations in the paper.

## Suggestions

1. Correct the claim in line 224 to acknowledge MLICv2's better Kodak performance and frame CMIC as "competitive or superior" across datasets.
2. Rephrase the GPP causality claims to describe the mechanism as "global output conditioning" or "global context injection" rather than "mitigating strict causality" in the state recurrence.
3. Add a controlled ablation: full CMIC transform with a baseline SCTX entropy model (without the gated MLP additions) to disentangle CAM contributions from entropy model improvements. At minimum, acknowledge the confound in the main text.
4. Specify whether the exact ZOH discretization or the simplified ΔB approximation is used.
5. Correct the "quadratic 2D scans" phrasing to "four directional scans."
6. Report total training epochs/steps and batch size.

## Score and Decision

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>