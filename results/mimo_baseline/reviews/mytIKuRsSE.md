## Summary

This paper introduces Dual-level Noisy Correspondence (DNC) in Multi-Modal Entity Alignment (MMEA), identifying that real-world MMKGs contain noise both within entity-attribute associations and across entity/attribute correspondences between graphs. The authors propose RULE, which estimates correspondence reliability via uncertainty (Dempster-Shafer theory) and consensus principles, uses these to robustly fuse intra-entity attributes and eliminate inter-graph discrepancy, and adds a test-time MLLM-based reasoning module to uncover latent attribute connections across graphs. Experiments on five benchmarks with seven baselines demonstrate strong improvements, particularly under high noise ratios.

## Strengths

- **Well-motivated and novel problem formulation.** The DNC problem is clearly defined, practically important, and under-explored. The authors provide compelling evidence that existing benchmarks contain substantial noise (e.g., >50% in ICEWS, cited from Appendix B), and empirically demonstrate in Figure 1(b) that both intra-entity and inter-graph noise degrade baselines significantly. This goes beyond prior noisy correspondence work that typically considers only a single level.

- **Principled reliability estimation framework.** The two-fold principle combining uncertainty (from Dempster-Shafer/Subjective Logic) and consensus is well-grounded. Theorem 1 provides a clear justification for why uncertainty alone is insufficient, motivating the consensus addition. The pair division into S_U, S_I, and S_C with tailored loss strategies (Eqs. 11-12) is a clean and well-motivated design. Figure 4 visually confirms that these two dimensions successfully separate noisy from clean subsets.

- **Consistently strong empirical results.** RULE outperforms all seven baselines across all five benchmarks and all noise settings (0%, 20%, 50%). On ICEWS-WIKI Non-name with 50% DNC, RULE achieves 58.2 H@1 vs. 43.9 for the second-best (HHREA), a 14+ point margin. Even on inherently noisy data without injected noise, RULE improves over the strongest baseline PMF by 5.2 points on ICEWS-WIKI (64.2 vs. 52.6 H@1). The performance degradation curves in Figure 3(a) confirm much slower degradation as noise increases.

- **Thorough ablation and analysis.** Table 3 systematically removes each component (DRL, DRF, uncertainty-only, consensus-only, TTR), clearly quantifying each contribution. Figures 3(b) and 5 provide interpretable visualizations of reliability distributions and fusion weights, confirming the method behaves as intended. The clean vs. noisy pair separation in Figure 3(b) is particularly convincing.

## Weaknesses

### Fatal

None.

### Major

- **Computational cost and scalability of test-time reasoning.** The TTR module uses Qwen2.5-VL-72B-Instruct, a 72B-parameter MLLM, requiring CoT-based inference for top-K candidate attribute pairs per query entity. The paper provides no runtime analysis, no discussion of latency, and no analysis of how many MLLM calls are needed per query. For practical deployment on large MMKGs (e.g., DBP15K has 15K+ entities per graph), this could be prohibitively expensive. While the ablation shows TTR contributes modestly (~1.7 H@1 on Non-name), the cost-benefit tradeoff is entirely unaddressed.

- **Potential circularity in self-adaptive threshold computation.** The thresholds β_u and β_c (Eq. 8) depend on S^TP = {i | argmax(s_i) = argmax(y_i)}, which relies on current model predictions matching ground truth. Early in training when the model is most affected by noise, S^TP identification may be unreliable, potentially causing the thresholds to be poorly calibrated. The paper does not discuss training dynamics, convergence of these thresholds, or whether a warm-up strategy is needed.

### Minor

- **Strength of Assumption 1.** The marginal contribution approach (Eq. 6-7) assumes correctly associated attributes always yield non-negative marginal contribution Δ ≥ 0. This could be violated when an attribute is correctly associated but shared across many entities (e.g., common attributes like "human" or "city"), providing no discriminative signal. While empirically supported, a sensitivity analysis of the greedy strategy's accuracy would strengthen the claim.

- **Noise injection is somewhat simplistic.** The artificial noise uses random entity replacement and Gaussian noise for images, which may not reflect real-world distribution of noise (e.g., visually similar but incorrect images, as in the "Jason Momoa" vs. "Elvis Tsui" example). The gap between synthetic and inherent noise behavior could be further studied.

- **DBP15K improvements are more modest.** While ICEWS gains are large (10-20+ points), DBP15K improvements are typically 1-3 percentage points over PMF/MEAformer, suggesting the method's advantage is most pronounced on noisier datasets. This relative performance difference across datasets could be better discussed.

### Trivial

None.

## Nice-to-Haves

- A runtime comparison table showing inference cost with and without TTR, and how this scales with graph size.
- Analysis of threshold convergence during training (e.g., plots of β_u and β_c over epochs).
- Experiments with smaller MLLMs to understand the minimum model size needed for effective correspondence reasoning.

## Novel Insights

The paper's key novel insight is that noisy correspondence in MMEA is a dual-level phenomenon that cannot be adequately addressed by treating either level in isolation. The empirical finding that intra-entity noise degrades inter-graph alignment performance and vice versa (Figure 1(b)) reveals a coupling between the two levels that prior work overlooked. The observation that low uncertainty does not guarantee correct correspondence (Theorem 1) is a valuable theoretical contribution that highlights why purely uncertainty-based approaches are insufficient, and the consensus principle fills this gap in a complementary manner. The test-time reasoning concept—that seemingly dissimilar but inherently identical attributes exist and can be uncovered through structured reasoning—opens an interesting direction for robust entity alignment beyond training-time defenses.

## Suggestions

- Add a table or discussion comparing inference time and computational cost (GPU hours, API calls) with and without the TTR module, especially on larger benchmarks.
- Provide a brief study on the sensitivity of the greedy correspondence estimation (Eq. 7) by varying the initial subset size |π_0| and measuring alignment quality.
- Discuss whether the training-time robust components alone (without the expensive MLLM) are sufficient for practical deployment, as the ablation shows they contribute the majority of the gains.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>