Now let me produce the final review.

## Summary

This paper proposes SigMap, a multimodal foundation model for wireless localization. The two claimed innovations are: (1) a cycle-adaptive masking strategy for pre-training that dynamically adjusts masking patterns based on CSI periodicity, and (2) a "map-as-prompt" framework that encodes 3D building geometry and base station positions into soft prompt tokens via a GCN, prepended to a frozen Transformer backbone during fine-tuning. Experiments on simulated ray-tracing datasets (DeepMIMO, WAIR-D) show substantial improvements over OMP, CNN, SWiT, and LWLM baselines, with strong parameter efficiency (0.085M trainable parameters during fine-tuning).

## Strengths

1. **Novel "map-as-prompt" approach.** Encoding 3D geographic context (building vertices + base station positions) into learned soft prompt tokens via a GCN and prepending them to a frozen Transformer backbone is a creative and well-specified mechanism (Section 3.4, Algorithm 1). The pipeline — Delaunay triangulation → 2-layer GCN → global mean pooling → projection — is concrete enough to be reproduced.

2. **Large quantitative margins.** The method achieves a 34.4% MAE improvement over LWLM in single-BS localization (Table 1: 1.564 m vs 2.382 m) and an 18.7% improvement in multi-BS localization (Table 2). CDF@1m approximately doubles in the single-BS case (60.5% vs 25.3%).

3. **Parameter efficiency is convincingly demonstrated.** Only 0.085M of 11.73M total parameters are trainable during fine-tuning, and the fine-tuning stage completes in 30 minutes (Table 5), making the approach practical.

## Weaknesses

### Fatal
None.

### Major

1. **"Zero-shot" overclaim contradicted by the paper's own experimental description.** The abstract states the model exhibits "strong zero-shot generalization in unseen environments," and Contribution 3 (Sec 1.2) repeats "strong zero-shot generalization to unseen environments." However, Section 4.5 explicitly describes the setup as "few-shot" — task heads are fine-tuned on ~100 labeled target samples. Zero-shot means no task-specific training data from the target domain; updating any parameters (even just task heads) on target data is few-shot, not zero-shot. This is a factual misrepresentation in the paper's central claims, appearing in the abstract, contributions list, and implicitly in the conclusion.

2. **NLoS-aware attention mechanism appears without architectural specification in the methodology.** Equation (11) in Section 4.2 introduces an "NLoS-aware attention mechanism" with a weight matrix W_NLoS and describes it as the source of the "key advantage" in single-BS localization. However, this mechanism is never described in the methodology section (Section 3). The self-attention described in Section 3.4 is standard dot-product attention; Section 3.5 describes a multi-BS fusion attention (Equation 9) using different notation. A reader cannot determine whether Equation (11) is part of the core architecture, a component of the task head, or a post-hoc interpretation.

### Minor

3. **Experimental evaluation is entirely on simulated data.** While the paper acknowledges that DeepMIMO data is "generated through ray-tracing simulations" (Section 4.1), the paper frames its contributions toward "practical wireless perception systems" without testing on any real-world measured CSI. Although simulated evaluation is standard in this area, the absence of real-data validation limits the strength of the practical claims.

4. **Missing comparisons against relevant SSL-based competitors.** The introduction discusses several self-supervised and foundation-model approaches for wireless — including WirelessGPT (Yang et al., 2025), CrowdBERT (Han et al., 2024), signal-guided MAE (Wang et al., 2025), WirelessLLM (Shao et al., 2024) — yet none are included in the experimental comparison. For a paper positioning itself as a "foundation model," the omission of the closest SSL-based competitors is a gap.

5. **Masking ablation lacks a random-masking baseline.** Table 3 compares cycle-adaptive masking against grid-only and strip-only variants, but does not include the standard random-masking baseline used in MAE literature. Without this control, it is impossible to assess whether the cycle-adaptive strategy outperforms a simpler, parameter-free approach.

6. **Numerical inconsistencies.** (a) Section 4.5 text states SigMap reaches "1.580 m on WAIR-D Scenario-2," but the table in the same section reports 1.880 m. The 44.3% improvement over LWLM is computed from the table value (1.880), not the text value (1.580). (b) Section 4.5 says "updating only 0.4% of parameters," while Section 4.6 calculates 0.7% (0.085M/11.73M ≈ 0.72%). These errors undermine confidence in numerical reporting.

7. **No statistical uncertainty on main results.** The paper states results are "averaged over 5 independent runs" (Section 4.1) but does not report standard deviations, confidence intervals, or error bars for any main result tables (Tables 1, 2, 3, 4.5). For comparisons where margins are modest (e.g., adaptive vs strip masking in RMSE: 1.099 vs 0.972), this is needed to assess significance.

8. **Periodicity detection algorithm for cycle-adaptive masking is underspecified.** Section 3.3 states that d_final is "the detected periodicity shift" computed via "row-wise cross-correlation," but the detection algorithm is never specified — how the dominant periodicity is extracted from cross-correlation (argmax of autocorrelation? handling of multiple periodicities?) is not described, making the masking strategy non-reproducible.

