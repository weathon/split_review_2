Now I have a thorough understanding of the paper, the harsh critic's input, the calibration anchors, and the weighted items. Let me compose the final review.

---

## Summary

This paper introduces Content-Aware Mamba (CAM) for learned image compression, addressing two specific limitations of standard Mamba SSMs when applied to images: (1) the content-agnostic raster scan fails to group tokens by feature similarity, and (2) the strict causal processing is misaligned with images' non-causal structure. The authors propose Content-Adaptive Token Permutation (CTP), which uses a learnable codebook-based clustering to reorder tokens by feature similarity before scanning, and Global-Prior Prompting (GPP), which conditions SSM outputs on global priors derived from all tokens. Their CMIC model achieves SOTA BD-rate savings of 15.91%, 21.34%, and 17.58% over VTM-21.0 on Kodak, Tecnick, and CLIC respectively, with favorable complexity (69.11M params, 2.39 TFLOPs).

## Strengths

- **Content-adaptive token permutation is a principled and well-executed idea.** Replacing Mamba's fixed scan with a learned, codebook-based clustering that groups similar tokens is well-motivated both from a compression perspective (redundancy correlates with feature similarity, not spatial proximity) and a practical one (the EMA-updated codebook avoids per-sample K-Means instability). Cluster visualizations in Fig. 10 confirm that learned centroids capture semantically meaningful groupings (edges, textured red regions, smooth backgrounds). Model weight: +6.89.

- **Strong empirical results across multiple benchmarks.** The BD-rate improvements over VTM-21.0 substantially exceed recent SOTA LIC models. Improvements over prior Mamba-based models are significant (7.51% over MambaVC on Kodak, 2.36–6.48% over MambaIC), and the complexity numbers (69.11M params, 2.39 TFLOPs, 0.405s latency) compare favorably to larger models like MambaIC (157M). Model weight: +5.90.

- **Informative ablation and analysis that supports mechanistic claims.** The component ablation (Tab. 2) cleanly isolates CTP and GPP, showing each contributes meaningfully (1.8–2.4% and 0.5–1.4% BD-rate respectively). The ERF visualizations (Fig. 9) are particularly effective — they concretely demonstrate that GPP expands the receptive field beyond the causal boundary and that CTP reshapes it from a raster band toward semantically meaningful regions. The structural ablation (Tab. 4) confirms CAM's advantage over Conv blocks, 2D Mamba, and attention-only designs at comparable parameter counts. Model weight: +5.37.

- **Well-motivated problem framing.** The paper identifies two precise weaknesses of Mamba for compression that go beyond generic criticism, giving the paper a clear and specific thesis from the start. Model weight: +2.42.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

- **Entropy model contribution not independently ablated against standard SCTX.** The paper builds an "enhanced SCTX entropy model" with depthwise convolutions and gated MLPs (Section 3.2, Fig. 3). The ablation study (Tab. 2) only toggles CTP and GPP in the transform blocks while keeping this enhanced entropy model fixed. The baseline "w/o CTP & GPP" at -13.26% BD-rate already includes the enhanced entropy model. The paper acknowledges (Section 4.5) that "for the entropy model, adding CAM yields negligible performance gains" and defers to an appendix, but never compares the full CMIC against a version using the standard SCTX entropy model (He et al., 2022). Without this comparison, it is unclear how much of the total BD-rate improvement is attributable to the entropy model refinements vs. the CAM architecture. Model weight: -1.28.

### Trivial

- **Naming inconsistency.** The paper oscillates between "CMiC" (lines 34, 189, figure captions) and "CMIC" (Abstract, Table 1, line 222), and between "MambaC" (Table 1, line 209) and "MambaIC" (text, line 222). These should be unified for consistency. Model weight: -1.97.

- **Table 1 bold formatting is misleading.** The entire CMIC row is bolded, including complexity metrics where CMIC is not strictly optimal (ELIC has fewer parameters at 33.29M, MambaVC has lower FLOPs at 2.10T, several models have lower peak memory). Only the BD-rate values merit bold formatting. Model weight: -3.08.

## Nice-to-Haves

- Add an ablation comparing CMIC with the standard SCTX entropy model (without the custom depthwise conv + gated MLP design) to cleanly separate the contributions of the entropy model from the CAM architecture.
- Report per-stage architecture details more explicitly: the mapping of {L1, L2, L3} = {3, 2, 2} to the six stages (given as {L1, L2, L3, L3, L2, L1} in Fig. 2) is inferable but should be stated directly in the main text.
- Provide a version of CMIC scaled to approximately MambaVC's parameter count (~48M) to strengthen the architectural comparison. (The paper already partially addresses this via Tab. 4 parameter-matched abations.)

