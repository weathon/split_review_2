## Summary

This paper studies a practical yet under-explored problem in Multi-modal Entity Alignment (MMEA): Dual-level Noisy Correspondence (DNC), where noise exists in both intra-entity (entity-attribute) and inter-graph (entity-entity and attribute-attribute) correspondences. The authors propose RULE, a framework that estimates correspondence reliability through a two-fold principle combining uncertainty (Dempster-Shafer theory) and consensus (marginal contribution), then uses these reliabilities to perform robust attribute fusion and discrepancy elimination. A test-time MLLM reasoning module further uncovers latent attribute-attribute connections. Experiments on five benchmarks with seven baselines show substantial gains over existing methods.

## Strengths

- **The DNC problem is well-motivated and practically relevant.** The paper identifies a genuine blind spot in the MMEA literature: existing methods assume faultless intra-entity and inter-graph correspondences, while real-world MMKGs contain substantial noise at both levels (over 50% NC in ICEWS benchmarks). The concrete example in Fig. 1(a) clearly illustrates the problem.

- **The reliability estimation framework combining uncertainty (Dempster-Shafer) and consensus (marginal contribution) is technically creative and validated by ablation.** Table 3 confirms both principles contribute: "Only Unc." (53.5 H@1) and "Only Cons." (48.3) each outperform "w/o DRL" (31.6). The visualization in Fig. 4 confirms clean separation of U/I/C subsets in the uncertainty-consensus plane.

- **The test-time correspondence reasoning (TTR) module using MLLM + CoT is a genuinely novel addition to the MMEA pipeline.** It addresses a real failure mode (e.g., linking "Cristiano Ronaldo" to attributes like "football player" and "Mexico") that training-time methods cannot fix. Ablation confirms non-trivial gains (1–4 points depending on setting).

- **Experimental breadth is strong.** Five benchmarks (ICEWS-WIKI, ICEWS-YAGO, DBP15K ZH/JA/FR-EN), two evaluation protocols (Non-name / All-attributes), three noise levels (inherent, 20%, 50%), and seven baselines. The degradation curves in Fig. 3(a) (noise ratio 0.0 to 0.7) convincingly show RULE degrades more gracefully than alternatives.

## Weaknesses

### Fatal

None.

### Major

- **The test-time MLLM creates an asymmetric comparison that undercuts the stated fairness claim.** Section 3.2 states: "For fair comparisons, we adopt the same backbone (i.e., CLIP) for all baselines and our method." This statement is technically true for the encoder backbone, but the TTR module uses Qwen2.5-VL-72B, a 72B-parameter model that baselines do not receive. The main comparison tables (Tables 1–2) report "Ours" with TTR included, conflating the training-time robust learning method with the benefit of a large MLLM at inference time. Ablation (Table 3) shows TTR contributes 3.7 H@1 points on the All-attributes setting (94.0 → 97.7). **However, the core training-time method remains competitive on its own:** the "w/o TTR" variant (56.5 Non-name H@1 at 50% DNC on ICEWS-WIKI) substantially beats the best baseline MEAformer (42.4). The issue is primarily about presentation fairness: the paper should separate TTR from the main comparisons, present results without TTR as the primary comparison, and show TTR as a clearly flagged add-on.

### Minor

- **The self-adaptive thresholding (Eq. 8) has a bootstrapping dependency that is not acknowledged.** The set S^{TP} used to set thresholds β_u and β_c is defined as pairs where argmax(s_i) = argmax(y_i) — i.e., where the current model's prediction agrees with the annotated correspondence. When up to 50% of annotations are noisy, this bootstraps on the model's own ability to identify clean samples. This is a standard technique in noisy-label learning (small-loss heuristics), but the paper does not discuss this limitation or potential failure modes (e.g., early in training or under extreme noise where the model itself is unreliable).

- **The ablation scope is limited, and many design choices lack empirical justification in the main paper.** The ablation (Table 3) tests only five high-level variants on a single dataset (ICEWS-WIKI) at a single noise level (50% DNC). Key design decisions — the tanh in Eq. 2 (evidence function), the initial subset size |π_0| = ⌊M/2+1⌋, the fixed γ=0.5 in Eq. 1 — are not empirically motivated in the main text. The hyperparameter study is deferred to appendices that are not available in this version.

- **The All-attributes setting is near ceiling.** At 50% injected DNC, MEAformer still achieves 94.7% average H@1 and RULE achieves 97.9% (Table 2). Fig. 5 does confirm E-A NC in name attributes, partially addressing whether names are corrupted. However, the paper does not report per-modality corruption rates, making it hard to assess the effective noise level and whether the most informative modality is sufficiently degraded.

- **Assumption 1 in consensus modeling ("correctly associated → Δ ≥ 0; irrelevant → Δ < 0") is strong and may not hold universally.** Adding a correct attribute may not always improve the average similarity if attributes have different discriminative power or if model representations are imperfect. The paper does not discuss failure modes for this assumption.

