Now I have all the information needed. Here is the final consolidated review.

---

## Summary

SigMap proposes a two-stage framework for wireless localization: (1) self-supervised pre-training with a cycle-adaptive masking strategy on CSI, and (2) prompt-based fine-tuning that encodes 3D map geometry as a soft prompt via a GNN, keeping 99.3% of the backbone frozen. The paper evaluates on DeepMIMO and WAIR-D ray-tracing simulations.

## Strengths

- **The "map-as-prompt" design is clean and parameter-efficient.** Encoding 3D map geometry via a GNN into a soft prompt that prepends a frozen Transformer keeps only 0.085M parameters trainable during fine-tuning (Table 5, Section 4.6), a genuine practical advantage for deployment. (favorability: 1.00)

- **The generalization evaluation on WAIR-D (100 city layouts from OpenStreetMap, Section 4.5)** is more diverse than what most wireless localization papers test, providing a reasonable stress test for cross-scenario robustness. (favorability: 1.00)

- **The multi-BS attention-based fusion mechanism (Equations 9–10, Section 3.5)** is a clean, interpretable way to handle variable numbers of base stations via learned attention weights and weighted averaging. (favorability: 1.00)

## Weaknesses

### Fatal
None.

### Major

- **Claim vs. evidence mismatch: "zero-shot" is actually few-shot.** The abstract and contributions (Section 1.2) claim "strong zero-shot generalization in unseen environments." However, Section 4.5 explicitly describes the experimental protocol as a "few-shot learning setup" where "only the downstream task heads are fine-tuned using limited target samples (approximately 100 instances per scenario)." This is a factual discrepancy — zero-shot means no labeled target data; the paper uses labeled fine-tuning data. The claim is simply incorrect as written. (favorability: 0.20)

- **Simulated-only evaluation for a claimed "foundation model."** All experiments (DeepMIMO O1_3p5, O2, WAIR-D) rely entirely on ray-tracing simulations. No real-world CSI measurements are used at any stage. Real channels include hardware impairments (I/Q imbalance, carrier frequency offset, phase noise), temporal dynamics, and measurement noise that simulated data do not capture. Given the paper's stated scope — autonomous driving, XR, smart manufacturing — and its "foundation model" framing, the absence of any real-data validation is a significant gap. (favorability: 0.00)

- **The cycle-adaptive masking mechanism — the paper's first claimed innovation — is critically under-specified.** Equation (6) defines the mask pattern using parameters \(d_{\text{final}}\), \(j_0\), and \(w\), but the paper never explains: (a) what cross-correlation is computed (auto-correlation of CSI amplitude? across which dimension — subcarriers, antennas, time?), (b) how the dominant periodicity is extracted from the correlation result, (c) how \(d_{\text{final}}\), \(j_0\), and \(w\) are set (per-sample or global hyperparameters). Without this information, the method cannot be reproduced or compared against. (favorability: 0.00)

### Minor

- **The NLoS-aware attention mechanism (Equation 11) appears without introduction.** It is presented in Section 4.2 (results) as the source of SigMap's advantage on NLoS scenarios, but it is never described in the methodology section (Sections 3.1–3.5). The "attention-based fusion" in Section 3.5 (Equations 9–10) is a different mechanism for combining multiple base station outputs — not this. This omission makes the architecture description incomplete. (favorability: 0.17)

- **No uncertainty measures on any quantitative result.** The paper states "All results are averaged over 5 independent runs" (Section 4.1) but reports no standard deviations, confidence intervals, or error bars for any main result (Tables 1–4, generalization table). Some margins are modest (e.g., SigMap w/o map MAE 2.275 vs. LWLM 2.382 in Table 1), and without variance the reader cannot assess statistical reliability. (favorability: 0.22)

- **Numerical inconsistency in WAIR-D generalization results (Section 4.5).** The text reports "1.580 m on WAIR-D Scenario-2," but the corresponding table entry shows 1.880 m for SigMap (w/ map). The stated 44.3% improvement over LWLM computes correctly from 1.880, so 1.580 is a typo. (favorability: 0.52)

- **Baseline pre-training status not clarified.** The paper does not state whether LWLM and SWiT were pre-trained on the same data as SigMap or trained from scratch on the downstream task. If the latter, the comparison is asymmetric — SigMap benefits from large-scale unlabeled pre-training while baselines do not. (favorability: 0.47)

- **Unusual pattern in masking ablation not discussed (Table 3).** Adaptive masking achieves better MAE (0.673) and CDF@1m (84.5%) than strip-masking (0.753, 75.3%), but worse RMSE (1.099 vs. 0.972). This counter-intuitive pattern — better CDF@1m but worse RMSE — is not explored. (favorability: 0.66)

### Trivial

- **Figure-reference error in Section 4.4.** The text references "near-overlapping error bars" in "Figure 1," but Figure 1 is the propagation-path illustration, not an error-bar plot. (favorability: 0.16)

- **Pre-training is on a single scenario (DeepMIMO O1_3p5, Section 4.1).** A narrow basis for a "foundation model" that claims general-purpose wireless representations. (favorability: 0.00)

## Nice-to-Haves

- Adding standard deviations (±σ) to all tables would strengthen the quantitative claims at negligible cost.
- A dedicated experiment ablating cycle-adaptive masking in the single-BS setting (Table 3 only ablates multi-BS) would improve completeness.
- The speculation about replacing 2-D polygons with street-level photographs (Section 4.4) is interesting but unsupported; a reference or preliminary experiment would help.

## Removed Points

These points are flagged to be removed; treat them with caution.

- **Map prompt lacks material properties (building materials, window density).** Scope creep — the paper explicitly targets geometric constraints and never claims to model material properties.
- **Pre-training would need to be repeated for new environments.** This is acknowledged implicitly via the fine-tuning setup; it is a standard property of pre-training paradigms.
- **"Could SSIM-like metrics capture periodic shortcuts instead?"** Speculative; no concrete evidence that the paper's approach fails to address the claimed problem.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Align the claims with the experimental protocol: replace "zero-shot" with "few-shot" throughout, or run a true zero-shot experiment.
2. Add real-world CSI validation, or at minimum acknowledge the simulated-only limitation prominently in the abstract and conclusion.
3. Fully specify the cross-correlation-based periodicity detection algorithm so the method can be reproduced.
4. Integrate the NLoS-aware attention mechanism into the methodology section with a clear architectural description.
5. Report standard deviations for all quantitative results.
6. Clarify the pre-training status of all baselines (and if they were trained from scratch, add a version that also receives pre-training).
7. Fix the WAIR-D numerical error (1.580 → 1.880).
8. Discuss the unusual RMSE vs. CDF@1m pattern in the masking ablation.

## Score and Decision

The paper proposes a sensible framework, and the parameter-efficiency results are credible. However, the paper suffers from three significant problems: (1) a clear factual mismatch between the claimed "zero-shot" generalization and the actual few-shot experimental protocol, (2) a simulated-only evaluation that undermines the "foundation model" framing given the paper's stated application domains, and (3) an under-specified core innovation (cycle-adaptive masking) that cannot be reproduced. These issues are structural rather than minor gaps, and together they prevent acceptance in the current form.

MY FINAL SCORE: <score>3</score>
MY FINAL DECISION: <decision>Reject</decision>