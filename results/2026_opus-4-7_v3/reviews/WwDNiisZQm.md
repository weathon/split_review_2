Now I've read the entire paper. Let me verify each claim before drafting.

Key verification points:
1. **GPP "relaxing causality" claim** — Section 3.4 line 183 says "effectively relaxing the strict causal constraint." The output equation becomes O_i = (C + P)h_i + Dx_i, but hidden state dynamics h_i = Āh_{i-1} + B̄x_i remain causal. The reviewer's criticism is valid — this is a readout-level modification, not a change to state dynamics.

2. **SOTA claim** — Table 1 confirms MLICv2 = −16.16% on Kodak vs CMIC = −15.91%. CMIC wins on Tecnick (−21.34% vs −20.13%) and CLIC (−17.58% vs −15.79%). The unqualified "SOTA" claim is slightly imprecise.

3. **Non-differentiable permutation** — The argmax in Algorithm 1 line 4 is indeed discrete. No discussion of gradient flow through this is present in the paper.

4. **Within-cluster ordering** — Section 3.3 says "first groups all tokens with g_i = 1, then those with g_i = 2, and so on" but does not specify intra-cluster order.

5. **Table 2 ablation** — Confirmed: baseline −13.26%, full model −15.91% on Kodak. CTP alone gives 2.0% gain, GPP alone 1.0%, combined 2.65%.

Let me now draft and submit the review.Now let me run calibration Round 1 — bracketing pass:Let me read the most relevant anchors to calibrate:Now I have enough calibration data. Let me form my bracket and write the final review.

**Round 1 Bracket:**
- MambaVC (4.80, Reject) — directly competing method; criticized for limited novelty (just applying existing Mamba blocks to compression). CMIC is clearly above — it proposes novel CTP/GPP mechanisms specifically for compression.
- Spatial-Mamba (7.00, Accept) — proposes structure-aware state fusion for Mamba with dilated convolutions. Comparable novelty level to CMIC; both add content-awareness to Mamba for 2D tasks with strong experimental validation.
- Progressive Compression (8.00, Accept) — more fundamental theoretical contribution with uniform noise diffusion for compression. CMIC is below this level.

**Initial bracket: 6.0–7.0**

CMIC sits clearly above MambaVC and roughly comparable to Spatial-Mamba. The CTP mechanism is arguably more creative than Spatial-Mamba's dilated convolution approach, though GPP is more incremental (adapted from MambaIRv2). The bounded weaknesses (framing precision, minor SOTA qualification) don't threaten core claims.

---

## Summary
This paper introduces Content-Aware Mamba (CAM) for learned image compression, addressing two limitations of standard Mamba in 2D vision: its content-agnostic raster scan order and strict causality. The first mechanism, Content-Adaptive Token Permutation (CTP), reorders tokens by codebook-based feature similarity before the SSM scan so that content-correlated tokens are processed consecutively. The second, Global-Prior Prompting (GPP), injects cluster-derived global priors into the SSM output equation to provide non-causal context. The resulting CMIC model achieves competitive-to-SOTA BD-rate performance across three standard datasets with a single selective scan, yielding 78% memory reduction over multi-directional Mamba approaches.

## Strengths
- **CTP is a genuinely novel, well-motivated contribution.** The observation that Mamba's raster scan is misaligned with image redundancy structure is precise, and the codebook-based reordering solution is both natural and effective. Table 2 shows CTP alone contributes 1.8–2.4% BD-rate reduction. Figure 10 confirms semantically coherent groupings (red doors, sky regions, feather textures), validating the mechanism beyond aggregate numbers.
- **Thorough and comprehensive evaluation.** The paper benchmarks against 14 learned methods plus VTM-21.0 across three datasets (Kodak, Tecnick, CLIC), reporting BD-rate, FLOPs, parameters, latency, and peak memory (Table 1). The ablation study (Tables 2, 4, 6) systematically isolates individual component contributions.
- **Compelling ERF visualizations provide mechanistic evidence.** The single-layer ERF decomposition (Figure 9) clearly demonstrates how CTP breaks raster-scan activation patterns and GPP introduces non-zero activations beyond the causal boundary — providing concrete, per-mechanism evidence rather than just aggregate metrics.
- **Favorable complexity-performance trade-off.** Using a single selective scan, CMIC reduces peak memory by 78% (4.44 GB vs. 20.32 GB) and latency by 39% compared to MambaIC, with CTP/GPP adding only ~5% training and ~4% inference overhead (Table 3).

