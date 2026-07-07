Now let me produce the final consolidated review.

## Final Review: Multi-Instance Learning for Whole-Slide Image Classification Using Higher-Order Moments

---

## Summary
This paper proposes HOMIL, a framework that augments attention-based multiple instance learning (ABMIL) for whole-slide image classification with second-order moment (covariance) information. The authors frame ABMIL's attention-weighted aggregation as a first-order moment estimator and argue that adding second-order statistics captures feature variability missed by mean-only aggregation. To maintain computational tractability, DBSCAN adaptively clusters patches into variable-sized groups, reducing the number of entities the attention mechanism must process. Experiments on CAMELYON16 (metastasis detection) and TCGA-NSCLC (lung cancer subtyping) show consistent accuracy improvements over nine MIL baselines, together with competitive runtime.

---

## Strengths

1. **Clear statistical framing (Sections 3.1–3.2).** The paper correctly identifies ABMIL's attention-weighted aggregation as a first-order moment estimator and motivates second-order statistics from a coherent statistical perspective. The connection between attention weights and probability-like distributions is pedagogically clean and provides solid motivation for the proposed extension.

2. **Computational efficiency via DBSCAN is demonstrated concretely.** On CAMELYON16, HOMIL runs in 310s (5-fold total) versus ABMIL's 455s — roughly 30% faster while reporting higher accuracy. On TCGA-NSCLC, the speed advantage is smaller but present (3685s vs 4056s). Tables 1 and 2 usefully report runtime alongside accuracy.

3. **Ablation study (Table 3) separates the contributions of the clustering module (CM) and the second-order moment module (SOM).** The full model outperforms both ablated variants, confirming that both components contribute. This is the minimal necessary control and the paper provides it.

---

## Weaknesses

### Major

1. **No statistical significance testing despite claiming "significantly improves."** The Abstract and Section 5.3 claim that HOMIL significantly outperforms baselines. However, metrics are reported as mean ± SE over only 5 folds. For CAMELYON16, HOMIL ACC is 96.98 ± 2.43 versus ABMIL's 94.72 ± 2.18. With n=5, the 95% confidence intervals overlap substantially, and the same pattern holds for AUC and F1 on both datasets. The paper provides no significance test (paired t-test, McNemar, permutation test, or similar) to support its central claim. This does not mean the improvements are illusory — the consistent direction across all metrics and both datasets is noteworthy — but the claim of significance as stated is unsupported by the presented evidence.

### Minor

2. **The "attention-weighted covariance matrix" label is imprecise.** In Section 4.3.3, the covariance matrix is computed as C = Σ (g_k − v^(1))(g_k − v^(1))^⊤, where v^(1) = Σ a_k g_k is the attention-weighted mean. The attention weights a_k do **not** appear in the outer-product summation; only the centering uses the attention-weighted mean. The paper calls this an "attention-weighted covariance matrix" at lines 108 and 147, which is misleading — it is an unweighted scatter matrix around an attention-weighted mean. While the centering does incorporate attention, a genuine attention-weighted covariance would weight each term by a_k. The authors should either include the attention weights in the summation or explicitly justify the unweighted formulation.

3. **Gap between motivation (patch-level covariance) and implementation (cluster-level covariance).** Section 3.2 motivates the approach by discussing the covariance of **patch** representation vectors {h_i} (line 71–73). However, Section 4.3.3 computes the covariance of **cluster** features {g_k}, which are mean-pooled representations of all patches within each cluster. A cluster containing 5,000 normal-tissue patches contributes one vector, the same as a cluster with 1 pathological patch. The paper does not discuss what information is lost — or what is gained — by operating at the cluster level rather than the patch level for the covariance computation. This discrepancy should be acknowledged and justified.

4. **Covariance-to-vector compression is unablated for alternatives.** The paper compresses the d×d covariance matrix to a d-dimensional vector via Conv1D+max-pooling (m=64, T=4) with no rationale for this specific design. Table 3 ablates the entire SOM module but does not test simpler alternatives (e.g., flattening the upper triangle, eigenvalue decomposition, compact bilinear pooling). A reader cannot tell whether performance depends critically on this vectorization scheme.

---

### Trivial

None.

---

## Nice-to-Haves

