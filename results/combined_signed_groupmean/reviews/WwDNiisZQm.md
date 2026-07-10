## Summary

This paper proposes Content-Aware Mamba (CAM), a modification of the Mamba state-space model for learned image compression that addresses two key limitations: (1) the content-agnostic raster scan that ignores feature-space proximity, and (2) Mamba's strict causality misaligned with the non-causal nature of images. CAM introduces Content-Adaptive Token Permutation (CTP), which uses a learned codebook (VQ-VAE-style) to cluster tokens by semantic similarity and reorder the scan sequence accordingly, and Global-Prior Prompting (GPP), which injects cluster-derived global prompts into the SSM readout to relax the causal constraint. The resulting model (CMiC) achieves state-of-the-art or competitive BD-rate performance on Tecnick (−21.34%) and CLIC (−17.58%), with efficiency far superior to prior Mamba-based LIC models (69M parameters, 2.39 TFLOPs vs. MambaIC's 157M, 5.56 TFLOPs).

## Strengths

- **Well-motivated problem with a practical solution.** The observation that Mamba's fixed raster scan poorly matches the redundancy structure of images—where semantically similar tokens may be spatially distant—is clearly articulated (Section 1, lines 15–28). The CTP mechanism using a shared codebook with EMA-updated centroids avoids per-sample iterative clustering at inference, a pragmatic design choice that is well justified (Section 3.3, lines 108–124) and supported by ablations showing a 1.8–2.4% BD-rate gain (Tab. 2). Cluster visualizations (Fig. 10) confirm semantically meaningful groupings.

- **Strong empirical results with comprehensive baselines.** CMiC achieves the best BD-rate on Tecnick (−21.34%) and CLIC (−17.58%) among the 13 compared methods, and improves over the previous best Mamba-based model (MambaIC) by 2.36–6.48% across datasets (Tab. 1). The advantage is larger at higher resolutions, consistent with the claim that better global modeling matters more for larger images. RD curves (Fig. 4–6) and rate-savings diagrams (Fig. 1c) support the aggregate numbers.

- **Favorable efficiency profile.** CMiC achieves SOTA results with 69.11M parameters and 2.39 TFLOPs—substantially leaner than MambaIC (157M, 5.56 TFLOPs) and comparable to methods like FTIC. Throughput ablation (Tab. 3) shows CTP+GPP add only ~5% overhead over a vanilla single-scan Mamba baseline (23.19 → 22.05 samples/s). GPU memory usage is reduced 78% versus MambaIC.

- **Comprehensive ablation and analysis.** The paper ablates CTP and GPP individually (Tab. 2), compares CAM blocks against Conv, 2D Mamba, attention-only, and CAM-only variants (Tab. 4), varies the cluster number K (Tab. 6), and provides ERF visualizations (Fig. 7–9) and clustering visualizations (Fig. 10) that support the claimed mechanisms. This is more thorough than typical for LIC papers.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

- **The "non-causal" framing is overstated relative to what GPP actually does.** The paper claims that GPP enables "non-causal long-range modeling" (line 34) and "relaxes the strict causal constraint" (line 183). However, the SSM state update remains strictly causal: **h**ᵢ = Ā·**h**ᵢ₋₁ + **B̄**·xᵢ. GPP modifies only the *output* matrix **C** → **C**+**P**, where **P** is a prompt derived from global clustering. This creates a gradient bypass path through the clustering assignment—evidenced by non-causal ERF gradients in Fig. 9(c)—but the recurrence itself is unchanged. The ERF visualizations genuinely show broader context, and GPP clearly helps (0.5–1.4% gain in Tab. 2). The weakness is one of framing precision: the paper conflates "gradients can flow non-causally through the prompt path" with "the SSM is now non-causal." The language should be refined to describe precisely what GPP relaxes.

- **The SOTA claim requires qualification on Kodak.** The abstract (line 34) and Section 4.3 (line 222) claim "state-of-the-art (SOTA) RD performance" and "superior performance" without qualification. In Tab. 1, however, MLICv2 achieves a better BD-rate on Kodak (−16.16% vs. CMiC's −15.91%). CMiC is the best overall across the three datasets (average −18.28% vs. MLICv2's −17.36%) and leads on Tecnick and CLIC, but the Kodak result should be acknowledged explicitly.