## Removed Points

These points from the input review were removed with justification:

- **Harsh Critic's "Critical Issue 1 — Causality mitigation claim is overstated."** Removed. The paper's claim that GPP "mitigates strict causality" refers to the overall model behavior, and the ERF visualizations (Fig. 9) empirically validate that GPP enables information flow beyond the causal boundary. The mechanism modifies the output projection O_i = (C + P)h_i + Dx_i (line 181) using P derived from all tokens — this genuinely introduces non-causal information into the output even though the state update h_i remains causal. The framing is a reasonable description of the practical effect.
- **Harsh Critic's "Critical Issue 3 — MambaVC comparison not parameter-matched."** Removed. The paper beats the much larger MambaIC (157M params) and provides parameter-matched structural ablations (Tab. 4) comparing CAM blocks against Conv blocks, 2D Mamba, etc. at comparable parameter counts (66–71M). The MambaVC comparison is one data point among many and follows standard LIC practice.
- **"Potential circular dependency" in Section 3.3.** Speculative concern, not verified as an actual training instability.
- **"Potential distribution shift at inference."** Speculative, no evidence of degradation presented.
- **Training detail gaps (epochs, batch size).** Standard for LIC papers; the appendix likely contains these details (stripped by parser).

## Novel Insights

None beyond the paper's own contributions. The reviews confirm the core narrative: the paper presents a well-motivated, well-executed method with strong empirical results and informative analysis, but could benefit from one additional ablation to fully isolate the entropy model's contribution.

## Suggestions

1. Add an ablation comparing CMIC with the standard SCTX entropy model (without depthwise conv + gated MLP) against the proposed enhanced version, keeping the CAM blocks fixed. This would cleanly separate the contributions.
2. Unify naming: consistently use "CMIC" and "MambaIC" throughout.
3. Fix Table 1 bold formatting to only bold BD-rate values, not the entire row.

## Score and Decision

**Calibration Anchors:**

| Path | Avg Score | Round | Itemized? | Comparison to Reviewed Paper |
|------|-----------|-------|-----------|------------------------------|
| RmmrHEH6Nx.md (GroupMamba) | 3.00 | R1 | No | SSM vision paper with stability issues; substantially weaker empirically and less novel than CMIC. |
| cagNCwQEEN.md (Hybrid SSM MLLM) | 3.40 | R1 | No | Multimodal LLM paper; different domain, lower quality. |
| KgJwbsfN7G.md (MambaVC) | 4.80 | R1 | Yes | Direct predecessor — applies VSS block to compression without compression-specific design. Key weakness was "limited novelty, straightforward application" (weight -11.77). Current paper overcomes this with CTP and GPP, which are compression-specific designs. Stronger results, better complexity trade-off. |
| iDe1mtxqK5.md (Spatial-Mamba) | 7.00 | R1 | Yes | Strong Mamba vision paper (Accepted). Novelty concern (-8.45) but compelling results and analysis. Current paper has comparable or better novelty (CTP + GPP are more than "dilated conv on hidden states"), comparably strong ablation/analysis, but has minor entropy-model isolation gap. |
| GRMfXcAAFh.md (Oscillatory SSMs) | 8.00 | R1 | Yes | Pure theoretical SSM paper; different domain and evaluation criteria. |

**Weighted-Item Comparison:** My draft's net positive weight (+14.25 across items) is substantially stronger than MambaVC's (4.80, net negative from -11.77 novelty weight), and comparable to Spatial-Mamba's (7.00, which had a strong -8.45 novelty weight but was balanced by positive strengths). The entropy model ablation gap (-1.28) is the only real negative signal, compared to Spatial-Mamba's novelty concern. This positions the paper between "borderline accept" and "accept."

**Final Score: 6.5**

The paper has a sound core contribution, strong empirical validation, and informative analysis. The only verifiable weakness is the missing entropy model isolation against standard SCTX, which is addressable. The causality framing concern raised by the harsh critic is not a genuine flaw — the mechanism's practical effect (non-causal information flow in the output) is empirically validated by ERF visualizations. The score reflects a paper that is clearly above rejection threshold but has one non-trivial ablation gap that keeps it from the top tier.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>