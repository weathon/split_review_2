I now have a clear picture of the paper and all calibration anchors. Let me produce the final consolidated review.

## Summary

This paper proposes SigMap, a two-stage foundation model for wireless localization. The first stage pre-trains a Transformer backbone on CSI data using a cycle-adaptive masking strategy designed to prevent shortcut learning from periodic signal patterns. The second stage fine-tunes via "map-as-prompt": 3D geographic information is encoded through a GNN into soft prompt tokens that are prepended to the frozen backbone's input sequence. Experiments on simulated ray-tracing datasets (DeepMIMO, WAIR-D) show consistent improvements over baselines across single-BS, multi-BS, in-distribution, and cross-domain settings, with only 0.7% of parameters updated during fine-tuning.

## Strengths

- **Well-motivated problem framing (Section 1.1).** The paper identifies two genuine gaps in existing SSL-based wireless localization work: generic masking lets models exploit periodic shortcuts in CSI rather than learning meaningful representations, and prior map integration is shallow. These are clearly articulated and provide a solid rationale for the proposed design.

- **Clean and interpretable architecture.** The two-stage pipeline (pre-train with cycle-adaptive masking → prompt-based fine-tuning with GNN-encoded map) is structurally coherent. The geographic prompt generation (Algorithm 1, Figure 4) is clearly described and easy to follow, and the multi-BS attention fusion mechanism (Section 3.5, Eqs. 9-10) is a sensible design.

- **Consistent empirical advantage across settings.** The method outperforms all baselines in every configuration reported — single-BS, multi-BS, in-distribution, and cross-domain (Tables 1, 2, 4.5). Margins are often large (e.g., 34.4% MAE improvement over LWLM in single-BS NLoS; 53.2% on DeepMIMO O2).

- **Parameter efficiency well-demonstrated.** Table 5 shows only 0.085M trainable parameters (0.7% of total) during fine-tuning, with 30 min total fine-tuning time for 1000 epochs, making the approach practically appealing for resource-constrained deployment.

## Weaknesses

### Major

1. **A key architectural component — the "NLoS-aware attention mechanism" (Eq. 11) — is introduced for the first time in the experimental results section without definition.** In Section 4.2 (line 247–251), the paper attributes SigMap's single-BS NLoS performance to Eq. 11, stated as "the key advantage." The symbols φ, o_s, and W_NLoS are never defined anywhere in the paper. This mechanism was not described in the methodology (Section 3); the attention in Section 3.5 (Eqs. 9-10) is a different standard scaled dot-product multi-BS fusion. Without knowing what this component is, where it resides in the architecture, or whether it is used only for single-BS or also for multi-BS, the paper's central experimental claim is uninterpretable — the reader cannot tell what model actually produced the reported results.

2. **The abstract and contributions list claim "strong zero-shot generalization" (lines 9, 43), but the generalization experiments use few-shot fine-tuning.** Section 4.5 (line 317) states: "only the downstream task heads are fine-tuned using limited target samples (approximately 100 instances per scenario)." This is few-shot, not zero-shot. The experiments show interesting few-shot transfer, but the headline claim is factually inconsistent with the evaluation protocol and should be corrected.

3. **The cycle-adaptive masking strategy — the paper's first claimed innovation — is critically underspecified.** The method is described as computing "row-wise cross-correlation" (line 41) and generating masks via Eq. 6 (M_cycle[i,j]=0 if |j-(j0+i·d_final)|≤w). The paper never specifies: what is the cross-correlation computed between (rows of what tensor? which dimensions?)? How is d_final extracted (peak detection? FFT? autocorrelation)? How is j_0 chosen? How does w scale relative to input dimensions or signal properties? What happens when no clear periodicity exists? A reader cannot implement, evaluate, or build on this mechanism. Some details may reside in the parser-stripped appendix, but a core contribution of this nature must be reproducible from the main text.

### Minor

