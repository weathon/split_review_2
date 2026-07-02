## Summary
# Final Review Report

## Summary

This paper proposes TAK (Task Arithmetic with KFAC regularization), a dataless regularization method for weight disentanglement in task arithmetic. The core idea is to frame representation drift regularization as a curvature matrix approximation problem, leveraging Kronecker-Factored Approximate Curvature (KFAC) to penalize task-vector directions that would interfere with other tasks' representations — without requiring access to those tasks' training data. The authors derive the connection between representation drift and the generalized Gauss-Newton matrix, then adopt KFAC for practical computation. A key contribution is an aggregation heuristic that merges per-task KFAC factors into a single surrogate, achieving O(1) training-time complexity in the number of tasks. Experiments on vision (CLIP ViT, 8-dataset benchmark) and language (T5-base, 6 NLP tasks) demonstrate that TAK achieves strong performance in task addition and negation, matching or approaching data-dependent regularizers while being privacy-preserving and robust to scaling coefficient tuning.

## Strengths
1. **Clean theoretical framing.** The connection between representation drift regularization and the generalized Gauss-Newton matrix is well-derived and clearly explained. Starting from the linearized fine-tuning approximation, the paper shows that the drift penalty reduces to a quadratic form involving the Jacobian Gramian, then identifies this as an instance of the GGN. This progression from practical problem to theoretical object is pedagogically effective.

2. **Data-free regularization is practically motivated.** The central challenge — that existing regularizers (e.g., τ-Jp) require external task data — is well-motivated by privacy, modularity, and decentralized training constraints. The proposed solution (pre-computing KFAC matrices once per task and sharing only the factorized curvature information) is elegant and directly addresses this limitation.

3. **Constant-complexity aggregation heuristic.** The Kronecker-factor merging scheme (Eq. 8), while theoretically inexact, is practically valuable. Table 3 shows that the accumulated regularizer closely matches the O(T) naïve multi-task formulation across ViT-B/16, ViT-B/32, and T5-base, with marginal degradation at most 0.7 absolute points. This makes the approach scalable to many tasks.

4. **Comprehensive evaluation across modalities.** Experiments cover vision (CLIP ViT-B/32, B/16, L/14 on 8 datasets) and language (T5-base on 6 tasks), in both linearized and non-linear fine-tuning regimes. The inclusion of task negation (unlearning), α-robustness analysis, and compression trade-offs (Fig. 7b) provides a well-rounded empirical picture.

5. **Practical efficiency.** The KFAC estimation using MC=1 and 128 examples per task takes only 4 minutes total, and the Kronecker-factor merging keeps training memory O(1) in task count. The analysis of applying the regularizer every N steps (Fig. 8) further demonstrates practical deployability.

6. **Task localization insight.** The qualitative analysis in Figure 5 showing that TAK separates in-distribution from out-of-distribution Jacobian-vector norms is interesting and suggests potential for OOD detection as a secondary application.

## Weaknesses
### W1. No variance or statistical significance reported (Critical)
Across all experiments — task addition (Table 1), task negation (Table 2), language tasks (Table 3a), and ablation studies — only point estimates are reported without standard deviations, confidence intervals, or significance tests. This is a critical omission because several comparisons show very small margins (e.g., TAK vs. τ-Jp on ViT-B/32: 86.0 vs 85.6; on ViT-B/16: τ-Jp actually leads in normalized accuracy 98.7 vs 98.1). Without variance information, readers cannot determine whether the claimed improvements are statistically reliable or within noise. This undermines the central performance claims, including the "state-of-the-art" assertion in the abstract.

**Severity:** Critical — affects all performance conclusions.  
**Required fix:** Report mean ± std over ≥3 random seeds for all main table entries. Add paired significance tests (e.g., Wilcoxon signed-rank) for TAK against the strongest baseline. If multi-seed experiments are infeasible, report min/max across seeds and explicitly acknowledge the limitation.

### W2. Accumulated regularizer is an unverified heuristic (Major)
Equation (8) merges per-task Kronecker factors via $(\sum B_t^l) \otimes (\sum \lambda_t A_t^l)$, which does not mathematically equal $\sum \lambda_t (B_t^l \otimes A_t^l)$. The Kronecker product does not distribute over addition, so this is always an approximation. While Table 3 shows the gap is small for 8 tasks, no theoretical bound or error analysis is provided. For larger task sets with heterogeneous curvature (e.g., mixing vision and language tasks), the approximation could degrade unpredictably.

**Severity:** Major — limis confidence in scalability claims.  
**Required fix:** (a) Analyze the approximation error as $\|\sum \lambda_t B_t^l \otimes A_t^l - (\sum B_t^l) \otimes (\sum \lambda_t A_t^l)\|_F$ on representative layer blocks. (b) Test with T > 8 more diverse tasks to stress-test the heuristic. (c) Provide conditions under which the approximation is provably tight (e.g., proportional per-task factors).

### W3. Non-linear regime justification is theoretically weak (Major)
The paper applies TAK regularization to non-linear fine-tuning by pairing it with Attention-Only Fine-Tuning, claiming this induces "approximately linear fine-tuning dynamics." However, no quantitative measurement of the residual nonlinearity is provided for the specific architectures used (CLIP ViT, T5-base). Terms like "kernel-like behavior" and "approximately linear dynamics" remain vague without empirical backing. The observed gains in the non-linear regime (Attn. Only FT + TAK outperforming Attn. Only FT alone) could stem from additional regularization rather than curvature-specific effects.

