## Summary

HOMIL extends ABMIL for whole-slide image classification by computing second-order statistics (a covariance matrix) on DBSCAN-derived cluster features and fusing them with the standard first-order (attention-weighted mean) representation. On CAMELYON16 and TCGA-NSCLC, it reports improved accuracy and AUC over nine baselines with competitive runtime. The core ideas are clearly motivated, but the experimental evidence has significant credibility issues.

## Strengths

- **Conceptually clear motivation.** The paper correctly identifies that ABMIL's mean-based aggregation discards feature variability and inter-feature relationships, and proposes second-order moments as a natural statistical extension. The reframing of ABMIL as first-order moment estimation (Section 3.1) is a clean pedagogical device that makes the extension intuitive.

- **DBSCAN's density-adaptive property aligns well with WSI characteristics.** The observation that normal tissue forms large, dense clusters while pathological regions form small, sparse ones (Section 4.2) is a genuine architectural insight that connects algorithm properties to problem structure, and is the paper's most interesting design choice.

- **Two standard benchmarks with 5-fold CV and unified splits.** CAMELYON16 and TCGA-NSCLC are appropriate choices, and the patient-level 5-fold partitioning is a defensible evaluation protocol.

## Weaknesses

### Major

- **Several baseline results on TCGA-NSCLC are anomalously poor, undermining fair comparison.** On TCGA-NSCLC (Table 2), multiple strong baselines perform below reasonable expectations: HMIL achieves only 93.59% AUC — well below Mean Pooling's 96.85%. TransMIL achieves 88.57% ACC — below Mean Pooling's 90.76%. Both CLAM-SB and CLAM-MB underperform ABMIL, despite being strictly more expressive architectures designed to improve upon it. These patterns suggest the "unified codebase" (line 200) may use hyperparameters that disadvantage some methods. The paper reports no hyperparameter search for baselines. Since the paper's "state-of-the-art" claim depends on outperforming these baselines, this is a serious concern — the same type of issue that led to rejection of similar WSI MIL papers (see Mamba-HMIL, reviewer note: "the performance of [...] on NSCLC is inconsistent with the results reported in the original papers").

- **Ablation shows second-order moments without clustering hurt performance — left unaddressed.** In Table 3, the "w/o CM" variant (second-order moments on all patches, no clustering) achieves AUC 98.14% — *worse* than plain ABMIL's 98.88%. Adding the second-order moment to raw patch features *reduces* performance. The only configuration where second-order moments help is when computed on cluster features. The paper does not analyze why (e.g., is the 512×512 covariance on ~3000 patches too noisy? does the 1D convolution destroy signal?), which undercuts the narrative that second-order statistics are inherently informative.

- **No statistical significance testing.** HOMIL's AUC gain over S4MIL on CAMELYON16 is only 0.21 percentage points (99.23 vs 99.02, both within one standard error), and on TCGA-NSCLC the gain over Max Pooling is 0.44 percentage points (97.41 vs 96.97, overlapping error bars). No significance tests are reported. Combined with the baseline tuning concerns, the headline performance claims are not supported by the evidence presented.

### Minor

- **Framing mismatch between motivation and implementation.** The abstract states the paper "compute[s] the covariance matrix of the *patch representation vectors* across the entire slide" (line 9), and Section 3.2 describes a *patch-level* covariance matrix (Eq. 2: Σ = Σ (h_i − μ)(h_i − μ)^T). However, the actual computation (Section 4.3.3) operates on **cluster features** g_k — which are mean-pooled representations of patches within each DBSCAN cluster. Within-cluster patch variability is discarded before the covariance is ever computed. While the introduction briefly notes moments are computed on cluster representations (line 25), the abstract and background section never correct this framing, leaving a disconnect between what is motivated and what is implemented.

- **Covariance vectorization via 1D convolution is ad-hoc and unmotivated.** The 512×512 covariance matrix C is reduced to a 512-D vector via row-wise 1D convolution with 4 kernels of size 64 and two rounds of max-pooling (Section 4.3.3, lines 156–168). The paper offers no justification for this specific design, no comparison to standard alternatives (flatten+linear, eigenvalue pooling, Cholesky decomposition, matrix log), and no analysis of what information survives the aggressive double max-pooling compression. The symmetry of C is also not exploited.

- **Covariance normalization omitted.** Equation (4) defines C as a raw sum of outer products with no 1/(K−1) or 1/K factor. The matrix magnitude therefore scales with K (the number of clusters per slide, which varies due to DBSCAN). While subsequent layers could compensate, the paper provides no analysis of this scale sensitivity.