4. **All experiments are on simulated data (DeepMIMO and WAIR-D, both ray-tracing).** The paper frames its contribution in terms of real-world 5G/6G applications and claims "practical deployability" (line 227) without acknowledging the simulation-only limitation or discussing which aspects may not transfer to real hardware, noise, calibration errors, or NLoS effects that simulations capture imperfectly. Adding a real-world dataset or a forthright limitations paragraph would substantiate the claims.

5. **The paper does not specify whether the self-supervised baselines (LWLM, SWiT) were pre-trained on the same DeepMIMO O1_3p5 data used for SigMap's pre-training.** If SigMap benefits from in-distribution pre-training while baselines do not, the claimed state-of-the-art advantage would be overstated. This should be clarified.

6. **No standard deviations or confidence intervals are reported in any results table**, despite "5 independent runs" (line 239). The ablation in Table 3 shows modest differences (e.g., adaptive masking 0.673 MAE vs. strip masking 0.753 MAE — a ~10% gap); without variance estimates, significance cannot be assessed. The mention of "near-overlapping error bars" (line 301) suggests variance estimates exist but were withheld.

7. **In the masking ablation (Table 3), adaptive masking achieves better MAE (0.673) and CDF@1m (84.5%) than strip masking (0.753, 75.3%), but worse RMSE (1.099 vs. 0.972).** The paper claims adaptive masking yields "the best trade-off" without remarking on this RMSE reversal, which complicates the claim of uniform superiority.

8. **The generalization experiments (Section 4.5) compare only against LWLM, not against SWiT, CNN, or OMP.** This narrower comparison limits the scope of the generalization claims relative to the main experiments.

### Trivial

None.

## Nice-to-Haves

- Provide pseudocode for the cycle-adaptive masking algorithm specifying the cross-correlation computation, periodicity detection method, and mask generation thresholds.
- Report standard deviations in all tables and at minimum discuss the RMSE anomaly in the masking ablation.
- Add a limitations paragraph acknowledging the simulation-only scope.

## Removed Points

**These points are flagged to be removed; treat them with caution:**

- *"Backbone architecture details (number of layers, hidden dimension, heads) not specified."* These may exist in the parser-stripped appendix; not a valid complaint on the main text alone.
- *"Pre-training data size and composition not specified."* May also be in the appendix.
- *"The paper lacks statistical significance testing."* Already covered more precisely by the "no std deviations" weakness above; the sharpened version is kept.
- *"Comparison with OMP and CNN is low-value."* This is a subjective judgment about baseline choice rather than a verifiable weakness. The comparison is standard for the field and informative about the relative advantage over both learned and non-learned methods.
- *"The geographic prompt generation is a straightforward application of GNNs + Delaunay."* This is a subjective assessment of degree of novelty, not a specific identified problem. The paper presents it as an application contribution and evaluates it effectively (Table 4).
- *"36-hour pre-training time not contextualized."* This is a minor point that the paper partially addresses by reporting fine-tuning efficiency; pre-training cost is typical for foundation models.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Integrate the NLoS-aware attention mechanism (Eq. 11) into Section 3 (Methodology)** with full definitions of φ, o_s, W_NLoS, and a clear statement of its architectural role (is it part of the backbone? A separate head? Used for single-BS only or also multi-BS?).

2. **Replace all instances of "zero-shot" with "few-shot" or "label-efficient"** to match the experimental design. The few-shot results (100 samples per scenario) are interesting on their own and do not need inflated framing.

3. **Fully specify the cycle-adaptive masking algorithm** in the main text: state the exact cross-correlation computation (between which tensor dimensions), the method for extracting d_final (peak detection in the cross-correlation sequence), the selection of j_0, and the scaling of w. If the algorithm is simple, this requires only a few lines; if complex, the details are essential for reproducibility.

4. **Report standard deviations** in all results tables, especially for the masking ablation where differences are modest.

5. **Clarify the pre-training protocol for all baselines** in the experimental setup.

