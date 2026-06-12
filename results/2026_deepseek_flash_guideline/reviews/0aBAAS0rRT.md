Now I have all the information I need. Let me produce the final review.

## Calibration Analysis

**Bracket assessment:**

Based on my reading of anchor papers:
- **1.0–1.5 range**: Completely irrelevant or non-rigorous work. SigMap is clearly above this range.
- **3.0–3.3 range**: ECG foundation model (3.33), wearable sensing FM (3.00). These have thin methodology or baseline issues. SigMap has stronger method novelty and cleaner ablations.
- **4.0–5.25 range**: DASFormer (5.25, self-supervised SSL for signal processing), WiMTR (4.00, CSI-based WiFi tasks), GenNet (4.25, wireless simulation). SigMap fits here — stronger method novelty than DASFormer (cycle-adaptive masking is genuinely creative), but hurt by numerical inconsistencies.
- **6.0–7.0 range**: Differentiable Wireless Simulation (7.00). Cleaner presentation, stronger evaluation methodology. SigMap is not at this level due to fixable but present flaws.
- **8.0+ range**: Exceptional papers. SigMap not in this category.

**Narrowest plausible range: 4.0–5.5. Final score anchored at 5.0.** The paper has genuine contributions and well-designed experiments, but the numerical inconsistency and missing method description prevent acceptance as-is.

---

Now the final consolidated review:

## Summary

SigMap proposes a wireless localization foundation model with two innovations: (1) **cycle-adaptive masked modeling** that detects periodic patterns in CSI and generates masks that prevent the model from exploiting periodic shortcuts during self-supervised pre-training, and (2) **geographic prompt tuning** that encodes 3D building maps via GNNs into soft prompt tokens, enabling parameter-efficient fine-tuning (0.7% of parameters updated) without modifying the pre-trained backbone. Experiments on DeepMIMO and WAIR-D datasets show strong improvements over baselines (OMP, CNN, SWiT, LWLM) in both single-BS and multi-BS settings, with cross-scenario generalization gains of 44–53%.

## Strengths

- **Cycle-adaptive masking contribution is isolated by controlled ablation (Table 3).** Adaptive masking achieves the best MAE (0.673 m vs. 0.770 m and 0.753 m) and CDF@1m (84.5% vs. 80.3% and 75.3%) compared to grid-masking and strip-masking under identical conditions. This directly validates that disrupting periodic shortcuts improves representation quality.

- **"Map-as-prompt" contribution is demonstrated through progressive ablation (Table 4).** A clean monotonic improvement from no-map (2.275 m MAE) to 2-D birdview (1.692 m) to full 3-D mesh (1.564 m) in single-BS localization confirms that the geographic prompt mechanism drives accuracy gains, not confounding factors.

- **Cross-scenario generalization gains substantially exceed in-distribution gains.** On unseen DeepMIMO O2, SigMap (w/ map) achieves 1.026 m MAE vs. LWLM's 2.213 m (53.6% improvement); on unseen WAIR-D Scenario-2, 1.880 m vs. 3.375 m (44.3% improvement). These margins are larger than the 34.4% improvement on the in-distribution task, supporting the paper's cross-scenario generalization claims.

- **Parameter efficiency is quantified end-to-end (Table 5).** Fine-tuning updates 0.085M parameters (0.7% of total) and completes in 30 minutes; inference runs at 0.83 ms/sample. These concrete numbers demonstrate practical deployability.

- **Consistent improvements across single-BS and multi-BS configurations.** SigMap (w/ map) achieves 1.564 m MAE (single-BS) and 0.673 m MAE (multi-BS), outperforming its own no-map variant and all baselines in both settings, showing robustness to the number of base stations.

## Weaknesses

### Major

1. **Numerical inconsistency between table and text (WAIR-D MAE).** The generalization table (Section 4.5) reports SigMap (w/ map) at **1.880 m** MAE on WAIR-D Scenario-2. However, the running text (line 340) states "1.580 m on WAIR-D Scenario-2." The 44.3% improvement margin cited in the same sentence is consistent with 1.880 m ((3.375−1.880)/3.375 ≈ 44.3%) but not with 1.580 m ((3.375−1.580)/3.375 ≈ 53.2%). This is a factual contradiction in the experimental record — a reviewer cannot determine which number is correct. While the error is fixable, it erodes confidence in the reported results.

