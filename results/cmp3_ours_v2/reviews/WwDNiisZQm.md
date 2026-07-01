Now I have strong calibration anchors. Let me finalize the review.

**Bracket reasoning**: Round 1 bracketing placed CMIC in the 5.5-7.5 range. It is clearly stronger than MambaVC (4.80, rejected) — CMIC has compression-specific innovations, baselines against SOTA methods, and thorough ablation that MambaVC lacked. It is weaker than Spatial-Mamba (7.00, accepted) — Spatial-Mamba offers a general vision backbone with theoretical analysis while CMIC's contributions are specific to compression. Comparing to accepted compression papers: ElasticTok (6.00), "How many tokens" (5.75), CMIC is empirically stronger within its domain. I narrow to **6.0**.

Here is the final review.

## Summary

This paper introduces Content-Aware Mamba for Image Compression (CMIC), which addresses two fundamental limitations of vanilla Mamba when applied to image compression: (1) content-agnostic raster-scan ordering, which fails to prioritize interactions between semantically similar but spatially distant tokens, and (2) strict causality, which prevents tokens from accessing information beyond their predecessors in the scan sequence. The paper proposes Content-Adaptive Token Permutation (CTP), which uses codebook-based K-Means clustering to reorder tokens by feature similarity, and Global-Prior Prompting (GPP), which injects sample-specific global priors into the state-space model to relax causality. CMIC achieves strong rate-distortion performance (−15.91%, −21.34%, −17.58% BD-rate on Kodak, Tecnick, CLIC against VTM-21.0) with competitive efficiency (69.11M params, 2.39 TFLOPs).

## Strengths

1. **Well-motivated problem with clear diagnostic evidence.** The paper identifies two specific failures of vanilla Mamba for image compression (content-agnostic scanning and strict causality), and each maps directly to a proposed component (CTP and GPP). The ERF visualization in Figure 9 provides striking confirmation: column (b) shows strict causal truncation, columns (c–e) show how GPP and CTP progressively expand the receptive field. This level of mechanistic diagnosis is uncommon and elevates the paper.

2. **Practical and well-justified clustering design.** The use of a shared learnable codebook with EMA updates (Section 3.3) replaces expensive and unstable online K-Means. It yields O(1) deterministic inference with no iterative updates (line 124). The ablation on K (Table 6) showing diminishing returns past 64 clusters is a responsible design decision. The cluster visualization (Figure 10) confirms semantically meaningful groupings (edges, sky, feathers).

3. **Clean ablation study that isolates contributions.** Table 2 shows baseline, CTP alone, GPP alone, and both. The improvements are additive but not perfectly so (2.7–3.6% combined vs ~2% + ~1% individually), consistent with complementary mechanisms. Table 4 tests structural alternatives (Conv, 2D Mamba, Attention-only, CAM-only vs full CMIC). Table 3 reports throughput overhead (~5% slowdown), which is honest and useful.

4. **Strong empirical results with competitive efficiency.** On Tecnick and CLIC, CMIC achieves the best BD-rate in Table 1. On Kodak, it is second only to MLICv2 by a small margin (0.25 pp). Complexity metrics (69.11M params, 2.39 TFLOPs, 0.405s latency, 4.44 GB peak memory) are competitive, particularly against MambaIC (157M params, 5.56 TFLOPs). The 78% GPU memory reduction over MambaIC (line 244) is a concrete practical advantage.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

1. **SOTA claim is slightly overstated on Kodak.** The paper states CMIC "consistently outperforms leading methods across all evaluated datasets" (lines 222–224). However, Table 1 shows MLICv2 achieves −16.16% BD-rate on Kodak versus CMIC's −15.91% (more negative is better), so MLICv2 outperforms CMIC on this dataset. The margin is small (0.25 pp) and CMIC is SOTA on the other two datasets, but the blanket claim of "consistent" outperformance should be qualified. *(Verified: Table 1, lines 205 and 210.)*