**Severity:** Major — weakens the claimed applicability scope.  
**Required fix:** (a) Quantify linearity error $\|f(x,\theta) - f_{\text{lin}}(x,\theta)\|/\|f(x,\theta)\|$ over training for attention-only FT vs. full FT. (b) Compare TAK against a simpler L2 regularizer on task vectors under the same non-linear setup to isolate curvature-specific effects. (c) If the theoretical justification remains heuristic, explicitly bound the applicability claim.

### W4. "State-of-the-art" claim is unbounded and unverifiable (Major)
The abstract and introduction claim "state-of-the-art results in task addition and negation." This assessment is based on comparisons against τ-Jp, Diag. GGN, TaLoS, Attention-Only FT, and three post-hoc merging methods. However, external literature verification is unavailable in this run (retrieval disabled), and even within the compared set, TAK does not uniformly outperform τ-Jp (e.g., normalized accuracy on ViT-B/16 favors τ-Jp). The SOTA claim should be bounded to the evaluated benchmarks and comparison set.

**Severity:** Major — overclaim without sufficient evidence breadth.  
**Required fix:** Replace "state-of-the-art" with context-bounded wording (e.g., "competitive with or exceeding existing data-dependent regularizers on the evaluated benchmarks"). Conduct a broader literature survey to substantiate any global SOTA claim.

### W5. Task localization analysis is qualitative only (Minor)
Figure 5 shows histograms of Jacobian-vector norms for in-distribution vs. out-of-distribution examples, visually suggesting better separation under TAK. However, no quantitative metric (AUROC, average precision, Jensen-Shannon divergence) is reported. The claim of "clear separation" is supported only by visual inspection.

**Severity:** Minor — interesting finding but incomplete.  
**Required fix:** Report AUROC per task with the normalcy score $s(x) = -\|J_\theta f(x,\theta_0) \tau_t\|_2^2$ under both Linear FT and TAK. Compare against simple baselines (e.g., maximum softmax probability).

### W6. Conclusion introduces unsupported future directions (Minor)
The conclusion mentions "gradient accumulators of the adaptive optimizer used for training" as an analogous asset to KFAC matrices, but this concept is not discussed anywhere in the paper body. Introducing new technical directions in the conclusion without prior analysis reduces focus on validated contributions.

**Severity:** Minor — editorial issue.  
**Required fix:** Move the optimizer-state discussion to a "Future Work" subsection or remove from conclusion. Keep the conclusion focused on validated findings and concrete limitations.

### W7. No dedicated Related Work section (Minor)
The paper lacks a standalone related-work section. Comparisons to prior methods are scattered across the introduction (Dhawan et al., 2023; Ortiz-Jimenez et al., 2023; Yoshida et al., 2025) and experimental sections (τ-Jp, TaLoS, Attention-Only FT, TIES, TSV, ISO). This makes it harder for readers to understand the full landscape and the paper's precise positioning.

**Severity:** Minor — readability issue.  
**Required fix:** Add a dedicated Related Work section organized around thematic axes (e.g., weight disentanglement, data-free regularization, post-hoc merging, curvature approximation) rather than paper-by-paper summaries.

## Score
**Final Score: 6/10**

**Scoring Rationale:**

The paper presents a technically sound and practically motivated method for data-free weight disentanglement in task arithmetic. The core idea — linking representation drift regularization to KFAC-based GGN approximation — is novel and well-executed. The empirical evaluation is broad (vision + language, multiple backbones, task addition + negation + ablation) and the practical efficiency analysis (KFAC estimation cost, compression, α-robustness) adds significant value.

**However, the score is constrained by the following factors:**

1. **No statistical reporting** (critical): The absence of variance information across all experiments fundamentally limits confidence in the reported rankings. Several comparison margins are small (<0.5 points), so without significance testing, the claimed advantages may not be robust.

2. **Unbounded "state-of-the-art" claim**: Without external literature verification (retrieval unavailable in this run) and without uniformly outperforming the main baseline (τ-Jp leads on ViT-B/16 normalized accuracy), the SOTA claim overreaches the evidence.

3. **Heuristic approximation without theoretical support**: The Kronecker-factor merging scheme (Eq. 8) lacks theoretical error bounds, leaving scalability to large/diverse task sets uncertain.

4. **Weak non-linear regime justification**: The extension to non-linear fine-tuning relies on an unquantified "approximate linearity" claim, weakening the paper's claimed applicability scope.

**Research value assessment:** The paper provides meaningful new knowledge (connecting curvature approximation to data-free disentanglement) and has good potential for practical impact (enabling privacy-preserving multi-task model merging). The reproducibility is reasonable given the level of experimental detail. The primary weaknesses are in evidence completeness (missing variance, unverified SOTA claim) rather than in the core methodological contribution.

**Strengths vs. Weaknesses balance:** The core contributions are solid and the experimental breadth is commendable. The weaknesses are fixable with additional experiments (multi-seed reporting, controlled ablations, theoretical analysis of the merging heuristic). With these addressed, the paper would warrant a significantly higher score (target range: 7-8/10).