9. **Strip-masking achieves lower RMSE than the proposed adaptive masking.** In Table 3, strip-masking achieves RMSE of 0.972 m vs adaptive masking's 1.099 m. The paper claims adaptive masking yields the "best trade-off" (better MAE and CDF@1m), but the higher RMSE suggests worse tail behavior that warrants discussion.

### Trivial
- Prompt token count: Section 3.4 describes "a single prompt" token, but the Figure 2 caption mentions "Prompt Tokens" (plural). Minor inconsistency.

## Nice-to-Haves
- Compare the GNN-based prompt encoding against a simpler baseline: directly concatenating hand-crafted geometric features (e.g., distance to nearest building, building density) to the [CLS] token. Such an ablation would isolate whether the learned GNN encoding genuinely outperforms cheap feature engineering.
- Discuss why map information provides less relative benefit in multi-BS setups (14.7% MAE improvement) compared to single-BS setups (31.2% improvement), as shown in Tables 1 and 2.

## Removed Points
(These points were flagged by the reviewer but removed per meta-reviewer filtering rules. Treat them with caution.)
- **"All experimental data is simulated" framed as a fatal/undisclosed overstatement:** The paper does acknowledge simulated data ("generated through ray-tracing simulations" in Section 4.1). Retained in weakened form as Minor #3.
- **"Missing appendix details":** The appendix was stripped by the parser; per policy, missing appendix content is not a valid criticism.
- **Criticism that cited models/datasets "are not yet released" or "cannot be independently verified":** Per policy, if the paper cites them, they are assumed to exist.
- **Scope-creep demands (larger datasets, more models beyond what is standard):** Removed.
- **Formatting/style nitpicks:** Removed per policy.
- **"Why does map information matter less when multiple base stations are available":** This is a discussion question rather than a weakness; moved to Nice-to-Haves.

## Novel Insights
The core insight from the harsh critic's analysis — that the "zero-shot" claim in the abstract and contributions is contradicted by the paper's own experimental setup (which is explicitly described as "few-shot") — is accurate and important. Beyond this, no genuinely novel insight beyond the paper's own contributions emerges from the reviews.

## Suggestions
- Correct the "zero-shot" claims throughout the paper to "few-shot" or "parameter-efficient few-shot" to accurately describe the experimental setup.
- Move the NLoS-aware attention mechanism description (Equation 11) into the methodology section (Section 3) with full architectural details, or clarify whether it is a distinct architectural component.
- Add a random-masking condition to Table 3 for proper ablation.
- Fix the numerical inconsistencies (1.580→1.880; 0.4%→0.7%).
- Add standard deviations/error bars to all main result tables.
- Include at least one relevant SSL-based baseline (e.g., signal-guided MAE or CrowdBERT) in the comparison.
- Specify the periodicity detection algorithm (how d_final is computed from cross-correlation) for reproducibility.

## Calibration Anchors

The following papers from the review corpus provided score calibration:

| Anchor Path | Avg Score | Round | Comparison |
|---|---|---|---|
| `9TClCDZXeh.md` (Wi-GATr) | 7.00 | 1 | Wireless simulation with geometric transformers; clearer paper with real-world validation. Significantly stronger execution. |
| `lG9fjBLb6d.md` (RFMamba) | 6.50 | 1 | RF-based perception with SSM; real-world experiments, clearer presentation. Stronger overall. |
| `7KDuQPrAF3.md` (Foundation Model for ECC) | 6.25 | 1 | Foundation model for error correction codes; clearer methodology. Stronger. |
| `fQSZMrjW8X.md` (LocDiffusion) | 5.80 | 1 | Image geolocalization with diffusion. Comparable novelty, better presentation. |
| `PdwrCm5Msr.md` (MapLearn) | 4.75 | 1 | Audio-based indoor mapping; simulation-only evaluation similar to this paper. Comparable quality. |
| `H8oCwBTDMv.md` (UrbanDiT) | 4.20 | 2 | Foundation model for urban spatio-temporal with prompt learning; similar zero-shot overclaim and missing baselines issues. Very comparable. |
| `q3WzT2mrhB.md` (WiMTR) | 4.00 | 1 | WiFi CSI mesh regression; clarity issues. Slightly weaker execution. |
| `XhdckVyXKg.md` (NormWear) | 3.00 | 1 | Foundation model for physiological signals; weaker contribution. |
| `ntSP0bzr8Y.md` (PowerGPT) | 3.00 | 1 | Foundation model for power systems; weaker contribution. |

**Round 1 bracket:** 4.0–6.0. The paper sits closest to UrbanDiT (4.20) and MapLearn (4.75) — papers with interesting ideas but significant presentation/evaluation gaps — and clearly below Wi-GATr (7.00) and RFMamba (6.50), which have stronger execution and real-world validation.

**Final score justification:** The paper has a genuinely creative core idea (map-as-prompt) and strong quantitative results. However, it is held back by two major issues — a factual overclaim about zero-shot generalization and an architectural ambiguity about the NLoS-aware attention — plus several minor issues (missing baselines, numerical errors, no variance reporting, underspecified algorithm). This places it at 4.5 on the ICLR scale: not fatally flawed, but not ready for acceptance in its current form.

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>