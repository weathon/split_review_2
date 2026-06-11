Now I have sufficient calibration data. Let me finalize my assessment.

**Calibration anchors summary:**

| Round | Paper | Score | Decision | Relevance |
|-------|-------|-------|----------|-----------|
| R1 | Pg-GAT | 3.00 | Reject | WSI MIL, graph-based |
| R1 | Mamba-HMIL | 3.25 | Reject | WSI MIL, state space |
| R1 | SMIL | 4.50 | Reject | MIL, clinical imaging |
| R1 | Set-level labels | 5.67 | Accept | MIL, histopathology |
| R1 | MFC | 6.00 | Accept | WSI MIL, CAMELYON16+TCGA |
| R1 | MIL for TSC | 8.00 | Accept | MIL, time series |
| R2 | MI-PLL | 5.00 | Reject | MIL theory |
| R2 | VLSA | 5.67 | Accept | WSI pathology, MIL |
| R2 | ViTally Consistent | 5.25 | Reject | Cell microscopy |

**Initial bracket: 5.0–6.0.** HOMIL is clearly better than rejected papers at 3.0–4.5 (clearer motivation, fair evaluation, better writing) but has a genuine methodological inconsistency that the 5.67–6.00 accepted papers don't have in the same way. The paper sits near the accept/reject boundary.

**Narrowing:** Compared to VLSA (5.67, Accept), HOMIL has fairer evaluation and clearer methodology but a more central methodological inconsistency (attention-weighting claim). Compared to MI-PLL (5.00, Reject), HOMIL has stronger practical contributions and clearer presentation. Compared to MFC (6.00, Accept), HOMIL has better writing and clearer methodology but less novel conceptual contribution.

**Final score: 5.5.** The paper has genuine contributions (statistical framing, efficiency, fair evaluation) with real but fixable issues (attention-weighting inconsistency, no significance testing). At an ICLR-level venue, this is borderline — the methodological inconsistency in the core claim tips it toward rejection.

---

## Summary

This paper proposes HOMIL, a multi-instance learning framework for whole-slide image (WSI) classification that augments standard attention-based first-order aggregation with second-order moment (covariance) representations and DBSCAN-based adaptive patch clustering. The method is evaluated on CAMELYON16 and TCGA-NSCLC against nine baselines, achieving best accuracy across all metrics with dramatically improved computational efficiency (310s vs. 7200s for MambaMIL on CAMELYON16).

## Strengths
- **Clear statistical framing of ABMIL as first-order moment estimation** — Section 3.1 (Eqs. 1–2) provides a clean interpretation of ABMIL's attention-weighted aggregation as E_{a_i}[h_i], motivating second-order moments as a natural extension and giving the method principled theoretical grounding.
- **Dramatic computational efficiency alongside best accuracy** — Tables 1 and 2 confirm HOMIL achieves 310s on CAMELYON16 vs. 7200s for MambaMIL and 10800s for HMIL, with compression ratios of 0.18 and 0.16 (Section 5.3), validating the DBSCAN clustering approach.
- **Fair and reproducible experimental setup** — All nine baselines in a unified codebase with identical 5-fold patient-level CV splits, shared 512-dimensional features, and consistent hardware (Section 5.2). This eliminates a common confound in MIL comparisons.
- **Consistent improvements across two distinct WSI tasks** — HOMIL outperforms all baselines on both CAMELYON16 (metastasis detection) and TCGA-NSCLC (lung cancer subtyping) across ACC, AUC, and F1, demonstrating robustness across different diagnostic challenges.

## Weaknesses

### Fatal
None

### Major
- **Mismatch between "attention-weighted covariance" framing and actual implementation** — The paper repeatedly describes the covariance as "attention-weighted" (Section 4.1 item 3, line 108; Section 4.3.3, line 147; section title "Weighted Covariance Matrix," line 150). However, the formula C = Σ_{k=1}^K g̃_k g̃_k^⊤ (line 152) uses uniform summation over clusters — the attention weights a_k do not appear. The centering uses v^{(1)} = Σ_k a_k g_k (attention-dependent), making the covariance implicitly attention-aware through centering, but the outer products are equally weighted. The paper should either incorporate attention weights into the sum (C = Σ_k a_k g̃_k g̃_k^⊤) or reframe the description to clarify that the "weighting" comes from centering, not from the outer product summation.
- **Lack of statistical significance testing** — The abstract claims HOMIL "significantly improves the state-of-the-art performance," but no significance tests are reported. With 5-fold CV, standard errors are comparable to improvements: CAMELYON16 ACC Δ=2.26% with SEs of ±2.18/±2.43; TCGA-NSCLC ACC Δ=0.35% with SEs of ±1.45/±2.47. Without paired t-tests or bootstrap CIs, the improvements could be within the noise of 5-fold CV.