2. **"NLoS-aware attention mechanism" credited as the key advantage but described only in the experiments section, not in the methodology.** Section 4.2 claims "The key advantage stems from our NLoS-aware attention mechanism that explicitly models multi-path propagation" and presents Equation 11. However, Section 3 (Methodology) describes only cycle-adaptive masking and geographic prompt tuning — this NLoS-aware mechanism is never defined, explained, or placed within the architecture. It is presented for the first time in the experiments section without any specification of where it fits in the forward pass, whether it is part of the backbone or an additional component, or whether it is used during pre-training or only fine-tuning. This makes it impossible to evaluate what is actually driving the reported gains.

### Minor

3. **"Zero-shot" framing mismatch with actual few-shot protocol.** The abstract and contributions claim "strong zero-shot generalization in unseen environments." However, Section 4.5 describes a protocol where "only the downstream task heads are fine-tuned using limited target samples (approximately 100 instances per scenario)" and correctly characterizes this as a "few-shot learning setup." Using 100 labeled instances is not zero-shot. Few-shot generalization is still valuable, but the headline claim should match the evaluation.

4. **No measures of uncertainty reported.** Results are "averaged over 5 independent runs" but no standard deviations, confidence intervals, or error bars are provided. Some comparisons show tight margins (e.g., multi-BS: SigMap w/ map at 0.673 m vs. SigMap w/o map at 0.789 m — a 0.116 m difference). Without variance, readers cannot assess whether these gaps are statistically significant. This is especially important given the single simulated dataset used for main results.

5. **Baseline set is thin.** The comparison includes only two learned SSL/transformer baselines (SWiT and LWLM) alongside a classical compressed-sensing method (OMP) and a simple supervised CNN. The related work section cites CrowdBERT, signal-guided MAE, and WirelessGPT as SSL/foundation-model approaches for wireless, but none are included as baselines. While some may not be directly applicable, the absence limits support for "state-of-the-art" claims.

6. **Strip-masking RMSE anomaly not discussed (Table 3).** Strip-masking achieves RMSE of 0.972 m, which is *better* than adaptive masking's 1.099 m, even though adaptive masking has better MAE (0.673 vs. 0.753) and CDF@1m (84.5% vs. 75.3%). The paper claims adaptive masking "yields the best trade-off" but does not explain why strip masking produces lower RMSE despite worse MAE and CDF. This may be interesting (suggesting adaptive masking reduces large errors at the cost of more medium errors) but requires explanation.

7. **Main results rely on a single simulated scenario.** Tables 1–3 all use DeepMIMO O1_3p5 (a simulated urban scenario). The generalization section adds DeepMIMO O2 (also simulated) and WAIR-D (real-world), which strengthens the paper, but the core "state-of-the-art" claims rest primarily on one simulated environment. This should be explicitly acknowledged as a limitation.

### Trivial

8. **Parameter efficiency percentage inconsistency.** The generalization section (line 340) states "updating only 0.4% of parameters," while the parameter efficiency section (line 352) states "only 0.7% of the total parameters" — the latter being consistent with Table 5 (0.085M/11.815M ≈ 0.72%). These should be reconciled.

9. **WAIR-D sampling ambiguity.** The paper states "approximately 100 instances per scenario" — it is unclear whether this means 100 samples total across all 100 cities, or 100 per city (totaling 10,000 samples). This matters for interpreting the "few-shot" claim.

10. **Interpretability claim unsupported.** The paper claims prompts enable "interpretable fusion of environmental constraints" (line 42) but provides no analysis or visualization of how the geographic prompt influences attention or predictions.

## Nice-to-Haves