2. **Training data confound between competitors is not addressed.** The paper trains on Flickr2W (line 189). Several competing methods (MLIC++, MLICv2, WeConvene, etc.) are known to use larger training sets (e.g., CLIC training set + Flickr2W). If CMIC outperforms these with *less* data, that is actually a *stronger* result — but the paper neither acknowledges this confound nor provides a controlled comparison (e.g., training a subset of baselines on Flickr2W). Given that LIC results are sensitive to training data scale, this omission weakens the basis for the SOTA claim. *(Does not undermine the method's validity.)*

3. **Gradient flow through the hard permutation is not discussed.** The forward pass applies a hard assignment (argmax over cosine similarities, Algorithm 1 line 4) to cluster tokens, then permutes, runs the SSM, and inverse-permutes. Since clustering assignments depend on input features from earlier layers, a non-differentiable argmax sits in the middle of the computational graph. The centroids are updated via non-gradient EMA (which avoids gradient through centroids themselves), but the paper does not explain how gradients flow through the *assignment* step. Standard approaches include stop-gradient or straight-through estimation; the paper should clarify. *(Does not invalidate results but is a reproducibility concern.)*

4. **The EMA decay λ for centroid updates is not reported.** Algorithm 1 uses λ for the exponential moving average (line 9: c_j ← λ c_j + (1−λ) c_j^*), but its value is not stated anywhere in the main text. This is a free parameter affecting clustering stability and training dynamics.

5. **Framing of multi-directional scan overhead as a major drawback.** The paper states that multi-directional scanning "quadruples computational complexity" (lines 28, 34), presenting this as a key motivation. While 4× is technically correct, the result is still linear in sequence length — a 4× constant factor, not a qualitative scaling change. Many Mamba vision papers use 4-direction scans because the overhead is manageable. This framing somewhat overstates the cost. *(Does not affect results.)*

### Trivial

1. **"MambaC" in Table 1 (line 209) should likely be "MambaIC"** to match the reference (Zeng et al., 2025) and the usage elsewhere in the paper.

2. **Figures 4–6 label the VTM-21.0 curve as "VTMM-21.0"** in figure captions (lines 153, 159, 165), which appears to be a typo.

## Nice-to-Haves

- Discuss whether T=5 K-Means iterations (line 214) is sufficient for convergence, or provide a small ablation on iteration count.
- Discuss potential training stability issues from noisy clustering assignments during early training (the EMA update partially addresses this, but explicit discussion would help).
- Report total training time comparison between CMIC and baseline to contextualize the 5% per-step overhead from K-Means iterations.
- A controlled experiment training a subset of competitors on Flickr2W (or training CMIC on the same mix as competitors) would transform the SOTA claim from suggestive to definitive.

## Removed Points

The following points from the input review are removed:

- **Entropy model modifications under-specified / contribution not disentangled** (Critical Issue #3 in the harsh review): The reviewer argued that the entropy model changes cannot be evaluated because Figure 3 is a garbled parser artifact and details are in the appendix. Per filter rules, the parser strips appendix content from all papers; the full details exist in the original submission (the paper states "More details and ablations are provided in Appendix A.3" at line 96). The paper also explicitly addresses the related concern by noting that "adding CAM [to the entropy model] yields negligible performance gains" (line 248), which separates entropy model improvements from CAM contributions. This criticism is removed.

- **MambaVC/MambaIC size comparisons not apples-to-apples** (from Section-by-Section Notes): The reviewer noted that MambaVC (47.88M params) is smaller than CMIC (69.11M), but CMIC outperforms MambaVC by a large margin (7.51% BD-rate on Kodak). The paper does not claim parameter-efficiency over MambaVC; it claims better RD performance. The comparison with MambaIC (157M → 69M) actually favors CMIC. This criticism does not identify a genuine weakness.

- **Suggestion to run additional ablations with fixed standard entropy model**: This is already partially addressed — the paper states CAM in the entropy model yields negligible gains, and detailed entropy model ablations are in the appendix (stripped by parser).

- **Speculative concerns about training stability from noisy clustering**: Moved to Nice-to-Haves as it is a speculative failure mode the paper could discuss but does not need to.

## Novel Insights

The harsh reviewer's most insightful observation is that the paper's mechanistic diagnosis (content-agnostic scan + strict causality) is validated through a carefully designed ERF ablation (Figure 9) that isolates each component's effect on the receptive field — a degree of diagnostic evidence rarely seen in compression papers. The reviewer also correctly notes that the additive but non-perfectly-independent improvement of CTP and GPP (2.7–3.6% combined vs ~2% + ~1% individually, Table 2) is exactly the pattern expected for complementary mechanisms, which strengthens the paper's narrative. Additionally, the observation that Table 4's CAM-only variant (−14.68%) versus full CMIC (−15.91%) shows that window attention still contributes 1.23 pp — meaning CAM is complementary to local attention, not a full replacement — is a nuanced take the paper itself does not explicitly discuss. None beyond the paper's own contributions.

## Suggestions

1. **Qualify the SOTA claim.** Acknowledge that on Kodak, MLICv2 achieves a marginally better BD-rate (−16.16% vs −15.91%), while CMIC is SOTA on Tecnick and CLIC. Change "consistently outperforms leading methods" to something like "achieves SOTA or highly competitive results across all datasets."

2. **Address the training data confound.** Add a brief discussion of training data configurations used by competing methods and acknowledge that Flickr2W-only training may make the comparison conservative for baselines trained on larger data.

3. **Clarify gradient flow.** State explicitly how gradients pass through the argmax-based clustering assignment — specifically, whether the assignment is detached (stop-gradient), uses a straight-through estimator, or applies the Gumbel-softmax trick.

4. **Report the EMA decay λ** used for centroid updates in Algorithm 1.

5. **Fix minor typos:** "MambaC" → "MambaIC" in Table 1; "VTMM-21.0" → "VTM-21.0" in figure captions.

## Score and Decision

**Calibration anchors** (all rounds):

| Anchor | Score | Round | Comparison |
|--------|-------|-------|------------|
| MambaVC (KgJwbsfN7G) | 4.80 (rejected) | R1 | Weaker: CMIC has compression-specific innovations (CTP, GPP), compares with SOTA, has thorough ablation that MambaVC lacks |
| GroupMamba (RmmrHEH6Nx) | 3.00 (rejected) | R1 | Much weaker: general vision Mamba with limited novelty |
| Autoregressive Pretraining w/ Mamba (PQpvhUrA1C) | 5.75 (accepted) | R2 | Comparable: both are Mamba-based vision methods, CMIC has stronger application-specific empirical validation |
| "How many tokens" (mb2ryuZ3wz) | 5.75 (accepted) | R2 | Comparable: variable-length tokenization for images, different focus |
| ElasticTok (tFV5GrWOGm) | 6.00 (accepted) | R2 | Slightly stronger: adaptive tokenization with broader application scope |
| RECOMBINER (VkWbxFrCC8) | 6.67 (accepted) | R2 | Stronger: neural compression with Bayesian INR, deeper theoretical contribution |
| Spatial-Mamba (iDe1mtxqK5) | 7.00 (accepted) | R2 | Stronger: general vision backbone with theoretical analysis, broader impact |
| Approaching RD Limits (Tv36j85SqR) | 7.20 (accepted) | R2 | Stronger: theoretical contribution to neural compression foundations |

**Round 1 bracket**: 5.5–7.5 (CMIC is clearly stronger than MambaVC at 4.80, clearly weaker than Spatial-Mamba at 7.00)

**Narrowing**: Compared to accepted compression papers at 5.75–6.00 (ElasticTok: 6.00, Autoregressive Pretraining: 5.75, "How many tokens": 5.75), CMIC has comparable contribution depth and stronger task-specific empirical validation. The weaknesses are all minor. The final score of **6.0** reflects a well-executed, empirically strong paper with incremental but clearly validated contributions.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>