- **There is a conceptual tension between the formal definition of attribute-attribute NC and the noise injection strategy.** The formal definition (Section 2.1) makes attribute-attribute NC entirely derivative (requiring correct entity-attribute and entity-entity correspondences). But the noise injection (Section 3.1) treats attribute-attribute NC as a distinct type with independent perturbations. This raises the question of whether the injected noise creates a different structure than what naturally occurs.

### Trivial

None.

## Nice-to-Haves

- Report computational cost or inference latency for the TTR module (Qwen2.5-VL-72B), since it is a large model that may be prohibitive for practical applications.
- Apply equivalent MLLM post-processing to the strongest baselines to create a completely fair comparison and demonstrate that the training-time method provides value beyond a strong MLLM.
- Add brief empirical motivation for the key design choices (tanh in Eq. 2, subset size ⌊M/2+1⌋, fixed γ=0.5) in the main paper, even if detailed sensitivity is in the appendix.

## Removed Points

These points are flagged to be removed; treat them with caution.

- **DBP15K garbled column labels in Table 2**: The column headers show "DBP15K <sub>GEN</sub>" repeated three times. This is a plain-text extraction artifact from LaTeX subscript rendering. Section 3.1 explicitly lists ZH-EN, JA-EN, FR-EN. [REMOVED: parser artifact]
- **Missing appendix content (CoT prompt design, hyperparameter study, proofs)**: The parser strips appendices/references from all papers; these exist in the original submission. [REMOVED: parser artifact]
- **Statistical significance absent**: Error bars and significance tests are not standard for large-scale entity alignment benchmarks where single-run evaluation is the norm. [REMOVED: community-standard practice]
- **"One of the first methods" claim overwrought**: This is a subjective assessment of phrasing, not a scientific weakness. [REMOVED: subjective]
- **Missing CoT prompt details**: The appendix (where these reside) was removed by the parser. [REMOVED: parser artifact]

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Restructure the main comparison**: Present a table of RULE (training-time components only, without TTR) vs. baselines, then show the incremental benefit of TTR as a clearly separated second table. This would make the comparison transparent and prevent conflation of the two contributions.
2. **Acknowledge the bootstrapping assumption** in Eq. 8 explicitly, noting that S^{TP} relies on the model's ability to identify clean samples and discussing what happens when this assumption fails (e.g., early training stages or under extreme noise).
3. **Report per-modality corruption rates** to clarify the effective noise level in each setting and confirm that the most informative modalities are sufficiently degraded.
4. **Add brief empirical motivation** for key design choices (tanh in Eq. 2, subset size ⌊M/2+1⌋, fixed γ=0.5) in the main body, even if detailed sensitivity analysis is relegated to the appendix.
5. **Discuss failure modes of Assumption 1** and how the method handles cases where correct attributes do not improve average similarity.

## Score and Decision

**Calibration anchors used:**

| Path | Avg Score | Round | Itemized? | Comparison |
|------|-----------|-------|-----------|------------|
| /home/.../z3dfuRcGAK.md | 6.67 | R1 | Yes | EA with generative models; less experimental breadth but similar topic. Paper under review has stronger breadth and clearer problem motivation. |
| /home/.../QQYpgReSRk.md | 6.25 | R1 | Yes | Noisy entity-annotated images; had a massive (−12.56) weakness about limited technical novelty. Paper under review has stronger technical novelty. |
| /home/.../9Cu8MRmhq2.md | 8.00 | R1 | Yes | Noisy correspondence in video-language; all weaknesses were minor/trivial. Paper under review has more significant weaknesses (TTR fairness, limited ablation). |
| /home/.../TPZRq4FALB.md | 8.00 | R1 | Yes | Test-time adaptation for multi-modal reliability bias; all weaknesses minor. Paper under review has stronger method weaknesses by comparison. |
| /home/.../NNUiUwQWx6.md | 5.75 | R2 | Yes | Neuro-symbolic EA; has more significant weaknesses (outdated datasets, missing comparisons). Paper under review is clearly stronger. |

**Round-1 bracket:** [6.67, 8.00]. The paper is clearly stronger than the 5.75–6.67 range (stronger technical novelty than QQYpgReSRk, better experiments than z3dfuRcGAK), but has more significant weaknesses than the 8.00 anchors (whose weaknesses were uniformly minor/trivial).

**Final score determination:** The most impactful negative-weight items in the draft are "ablation scope limited" (−4.14) and "self-adaptive thresholding bootstrap" (−1.93). These are comparable in magnitude to the strongest negatives of mid-range anchors. The "TTR fairness" weakness has weight −0.91, confirming it is a significant-but-not-fatal presentation issue. Counterbalanced by strong positives (+4.90 for reliability framework, +5.81 for TTR novelty, +4.54 for experimental breadth), the paper sits above the 6.25–6.67 range but below the 8.00 ceiling. **Score: 7.0 — a clear accept with required presentation fixes.**

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>