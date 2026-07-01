Now I have all the information I need. Let me write the final consolidated review.

**Calibration Summary (Round 1 — Bracketing):**

| Anchor | Avg Score | Round | Comparison |
|--------|-----------|-------|------------|
| GroupMamba | 3.00 (Reject) | R1 | Limited novelty (channel-reduced VMamba + SE-like module). Current paper has more specific, well-motivated architectural innovations. |
| MambaVC | 4.80 (Reject) | R1 | First Mamba LIC paper, rejected for limited novelty (just applying VSS block, no compression-specific design). Current paper clearly stronger with targeted CTP/GPP innovations and more thorough evaluation. |
| Spatial-Mamba | 7.00 (Accept) | R1 | Improves Mamba for vision via structure-aware state fusion. Similar in nature to current paper. Accepted with minor weaknesses. Current paper comparable in contribution depth with slightly more vulnerable evaluation (entropy model confound). |

**Bracket:** 6.0–7.5. The paper is clearly above MambaVC (conceptually naive application of Mamba) and comparable to Spatial-Mamba (principled improvement of Mamba for vision). It does not reach the 8.0 level of papers with more fundamental theoretical contributions.

**Narrowing:** The entropy model confound (partially addressed but present) and training-data comparison issue (standard but real) prevent this from reaching the Spatial-Mamba level of confidence. Final score: **7.0**.

---

## Summary

This paper introduces Content-Aware Mamba (CAM) for learned image compression, proposing two mechanisms to address limitations of vanilla Mamba: **(1) Content-Adaptive Token Permutation (CTP)**, which clusters tokens by content similarity and reorganizes the scan order to prioritize feature-space proximity over spatial adjacency, and **(2) Global-Prior Prompting (GPP)**, which injects sample-specific global priors into the SSM's output matrix **C** to mitigate strict causality without multi-directional scans. The full model CMiC achieves competitive BD-rate results on Kodak (-15.91%), Tecnick (-21.34%), and CLIC (-17.58%) against VTM-21.0 with favorable complexity (69.11M params, 2.39 TFLOPs). The paper provides thorough diagnostic analysis including ERF visualizations that directly validate the claimed mechanisms.

---

## Strengths

1. **Precise problem diagnosis with targeted architectural response.** The paper identifies two specific limitations of Mamba for image compression — content-agnostic raster scanning and strict causality mismatched with 2D images (Sec. 1, lines 15–28) — and designs one mechanism that directly addresses each. This is not a generic module swap; it is a principled fix for known failures.

2. **Clean and principled technical design.** The codebook-based clustering with EMA updates (Sec. 3.3) adapts VQ-VAE's approach to avoid the instability of per-sample K-Means while preserving training stability. The Global-Prior Prompting mechanism (Sec. 3.4, Eq. on line 181) is elegant: modifying the SSM's output projection matrix **C** with sample-specific prompts is a lightweight way to introduce non-causality without the 4× cost of multi-directional scanning. The paper also correctly distinguishes its prompting from MambaIRv2's (line 177).

3. **Strong empirical results with favorable complexity trade-off.** CMiC achieves -15.91%, -21.34%, -17.58% BD-rate on Kodak, Tecnick, CLIC against VTM-21.0 (Table 1) with 69.11M params and 2.39 TFLOPs — substantially more efficient than the prior Mamba-based MambaIC (157.09M, 5.56 TFLOPs) and competitive with transformer-based methods. The 78% GPU memory reduction vs. MambaIC (attributed to single-directional scan) is a significant practical advantage.

4. **Diagnostic ERF analysis convincingly validates the claimed mechanisms.** Figure 9 is the most informative figure in the paper. It separates the effects of CTP and GPP by showing: (a) baseline — ERF stops at center token position (strict raster causality); (b) +GPP — non-zero activations extend beyond the scanned position; (c) +CTP — raster pattern broken, activation spreads to semantically related regions; (d) both — fully global content-adaptive ERF. This goes beyond what most LIC papers provide.

5. **Comprehensive ablation structure.** The paper systematically isolates CTP and GPP (Table 2), compares against architectural alternatives (Table 4: Conv block, 2D Mamba, attention-only, CAM-only), ablates cluster count K (Table 6), reports throughput (Table 3), visualizes clustering results (Figure 10), and shows per-image content-adaptive ERFs (Figure 8).

---

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

1. **Incomplete disentanglement of entropy model and CAM contributions.** The entropy model is built upon SCTX with modifications including depthwise convolution and gated MLPs (line 96). The baseline in Table 2 (no CTP, no GPP) achieves -13.26% BD-rate on Kodak — already stronger than many published methods (e.g., ELIC at -3.10%, TCM at -10.04%, CCA at -11.99%). This baseline includes the improved entropy model + window attention + vanilla Mamba. The paper correctly isolates CAM's marginal contribution (2.65% on Kodak), but it would benefit from a dedicated ablation that compares the baseline SCTX entropy model against the paper's enhanced version (without any CAM in the transforms) to quantify the entropy model's standalone contribution. The paper partially acknowledges this (line 248) but a clearer separation would make the attribution more transparent.

2. **Comparison fairness across training datasets.** The paper trains on Flickr2W but cites baseline numbers from original publications (Table 1), which may have been trained on different datasets (ImageNet, COCO, or larger proprietary sets). The paper does not explicitly acknowledge this discrepancy or discuss its potential impact. While this is standard practice in LIC evaluation and the comparisons against MambaVC/MambaIC (same SSM family, likely similar data scale) are informative, a clearer note about training data differences would improve rigor. Retraining the most direct competitors (MambaVC, MambaIC) on Flickr2W would be the strongest fix.

3. **No discussion of limitations.** The conclusion (Section 5) does not mention any limitations. Two honest limitations worth noting: (a) the clustering is based on cosine similarity of latent features, which may not capture all forms of visual redundancy important for compression; (b) the fixed codebook size (K=64) acts as a ceiling on adaptivity — images requiring finer-grained grouping may be under-served.

### Trivial
None.

---

## Nice-to-Haves
- Report variance across runs (e.g., 3 training seeds for Kodak). Not standard in LIC but would raise rigor.
- Clarify whether the inverse permutation π⁻¹ (line 122) restores the original spatial layout *before* or *after* the SSM output — the current phrasing is slightly ambiguous (the mechanism is correct, but could be clearer).

---

## Removed Points
These points from the input review are removed with justification:

- **"The entropy model confound is an evidential concern"** — Kept but downgraded to Minor. The paper partially addresses this via Table 2 (which isolates CAM's 2.65% incremental gain). The concern is valid but does not threaten the core claim.
- **Criticisms about appendix content** (missing proofs/ablations in appendix) — Removed per hard rules. The parser strips appendix content; these exist in the original submission.
- **"Retrain baselines on Flickr2W"** — Kept as a suggestion in Minor #2. Not required for acceptance but would strengthen.
- **Formatting/style nitpicks and grammar concerns** — Removed per hard rules.
- **Variance reporting** — Moved to Nice-to-Haves. Not standard for LIC single-run evaluations.

---

## Novel Insights

None beyond the paper's own contributions.

---

## Suggestions

1. Add a dedicated ablation comparing the baseline SCTX entropy model against the paper's enhanced entropy model (without any CAM in the transforms) to separately quantify the entropy model's contribution.
2. Explicitly state in the experimental setup that all baseline numbers are from original publications, and note potential training data differences.
3. Add a limitations paragraph to the conclusion discussing the scope/constraints of the clustering-based approach.

---

## Score and Decision

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>