- Include at least one additional SSL-based localization baseline (e.g., the signal-guided MAE or CrowdBERT cited in related work). If these methods are not directly applicable, explain why.
- Clarify the cycle detection mechanism: specify which cross-correlation is computed (auto-correlation of CSI amplitude? across which dimensions?), how periodicities are identified, and whether this is done per-sample or dataset-wide.
- Consider ablating over prompt dimensionality or number of prompt tokens to address the concern that a single pooled token may lose discriminative spatial information.
- Report error bars throughout and discuss the strip-masking RMSE anomaly.

## Removed Points

- **"Cycle detection method is underspecified"** (moved from Major): The paper mentions "cross-correlation analysis" without full specification. However, the core mechanism (Equation 6 defining the mask pattern given a detected periodicity) is described, and detailed cross-correlation computation is standard practice that can be deferred to an appendix (which is stripped in this version). This is a reproducibility concern but not a structural flaw.
- **"Geographic prompt tuning compression concern"** (moved from Minor): The concern that a single prompt token from global mean pooling may lose discriminative information is speculative — the paper's strong empirical results (60.5% CDF@1m with 3-D map vs. 31.0% without) suggest the representation is effective as-is. This is a reasonable extension direction but not a demonstrated weakness.
- **Strength Finder — generic strengths removed**: Several strengths flagged by the Strength Finder ("the research problem is important," "the paper is well-written") are generic and not specific to this paper's content. Removed accordingly.
- **"Missing related works"**: Removed per policy — I cannot confirm which works exist beyond the paper.
- **"Missing appendix details"**: Removed per policy — the appendix is stripped due to parser constraints.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Fix the numerical inconsistency.** The WAIR-D MAE (1.880 m in the table vs. 1.580 m in the text) must be reconciled. Verify against raw experimental records and correct whichever is wrong. Similarly, reconcile the 0.4% vs. 0.7% parameter-efficiency claim.

2. **Describe the NLoS-aware attention mechanism (Eq. 11) in Section 3 (Methodology).** Clarify where it fits in the architecture, whether it is a modification of the self-attention mechanism itself or a separate module, and whether it operates during pre-training, fine-tuning, or both. Without this, the reader cannot evaluate the "key advantage" claimed in the experiments.

3. **Fix the zero-shot/few-shot framing.** Replace "zero-shot" with "few-shot" (or a more precise term like "domain generalization with limited fine-tuning") throughout the abstract, contributions, and introduction to match the actual experimental protocol.

4. **Add standard deviations** to all tables reporting results over 5 runs.

5. **Discuss the strip-masking RMSE anomaly** in the ablation analysis. If this is an interesting signal about error distribution, it should be explained rather than ignored.

## Score and Decision

**Round 1 bracket: 4.0–5.5.** The paper lacks fatal flaws — the methodology is coherent and the empirical evidence (aside from the numerical inconsistency) supports the core claims. However, the numerical inconsistency, missing method description, and framing mismatch prevent acceptance at ICLR as-is.

**Anchor comparison:**
- ECG Foundation Model (3.33 avg): Similar "application of SSL to signals" framing, but SigMap has stronger ablations and cleaner methodology. SigMap is stronger.
- Wearable Sensing FM (3.00 avg): Thin baseline comparison. SigMap has better empirical validation. SigMap is stronger.
- DASFormer (5.25 avg): Self-supervised pretraining for signal processing with similar evaluation structure. DASFormer lacked strong baselines and had unclear novelty. SigMap has clearer method novelty but the numerical inconsistency is a liability. Roughly comparable; SigMap slightly lower due to the numerical error.
- Differentiable Wireless Simulation (7.00 avg): Cleaner evaluation and presentation. SigMap is weaker.
- WiMTR (4.00 avg): WiFi CSI for 3D meshes. WiMTR had dataset contribution but limited method novelty. SigMap has stronger methodology.

**Final score: 5.0.** The paper makes genuine contributions (cycle-adaptive masking is well-motivated and validated; the geographic prompt framework is cleanly designed) with strong generalization results. However, the numerical inconsistency (1.880 vs. 1.580), the missing description of what is claimed as the "key advantage," and the zero-shot/few-shot framing mismatch collectively prevent acceptance in the current form. These issues are fixable, and a revised version addressing them could be competitive.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>