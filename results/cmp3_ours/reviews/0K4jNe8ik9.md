I have sufficient calibration data. Let me write the final review.

**Round 1 bracket: 3.0 – 4.0.** The paper is weaker than EEGPT (4.00) and DBGMS (4.00) due to structurally compromised evaluation, comparable to Invariant Spatiotemporal (3.00), and stronger than UniEEG (2.00). **Narrowing to: 3.0 – 3.5.** Final score: **3.5**.

---

## Summary

This paper proposes DGNet, a self-supervised framework for multi-band EEG representation learning applied to dementia classification (AD vs. CN). The core idea is to decompose EEG into five canonical frequency bands (δ, θ, α, β, γ) and apply independent SimCLR-style contrastive learning per band, followed by a frozen-encoder + MLP classifier. The method reports 92.90% accuracy on an 88-subject public dataset.

## Strengths

- **Neurophysiologically motivated design.** Decomposing EEG into its five canonical frequency bands and assigning independent encoders per band is well-grounded: the known spectral signatures of dementia (increased delta/theta power, decreased alpha/beta/gamma power) provide a clear rationale (Section 2.1). This is the paper's most defensible contribution.

- **Well-characterized dataset.** The 88-subject dataset (36 AD, 23 FTD, 29 CN) with detailed clinical metadata (MMSE scores, disease duration, recording protocol) is described transparently (Section 3.1). Using a publicly available dataset (Miltiadous et al., 2023b) is positive for reproducibility.

- **Appropriate evaluation protocol.** Leave-One-Subject-Out (LOSO) evaluation is correctly identified as the appropriate protocol for EEG data with high inter-subject variability, preventing subject-level data leakage at the evaluation stage (Section 3.4).

## Weaknesses

### Fatal
None.

### Major

- **Table 1 baseline comparisons are unreliable, undermining the SOTA claim.** Several well-known EEG models are reported at or below chance level for binary AD/CN classification: EEGNet (46%), Deep4Net (49%), EEGInception (39%), TIDNet (44%), FBCNet (48%), S-JEPA (50%) (Table 1, lines 156–170). Models that have been extensively validated on EEG benchmarks should not perform at chance on a two-class problem unless the implementation or hyperparameter configuration is incorrect. In contrast, prior work on this same dataset (Table 2) reports methods achieving 60–91%, with BI-MCGNN reaching 91.25%. Either the baselines were untuned by the authors (making the comparison staged) or the evaluation pipeline is incompatible. Either way, beating these broken baselines does not constitute evidence of superiority, and the paper's central claim of "significantly outperforming all comparison models" is not supported.

- **The "linear evaluation" uses a 3-layer MLP, not a linear probe.** The paper claims to follow the standard SSL linear evaluation protocol, but the classifier consists of three linear layers (512 → 256 → classes) with ReLU activations, batch normalization, and dropout (Section 2.1, "Downstream Task," lines 82–83). In standard SSL (Chen et al., 2020 SimCLR), linear evaluation uses a single linear layer on frozen features specifically to measure representation quality without adding nonlinear capacity. Using a 3-layer MLP conflates representation quality with classifier capacity, making the results uninterpretable as a measure of representation learning and invalidating comparisons with methods that use proper linear probes.

- **Loss function ambiguity.** Equation (1) (line 104) defines a loss that uses *only the hardest negative* (maxₙ over negative similarities), which is a triplet-like objective. Equation (2) (line 110) defines the standard NT-Xent loss that sums over *all* negatives. The paper states it uses SimCLR but never clarifies which loss is actually implemented. This is a critical underspecification — these are fundamentally different objectives and the method cannot be reproduced or properly evaluated without resolving this ambiguity.

- **Unclear whether SSL pretraining leaks subject information.** The paper describes a two-stage pipeline: SSL pretraining on unlabeled EEG data (Section 2) followed by LOSO linear evaluation (Section 3.4). It is never stated whether the SSL pretraining is nested inside each LOSO fold (trained only on the 87 training subjects) or performed once on all 88 subjects. If the latter — and the single description of pretraining followed by a single LOSO evaluation suggests a single pretrained model — then the held-out subject's unlabeled signal statistics have shaped the encoder's representations before the classifier is trained. While this does not leak labels, it provides the encoder with subject-specific distributional information that may inflate cross-subject generalization estimates.

### Minor

- **No variance or confidence intervals reported.** The proposed model's 92.90% accuracy is reported as a point estimate with no standard deviation across LOSO folds, despite other methods in Table 2 (e.g., BI-MCGNN at 91.25 ± 0.38) reporting variance. With only 65 subjects in the AD/CN comparison, the variance could be substantial.

- **No full-band baseline without frequency decomposition.** The ablation study (Table 3) does not include a model that processes the full broadband signal with the same total capacity but without band separation. This makes it impossible to determine whether the multi-band design or simply having more parameters drives the results.

- **The claimed SOTA is hedged to the point of being unverifiable.** The abstract states "state-of-the-art performance in multi-head approaches" (line 9). "Multi-head approaches" is not an established model class; this is essentially claiming SOTA in a class of one. The paper should state what it is actually SOTA *compared to* in the broader literature, with properly configured baselines.

- **No analysis of adaptive temperature evolution.** The adaptive temperature mechanism is a key claimed contribution, but the paper provides no analysis of how temperatures evolve during training, per-band loss curves, or sensitivity to the regularization strength β. The ablation table (Table 3) shows the gap between "Multi-head (5 heads)" (79.55%) and the full model (92.90%) is 13.35 percentage points; while intermediate ablations partially bridge this gap ("constant temperature" at 86.53%, "w/o regularization" at 90.64%), the mechanism's behavior is never examined directly.

