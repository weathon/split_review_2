Now I have all the information I need. Let me write the final consolidated review.

## Summary
This paper introduces Content-Aware Mamba (CAM) for learned image compression, addressing two fundamental limitations of applying Mamba-style SSMs to images: (1) the content-agnostic raster scan that ignores feature-space correlations, and (2) strict causality that prevents tokens from accessing subsequent context. The proposed solutions are Content-Adaptive Token Permutation (CTP), which reorders tokens by clustering them based on feature similarity, and Global-Prior Prompting (GPP), which injects centroid-derived global priors into the SSM output projection. Their model CMiC achieves competitive BD-rate savings (−15.91%, −21.34%, −17.58% over VTM-21.0) with moderate complexity (69.11M params, 2.39 TFLOPs).

## Strengths

- **Well-motivated problem diagnosis with mechanistic evidence.** The paper clearly identifies two genuine architectural mismatches between Mamba and image compression: the rigid, content-agnostic scan path and the misaligned causal processing. The ERF visualization in Figure 9 provides direct empirical evidence — column (b) shows a clean cutoff at the center token, confirming that strict causality creates a hard boundary in the baseline.

- **Clean ablation isolating two complementary mechanisms.** Table 2 demonstrates that CTP contributes ~1.8–2.4% BD-rate improvement and GPP contributes ~0.5–1.4%, with the combined effect (~2.7–3.6%) being roughly additive. This validates the authors' decomposition of the problem. The ERF analysis in Figure 9 further provides mechanistic insight: GPP breaks the causal cutoff (columns b→c), while CTP reshapes the ERF toward semantically related regions (columns c→d).

- **Competitive rate-distortion performance with favorable efficiency.** The model achieves strong BD-rate savings while using 69.11M params and 2.39 TFLOPs — substantially more efficient than several competitors (MLIC++: 116.48M/2.64T, MambaIC: 157.09M/5.56T, DCAE: 119.22M/2.28T). The 78% peak-memory reduction over MambaIC (4.44 GB vs 20.32 GB) is notable and plausibly attributed to the single-scan design.

- **Thorough empirical analysis.** Beyond component ablations, the paper provides structural ablations (Table 4: Conv block, 2D Mamba, Attention-only, CAM-only), cluster-number sensitivity (Table 6), adaptive cluster activation analysis (Table 5), clustering visualizations (Figure 10), and ERF analysis across models (Figures 7-9). Together these build a coherent picture of how and why the method works.

## Weaknesses

### Fatal
None.

### Major

1. **Gradient flow through the hard clustering assignment is not addressed.** The CTP mechanism involves: (a) assigning each token to a cluster via argmax over cosine similarity to centroids (producing hard one-hot assignments), (b) permuting the sequence based on these assignments, and (c) running the SSM on the permuted sequence. The paper states that the centroid codebook is updated via non-gradient EMA (line 121, line 177), but it never explains how gradients back-propagate through the argmax into the token features (and hence into the layers that produce them). The paper draws inspiration from VQ-VAE (line 110) but does not mention using a straight-through estimator, Gumbel-softmax, or any other gradient approximation. This is the single most important methodological detail missing from the paper. It is likely addressable (e.g., the features receive gradients directly through the SSM path since tokens are permuted but not replaced by centroids, and the EMA centroid update provides an EM-like training loop), but the paper must state how this is handled for a reader to evaluate the method's correctness.

### Minor

2. **GPP's causal relaxation is limited to the output readout, not the state update.** The prompt is added to the C matrix in the output equation O_i = (C+P)h_i + Dx_i (line 181), but the state update h_i = Āh_{i-1} + B̄x_i remains strictly causal. The paper's claim that GPP "relaxes strict causality" is reasonable — the global prompt carries information from the entire image into each output step — but the paper overstates this somewhat. The state propagation itself does not become non-causal; the "non-causal" effect operates through a side channel (the sample-specific prompt). The ERF evidence in Figure 9(c) is consistent with this interpretation (global prior influences the output), but the paper should explicitly acknowledge this distinction.

