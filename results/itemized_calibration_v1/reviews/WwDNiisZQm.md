Now I'll write the final consolidated review.

## Summary

This paper introduces Content-Aware Mamba (CAM) for learned image compression, addressing two specific limitations of standard Mamba SSMs: (1) content-agnostic raster scanning, solved by Content-Adaptive Token Permutation (CTP) which clusters and reorders tokens by feature similarity; and (2) strict causality misaligned with images, mitigated by Global-Prior Prompting (GPP) which injects sample-specific global context into the SSM output. The resulting CMIC model achieves competitive BD-rate savings (-15.91%, -21.34%, -17.58% vs VTM-21.0) with moderate complexity (69.11M params, 2.39 TFLOPs).

## Strengths

- **Well-diagnosed problem.** The paper identifies two concrete, compression-specific limitations of Mamba (content-agnostic scanning and misaligned causality) and designs targeted solutions for each — not a generic "Mamba could be better" motivation. Section 1 states the problems clearly.

- **Principled clustering design.** The codebook-based clustering with EMA centroid updates (Section 3.3, Algorithm 1) avoids per-sample online K-Means instability, requires no iterative inference-time updates, and ties the prompt dictionary to centroids ($\mathbf{U} = \mathcal{A}([\mathbf{c}_1; \dots; \mathbf{c}_K])$), grounding prompts semantically rather than leaving them as free parameters. This is a cleaner design than free-learnable prompt pools.

- **Direct mechanistic evidence via ERF.** The controlled single-layer ERF experiments (Figure 9) isolate the effect of each component: GPP produces non-zero activations beyond the causal boundary, CTP reshapes the ERF toward semantically correlated regions, and together they yield broad content-aware coverage. This level of mechanistic analysis is unusually thorough for an LIC paper.

- **Competitive results with reasonable complexity.** BD-rate savings (-15.91%, -21.34%, -17.58% vs VTM-21.0) are competitive with SOTA while using 69.11M params and 2.39 TFLOPs — substantially smaller than MambaIC (157.09M) and comparable to TCM-L (75.89M). The 78% GPU memory reduction vs MambaIC is a genuine practical advantage.

## Weaknesses

### Major