- **No per-band contribution analysis.** The central premise is that different frequency bands carry different diagnostic information, yet there is no analysis of which bands contribute most or whether all five bands are needed.

### Trivial

- None.

## Nice-to-Haves

- Run the SSL pretraining nested inside each LOSO fold and report whether results change.
- Replace Table 1 with properly tuned baselines using the same LOSO protocol, or remove it and rely on Table 2 for comparison.
- Replace the MLP classifier with a genuine single-layer linear probe for the main evaluation, and relegate the MLP result to a secondary "full fine-tuning" row.
- Report per-fold results or standard deviations across LOSO folds for all metrics.
- Add a leave-one-band-out ablation and/or t-SNE/UMAP visualization of per-band embeddings to validate the multi-band design hypothesis.
- Analyze how adaptive temperatures evolve during training and how results depend on β.

## Removed Points

These points were flagged by the harsh reviewer but are removed with brief justification:

1. **"The paper does not discuss whether segments from the same subject are used as negatives"** — This is speculative. The paper does not discuss this, but neither does most SSL work on EEG. Not a specific identifiable problem.
2. **"Abstract is hyperbolically phrased ('tsunami')"** — This is a stylistic judgment about framing, not a technical weakness. Removed per formatting/style rule.
3. **"The gap between Multi-head (5 heads) and full model is implausible"** — The harsh reviewer overstated this. The ablation table shows intermediate steps (constant temperature at 86.53%, w/o regularization at 90.64%), so the gap is not a direct jump. However, the point about missing analysis of temperature evolution is retained as Minor.
4. **"Several models perform at or below the 50% chance baseline"** — This is kept as a Major weakness (see above), not removed. It is a verified concern.
5. **Criticisms framed as questions rather than identified problems** (e.g., "could the metric be measuring a proxy?") — Removed per filtering discipline.
6. **Related work concerns about missing citations** — Removed per rules (cannot verify external knowledge).

## Novel Insights

None beyond the paper's own contributions. The reviews surface the same structural evaluation problems without adding novel conceptual insights about the method itself.

## Suggestions

1. **Restructure the evaluation pipeline.** Train SSL models and baselines under identical, properly controlled conditions. If Table 1 baselines are the authors' implementations, re-tune them for this task. If they were cited from other papers, specify this clearly and treat Table 2 as the primary comparison.
2. **Use a genuine linear probe** (single linear layer on frozen representations) for the main evaluation. Report the 3-layer MLP result as a secondary "frozen features + nonlinear classifier" baseline.
3. **Clarify the loss function.** State explicitly which loss (Eq 1 or Eq 2) is used, or explain how they relate. If Eq 1 is used, acknowledge that it differs from standard SimCLR.
4. **Document the SSL pretraining data boundary.** Specify whether pretraining is nested inside each LOSO fold or performed once on all subjects.
5. **Report variance.** Provide standard deviations or per-fold results for all reported metrics.
6. **Add a full-band decomposition ablation** where the same architecture processes the broadband signal without frequency separation, to isolate the benefit of the multi-band design.

## Score and Decision

**Calibration anchors used:**

| Path | Avg Human Score | Round | Comparison to this paper |
|------|----------------|-------|------------------------|
| deepreview_13k_calibration/6uReXuDWrw.md (UniEEG) | 2.00 | R1 | Weaker writing, less motivation; our paper is better |
| deepreview_13k_calibration/TkbjqexD8w.md (Invariant Spatiotemporal) | 3.00 | R1 | Similar evaluation concerns; comparable quality |
| deepreview_13k_calibration/YKfJFTiRz8.md (Pre-Training GCL) | 5.00 | R1 | Stronger evaluation, more comprehensive; our paper is weaker |
| deepreview_13k_calibration/V5Zn0VVvBE.md (Learning Robust EEG) | 5.40 | R1 | Stronger comprehensive evaluation; our paper is weaker |
| deepreview_13k_calibration/wJ6Bx1IYrQ.md (EEGPT) | 4.00 | R2 | More ambitious, more data, but also evaluation concerns; our paper is weaker |
| deepreview_13k_calibration/70lFRMBygi.md (DBGMS) | 4.00 | R2 | Stronger evaluation with two datasets; our paper is weaker |
| deepreview_13k_calibration/dhLIno8FmH.md (Decoding Natural Images) | 6.75 | R1 | Significantly stronger evaluation and analysis; our paper is much weaker |

**Round 1 bracket:** 3.0 – 4.0  
**Final score rationale:** The paper has a well-motivated neurophysiological architecture and transparent dataset description, but the evaluation is structurally compromised in ways that prevent accepting its core claims. Table 1 baselines at/below chance level indicate a broken comparison framework, the "linear evaluation" uses a 3-layer MLP rather than a true linear probe, the loss function is underspecified between two different objectives, and it is unclear whether SSL pretraining leaks subject-level information. These are not fixable by minor revisions — they require re-running the entire evaluation pipeline. The paper compares unfavorably to EEG foundation model papers scoring 4.00–5.40 that at minimum have properly configured baselines and comprehensive evaluation, and is comparable to Invariant Spatiotemporal (3.00) in its level of methodological issues.

MY FINAL SCORE: <score>3.5</score>
MY FINAL DECISION: <decision>Reject</decision>