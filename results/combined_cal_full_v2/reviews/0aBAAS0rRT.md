Now I'll produce the final consolidated review.

## Summary

This paper presents SigMap, a multimodal foundation model for wireless localization that combines (1) cycle-adaptive masked modeling, which detects periodicities in CSI to prevent shortcut learning during masked reconstruction, and (2) a map-as-prompt framework that encodes 3D geographic information via GCNs into lightweight soft prompts for cross-scenario adaptation. The model follows a pre-train-then-fine-tune paradigm and achieves strong localization accuracy on simulated ray-tracing datasets with very few fine-tuning parameters (0.085M).

## Strengths

- **Cycle-adaptive masking is a conceptually novel and well-motivated idea.** The observation that periodic structures in CSI can serve as shortcuts for standard MAE-style reconstruction (Section 3.3) is non-trivial. Dynamically disrupting these periodic patterns during pre-training is a genuine insight for the wireless domain that other SSL-based localization methods have not addressed. The ablation (Table 3) confirms that adaptive masking improves MAE over fixed grid/strip masking (0.673 vs. 0.770/0.753).

- **The map-prompt mechanism is cleanly designed and parameter-efficient.** Encoding 3D building geometry via Delaunay triangulation → GCN → prompt projection (Algorithm 1, Figure 4) follows a well-defined pipeline. The parameter efficiency claim is well-supported — Table 5 shows only 0.085M trainable parameters (0.7% of total) during fine-tuning, requiring merely 30 minutes for 1000 epochs. This is genuinely lightweight and practically relevant.

- **Strong results on simulated benchmarks.** SigMap consistently outperforms all baselines (OMP, CNN, SWiT, LWLM) on both single-BS and multi-BS localization on DeepMIMO, with particularly large gains in the challenging single-BS NLoS setting (1.564 m MAE vs. 2.382 m for LWLM, Table 1). The generalization experiments (Table 4.5) show meaningful improvements on unseen simulated scenarios.

## Weaknesses

### Major

- **"Zero-shot generalization" is claimed but only few-shot is evaluated.** The abstract and Section 1.2 (Contributions) state the model exhibits "strong zero-shot generalization in unseen environments." However, Section 4.5 explicitly describes a few-shot setup: "only the downstream task heads are fine-tuned using limited target samples (approximately 100 instances per scenario), while the self-supervised backbone remains frozen. This few-shot learning setup…" Zero-shot would require no fine-tuning on the target environment whatsoever. The paper's own experiment section correctly calls this "few-shot," creating a direct contradiction with the front-end framing. This overclaim is fixable by reframing, but as written it is misleading and undermines reviewer trust.

- **Insufficient baselines to substantiate the "state-of-the-art" claim.** The related work (Section 1, lines 26–27) explicitly cites **CrowdBERT** (Han et al., 2024) and **signal-guided masked autoencoders** (Wang et al., 2025) as SSL-based localization methods closest in spirit to this work. Neither appears in the experiments. The comparison set (OMP, CNN, SWiT, LWLM) contains only two contemporary SSL methods. Claiming SOTA across the field without comparing against the most directly related SSL-based localization baselines is a significant experimental gap.

- **The cycle-adaptive masking's periodicity detection is under-specified.** Equation (6) defines the mask pattern M_cycle[i, j] using d_final — "the detected periodicity shift." The text (line 133) states only that patterns are computed "using cross-correlation analysis." No algorithm, cross-correlation function, decision rule, or threshold is provided for how d_final is derived from the CSI data. Without this, the paper's first claimed contribution is not reproducible. This is a methodological gap, not just a presentation issue — the entire masking strategy hinges on this detection step.

- **All experiments use simulated ray-tracing data; no real-world validation.** The evaluation relies entirely on DeepMIMO and WAIR-D (ray-tracing simulation). The paper claims "practical deployability" (Section 3.5, line 227) for real-world applications (autonomous driving, smart manufacturing) but provides no evidence that the approach transfers to real hardware with measurement noise, hardware impairments, and dynamic obstacles. Ray-tracing simulations cannot capture these factors, and the sim-to-real gap is unaddressed. At minimum, this limitation should be prominently acknowledged rather than omitted.

### Minor

- **Numerical inconsistency in results.** Table 4.5 shows WAIR-D Scenario-2 MAE as **1.880 m**, but the running text (line 340) states **1.580 m**. The 44.3% improvement over LWLM (3.375 m) is consistent with 1.880, confirming the text value is erroneous. While fixable, this erodes confidence in the reported numbers.

- **RMSE discrepancy in masking ablation unexplained.** Table 3 shows adaptive masking achieves lower MAE (0.673 vs. 0.753) but higher RMSE (1.099 vs. 0.972) than strip-masking. The paper notes the numbers but offers no explanation. A method that reduces typical error while increasing extreme outliers has different reliability characteristics that warrant discussion for a localization application.

- **Unclear fine-tuning protocol for LWLM on WAIR-D.** The generalization experiments (Section 4.5) state "approximately 100 instances per scenario" for fine-tuning SIGMAP, but it is not specified whether LWLM received the same 100 labeled samples or was trained on more data. This affects the fairness of the comparison.

