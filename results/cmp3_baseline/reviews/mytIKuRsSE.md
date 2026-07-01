## Summary
This paper identifies and formalizes a new problem in Multi-modal Entity Alignment (MMEA) called Dual-level Noisy Correspondence (DNC), which encompasses misalignments in both intra-entity (entity-attribute) and inter-graph (entity-entity and attribute-attribute) correspondences. To address DNC, the authors propose RULE, a framework that estimates correspondence reliability via uncertainty and consensus principles, uses these estimates for robust attribute fusion and inter-graph discrepancy elimination, and incorporates a test-time correspondence reasoning module using MLLMs. Extensive experiments on five benchmarks demonstrate that RULE significantly outperforms seven state-of-the-art MMEA methods under various noise levels.

## Strengths
- **Novel and well-motivated problem formulation:** The paper identifies and formalizes the Dual-level Noisy Correspondence (DNC) problem, which is a practical and under-explored challenge in MMEA. The authors provide clear empirical evidence (Fig. 1b) showing that existing methods degrade significantly under both intra-entity and inter-graph noise, justifying the need for a dedicated solution.
- **Comprehensive and principled methodology:** The proposed RULE framework is well-structured, with a clear two-fold reliability estimation principle (uncertainty + consensus) that is theoretically grounded (Theorem 1, Definition 1-3). The design of separate robust modules for intra-entity fusion (DRF) and inter-graph discrepancy elimination (DRL) is logically sound and directly addresses the dual nature of the noise.
- **Strong and consistent empirical results:** RULE achieves state-of-the-art performance across all five benchmarks and three noise settings (inherent, 20%, 50%), with particularly large margins on the more challenging ICEWS datasets (e.g., +11.7 H@1 on ICEWS-WIKI under inherent DNC). The ablation studies (Table 3) and analytical experiments (Fig. 3, 4, 5) convincingly validate the contribution of each component.

## Weaknesses
### Major
- **Limited novelty of the test-time reasoning module:** The test-time correspondence reasoning (TTR) module, while effective, largely relies on prompting a large MLLM (Qwen2.5-VL-72B) with Chain-of-Thought. The core technical contribution here is relatively thin compared to the training-time components, as it primarily involves applying existing MLLM capabilities to the problem. The paper would benefit from a more detailed analysis of the MLLM's failure cases or a more novel integration mechanism.
- **Dependence on a very large MLLM:** The TTR module uses Qwen2.5-VL-72B-Instruct, a 72B parameter model. This introduces significant computational and memory overhead during inference, which may limit the practical applicability of the method. The paper does not discuss the computational cost or latency of this module, nor does it explore smaller, more efficient alternatives.

### Minor
- **Clarity of the consensus modeling for inference:** The method for estimating the correct correspondence during inference (Eq. 6-7) using marginal contribution and a greedy strategy is somewhat complex and its justification (Assumption 1) could be more rigorously connected to the problem. The paper would benefit from a more intuitive explanation or a toy example illustrating this process.
- **Hyperparameter sensitivity:** The method introduces several hyperparameters (γ, β, λ, τ). While the paper states that γ is fixed at 0.5 and provides a sensitivity analysis for β in Appendix G.10, a more thorough discussion of the sensitivity to all hyperparameters, especially λ, would strengthen the paper.

### Trivial
- The paper uses "i.f.f" in the problem formulation (Section 2.1), which appears to be a typo for "iff" (if and only if).

## Nice-to-Haves
- An analysis of the computational cost (FLOPs or runtime) of the TTR module compared to the training-time components.
- An ablation study using a smaller, open-source MLLM for the TTR module to assess the trade-off between performance and efficiency.
- A more detailed discussion of the failure cases of the uncertainty and consensus principles, e.g., scenarios where both are high but the correspondence is still incorrect.

## Novel Insights
Beyond the paper's own contributions, a genuinely novel insight is the formalization of the *dual-level* nature of noise in MMEA and the demonstration that these two levels (intra-entity and inter-graph) are not independent but interact. The paper shows that inter-graph attribute-attribute noise is a by-product of intra-entity entity-attribute noise and inter-graph entity-entity noise. This insight is crucial because it suggests that a holistic approach, like RULE, which jointly estimates and mitigates noise at both levels, is necessary for robust MMEA, rather than treating them as separate problems.

## Suggestions
- Provide a more detailed analysis of the TTR module's failure cases and a discussion of the computational overhead of using a 72B MLLM. Consider including an experiment with a smaller MLLM to demonstrate the trade-off.
- Simplify the explanation of the consensus modeling for inference (Eq. 6-7) with a concrete example to improve readability and intuition.

## Score and Decision
The paper makes a clear and significant contribution by identifying a novel, practical problem (DNC) in MMEA and proposing a well-designed, principled, and empirically strong solution. The weaknesses, primarily the reliance on a large MLLM for the test-time module, are notable but do not invalidate the core contribution. The training-time components (reliability estimation, DRF, DRL) are novel and well-validated. The paper is clearly written and the experiments are thorough. The work is of high value to the MMEA and broader multi-modal learning community.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>