- **Multi-class evaluation.** Both datasets are binary (metastasis vs. normal; LUAD vs. LUSC). Testing on a multi-class WSI dataset (e.g., TCGA kidney cancer subtypes) would strengthen the generality claim.
- **Simpler second-order baseline.** A baseline that concatenates the variance (diagonal of the covariance) with the first-order mean would provide a more direct test of whether second-order statistics add value beyond a straightforward extension.
- **Clustering quality analysis.** The paper reports compression ratios (0.18, 0.16) but does not analyze whether DBSCAN clusters correspond to semantically meaningful tissue types. Such analysis would validate that the adaptive grouping is meaningful, not just computationally convenient.

---

## Removed Points

- **Missing related work on covariance pooling** (Bilinear CNNs, DeepO₂P, etc.): Removed per instructions — these are from fine-grained visual recognition, a different scope, and this reviewer cannot verify their existence externally. Also scope-mismatched for MIL-based WSI analysis.
- **"ABMIL becomes a special case" claim is "misleading":** Removed — the claim is technically correct when each cluster contains one patch and only first-order information is used.
- **"Appendix would clarify hyperparameter choice":** Removed per instructions (parser strips appendix sections; they exist in the original submission).
- **Formatting/style nitpicks:** Removed per instructions (parser artifacts, not author errors).
- **Generic strengths** (e.g., "important problem"): Removed as too generic to be informative.

---

## Novel Insights

None beyond the paper's own contributions. The main novel observation surfaced by the review — that the covariance computation operates on cluster centroids rather than patches, creating a gap between the stated motivation and the implementation — is accurate and has been included as a Minor weakness above.

---

## Suggestions

1. **Add statistical significance testing.** A paired t-test on per-fold metrics (or a non-parametric alternative like the Wilcoxon signed-rank test) is the minimum bar. If results are not significant at conventional levels, soften the "significantly improves" claim accordingly.
2. **Fix the covariance terminology.** Either make the summation genuinely attention-weighted (include a_k in the sum) or rename the quantity to "scatter matrix around the attention-weighted mean" and justify the unweighted formulation.
3. **Address the patch-level vs. cluster-level gap.** Acknowledge explicitly that the covariance captures between-cluster rather than between-patch variability, and discuss what is gained (computational efficiency, reduced noise) and what may be lost (fine-grained patch-level interactions).
4. **Ablate the vectorization method.** Compare the Conv1D+max-pooling compression against at least one simple alternative (e.g., flattening the upper triangle + linear projection).

---

## Score and Decision

**Calibration anchors used (all rounds):**

| Path | Avg Score | Round | Itemized? | Comparison |
|------|-----------|-------|-----------|------------|
| `5lUdTogEL3.md` (Person Re-ID) | 1.00 | 1 | No | Topically unrelated; very low score |
| `0yVP49SDg0.md` (Mamba-HMIL) | 3.25 | 1–2 | Yes | MIL for WSI; criticized for poor writing/novelty — HOMIL is cleaner and better motivated |
| `Ng4HaH4L6P.md` (SlideChat) | 3.40 | 1 | Yes | WSI VQA; different task but similar domain — HOMIL has stronger evidential basis |
| `jHdsZCOouv.md` (SHAP-CAT) | 3.40 | 1 | Yes | WSI classification; flawed experimental setup (no std dev) — HOMIL is more rigorous |
| `lo9HMoGNwQ.md` (Seq. MIL) | 4.50 | 2 | Yes | MIL for medical imaging; unclear clinical framing — HOMIL has clearer motivation |
| `T7ZVzuObcj.md` (PointMIL) | 5.50 | 2 | Yes | MIL for point clouds; limited novelty (-9.28) — HOMIL's novelty is better scoped |
| `6xrDPHhwD3.md` (MFC Freq Domain) | 6.00 | 1–2 | Yes | MIL for WSI; severe method clarity issues (-9.79) and no uncertainty measures (-6.24) — HOMIL is cleaner but shares the evidential gap |

**Round 1 bracket:** 4.5–6.0. Narrowed to 5.5 based on weighted-item comparison: HOMIL's weaknesses are less severe than the MFC anchor's (6.00) worst negatives, but the unaddressed significance gap prevents reaching the MFC's score. HOMIL's writing, motivation, and method clarity are stronger than the Mamba-HMIL (3.25) and SHAP-CAT (3.40) anchors.

The paper presents a well-motivated contribution with clean exposition and consistent empirical results, but the lack of statistical significance testing for the claimed improvements is a notable evidential gap that prevents a stronger score.

**MY FINAL SCORE: <score>5.5</score>**
**MY FINAL DECISION: <decision>Accept</decision>**