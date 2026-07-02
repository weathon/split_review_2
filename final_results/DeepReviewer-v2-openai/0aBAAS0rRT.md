## Summary
# Final Review Report

## Summary

This paper presents SigMap, a multimodal foundation model for wireless localization that combines two technical innovations: (1) a cycle-adaptive masking strategy for self-supervised pre-training on CSI data that disrupts periodic shortcuts, and (2) a "map-as-prompt" framework that encodes 3D building geometry into soft prompt tokens via a GNN for parameter-efficient fine-tuning. The model is evaluated on ray-tracing datasets (DeepMIMO O1_3p5, O2, WAIR-D) and achieves reported MAE of 1.564 m (single-BS) and 0.673 m (multi-BS), outperforming four baselines (OMP, CNN, SWiT, LWLM). The paper addresses a relevant and practical problem—accurate NLoS wireless localization—and the core ideas (periodicity-aware masking, geographic prompt tuning) are technically interesting. However, the manuscript has significant weaknesses that limit its current impact: (i) overclaimed and factually inaccurate statements (e.g., "zero-shot" generalization when only few-shot fine-tuning is performed, "state-of-the-art" versus only four baselines), (ii) missing variance reporting despite claiming 5-run averages, (iii) reproducibility gaps in method description (transformer architecture, cross-correlation details, normalization), (iv) a mathematical inconsistency between the GCN equation and the algorithmic pseudocode, and (v) incomplete parameter efficiency comparisons without baseline costs. External literature verification was unavailable in this run, so novelty claims require manual verification.

## Strengths
1. **Relevant problem and practical motivation**: The paper tackles wireless localization under NLoS conditions, a well-recognized bottleneck for 5G/6G applications. The motivation is sound and the problem framing (cross-scenario generalization with minimal data) addresses a real deployment challenge.

2. **Technically interesting dual innovation**: The two core ideas—cycle-adaptive masking to break periodic shortcuts and map-conditioned prompt tuning for geographic awareness—are conceptually novel within the wireless localization literature. The cycle-adaptive masking idea is non-trivial because it requires detecting dominant periodicities in CSI and generating masks that prevent simple interpolation-based reconstruction. The geographic prompt mechanism is a creative application of prompt tuning from NLP to the spatial domain.

3. **Strong empirical results on tested scenarios**: SigMap achieves 1.564 m MAE (single-BS NLoS) and 0.673 m MAE (multi-BS), which are competitive against the four baselines tested. The multi-BS CDF@1m of 84.5% represents a notable improvement over the best baseline (LWLM, 75.6%). The generalization results on WAIR-D (100 city scenes) demonstrate meaningful cross-scenario transfer.

4. **Parameter-efficient fine-tuning is demonstrated**: With only 0.085M trainable parameters (0.7% of total) and 30 minutes fine-tuning time, the method's efficiency is quantitatively demonstrated. This is a practical advantage for deployment scenarios where labeled data is scarce.

5. **Informative ablation study on map modalities**: The comparison between 3-D mesh, 2-D bird's-eye, and no-map conditions (Table 4) provides useful insight: the 2-D variant retains most of the benefit (MAE 1.692 vs 1.564 m), suggesting that horizontal topology is the dominant factor. This has practical implications for deployment where 3-D data may be unavailable.

## Weaknesses
The weaknesses are ordered from most critical to least critical based on impact on validity, reproducibility, and research value.

### 1. Factual inaccuracy: "Zero-shot generalization" is actually few-shot (Critical)
**Evidence**: Section 4.5 states "only the downstream task heads are fine-tuned using limited target samples (approximately 100 instances per scenario)." The Abstract and Contribution list claim "strong zero-shot generalization in unseen environments." Zero-shot requires no task-specific training samples; fine-tuning on 100 labeled instances is few-shot, not zero-shot.
**Impact**: This is a factual error that misrepresents the method's capability. A reviewer familiar with zero-shot/few-shot terminology will flag this as an overclaim.
**Recommended fix**: Replace all instances of "zero-shot" with "few-shot" (or "few-shot adaptation with ~100 samples"). Adjust the abstract and contributions accordingly.

### 2. Unsupported "state-of-the-art" claim (Major)
**Evidence**: The Abstract claims "state-of-the-art performance across multiple localization tasks" and Contributions claim "Our foundation model achieves state-of-the-art performance." The experiments compare against only four baselines (OMP, CNN, SWiT, LWLM). The paper does not survey or compare against the full landscape of wireless localization methods, including recent deep learning approaches, model-based methods with NLoS mitigation, or hybrid approaches.
**Impact**: Claims of "SOTA" require comprehensive cross-paper comparison under standardized protocols. Without this, the claim is unsubstantiated and may be rejected during review.
**Recommended fix**: Replace "state-of-the-art" with bounded comparative wording, e.g., "outperforms selected baselines (OMP, CNN, SWiT, LWLM) under the DeepMIMO O1_3p5 evaluation protocol."

