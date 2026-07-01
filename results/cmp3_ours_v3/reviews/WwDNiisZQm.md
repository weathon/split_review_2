## Summary

This paper introduces Content-Aware Mamba (CAM) for learned image compression, addressing two fundamental limitations of vanilla Mamba when applied to images: (1) the fixed raster-scan order is content-agnostic, and (2) Mamba's strict causality is misaligned with the 2D structure of images. The authors propose Content-Adaptive Token Permutation (CTP), which reorders tokens by feature similarity via codebook-based clustering, and Global-Prior Prompting (GPP), which injects sample-specific global priors into the SSM output. The resulting CMIC model achieves competitive BD-rate savings over VTM-21.0 (15.91% on Kodak, 21.34% on Tecnick, 17.58% on CLIC) while maintaining favorable efficiency (69.11M params, 2.39 TFLOPs, 4.44 GB peak memory) — outperforming prior Mamba-based LIC methods by substantial margins with significantly lower compute.

## Strengths

1. **Well-motivated problem-to-solution mapping.** The paper clearly identifies two specific weaknesses of vanilla Mamba for image compression (rigid scan order and causality mismatch) and introduces two mechanisms (CTP and GPP) directly and cleanly motivated by these weaknesses. The connection between diagnosis and design is unusually tight (Sections 1, 3.3, 3.4).

2. **Convincing ablation evidence for both components.** Table 2 shows that CTP alone yields 1.8–2.4% BD-rate improvement over the vanilla baseline, GPP alone yields 0.5–1.4%, and together they achieve 2.7–3.6%. The ERF visualizations in Figure 9 further substantiate the mechanism: removing both components yields a narrow raster-band ERF; adding GPP widens it non-causally; adding CTP reshapes it toward semantically correlated regions; the full model gives a global, content-adaptive ERF. The qualitative and quantitative evidence tell exactly the same story.

3. **Competitive results with credible efficiency metrics.** CMIC outperforms prior Mamba-based LIC methods (MambaVC, MambaIC) by substantial margins (2.36–10.09% BD-rate improvement across datasets) while using fewer parameters (69.11M vs 157.09M for MambaIC), fewer FLOPs (2.39 vs 5.56 TFLOPs), and 78% less GPU memory. The throughput ablation (Table 3) confirms that CTP+GPP add only ~5% overhead to the vanilla Mamba baseline (23.19 to 22.05 samples/s), making the efficiency story credible.

## Weaknesses

### Major

- **"Consistently outperforms" claim is inaccurate on Kodak vs MLICv2.** The paper states at line 224 that "CMIC consistently outperforms leading methods across all evaluated datasets." However, Table 1 shows that on Kodak, CMIC achieves -15.91% BD-rate while MLICv2 achieves -16.16% — meaning MLICv2 is better by ~1.5% relative. On Tecnick and CLIC, CMIC does outperform MLICv2 (-21.34% vs -20.13%; -17.58% vs -15.79%). The Kodak comparison directly contradicts the unqualified claim. The authors should qualify this (e.g., "outperforms on most datasets, and is competitive with MLICv2 on Kodak"). This does not invalidate the overall contribution but weakens the paper's precision and should be corrected.

### Minor

- **"Inverted SSM block" is named in the architecture diagram but never explained.** The Figure 2 caption (line 76) lists the CAM block as containing "a Content-Aware SSM block, a CAM block, and an Inverted SSM block." While the Content-Aware SSM block is thoroughly detailed in Sections 3.3 and 3.4, the "Inverted SSM block" receives no description in the text. This is a gap in the method description — it may be a standard reverse-scan element, but the reader cannot determine this from the paper as written.

- **Clustering training dynamics are underexplored in the main text.** Centroids are updated via non-gradient K-Means with EMA smoothing while the feature extractor is trained via gradient descent — a setup reminiscent of VQ-VAE training, which is known to suffer from codebook collapse and low utilization. The paper provides some evidence this works (Table 5 reports mean activation of 23-26 out of 64 centroids) and references Appendices A.8-A.10. However, the main text does not discuss potential instability, sensitivity to the EMA decay parameter λ, or the risk of dead centroids. A brief discussion in the main text (not just the appendix) would strengthen confidence.

