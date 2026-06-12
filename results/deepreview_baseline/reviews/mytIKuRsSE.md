## Summary

This paper identifies and formalizes a new problem in multi-modal entity alignment (MMEA) called Dual-level Noisy Correspondence (DNC), where both intra-entity (entity-attribute) and inter-graph (entity-entity, attribute-attribute) correspondences can be noisy. The authors propose RULE, a robust framework that estimates correspondence reliability via uncertainty (from Dempster-Shafer theory) and consensus (via marginal contribution), then uses these estimates to guide robust attribute fusion and inter-graph discrepancy elimination. A test-time correspondence reasoning module leveraging a large multimodal LLM further uncovers latent attribute connections. Experiments on five benchmarks under various noise levels show consistent and substantial improvements over seven state-of-the-art methods.

## Strengths

- **Novel and well-motivated problem**: The paper is the first to systematically study dual-level noisy correspondence in MMEA, providing clear empirical evidence (Fig. 1b) that both intra-entity and inter-graph noise degrade existing methods, and that the problem is prevalent in real benchmarks (over 50% noise in ICEWS).
- **Principled reliability estimation**: The two-fold principle combining uncertainty (from evidential theory) and consensus (from marginal contribution) is theoretically grounded (Theorem 1, Assumption 1) and empirically validated (Fig. 3b, Fig. 4) to separate clean from noisy pairs effectively.
- **Comprehensive and convincing experiments**: The method is evaluated on five diverse benchmarks under three noise settings (inherent, 20%, 50%) with two evaluation protocols (Non-name, All-attributes). RULE outperforms all baselines by large margins (e.g., +6.8% avg H@1 on Non-name inherent DNC, +4.5% on 50% DNC), and the performance degradation with increasing noise is much slower than competitors (Fig. 3a).
- **Well-designed ablation and analysis**: Ablation studies (Table 3) isolate the contributions of each component (DRL, DRF, TTR, uncertainty vs. consensus), and visualizations (Fig. 5) confirm that reliability weights correctly suppress noisy attributes during fusion.

## Weaknesses

### Major

- **Reliance on a very large MLLM at test time**: The test-time correspondence reasoning module uses Qwen2.5-VL-72B-Instruct, a 72B-parameter model. This introduces significant computational cost and potential reproducibility concerns (API access, cost, versioning). The paper does not discuss the practical feasibility or provide ablation with smaller/cheaper models.
- **Hyperparameter sensitivity and threshold design**: The pair division thresholds (β_u, β_c) are determined via a self-adaptive formula (Eq. 8) that depends on the set of true positive pairs S^TP, which itself is estimated via the greedy marginal contribution strategy. This circular dependency and the fixed β=0.3 may not generalize across datasets; the paper only tests one β value in Appendix G.10 and does not analyze sensitivity on other datasets.

### Minor

- **The consensus modeling via marginal contribution (Eq. 6-7) is heuristic**: While Assumption 1 is intuitive, the greedy selection of attributes based on marginal contribution of similarity scores lacks formal guarantees. The initial subset size (⌊M/2+1⌋) seems arbitrary and is only justified for M≥3.
- **Limited discussion of failure cases**: The paper does not analyze scenarios where the method might fail (e.g., when both uncertainty and consensus are misleading, or when the MLLM reasoning is incorrect). The test-time reasoning module's output is combined with prior similarity (s_i^{joint} = s_i + \hat{s}_i) without weighting, which may not be optimal.

### Trivial

- The notation in Eq. 10 uses α_i^m and \hat{y}_i^m but these are not clearly defined in the main text (they appear to be for attribute-level correspondences, but the derivation is brief).

## Nice-to-Haves

- An analysis of the computational overhead of the MLLM-based reasoning module (e.g., inference time per query) and a comparison with a lighter alternative (e.g., a smaller LLM or a trained reasoning network).
- A discussion of potential negative societal impacts or biases that could arise from using a large MLLM for entity alignment (e.g., hallucination, cultural bias in attribute reasoning).

## Novel Insights

Beyond the paper's own contributions, the key insight is that noisy correspondences in MMEA are not monolithic—they manifest at two distinct levels (intra-entity and inter-graph) and require different mitigation strategies. The use of evidential uncertainty to quantify correspondence reliability, combined with a consensus check via marginal contribution, provides a principled way to distinguish different types of noise. The idea of using an MLLM at test time to reason about latent attribute connections (e.g., "Cristiano Ronaldo" ↔ "football player" ↔ "Mexico") is a creative way to overcome the limitations of training-time denoising alone.

## Suggestions

- Provide an ablation study using a smaller, open-source MLLM (e.g., LLaVA-7B) to assess the trade-off between performance and computational cost for the test-time reasoning module.
- Include a sensitivity analysis of the threshold β across all datasets (not just one) to demonstrate robustness of the self-adaptive threshold mechanism.
- Clarify the definition of α_i^m and \hat{y}_i^m in Eq. 10, and provide a brief derivation or reference to the appendix for the attribute-level loss.

## Score and Decision

**Score**: 8

**Decision**: Accept

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>