3. **The prompt dimension d_s is not reported.** The paper introduces U ∈ ℝ^{K×d_s} and a projection A: ℝ^d → ℝ^{d_s} (line 173-175) but never states the value of d_s. This is needed to assess the computational overhead of GPP.

4. **Incomplete training details.** The paper reports the optimizer (Adam), initial learning rate (10⁻⁴), and λ values, but omits the total number of training steps/epochs, batch size, learning rate schedule, and number of GPUs. These are standard details necessary for reproducibility.

5. **Baseline number provenance is unclear.** Table 1 compares against a large set of published methods, but the paper does not state which numbers are re-implemented vs. taken from original papers. While this is common practice in LIC literature, stating the source of each baseline would improve transparency.

6. **Table 1 uses "MambaC" while the text consistently uses "MambaIC"** (Zeng et al., 2025). This is a minor naming inconsistency.

### Trivial

7. **"Quadruples computational complexity" (line 28) is a simplification.** The claim that multi-directional scanning quadruples complexity is directionally correct but glosses over capacity trade-offs (four scans also increase representational power). This does not affect the paper's contribution.

## Nice-to-Haves

- **Direct comparison against MambaIRv2-style prompt pool.** The paper positions GPP as distinct from MambaIRv2 by tying prompts to clustering centroids rather than using a freely-learned prompt matrix. A direct ablation (replace centroid-derived prompts with a learnable matrix of the same size, keeping everything else identical) would cleanly quantify the value of this design choice.

- **Clarify whether tokens are L2-normalized before the cosine distance computation.** Algorithm 1 computes cosine similarity with both numerator and denominator, so pre-normalization is not strictly necessary, but stating this explicitly would preempt confusion.

## Removed Points

- The critic's claim that the GPP-vs-MambaIRv2 distinction is "narrower than the paper's framing might suggest" is retained in weakened form as a Minor weakness (item 2 above) about the state vs. output distinction. The critic's broader characterization of the contribution as "modest" is a subjective judgment that goes beyond what the evidence supports; the centroid-based prompt construction is meaningfully different from a free parameter matrix and the paper states the difference clearly (line 177).

- The critic's observation that "the paper could more directly contrast its content-adaptive clustering with Zhang et al. (2024b)" is not retained as a weakness because (a) the paper already cites this work, (b) the paper promises a detailed comparison in Appendix A.2 (removed by the parser), and (c) without access to that appendix content or the cited paper, this cannot be verified as a genuine gap.

- The critic's suggestion about feature normalization before clustering is moved to Nice-to-Haves since the cosine similarity formula already handles normalization in the distance computation.

## Novel Insights

The harsh critic's analysis surfaces a genuinely novel observation about the gradient-flow gap in the CTP mechanism that is not discussed in the paper. This is the most actionable insight: the paper draws an explicit parallel to VQ-VAE but never clarifies whether a straight-through estimator or alternative gradient approximation is used for the argmax assignment. The critic's dissection of where the gradient can and cannot flow (through the token values via the SSM, but not through the assignment operation itself) is a nuanced read that identifies a real omission in the methodological description. The second useful insight is the observation that GPP's "non-causal" effect operates on the output readout rather than the state propagation — the paper's framing is technically accurate (the global prompt does carry information from the entire image) but would benefit from acknowledging this architectural distinction.

## Suggestions

1. **Explicitly state how gradients are handled through the discrete clustering assignment.** This is the single most important clarification. Specifically: are straight-through estimators used? Is the argmax softened during training? Or are the assignments treated as fixed in the backward pass (stop-gradient), with the centroids updated only via EMA? Each approach has different implications, and the paper must disclose this.

2. **Report the missing training hyperparameters:** total training steps/epochs, batch size, learning rate schedule, and d_s value. Clarify baseline number provenance in Table 1.

3. **Acknowledge the GPP mechanism more precisely:** explicitly state that the prompt conditions the output but not the state update, and clarify that the "relaxed causality" operates through global information carried by the prompt rather than through non-causal state propagation.

## Score and Decision

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>