- **The "2D Mamba" baseline in Tab. 4 is underspecified.** The paper states "substitute [CAM blocks] with Conv block and 2D Mamba blocks in stages 3–5" (line 283) but does not define what "2D Mamba" means architecturally—whether it is standard 4-directional scanning, a different multi-scan variant, or something else. The reported FLOPs (2.54T vs. CAM's 2.39T) suggest it is not full 4-directional scanning. Without a clear specification, the reader cannot interpret what this comparison demonstrates, which matters because the paper's narrative depends on showing CAM outperforms 2D Mamba variants.

### Trivial
None.

## Nice-to-Haves

- An ablation applying CTP with *random* cluster assignments (rather than learned centroids) would separate the benefit of "grouping similar tokens" from "the clustering representation itself."
- An ablation comparing GPP against simply widening the hidden state or adding an extra Mamba layer with equivalent parameters would strengthen the attribution of GPP's 0.5–1.4% gain to "global information injection" rather than "more capacity."
- An ablation comparing prompt dictionaries tied to centroids (GPP's design) vs. learned independently (MambaIRv2 style) would strengthen the claimed novelty of the tying strategy.

## Removed Points

- **Missing MS-SSIM BD-rate table (Critical Issue 3 from Harsh Critic):** The paper claims MS-SSIM improvements in the main text with specific numbers (−7.34% vs. TCM-L, −3.87% vs. FTIC) and references an appendix figure. Since the parser strips appendix content, this table may exist in the original submission. Removed per rule: remove weaknesses about missing appendix content.
- **Code URL is blank (line 9):** Removed per rule: do not question availability of cited resources.
- **No statistical significance / variance reporting:** Single-run evaluation is standard practice in LIC papers. Removed as a field-practice norm.
- **Training dataset observation (Flickr2W):** The critic acknowledged this is not a flaw. Removed.

## Novel Insights

None beyond the paper's own contributions. The reviews confirmed the paper's claims and identified framing imprecisions, but raised no genuinely novel technical observations about the method beyond what the authors already discuss.

## Suggestions

- Refine the language about GPP's effect on causality: distinguish between "the SSM recurrence remains strictly causal" and "the output is conditioned on global priors via a prompt that creates non-causal gradient paths."
- Acknowledge the MLICv2 result on Kodak (−16.16% vs. −15.91%) when making SOTA claims.
- Define the "2D Mamba" baseline architecture precisely (number of scan directions, whether scans are independent or fused, etc.) to make Tab. 4 interpretable.

## Score and Decision

**Calibration summary:**
| Anchor | Path | Avg Score | Round | Itemized? | Comparison |
|--------|------|-----------|-------|-----------|------------|
| GroupMamba | /home/.../RmmrHEH6Nx.md | 3.00 | 1 | No | Lower novelty, weaker results |
| MambaVC | /home/.../KgJwbsfN7G.md | 4.80 | 1 | Yes | Simple Mamba application with no specific LIC design; ours has genuine novel contributions and far stronger results |
| Multimodal Mamba | /home/.../cagNCwQEEN.md | 3.40 | 1 | No | Different task; less rigorous evaluation |
| Spatial-Mamba | /home/.../iDe1mtxqK5.md | 7.00 | 1 | Yes | Visual SSM paper; weaknesses include "re-inventing convolution" (−9.97) and "limited contribution" (−9.99) vs. our max weakness of −2.24 |
| Frequency-Aware Transformer | /home/.../HKGQDDTuvZ.md | 6.00 | 2 | Yes | LIC transformer paper; missing comparisons (−8.90, −9.73) vs. our comprehensive baselines |
| Disentangled Training | /home/.../U67J0QNtzo.md | 7.50 | 2 | Yes | LIC training acceleration paper; missing related work (−9.18) vs. our minor weaknesses |
| Progressive Compression | /home/.../CxXGvKRDnL.md | 8.00 | 2 | No | Diffusion-based compression; different methodology, uniformly positive reviews |

**Round 1 bracket:** 7.5–8.5. My draft's weaknesses have impact scores (−0.00, −0.09, −2.24) far smaller than any anchor's top weakness (all claimed anchors have at least one weakness at −9.x to −10.0). My draft's top strengths (empirical results +9.97, efficiency +9.87 and +9.26, ERF visuals +6.09) are competitive with top anchors. The paper's weaknesses are exclusively minor framing/presentation issues that do not threaten the core contribution.

**Final score: 8.0.** This places CMiC above Spatial-Mamba (7.0) and Disentangled Training (7.5), whose weaknesses are an order of magnitude more severe, and in line with uniformly strong papers like Progressive Compression with Diffusion (8.0). The score reflects a well-executed paper with a clear novel contribution, strong empirical support, comprehensive ablations, and no fundamental flaws.

MY FINAL SCORE: <score>8.0</score>
MY FINAL DECISION: <decision>Accept</decision>