### Minor
- **Non-monotonic AUC in ablation (Table 3)** — ABMIL AUC (98.88%) exceeds both w/o CM (98.14%) and w/o SOM (98.51%), meaning each component individually *hurts* AUC relative to plain ABMIL; only the full combination helps (99.23%). While ACC and F1 show monotonic improvements, this non-monotonic AUC pattern is unexplained and suggests complex component interactions. The paper should discuss this anomaly rather than claiming both components are independently "critical."
- **Limited ablation scope** — Ablation only on CAMELYON16, not TCGA-NSCLC. Missing: alternative clustering methods, alternative covariance compression approaches (the 1D-conv compression from 512×512→512 is ad hoc with no motivation or alternatives compared), and attention-weighted vs. uniform covariance.
- **No analysis of what the covariance captures** — Figure 2(b) shows α^(1) ≈ 0.6 and α^(2) ≈ 0.4, suggesting the model relies primarily on first-order information. The tension between this observation and the paper's emphasis on second-order moments deserves deeper analysis (e.g., visualization of discriminative covariance dimensions or probe experiments).

## Nice-to-Haves
- Add at least one additional dataset or task type (e.g., multi-class subtyping, survival prediction) to assess generalizability beyond binary classification.
- Compare the 1D-conv compression against alternatives (e.g., eigendecomposition/top-k eigenvalues, flattened projection, bilinear pooling).
- Discuss whether the 0.4 fusion weight for second-order moments indicates first-order dominance and what that implies about the marginal value of covariance.

## Removed Points
These points are flagged to be removed, treat them with caution:
- "DBSCAN parameters are fixed heuristics" — Removed because DBSCAN's adaptivity inherently comes from the density structure of the data; using 65th-percentile epsilon and minPts=4 is standard practice.
- "Oversimplification of existing methods as first-order only" — Removed as this is the paper's reasonable conceptual framing for motivating the contribution.
- "Hyperparameter tuning fairness for baselines" — Removed as too speculative; without evidence of asymmetric tuning, the unified codebase setup is a strength.
- "Missing related works" — Removed per policy (no external sources to verify existence).
- "Covariance compression being ad hoc" — Partially removed; while the 1D-conv approach lacks motivation, it is a practical engineering choice and the paper describes it clearly. Kept as a minor ablation gap.

## Novel Insights
The non-monotonic AUC pattern in Table 3 is a genuinely noteworthy observation: ABMIL achieves 98.88% AUC which exceeds both single-component ablations (w/o CM: 98.14%; w/o SOM: 98.51%), yet the full model reaches 99.23%. This synergy-over-additivity pattern has implications for how MIL ablations should be designed — simple "remove one component" ablations may fail to capture interaction effects.

## Suggestions
- Either apply attention weights to the covariance computation (C = Σ_k a_k g̃_k g̃_k^⊤) to match the "attention-weighted" framing, or explicitly acknowledge that the "weighting" comes from attention-dependent centering and adjust the framing accordingly.
- Add significance tests (paired t-test or permutation test on fold-level results) for all metric comparisons in Tables 1–3. If significance cannot be achieved with 5 folds, consider per-slide bootstrap evaluation for tighter confidence intervals.
- Discuss the non-monotonic AUC ablation result and provide additional analysis of what the second-order representation captures that the first-order does not (e.g., dimension-wise variance analysis, classifier probe, or visualization).

## Anchor Papers Retrieved

| Anchor | Score | Round | Comparison |
|--------|-------|-------|------------|
| Pg-GAT | 3.00 | R1 | WSI graph-based MIL, rejected for lack of novelty and insufficient baselines. HOMIL has clearer motivation and fairer evaluation. |
| Mamba-HMIL | 3.25 | R1 | WSI hierarchical MIL, rejected for component combination without motivation. HOMIL has better principled framing. |
| SMIL | 4.50 | R1 | Sequential MIL for clinical imaging, rejected for limited novelty and overclaimed interpretability. HOMIL has stronger efficiency claims and clearer methodology. |
| Set-level labels | 5.67 | R1 | MIL with histopathology application, accepted. HOMIL is comparable in quality with more comprehensive baselines. |
| MFC | 6.00 | R1 | WSI MIL causal framework on same datasets, accepted. HOMIL has clearer methodology but more central methodological inconsistency. |
| MIL for TSC | 8.00 | R1 | Interpretable MIL for time series, accepted. HOMIL is not as strong. |
| MI-PLL | 5.00 | R2 | MIL theory paper, rejected. HOMIL has stronger practical contributions. |
| VLSA | 5.67 | R2 | WSI pathology survival analysis with MIL, accepted. HOMIL has fairer evaluation but the attention-weighting inconsistency is a unique concern. |
| ViTally Consistent | 5.25 | R2 | Cell microscopy representation learning, rejected. Less directly relevant. |

**Round-1 bracket: 5.0–6.0.** HOMIL is above rejected 3.0–4.5 papers (clearer motivation, fair evaluation, better writing) but below accepted 5.5–6.0 papers due to the central methodological inconsistency in the attention-weighting claim.

**Final calibration: 5.5.** The paper has genuine contributions (principled statistical framing, dramatic efficiency gains, fair multi-baseline evaluation) but the attention-weighting inconsistency in the core method description and the unsupported "significant improvement" claim in the abstract are substantive issues that prevent a clear accept recommendation. These are fixable — addressing them would likely push the paper into the 6.0+ range.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>