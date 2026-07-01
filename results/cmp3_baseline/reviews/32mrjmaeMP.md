## Summary

This paper proposes TAK (Task Arithmetic with KFAC regularization), a dataless method for improving weight disentanglement in task arithmetic. The key insight is that representation drift regularization can be reformulated as a curvature matrix approximation problem, allowing the authors to leverage Kronecker-Factored Approximate Curvature (KFAC) to create a practical regularizer that requires no external task data. The method achieves state-of-the-art results on task addition and negation benchmarks while maintaining constant complexity in the number of tasks and exhibiting robustness to task vector rescaling.

## Strengths

- **Novel and principled connection**: The paper establishes a clean theoretical link between representation drift regularization in task arithmetic and the generalized Gauss-Newton matrix, enabling the use of well-established curvature approximation techniques from optimization literature. This is a genuinely creative insight that bridges two previously separate areas.

- **Strong empirical results**: TAK achieves state-of-the-art performance on the 8 Vision benchmark for task addition, matching or exceeding the data-dependent τJp method while being fully dataless. The results are consistent across multiple backbone architectures (ViT-B/32, ViT-B/16, ViT-L/14) and extend to language tasks with T5-base.

- **Practical contributions**: The constant-complexity aggregation scheme (Eq. 8) and the robustness to α scaling are practically valuable properties. The method eliminates the need for held-out validation data for tuning, which is a meaningful practical advantage in decentralized or privacy-constrained settings.

- **Thorough experimental analysis**: The paper provides extensive ablation studies on KFAC estimation quality (number of examples, MC samples), compression strategies, computational overhead, and the impact of applying regularization at different frequencies. The analysis of task localization (Figure 5) provides compelling evidence that the method achieves its intended effect.

## Weaknesses

### Fatal
None.

### Major
- **Limited novelty of the core technical contribution**: The paper's main technical contribution is applying KFAC to approximate the Jacobian Gram matrix for representation drift regularization. While the connection between representation drift and the GGN is well-motivated, the use of KFAC itself is a straightforward application of existing techniques. The aggregation heuristic (Eq. 8) is presented as a contribution but is essentially a simple approximation (sum of Kronecker products approximated as Kronecker product of sums) without theoretical justification for why it should work well.

- **The non-linear regime justification is weak**: The paper applies TAK in the non-linear fine-tuning regime, claiming it can be "justified whenever linearized behavior is implicitly enforced." However, the theoretical derivation of the regularizer (Eq. 3) relies critically on model linearization. The empirical results in the non-linear regime (Table 1, right side) show TAK underperforms compared to the linearized regime, and the justification via attention-only fine-tuning is post-hoc rather than principled. This weakens the claim of broad applicability.

- **Missing comparison with important baselines**: The paper compares against τJp, TaLoS, and diagonal GGN, but does not compare against other dataless regularization approaches for task arithmetic, such as RegMean (Jin et al., 2023) or Fisher-weighted merging. Given that the paper's main selling point is being "dataless," a comparison with other dataless merging methods would strengthen the evaluation.

### Minor
- **The task negation results are difficult to interpret**: Table 2 reports target accuracy (lower is better for forgetting) and control accuracy (higher is better). TAK achieves the lowest target accuracy but also has the highest control accuracy on some backbones. However, the paper does not discuss whether the differences are statistically significant or whether the trade-off is meaningful in practice.

- **Limited analysis of the aggregation heuristic**: Table 3 shows that the accumulated regularizer (O(1)) performs comparably to the naïve multi-task formulation (O(T)), but only for two vision backbones and one language model. The paper does not analyze when this approximation might break down (e.g., with very different task distributions or many tasks).

### Trivial
None.

## Nice-to-Haves

- An analysis of how the KFAC approximation quality varies across different layers of the network (e.g., early vs. late layers) would provide insight into which parts of the model benefit most from curvature-aware regularization.
- A discussion of limitations when tasks have very different numbers of classes or output dimensions, since the Jacobian Gram matrix depends on the output dimensionality.

## Novel Insights

The paper's key insight is that representation drift regularization in task arithmetic can be reframed as a curvature matrix approximation problem, specifically the generalized Gauss-Newton matrix. This connection is novel and opens up a principled path to making data-dependent regularization dataless by pre-computing and sharing curvature information instead of raw data. The observation that this curvature information can be efficiently approximated via KFAC and aggregated across tasks with constant complexity is practically valuable. The finding that such regularization naturally induces task localization (Figure 5) is an interesting emergent property that could have applications beyond task arithmetic, such as out-of-distribution detection.

## Suggestions

- Strengthen the non-linear regime analysis by either providing a theoretical justification for why KFAC regularization should work without linearization, or clearly delineating the conditions under which it is expected to be effective.
- Add comparisons with other dataless merging methods (e.g., RegMean, Fisher-weighted averaging) to better contextualize the advantages of the proposed approach.
- Provide statistical significance tests for the main results, particularly for the task negation experiments where differences are small.

## Score and Decision

The paper makes a solid contribution by connecting representation drift regularization to curvature approximation, enabling a practical dataless method for task arithmetic. The empirical results are strong and the analysis is thorough. However, the core technical novelty is somewhat limited (applying KFAC to a known problem), and the non-linear regime justification is weak. The paper is clearly above the acceptance threshold but not at the level of a top-scoring paper.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>