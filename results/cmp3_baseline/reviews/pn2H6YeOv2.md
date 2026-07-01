## Summary

Pi-CCA reframes forgetting in continual vision-language learning as drift in the cross-modal alignment geometry, and introduces a compact, replay-free certificate that stores the top-\(k\) canonical correlations and a sketch of the canonical subspaces from a frozen pre-trained model. During adaptation, the certificate is used to penalize spectral and subspace drift through losses that operate on mini-batch statistics, while a prompt-invariance term averages text-side projectors over synthetic perturbations. The method is compatible with parameter-efficient tuning (LoRA) and achieves state-of-the-art performance among replay-free approaches on MTIL, X-TAIL, VLCL, and ConStruct-VL.

## Strengths

- **Novel and principled formulation**: The paper correctly identifies that prior VL-CL methods regularize proxy quantities (logits, similarities, weights) rather than the cross-modal alignment geometry that actually underlies zero-shot generalization. Preserving the canonical spectrum and subspaces of the whitened cross-covariance is a well-motivated, geometry-first alternative.
- **Replay-free with constant memory**: The sketched CCA certificate has size \(O(hk)\) independent of feature dimensions and requires no stored examples, generators, or task-specific metadata. This makes the method practical for privacy-sensitive and resource-constrained deployment.
- **Strong empirical validation**: Pi-CCA outperforms a comprehensive set of recent replay-free baselines (C-CLIP, MG-CLIP, Proxy-FDA, LADA, DIKI, RAIL, ZAF, DDAS, ZSCL, Mod-X) across all four evaluated tracks, often by clear margins. Retrieval results are competitive even with a synthetic-replay method (GIFT), and the structured-concept results (ConStruct-VL) confirm benefits beyond classification and retrieval.
- **Thorough analysis**: Single-factor ablations (Table 3) isolate the contribution of each loss term and EMA component. The certificate capacity Pareto analysis (Figure 2) demonstrates a clear efficient frontier, and the geometric drift vs. performance correlation (Figure 3), while very high, supports the central thesis. Task-order sensitivity (Figure 5) is explicitly tested and robust, and the prompt-invariance stress test (Figure 4) provides actionable insight.

## Weaknesses

### Fatal

None.

### Major

1. **Near-perfect geometric drift–performance correlation appears circular**: Figure 3 reports Pearson \(r \approx 1.00\) and Spearman \(\rho \approx 1.00\) between subspace/spectral drift and performance drops. Because the training objective explicitly minimizes those same drift measures, the high correlation is nearly tautological: the model is being optimized to keep them small, so they naturally co-vary with performance. This weakens the claim that geometry preservation _predicts_ retention in a causal, independent sense. A more convincing analysis would compare drifts of models trained with different objectives (e.g., other baseline methods) against their performance drops, rather than only within the Pi-CCA family.

2. **Prompt-invariance gains are modest**: The invariance loss improves R@1 by \(\approx 2.5\) p.p. and reduces AF by \(\approx 1.0\) under strong perturbations. While directionally positive, the absolute effect is modest, especially given the additional hyperparameter (\(\eta\), \(M\)) and computational cost of processing multiple perturbations per step. The paper would benefit from a discussion of the practical trade-off (e.g., compute vs. robustness) and whether similar robustness could be achieved with simpler augmentation strategies.

3. **Choice of \(k\) and \(h\) is entirely empirical**: The Pareto analysis shows that \((k,h)=(64,256)\) is near the knee, but no principled criterion is given for selecting the certificate rank. A model-agnostic rule (e.g., based on cumulative explained variance of the canonical correlations, or a target sketch error bound) would strengthen the method. As presented, the user must sweep to find a good operating point, which could be a barrier in practice.

### Minor

1. **The use of “invariant” is slightly imprecise**: The certificate is not invariant under all distribution shifts; it is a _constraint_ that penalizes drift relative to a reference computed once. The label “invariant” is defensible (the losses encourage invariance to new tasks and prompts), but it could mislead readers into expecting exact preservation.

2. **Sensitivity of the prompt-invariance loss to the perturbation set \(\mathcal{P}\)**: The choice of anchor prompts and perturbation distribution will affect the resulting \(\bar{\mathbf{Q}}_t^*\) and thus the behavior of \(\mathcal{L}_{\text{pi}}\). While the paper tests ID vs OOD templates, a broader sensitivity study over perturbation families (e.g., synonym rates, back-translation languages, number of perturbations \(M\)) is not provided in the main paper.

3. **Missing comparison on zero-shot retention benchmarks**: The performance drop (PD) on a held-out zero-shot suite is mentioned in §4.1 as a metric but is only partially reported (e.g., in the prompt stress test). Tables 1 and 2 could include PD as a column to give a fuller picture of forgetting.

### Trivial

- The paper uses double parentheses notation like \((\text{↑})\) in tables, which is visually dense but not a barrier.

## Nice-to-Haves

- Verify the geometric drift correlation across multiple baseline methods, not just Pi-CCA variants, to strengthen the causal claim.
- Provide a rule-of-thumb for selecting \(k\) and \(h\) (e.g., based on explained variance or budget).
- Report zero-shot performance drop (PD) in the main tables for all benchmarks.

## Novel Insights

The core insight—that forgetting in VL-CL can be characterized as drift in the canonical geometry of the whitened cross-modal covariance, and that constraining this drift by a compact sketched certificate yields strong retention without replay—is genuinely novel and well supported. The paper also provides useful empirical evidence that preserving both the spectrum and the subspace directions is critical, and that prompt sensitivity can be reduced by averaging projectors over perturbations rather than by learning additive prompts. The Pareto analysis demonstrating that a relatively small certificate (e.g., \(k=64, h=256\)) suffices for current benchmarks is a practical contribution.

## Suggestions

1. **Clarify the causal interpretation of the geometry–performance correlation.** Provide supplementary experiments where drift measures are computed for baseline methods (e.g., C-CLIP, RAIL) and plotted against their performance drops. This would show whether the correlation holds across different training strategies, or whether it is simply a consequence of Pi-CCA’s loss design.
2. **Discuss practical guidelines for selecting certificate capacity without a sweep.** Consider adding a simple heuristic such as “choose \(k\) such that \(\sum_{i=1}^k \rho_i^* / \sum_{i=1}^{\min(d_v,d_t)} \rho_i^* \geq 0.8\)” or “set \(h = 4k\)” and validate it retroactively.
3. **Report all four main metrics (Avg, Last, Transfer, PD) consistently in each row of Tables 1 and 2,** so that readers can assess zero-shot retention directly without searching appendices.

## Score and Decision

**Score:** 8

**Decision:** Accept

This paper makes a significant and principled contribution to continual learning for vision-language models. The geometry-based certificate idea is novel, the method is replay-free and parameter-efficient, and the empirical results are strong across a diverse set of benchmarks. The major weakness—the near-perfect correlation that may be partly tautological—does not invalidate the approach; it primarily limits one of the interpretive claims. The prompt-invariance gains are modest but genuine. Overall, the paper provides clear evidence that directly preserving cross-modal alignment geometry is an effective strategy, and it is likely to influence future work in this area.

MY FINAL SCORE: 8
MY FINAL DECISION: Accept