- **No standard deviations in main result tables.** Results are "averaged over 5 independent runs" (Section 4.1), but Tables 1, 2, 3, and 4.5 lack standard deviations or confidence intervals. Only the map ablation figure mentions error bars. This makes it difficult to assess whether reported improvements are statistically significant.

### Trivial

None.

## Nice-to-Haves

- Real-world validation on any modest measurement campaign (even a single indoor/outdoor scenario with commercial hardware) would substantially strengthen the practical claims. If infeasible, a dedicated limitations paragraph discussing the sim-to-real gap would be appropriate.
- Explanation of why 3D vs. 2D map input yields only ~8% MAE improvement (Table 4) — is the 3D mesh complexity justified, or could a 2D+height representation suffice?
- An analysis of where adaptive masking's RMSE increase comes from (e.g., are certain CSI patterns or locations particularly prone to outlier errors?).

## Removed Points

- *Criticism about Section 2.2's claim that the model "learns implicitly" to decompose LoS/NLoS without evidence* — Removed because the paper frames this as an implicit capability, which is standard for learned representations; no specific experiment testing this decomposition is standard practice.
- *Delaunay triangulation mesh quality concern* — Removed as a generic concern applicable to any graph construction method, not specific enough to this implementation.
- *Question about whether 2D vs 3D map benefit justifies complexity* — Removed because the paper acknowledges this finding and discusses it as a positive observation about robustness; the criticism elevates a discussion point to a weakness.
- *Conclusion not acknowledging limitations* — Removed because this is subsumed by the zero-shot overclaim and simulated-only evaluation weaknesses above.

## Novel Insights

None beyond the paper's own contributions. The main insight from the review process is the identification of the zero-shot/few-shot framing contradiction, which is a genuine oversight that the authors can address straightforwardly.

## Suggestions

1. **Reframe "zero-shot" to "few-shot cross-scenario adaptation"** throughout the paper to accurately reflect what is evaluated.
2. **Specify the periodicity detection algorithm** — provide the cross-correlation function, thresholding rule, and dominant period identification procedure.
3. **Add CrowdBERT and Wang et al. 2025 as baselines**, or if their code is unavailable, explicitly acknowledge this limitation.
4. **Correct the numerical error** (1.580 → 1.880 for WAIR-D Scenario-2 MAE in the text).
5. **Explain the RMSE increase from adaptive masking** and discuss implications for localization reliability.
6. **Add standard deviations to all main result tables.**
7. **Clarify the LWLM fine-tuning protocol** on WAIR-D.

## Score and Decision

**Calibration report:**

| Anchor | Avg Score | Round | Itemized | Comparison to this paper |
|--------|-----------|-------|----------|--------------------------|
| Wi-GATr (wireless simulation with geometric transformers) | 7.00 | 1,2 | Yes | Stronger evidence base (real-world validation, clearer framing); comparable novelty but SigMap has more ML innovation |
| RFMamba (RF-based human perception with SSM) | 6.50 | 1,2 | Yes | First-to-apply novelty, real-world validation; SigMap has stronger claimed contributions but weaker evidence |
| EM-GANSim (EM simulation with GANs) | 6.00 | 1,2 | Yes | Rejected despite 6.00; missing SOTA comparisons similar to SigMap's missing baselines |
| Foundation Model for ECC | 6.25 | 2 | Yes | Similar ambition-to-evidence gap; "foundation model" framing questioned like SigMap's zero-shot claim |
| RedMotion (motion prediction) | 5.33 | 1,3 | No | SSL pre-training for trajectory tasks; comparable score band |
| DASFormer (self-supervised earthquake monitoring) | 5.25 | 2 | No | SSL pre-training for signal data; similar approach but different domain |

**Weighted-item comparison:** My draft's most negative weakness is "missing baselines" (weight -1.12), comparable to EM-GANSim's missing SOTA comparison (-2.50). The zero-shot claim (weight +0.52) is treated by the model as a mild concern rather than a severe flaw, consistent with it being a fixable framing issue. The simulated-only evaluation (weight -0.09) is nearly neutral. My strengths (weights 7.55–10.62) are competitive with the anchors'. The paper's core novel ideas (cycle-adaptive masking, map prompts) are stronger than Wi-GATr's "applying an existing architecture" and RFMamba's "first to apply SSM" — but the evidence is substantially weaker (no real validation, under-specified algorithm, missing baselines, overclaiming).

**Final placement:** Round 1 bracket = 5.5–7.5. Round 2 narrowed to 5.0–6.0 based on comparison with Wi-GATr (7.00, stronger evidence), RFMamba (6.50, real validation), and EM-GANSim (6.00, rejected with similar baseline gaps). The paper sits below 6.0 because the zero-shot overclaim and missing baselines are significant enough to prevent acceptance, but above 4.0 because the core technical ideas are genuinely novel and the simulated results are strong. Score 5.5 reflects a paper with promising contributions that needs substantial revision (particularly correcting the zero-shot claim, adding baselines, and specifying the algorithm) before it can be accepted.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>