- **Training details are underspecified for reproducibility.** The paper mentions Flickr2W, Adam with learning rate 1e-4, and A100 GPUs, but omits total training steps/epochs, training batch size, learning rate schedule, weight decay, gradient clipping, and data augmentation. These are standard reporting requirements for LIC.

### Trivial

- **Naming inconsistency between "CMiC" and "CMIC"** (e.g., line 9 vs line 34 vs Table 1). Also, the row labeled "MambaC" (line 209) in Table 1 cites Zeng et al. (2025), but the related work refers to this method as "MambaIC" — naming should be consistent.

## Nice-to-Haves

- Clarify whether window-attention and CAM blocks are arranged sequentially or in parallel — the description at line 94 ("we first utilize window-attention … while our proposed CAM blocks are introduced") is slightly ambiguous.
- Provide brief context for FTIC's ">10" second latency in Table 1, which is an order of magnitude larger than all other methods.

## Removed Points

These points from the input review are removed or demoted:

- **"Non-causal" overstatement (Issue 2 from Harsh Critic).** Removed because the paper's language about causality is defensible: the prompt P is derived from the full image (non-causal), and while the hidden state update remains causal, the output O_i = (C+P)h_i carries globally-conditioned information. The paper uses qualifiers like "mitigates," "relaxes," and "effectively" throughout, and the ERF evidence (Figure 9) confirms non-causal activation. The criticism overstates the issue.
- **Section-by-section formatting notes, minor phrasing suggestions.** These are either parser artifacts or style nitpicks removed per instructions.
- **Concerns about missing appendix content (A.8-A.10).** The parser strips appendices from all papers; the authors likely include these details. Not a valid criticism of the paper as submitted.
- **Generic concerns about missing confidence intervals / theoretical proofs.** These demand practices not standard for this type of empirical systems paper.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Correct the "consistently outperforms" claim to acknowledge the MLICv2 comparison on Kodak.
2. Add a paragraph in Section 3.2 describing the Inverted SSM block.
3. Include a brief discussion of training stability (EMA decay sensitivity, potential centroid collapse) in the main text.
4. Add standard training hyperparameters (epochs, batch size, schedule, weight decay) for reproducibility.
5. Standardize naming conventions (CMiC/CMIC, MambaC/MambaIC).

## Score and Decision

**Calibration anchors (all rounds):**

| Paper | Avg Score | Round | Comparison to CMIC |
|-------|-----------|-------|-------------------|
| MambaVC (KgJwbsfN7G) | 4.80, Reject | R1 | Same topic (Mamba for LIC), but CMIC has genuine compression-specific innovations, full SOTA comparisons, and strong ablations — clearly stronger. |
| GroupMamba (RmmrHEH6Nx) | 3.00, Reject | R1 | Parameter-efficient visual SSM — less relevant, lower score due to stability issues. |
| Spatial-Mamba (iDe1mtxqK5) | 7.00, Accept | R1 | Visual SSM with novel mechanism, more general-purpose contribution. Similar rigor; CMIC is domain-specific, slightly below in scope. |
| FTIC (HKGQDDTuvZ) | 6.00, Accept | R2 | Direct LIC competitor (CMIC outperforms it). Similar depth of innovation; CMIC has slightly stronger ablations and more novel mechanisms. |
| CMC-Bench (foKwWau15m) | 6.00, Reject | R2 | Compression benchmark — different contribution type, less relevant. |

**Round 1 bracket:** [5.5, 7.0]

**Final score rationale:** The paper presents genuine, compression-specific innovations (CTP and GPP) with strong ablation evidence and competitive results. It is clearly stronger than MambaVC (4.80), which was a straightforward application of Mamba without domain-specific design. It is comparable to FTIC (6.00) with slightly stronger evidence, but its contribution is domain-specific to compression rather than general-purpose like Spatial-Mamba (7.00). The overclaim on Kodak vs MLICv2 and the missing Inverted SSM description prevent a higher score.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>