6. **Add a limitations paragraph** acknowledging the simulation-only scope and discussing which results may not transfer to real hardware.

## Score and Decision

**Calibration summary and anchoring:**

Across two rounds, the most relevant calibration anchors are:

| Anchor | Avg Score | Domain | Itemized | How it compares to SigMap |
|---|---|---|---|---|
| Wi-GATr (9TClCDZXeh.md) | 7.00 / Accept | Wireless simulation + geometric transformers | Yes | Accepted. Stronger real-world validation (35% error reduction on real data). SigMap lacks real-world experiments. Wi-GATr's lowest-favorability weakness (-2.85, "novelty unclear") was more severe than SigMap's worst, but Wi-GATr compensated with real-world results and full architectural disclosure. |
| RFMamba (lG9fjBLb6d.md) | 6.50 / Accept | RF-based human perception with SSM | Yes | Accepted. Real-world experiments on a custom radar dataset. Weaknesses about missing details (favorability -1.58) less severe than SigMap's undefined NLoS-attention. Stronger empirical validation (real data). |
| RelCon (k2uUeLCrQq.md) | 6.75 / Accept | Motion foundation model (SSL) | Yes | Accepted. Trained on 1B segments from 87K participants — orders of magnitude larger pretraining than SigMap. Weaknesses about evaluation fairness (-1.97) but strong large-scale empirical support. |
| EM-GANSim (29JDZxRgPZ.md) | 6.00 / Reject | Wireless EM simulation with GANs | Yes | Rejected despite 6.00 avg. Weaknesses about missing architectural details and unclear 3D capability. Similar to SigMap in having specification gaps, but SigMap's NLoS-attention omission is more severe for the core claim. |
| FECCT (7KDuQPrAF3.md) | 6.25 / Accept | Foundation model for error correction codes | Yes | Accepted. Weaknesses about limited code length and missing comparisons. Stronger theoretical framing and architectural novelty. |
| Freq-Aware MAE (t5LXyWbs5p.md) | 5.50 / Reject | Frequency-domain MAE for biosignals | Yes | Rejected. Weaknesses about lack of novelty (favorability -3.00) and inadequate related-work discussion. SigMap's weaknesses are about specification rather than novelty. |

**Round-1 bracket:** After initial calibration, I identified the plausible range as 4.0–6.0 based on the closest anchors: accepted wireless papers (Wi-GATr 7.00, RFMamba 6.50) have stronger validation, while the rejected EM-GANSim (6.00) has similar specification problems but SigMap's NLoS-attention omission is a more severe architectural gap.

**Round-2 narrowing:** Comparing SigMap's lowest-favorability items against the anchors':
- SigMap's worst items: NLoS-attention in results (favorability **0.12** — very low for a core mechanism), zero-shot overclaim (**-0.96**), simulation-only (**-0.95**)
- Wi-GATr's worst items: novelty unclear (**-2.85**), missing comparisons (**-1.77**, **-1.27**) — worse raw favorability but compensated by real-world validation
- EM-GANSim's worst: unclear 3D treatment (**-1.09**), missing dataset details (**-1.37**) — similar severity but less central to the main claim

SigMap's NLoS-attention issue (favorability 0.12) is distinctively harmful because it renders the primary experimental claim unverifiable. The zero-shot overclaim (favorability -0.96) is a clear factual mismatch. Together, these push the paper below the acceptance threshold despite its genuine strengths.

**Final score:** 5.0. The paper has a solid motivation, coherent architecture, and consistent empirical results. However, (1) the NLoS-aware attention mechanism that explains the main single-BS results is introduced in the results section with undefined symbols and no architectural context — the reader cannot verify what model was evaluated; (2) the core cycle-adaptive masking contribution is underspecified; and (3) the "zero-shot" headline claim is factually inconsistent with the few-shot protocol. These are presentation/specification problems rather than fundamental invalidity, but in their current form they prevent proper evaluation of the claimed contributions. A thorough revision addressing these three issues could produce a solid submission.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>