## Weaknesses

### Fatal
None

### Major
- **GPP's "relaxing causality" framing overstates the mechanism's actual effect (Section 3.4).** The paper claims GPP "effectively relaxes the strict causal constraint" (Section 3.4), but the hidden state dynamics h_i = Āh_{i-1} + B̄x_i remain entirely causal — only the readout equation is modified to O_i = (C + P)h_i + Dx_i. The hidden state, which is the information carrier across the sequence, still suffers from causal information decay. GPP conditions the *readout* on a global summary statistic but does not alter the *state evolution*. The mechanism demonstrably works (Figure 9(c) confirms non-zero activations beyond the causal boundary; ablation shows 0.5–1.4% BD-rate improvement), but the theoretical narrative conflates readout conditioning with actual causality relaxation. A more precise characterization — "providing global context to the SSM readout" — would be both accurate and still compelling.

### Minor
- **SOTA claim requires minor qualification (Table 1).** MLICv2 achieves −16.16% BD-rate on Kodak versus CMIC's −15.91%. CMIC is best on Tecnick (−21.34% vs. −20.13%) and CLIC (−17.58% vs. −15.79%), so the overall picture is favorable, but the unqualified "state-of-the-art" claim in the abstract slightly overreaches. Acknowledging the Kodak result explicitly would strengthen credibility.
- **No discussion of gradient flow through the discrete permutation (Section 3.3).** The argmax cluster assignment (Algorithm 1, line 4) is non-differentiable. Gradients cannot flow through the permutation indices — the model must implicitly learn features that cluster well under this fixed procedure. While VQ-VAE operates similarly and works well, the complete absence of discussion about this training dynamic is a gap for a method paper that proposes permutation as a core mechanism.
- **Within-cluster and inter-cluster ordering are unspecified.** Section 3.3 states tokens are grouped by cluster ("first groups all tokens with g_i = 1, then those with g_i = 2, and so on") but never specifies the ordering within each cluster. For SSM processing, the sub-sequence ordering determines which within-cluster correlations the model can capture. The inter-cluster ordering (why cluster 1 before cluster 2?) is similarly undiscussed, yet determines cross-cluster interactions.
- **K sensitivity ablated only on Kodak (Table 6).** The K=32/64/128 comparison uses only the smallest dataset (768×512). Given that Tecnick (1200×1200) and CLIC (2K) have substantially more tokens, the optimal K may differ at higher resolutions.

### Trivial
None

## Nice-to-Haves
- Per-image analysis correlating CTP benefit with image characteristics (e.g., do images with spatially scattered semantic regions benefit more than those with spatially contiguous structures?).
- A targeted experiment measuring reconstruction quality as a function of scan position (early vs. late tokens) with and without GPP, directly demonstrating the information decay mitigation.
- Discussion of soft/differentiable permutation alternatives (e.g., optimal transport, Sinkhorn) as a potential direction for improvement.
- Extending the K ablation to Tecnick and CLIC to verify robustness across resolutions.

## Removed Points
*These points are flagged as removed; treat them with caution.*

- **"Quadruples computational complexity" caveat (Introduction).** The reviewer noted the claim understates the design space. However, the paper specifically refers to multi-directional scanning with 4 scan directions, and the claim is factually correct for that specific technique. The paper acknowledges other approaches in its related work. *Removed: factually correct in context.*
- **Comparison with Zhang et al. (2024b).** The reviewer requested experimental comparison with a CNN-based clustering method. However, the paper's scope is Mamba-based compression; the conceptual differences are discussed in the related work (Section 2.3). *Removed: scope creep.*
- **GPP's hybrid optimization path instability.** The reviewer speculated about potential instability from the EMA codebook + learned projection A operating on the same representation. No evidence of instability is presented, and the training results are strong. *Removed: speculative, no supporting evidence.*
- **One-hot assignment noise at cluster boundaries.** The reviewer speculated that hard assignments near cluster boundaries could introduce training noise. No evidence this is a practical problem. *Removed: speculative.*
- **Contribution attribution framing.** The reviewer noted CAM contributes ~17% of total BD-rate improvement over VTM. This is an observation about the nature of component-level contributions in architectural papers, not a weakness — all papers that introduce modules within larger architectures face this. *Removed: not a weakness.*