### 3. Missing variance/statistical reporting despite 5 runs (Major)
**Evidence**: Section 4.1 states "All results are averaged over 5 independent runs," but Tables 1, 2, 3, and 4 report only point estimates without standard deviations, confidence intervals, or significance tests. The ablation study (Section 4.4) claims "near-overlapping error bars" without showing any error bars or variance data.
**Impact**: Without variance, the statistical significance of reported improvements cannot be assessed. In Table 2, the gap between SIGMAP w/o map (0.789 MAE) and LWLM (0.828 MAE) could be within noise range. The claimed "near-overlapping error bars" in Section 4.4 are unverifiable.
**Recommended fix**: Report mean ± std for all metrics in all tables. Add a paired significance test (e.g., Wilcoxon signed-rank) between SIGMAP and the strongest baseline for each setting.

### 4. Mathematical inconsistency between GCN equation and Algorithm 1 (Major)
**Evidence**: Section 3.4 provides a standard Kipf-Welling GCN equation: H^{(l+1)} = sigma( D^{-1/2} A~ D^{-1/2} H^{(l)} W^{(l)} ). However, Algorithm 1 (lines 5-8) uses a different message-passing rule: h_i^{(l)} = sigma( W^{(l)} h_i^{(l-1)} + sum_{j in N(i)} U^{(l)} h_j^{(l-1)} ), which uses separate self and neighbor weight matrices (W vs U). These two formulations are not equivalent.
**Impact**: This is an implementation ambiguity. Readers cannot determine which formulation was actually used, compromising reproducibility. If the algorithm version is correct, the equation is wrong; if the equation is correct, the algorithm is wrong.
**Recommended fix**: Unify the descriptions. Either (a) adopt the Algorithm 1 formulation as the canonical definition and revise the equation to: H^{(l+1)} = sigma( A_norm H^{(l)} U^{(l)} + H^{(l)} W^{(l)} ), or (b) adopt the standard GCN formulation and revise Algorithm 1 accordingly.

### 5. Cycle-adaptive masking is underspecified for reproducibility (Major)
**Evidence**: Section 3.3 states that "we compute shift patterns using cross-correlation analysis and generate adaptive mask patterns" but does not specify: (a) along which axis the cross-correlation is computed (subcarrier, time, antenna), (b) what reference signal is used, (c) how the detected periodicity shift d_final is extracted from the correlation output. Equation (6) uses indices i, j without defining which axes they correspond to.
**Impact**: The core technical contribution cannot be reproduced or built upon by other researchers.
**Recommended fix**: Provide a detailed specification: "For each CSI sample X in R^{2 x N_r x N_t x N_s}, we average over the real/imag and antenna dimensions to obtain a 1D sequence along the subcarrier axis, compute its autocorrelation, and detect the first non-zero peak offset as d_final. The mask M[i,j] is defined over (antenna pair index i, subcarrier index j)..."

### 6. Transformer backbone architecture is not specified (Major)
**Evidence**: Section 3.1 states "a transformer-based backbone network" but does not report: number of layers, number of attention heads, hidden dimension, FFN dimension, tokenization scheme (patch embedding vs per-subcarrier), positional encoding type, or dropout rates.
**Impact**: A foundation model paper must specify its backbone architecture for reproducibility. Current description is insufficient for independent reimplementation.
**Recommended fix**: Add a table specifying all architecture hyperparameters, including the exact input tensor transformation through each stage.

### 7. MAE-RMSE discrepancy unexplained (Major)
**Evidence**: In Table 1 (Single-BS), SIGMAP w/ map has MAE=1.564 m but RMSE=5.675 m, giving RMSE/MAE ≈ 3.6. In contrast, the multi-BS results (Table 2) show RMSE/MAE ≈ 1.6. SIGMAP w/o map in O2 (Table 4.5) shows MAE=1.282, RMSE=5.824, ratio ≈ 4.5.
**Impact**: An RMSE 3-5x larger than MAE indicates heavy-tailed errors with extreme outliers. The paper does not analyze what causes these outliers (specific regions, NLoS geometries, etc.) or acknowledge this as a limitation.
**Recommended fix**: Add an error distribution analysis (e.g., percentile CDF curves, geospatial error heatmaps) and discuss failure cases. Bound the accuracy claims to reflect the heavy-tailed nature.

