Now I have all the verification I need. Let me write the final review.

## Summary

The paper proposes SigMap, a multimodal foundation model for wireless localization with two technical innovations: (1) a cycle-adaptive masking strategy that dynamically adjusts mask patterns based on detected periodicities in CSI, and (2) a "map-as-prompt" framework that encodes 3D building geometry via a GNN into soft prompt tokens prepended to a frozen transformer backbone. Evaluation is on simulated ray-tracing datasets (DeepMIMO, WAIR-D) for single-BS and multi-BS localization tasks.

## Strengths

1. **Domain-aware masking motivation.** The observation that CSI has inherent periodic structure (OFDM subcarrier grid, antenna array geometry) and that standard random masking could let the model exploit periodic shortcuts rather than learn meaningful representations is specific to the wireless domain and well-motivated (Section 3.3). This is not a generic augmentation borrowed from CV/NLP.

2. **Clean architectural design for map integration.** Using a GNN over Delaunay-triangulated 3D building meshes to generate soft prompt tokens that are prepended to a frozen transformer backbone is a natural and coherent way to inject geometric priors without retraining the backbone (Section 3.4, Algorithm 1).

3. **Genuine parameter efficiency.** Fine-tuning only 0.085M of 11.73M parameters (0.7%) with 1000 epochs completing in 30 minutes and 0.83 ms/sample inference latency is practically meaningful (Section 4.6, Table 5).

## Weaknesses

### Fatal
None.

### Major

1. **Under-specified core algorithm: cycle-adaptive masking cannot be reproduced from the main text.** The paper's first claimed contribution (Section 3.3, Equation 6) depends on a periodicity detection step that is never explained concretely. Specifically: (a) The input is a 4D tensor (Eq. 5: 2 × N_r × N_t × N_s), but Eq. 6 treats it as 2D without specifying which dimensions i and j index — the reader cannot tell whether the mask is applied to the subcarrier×antenna plane, subcarrier×time, or something else. (b) The paper says "compute shift patterns using cross-correlation analysis" and "detect dominant periodicities" but never explains how d_final is extracted from the cross-correlation output (which peak? what threshold? per-sample or per-batch?). (c) The mask width parameter w is never given a value or ablated. (d) The baselines "grid-masking" and "strip-masking" in Table 3 are not defined, making the ablation uninformative. For a methods paper where this is the first claimed innovation, this level of vagueness is a serious deficiency.

2. **Concrete data inconsistency in a reported result.** The generalization table (Section 4.5) reports SIGMAP (w/ map) MAE = **1.880 m** on WAIR-D Scenario-2, but the immediately following paragraph (line 340) says **1.580 m** on WAIR-D Scenario-2 — a 30 cm discrepancy. One of these is wrong. Combined with the absence of standard deviations despite claiming 5 independent runs (line 239), this erodes confidence in the numerical results.

3. **Evaluation entirely on simulated data without acknowledgment of the limitation.** Every experiment uses ray-tracing simulations (DeepMIMO, WAIR-D). The paper frames SigMap as a "foundation model" and claims "strong zero-shot generalization," but no experiment involves real measured CSI from hardware. Simulated CSI systematically differs from real captured CSI in hardware impairments (I/Q imbalance, phase noise, amplifier nonlinearities), synchronization assumptions, and noise/interference structure. The paper does not acknowledge this limitation or discuss which conclusions are likely to transfer to real deployments. For a paper claiming a "foundation model" for a physical sensing modality, at minimum the limitation should be explicitly stated and discussed.

### Minor

4. **NLoS-aware attention mechanism introduced ad-hoc in the experimental section.** Equation (11) in Section 4.2 is described as "the key advantage" — an "NLoS-aware attention mechanism that explicitly models multi-path propagation" — but this mechanism was never mentioned or defined in the Methodology section (Section 3). The notation (o_s, φ, W_NLoS) is undefined. It is unclear whether this is part of the architecture or a post-hoc analysis tool. A component described as a "key advantage" should be fully specified in the method description.

5. **Incomplete baseline comparison in generalization experiments.** The zero-shot/few-shot generalization results (Section 4.5) compare SigMap against only LWLM and the SigMap w/o map ablation. CNN, SWiT, and OMP — all evaluated in the main tables — are dropped without explanation. Since generalization is a central claim, readers cannot assess whether the advantage is specific (beats LWLM) or general (beats all baselines). This is especially notable for SWiT, which is also an SSL-based method.

6. **Abstract claims "zero-shot" but experiments use few-shot fine-tuning.** The abstract states "strong zero-shot generalization in unseen environments," but Section 4.5 explicitly describes fine-tuning on "approximately 100 instances per scenario" (line 317), which is few-shot, not zero-shot. This framing mismatch between the abstract and the actual experimental protocol is misleading and should be corrected.

7. **No standard deviations reported despite multi-run experiments.** The paper states "All results are averaged over 5 independent runs" (line 239) but no tables report standard deviations or error bars. Given the variance typical of wireless localization (especially under NLoS), the reader cannot assess whether reported gaps between methods are statistically meaningful.

### Trivial
None.

## Nice-to-Haves
- Show a learning curve (localization error vs. number of labeled fine-tuning samples) to directly support the "parameter-efficient generalization" claim.
- Include an ablation of mask width w to demonstrate robustness to this hyperparameter.
- Add a random-masking baseline with the same mask ratio to isolate the benefit of periodicity awareness from the masking ratio.
- Discuss scalability of the GNN prompt generation to very large city models.
- Clarify the relationship between Equation 9 (multi-BS attention fusion, Section 3.5) and Equation 11 (NLoS-aware attention, Section 4.2).

## Removed Points
These points from the input review were excluded for the following reasons:

- **"Why CSI periodicity is qualitatively different from image spatial autocorrelation"** — This is a conceptual discussion question, not a specific weakness. The paper grounds its argument in the periodic structure of OFDM subcarriers and antenna arrays, a domain-specific property distinct from natural image statistics. The paper does not need to argue this point beyond its domain-specific motivation.
- **"Missing CrowdBERT and signal-guided MAE baselines from related work"** — Per guidelines, criticisms about omitted references are not included when evaluation setup compatibility cannot be verified by the reviewer.
- **"Scalability of GNN to large city models"** — A reasonable question but not a central weakness. Moved to Nice-to-Haves.
- **"GNN training for each new environment still requires labeled data"** — The paper acknowledges the few-shot setting (~100 samples), so this is not an omission; it is a correctly scoped claim.

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
1. Fully specify the cycle-adaptive masking algorithm: which dimensions of the CSI tensor the mask operates on, how d_final is computed from cross-correlation (which peak, what threshold), and what value(s) of w are used. Define grid-masking and strip-masking baselines.
2. Correct the data inconsistency (1.880 m vs. 1.580 m on WAIR-D) and report standard deviations for all main results.
3. Add a real-data experiment or, at minimum, explicitly acknowledge the simulation-only limitation.
4. Move the NLoS-aware attention mechanism to the Methodology section with full specification, or clarify its role explicitly.
5. Include all baselines (CNN, SWiT, OMP) in the generalization experiments or explain why they cannot be evaluated in that setting.
6. Correct "zero-shot" in the abstract to reflect the actual few-shot protocol.

## Score and Decision

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>