## Novel Insights
The core insight — that reordering tokens by feature-space similarity before SSM processing can effectively substitute for multi-directional scanning while being substantially cheaper (single scan vs. four scans) — is genuinely valuable and could generalize beyond image compression to other SSM-based vision tasks (e.g., image restoration, segmentation). The finding that a shared EMA-updated codebook naturally adapts its effective cluster count per image (Table 5: mean ~23 active out of 64 on Kodak) without any explicit mechanism for dynamic K selection is a useful observation for codebook-based methods more broadly.

## Suggestions
- Reframe the GPP contribution as "providing global context to the SSM readout" rather than "relaxing causality." This is more precise and remains compelling.
- Add a brief paragraph discussing gradient flow through the discrete permutation, explicitly drawing the parallel to VQ-VAE's codebook update mechanism.
- Qualify the SOTA claim: e.g., "CMIC achieves state-of-the-art performance on Tecnick and CLIC, and competitive performance on Kodak."
- Specify the within-cluster token ordering (presumably raster-scan preserved?) and briefly discuss whether inter-cluster ordering matters.
- Extend the K ablation to Tecnick and CLIC.

## Score and Decision

### Calibration Anchors

| Paper | Path | Avg Score | Round | Comparison to CMIC |
|-------|------|-----------|-------|--------------------|
| MambaVC | KgJwbsfN7G.md | 4.80 | 1 | Directly competing method; criticized for limited novelty (just applying existing VSS blocks). CMIC is significantly above — it proposes genuinely novel CTP mechanism with strong ablations. |
| GroupMamba | RmmrHEH6Nx.md | 3.00 | 1 | Mamba for vision; rejected for limited contribution. CMIC is clearly above. |
| Multimodal Mamba | cagNCwQEEN.md | 3.40 | 1 | Mamba + multimodal; rejected. CMIC has stronger domain-specific contributions. |
| Mamba Neural Operator | VtP7CamOR5.md | 3.00 | 1 | Mamba for PDEs; rejected for limited novelty. CMIC is clearly above. |
| Mamba-HMIL | 0A6f1b66pE.md | 3.25 | 1 | Mamba for WSI; rejected. CMIC has better evaluation and clearer contribution. |
| HRVMamba | 4UxXe3JZta.md | 4.50 | 1 | Mamba for dense prediction; rejected. CMIC has more novel mechanisms. |
| Unleashing Mamba in VLM | 0A6f1b66pE.md | 4.60 | 1 | Mamba for VLMs; rejected. CMIC has more specific and well-supported contributions. |
| Integrating SSM+Transformer for SR | 1YZw3RK2kg.md | 4.00 | 1 | SSM+Transformer hybrid; rejected for straightforward combination. CMIC's CTP is more novel. |
| Spatial-Mamba | iDe1mtxqK5.md | 7.00 | 1 | Adds structure-aware state fusion to Mamba via dilated convolution. Comparable novelty level; both well-executed. CMIC's CTP is arguably more creative, but GPP is somewhat incremental. |
| Mamba original | AL1fq05o7H.md | 6.25 | 1 | The foundational Mamba paper; mixed reviews (3,6,8,8). Much higher impact scope. Not directly comparable. |
| MambaPEFT | UAKnJMIBwf.md | 6.00 | 1 | PEFT for Mamba; accepted. Different scope. CMIC has stronger empirical results in its domain. |
| Autoregressive Pretraining Mamba | PQpvhUrA1C.md | 5.75 | 1 | Pretraining Mamba; accepted. Different scope. |
| Oscillatory SSM | GRMfXcAAFh.md | 8.00 | 1 | Theoretical SSM contribution; above CMIC's contribution level. |
| Progressive Compression | CxXGvKRDnL.md | 8.00 | 1 | Fundamental theoretical contribution to compression via diffusion; above CMIC. |

**Round 1 bracket: 6.0–7.0**

CMIC sits clearly above the rejected Mamba-for-vision papers (3.0–4.8) which were criticized for limited novelty or just applying existing blocks. It is comparable to Spatial-Mamba (7.0, accepted), which also proposes a specific mechanism to enhance Mamba for 2D tasks but was criticized for the straightforward nature of adding convolution. CMIC's CTP is arguably more novel than dilated convolution, but GPP is incremental (adapted from MambaIRv2), and the framing issues pull it slightly down.

**Final Assessment:** The paper makes a genuine, well-supported contribution through the CTP mechanism. The experimental evaluation is comprehensive and the results are strong. The weaknesses are real but bounded — the GPP framing is overstated but the mechanism works, the SOTA claim needs minor qualification, and some discussions are missing but none threaten the core contribution. This is a solid borderline-accept paper.

**Final Score: 6.5**

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>