- **Figure 1 caption vs. text discrepancy.** The Figure 1 caption describes "Conv1D layer to produce first-order features v^(1)" for instance features, while Section 4.3.2 describes v^{(1)} as a simple attention-weighted sum of cluster features with no Conv1D. The figure and text disagree on the first-order computation path.

### Trivial

None.

## Nice-to-Haves

- Provide statistical significance tests (paired permutation or McNemar's) or more random seeds to tighten error estimates.
- Re-run TCGA-NSCLC baselines with per-method hyperparameter tuning, or explain why the reported baseline numbers are credible.
- Analyze why the "w/o CM" ablation underperforms ABMIL — this could reveal important properties of the method.
- Compare the 1D convolution vectorization against simpler alternatives (e.g., flatten + linear projection).

## Removed Points

These are flagged as removed; treat with caution if referenced.

- **DBSCAN non-learnable (from harsh critic Issue 6):** Removed. The paper clearly describes clustering as a preprocessing step. The term "adaptive" refers to DBSCAN's spatial adaptivity (different granularity for different density regions), not training-time adaptation. The criticism misreads the paper.
- **"Attention-weighted covariance" label without attention in the sum:** Removed. The centering uses v^{(1)} (the attention-weighted mean), so the label is defensible. The covariance sum does not need to separately multiply by attention weights.
- **Timing comparison ambiguity:** Removed. The paper transparently states (line 240): "including clustering for HOMIL, or training+inference only for other methods." This is clear.
- **Missing related works references:** Removed per policy — cannot be verified and may be an artifact of appendix stripping.
- **Formatting/typo nitpicks:** Removed per policy — parser artifacts, not author errors.

## Novel Insights

None beyond the paper's own contributions. The harsh critic's most interesting observations (the DBSCAN-WSI alignment, the ablation paradox) are already surfaced in the review above, but do not constitute genuinely novel insights beyond what the paper provides.

## Suggestions

1. Re-run the TCGA-NSCLC baselines with per-method hyperparameter tuning and report the search ranges. The current numbers for HMIL, TransMIL, and CLAM on this dataset damage the paper's credibility.
2. Either recompute the covariance at the patch level to align with the stated motivation, or explicitly reframe the contribution as operating on cluster-level features and discuss what within-cluster information is lost.
3. Add statistical significance tests, or substantially temper the "state-of-the-art" language to match what the evidence supports (marginal gains on one of two datasets, with overlapping error bars).
4. Provide even a brief paragraph analyzing why the "w/o CM" ablation underperforms ABMIL.

## Score and Decision

**Round-1 bracket:** 3.0–5.0 (based on calibration against Mamba-HMIL at 3.25, MILCA at 3.50, SMIL at 4.50, and MFC at 6.00; HOMIL is closer to the 3–4 reject range than to SMIL's 4.5 because its experimental evidence has a credibility problem beyond incremental novelty).

**Calibration anchors used across rounds:**
- Mamba-HMIL (3.25, reject) — Similar WSI MIL paper with comparable baseline issues on TCGA-NSCLC; HOMIL has better writing and clearer motivation but similar experimental weakness.
- MILCA (3.50, reject) — MIL paper with limited novelty; HOMIL has stronger motivation but more severe experimental concerns.
- SMIL (4.50, reject) — Sequential MIL with comprehensive experiments but limited novelty; HOMIL has weaker experimental support.
- Pg-GAT (3.00, reject) — WSI GNN-based MIL; similar scope and rejection level.
- SHAP-CAT (3.40, reject) — Multimodal WSI classification; similar tier.
- MFC (6.00, accept) — WSI causal MIL with stronger perceived novelty; HOMIL's contribution is more incremental.
- Dual-Metric SSL (2.50, reject) — Histopathology SSL; less directly relevant.
- Enhancing Instance-Level (5.67, accept) — Set-level histopathology labels; less directly relevant.

**Final score: 3.5.** The paper has a clear motivation and one genuinely interesting architectural insight (DBSCAN density adaptivity for WSI). However, the experimental evaluation has a serious baseline-tuning credibility issue, the ablation reveals an unaddressed inconsistency, the performance gains are small and untested for significance, and there is a framing mismatch between what is motivated and what is computed. These problems collectively prevent the claimed contributions from being supported by the presented evidence.

MY FINAL SCORE: <score>3.5</score>
MY FINAL DECISION: <decision>Reject</decision>