- **"Consistently outperforms" claim is imprecise.** Section 4.3 states "The proposed CMIC model consistently outperforms leading methods across all evaluated datasets." However, Table 1 shows MLICv2 achieves a better BD-rate on Kodak (-16.16% vs CMIC's -15.91%). CMIC wins on Tecnick and CLIC, and is generally competitive or better overall, but the blanket "consistently outperforms" wording is inaccurate for this comparison. The claim should be tightened to acknowledge the MLICv2 result on Kodak.

### Minor

- **The "mitigating strict causality" language for GPP oversells the mechanism's operation.** The paper describes GPP as "overcoming the sequential dependency" (Abstract) and "relaxing strict causality" (Section 3.4). However, the math (Eq. 3, Eq. 7) shows GPP conditions the *output* projection: $\mathbf{O}_i = (\mathbf{C} + \mathbf{P})\mathbf{h}_i + \mathbf{D}\mathbf{x}_i$, while the state update $\mathbf{h}_i = \bar{\mathbf{A}}\mathbf{h}_{i-1} + \bar{\mathbf{B}}x_i$ remains strictly causal. The ERF evidence (Figure 9c) does show broadened receptive fields, which is real and useful — but the mechanism augments the read-out with cluster-level global context rather than altering the causal state update. More precise language (e.g., "broadens the effective receptive field via global context conditioning") would better match what the math does.

- **The baseline architecture accounts for most of the absolute performance.** From Table 2, the vanilla single-scan Mamba baseline (no CTP, no GPP) already achieves -13.26% on Kodak, outperforming MambaVC (-8.10%), CCA (-11.99%), and FTIC (-12.94%), and coming within 0.25pp of MambaIC (-13.01%). CTP+GPP add ~2.7pp. The paper transparently reports this, but the narrative frames CTP/GPP as the main SOTA drivers when the backbone contributes more. The contribution is genuine but the framing should be more measured.

- **"Quadratic 2D scans" terminology is imprecise.** Section 4.4 attributes the memory reduction to "single selective scan rather than the quadratic 2D scans." Standard multi-directional Mamba scanning has complexity O(4N) — linear in sequence length, not quadratic. The paper itself correctly notes elsewhere that multi-directional scanning "quadruples computational complexity" (Section 1). The term "quadratic" should be replaced with "multi-directional" or "4×."

- **Within-cluster ordering is unspecified.** Section 3.3 states the permutation groups tokens by cluster ($g_i=1$, then $g_i=2$, etc.) but does not specify the ordering of tokens *within* a cluster. Since the SSM is causal within the reordered sequence, this ordering matters for tokens in the same cluster. This asymmetry should be acknowledged.

### Trivial

- **Naming inconsistency.** The method by Zeng et al. (2025) is referred to as "MambaIC" in most of the text but appears as "MambaC" in Table 1 and once in Section 4.3. This should be harmonized.

## Nice-to-Haves

- Compare against a simpler permutation baseline (e.g., random permutation) to isolate whether the benefit comes from *any* reordering or specifically from semantic clustering.
- Add a quantitative measure of non-causality (e.g., percentage of ERF mass outside the causal region) to complement the qualitative ERF visualizations.
- Explicitly acknowledge the MLICv2 comparison on Kodak and explain why the overall comparison still favors CMIC.

## Removed Points

These points from the input review were removed with justification:

- **Training details sparsity** — The harsh critic noted missing training steps/epochs, batch size, and LR schedule. These details are likely in the stripped appendix; the paper references Appendix A.3, A.8-A.10 for supplementary details. Per the hard rules, I cannot penalize for absent appendix content introduced by the PDF extraction process.
- **Throughput comparison fairness (TCM-L measurement conditions)** — The critic questioned whether TCM-L's throughput was measured under identical conditions. This is speculative without evidence either way; the paper reports its own measurements clearly.
- **Generic suggestions (corrupting centroids, random permutation baseline, quantitative causality metric)** — These are constructive suggestions for strengthening the paper, not weaknesses. Moved to Nice-to-Haves.

## Novel Insights

None beyond the paper's own contributions. The reviewer analysis confirms the paper's primary claims but identifies framing imprecisions rather than uncovering unrecognized issues.

## Suggestions

- Tighten the "consistently outperforms" claim (Section 4.3) to reflect the MLICv2 result on Kodak.
- Recast GPP's effect as "conditioning the SSM output with global cluster-level context to broaden the effective receptive field" rather than "mitigating strict causality."
- Replace "quadratic 2D scans" with "multi-directional scans" or "4× scans" (Section 4.4).
- Specify the within-cluster ordering (Section 3.3) and discuss any implications for the causal scan.
- Harmonize the "MambaIC"/"MambaC" naming throughout.

## Score and Decision

**Calibration anchor comparison:**

| Anchor | Path | Avg Score | Round | Itemized | Comparison |
|--------|------|-----------|-------|----------|------------|
| MambaVC (SSM for visual compression) | KgJwbsfN7G.md | 4.80 | R1 | Yes | CMIC is clearly stronger: more SOTA baselines, greater technical novelty (CTP/GPP vs applying VSS block), stronger ablations |
| Architecturally Aligned Comparisons (ConvNet vs Vision Mamba) | QBiFoWQp3n.md | 4.60 | R1 | Yes | Less directly comparable; CMIC has more technical contribution |
| Autoregressive Pretraining with Mamba in Vision | PQpvhUrA1C.md | 5.75 | R1 | Yes | Comparable quality; CMIC has stronger mechanistic evidence but both have incremental contributions |
| Frequency-Aware Transformer for LIC | HKGQDDTuvZ.md | 6.00 | R2 | Yes | Most comparable accepted LIC paper; CMIC has stronger ablations and ERF analysis, comparable contribution level |
| Spatial-Mamba (Structure-Aware SSM for vision) | iDe1mtxqK5.md | 7.00 | R1 | Yes | Broader domain applicability; CMIC has more targeted contribution with better mechanistic evidence |

**Bracket reasoning (Round 1):** CMIC sits above MambaVC (4.80) due to stronger baselines, greater novelty, and more thorough evaluation. It sits below Spatial-Mamba (7.00) which addresses a more general vision problem with broader impact. The narrowest plausible bracket is [5.5, 7.0].

**Narrowing (Round 2):** The Frequency-Aware Transformer anchor (6.00) is the most directly comparable accepted LIC paper. CMIC matches it on SOTA performance, has stronger ablation studies and mechanistic evidence (ERF), but has some framing imprecisions that FAT does not. The weighted-item comparison: CMIC shares FAT's heavy-weight strengths (SOTA performance, clear motivation) but has heavier weaknesses (overclaiming language, causality imprecision). This places CMIC marginally above FAT, at **6.5**.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>