### 8. Parameter efficiency lacks baseline comparisons (Major)
**Evidence**: Section 4.6 reports only SigMap's parameter counts and training costs. The paper claims "parameter-efficient generalization" as a contribution but provides no comparison to the parameter counts, training time, or inference latency of LWLM, SWiT, or CNN baselines.
**Impact**: The contribution claim for parameter efficiency is incomplete. A method can claim efficiency only relative to alternatives under comparable settings.
**Recommended fix**: Add a column to Table 5 reporting total parameters, fine-tuning parameters, inference time, and total pre-training cost for each baseline method under identical hardware.

### 9. Signal preprocessing and normalization unspecified (Minor)
**Evidence**: Section 3.2 converts complex CSI to real-valued representation but does not specify any normalization (per-sample standardization? min-max? per-dataset statistics?), phase handling, or whether normalization parameters are frozen during cross-scenario fine-tuning.
**Impact**: Normalization choices significantly affect cross-domain generalization. Missing specification hinders reproducibility.
**Recommended fix**: Add a paragraph detailing the exact preprocessing pipeline.

### 10. Conclusion lacks limitations and overclaims (Minor)
**Evidence**: The conclusion reasserts "state-of-the-art performance" and "robustly generalizes" without acknowledging the MAE-RMSE gap, the limited baseline comparison, or the ray-tracing-only evaluation (no real-world measurements). Future work directions are speculative without grounding in current results.
**Impact**: Missed opportunity to demonstrate scientific maturity by candidly bounding the contributions.
**Recommended fix**: Restructure conclusion as: validated findings (bounded to tested scenarios), explicit limitations (heavy-tailed errors, synthetic data only), then concrete next steps.

**Additional observations (Minor)**:
- The title claims "Foundation Models" (plural) but only one model (SigMap) is presented for a single task (localization).
- Figure reference error in Section 4.4: "Two-dimensional and three-dimensional map ablations are illustrated side-by-side in Figure 1" — Figure 1 shows propagation paths, not the ablation comparison.
- The NLoS attention mechanism in Eq. (11) appears only in Section 4.2 and is not ablated; its contribution relative to the geographic prompt is unclear.

**Novelty and literature positioning note**: External literature verification was not available in this run (paper_search unavailable). Therefore, novelty assessment of the three claimed contributions (cycle-adaptive masking, map-conditioned prompt tuning, parameter-efficient generalization) against the existing literature is **deferred to manual verification**. The authors should ensure that the paper includes comprehensive comparison to related SSL-based wireless methods (e.g., CrowdBERT, signal-guided MAE, LWM, WirelessGPT, LWLM) and discusses overlap/differences explicitly.

## Score
**Final Score: 5/10**

**Rationale**: The score reflects the following evidence-graded assessment:

- **Research value/novelty**: The core ideas (cycle-adaptive masking, geographic prompt tuning) are technically interesting and address a relevant problem. However, the factual inaccuracies ("zero-shot" misrepresentation, unsupported "SOTA" claims) and incomplete baselines reduce confidence in the claimed contribution magnitude. Without external literature verification, the true novelty relative to the broader SSL-for-wireless field is uncertain. *(Weight: high, Score contribution: 5)*

- **Validity/soundness**: The empirical results show clear improvements on tested scenarios, but missing variance reporting, unablated components (Eq. 11), and the unexplained MAE-RMSE gap limit statistical reliability. The GCN equation-algorithm inconsistency is a concrete mathematical flaw. *(Weight: high, Score contribution: 5)*

- **Reproducibility**: Several key components are underspecified (transformer architecture, cross-correlation details, normalization, GCN formulation), which prevents independent reimplementation. This is a significant weakness for a methods paper. *(Weight: medium, Score contribution: 4)*

- **Writing/presentation**: The paper is generally well-structured with clear figures and tables. However, overclaimed language ("zero-shot," "SOTA," "foundation models"), one incorrect figure cross-reference, and a conclusion that lacks limitations detract from clarity and scientific candor. *(Weight: low, Score contribution: 6)*

The manuscript has a solid technical core and addresses a practically important problem. The main issues are corrigible: fixing factual inaccuracies, adding variance reporting, specifying architecture details, and reconciling the GCN inconsistency. With a thorough revision addressing the major weaknesses identified above, the paper could become a meaningful contribution to the wireless localization literature.

**External literature verification**: Not available in this run. Novelty assessment is deferred. Authors should manually verify that their contribution claims are appropriately scoped relative to existing work.