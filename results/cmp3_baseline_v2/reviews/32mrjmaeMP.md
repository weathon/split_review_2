## Summary

This paper introduces TAK (Task Arithmetic with KFAC regularization), a dataless regularizer that improves weight disentanglement in task arithmetic by framing representation drift regularization as a curvature matrix approximation problem. The authors leverage Kronecker-Factored Approximate Curvature (KFAC) to approximate the intractable Jacobian Gram matrix, and propose an aggregation scheme that merges per-task curvature factors into a single surrogate, achieving constant complexity in the number of tasks. The method achieves state-of-the-art results on vision and language benchmarks for task addition and negation, while being robust to task vector rescaling and requiring no external task data.

## Strengths

- **Novel and well-motivated connection**: The paper establishes a principled link between representation drift regularization in task arithmetic and the generalized Gauss-Newton (GGN) matrix, enabling the use of well-studied curvature approximation techniques. This is a creative and theoretically grounded contribution.
- **Practical efficiency**: The Kronecker aggregation heuristic (Eq. 8) reduces memory and computation from linear to constant in the number of tasks, and the KFAC estimation requires only a few minutes of pre-computation. The method also shows robustness to infrequent application of the regularizer (Fig. 8), further reducing overhead.
- **Strong empirical results**: TAK matches or exceeds the data-dependent method τJp on task addition and negation across multiple architectures (ViT-B/32, B/16, L/14, T5-base) while being fully dataless. The method also demonstrates clear task localization (Fig. 5) and robustness to the scaling coefficient α (Fig. 4a), eliminating the need for held-out tuning.
- **Thorough experimental analysis**: The paper includes extensive ablations on KFAC estimation quality (number of examples, MC samples), compression strategies (quantization, pruning, SVD), and the impact of the aggregation heuristic. The analysis of computational overhead (Fig. 6) is transparent and informative.

## Weaknesses

### Fatal
None.

### Major
- **The aggregation heuristic (Eq. 8) lacks theoretical justification**: The approximation of the sum of Kronecker products as a single Kronecker product of sums is not generally valid, and the paper provides no analysis of the approximation error or conditions under which it holds. While the empirical results show negligible degradation, a theoretical understanding would strengthen the contribution and guide practitioners.

### Minor
- **Extension to the non-linear regime is heuristic**: The paper applies TAK to non-linear fine-tuning by pairing it with attention-only fine-tuning, which is argued to induce approximately linear behavior. The justification is plausible but not rigorously established, and the performance gains in this regime are smaller than in the linearized regime. The paper could more clearly delineate the limitations of this extension.
- **Limited task diversity**: The evaluation is confined to classification tasks (vision and language). It would be valuable to see whether the method generalizes to other modalities or task types (e.g., generation, regression), especially given the claim of broad applicability.

### Trivial
- Some figures (e.g., Fig. 2 radar charts) are dense and difficult to parse at a glance, though the key information is conveyed in the tables.

## Nice-to-Haves
- A theoretical bound on the error introduced by the Kronecker aggregation heuristic, or an empirical study of when it might break down (e.g., with highly heterogeneous task distributions).
- Application to parameter-efficient fine-tuning (e.g., LoRA) to further reduce storage and computation.
- Release of pre-computed KFAC factors as a standard asset alongside pre-trained models, as suggested in the conclusion.

## Novel Insights

Beyond the paper’s own contributions, the key insight is that weight disentanglement in task arithmetic can be reframed as a curvature-aware optimization problem, bridging two previously separate literatures: model merging and second-order optimization. The observation that the Jacobian Gram matrix (a GGN) can be pre-computed and shared instead of data, and that KFAC provides a practical approximation, is both elegant and actionable. The task localization property (Fig. 5) is a particularly nice byproduct, suggesting potential applications in out-of-distribution detection.

## Suggestions
- Provide a theoretical analysis of the aggregation heuristic (Eq. 8), even if only for simplified settings (e.g., isotropic factors), to build confidence in its general applicability.
- Discuss the limitations of the non-linear regime extension more explicitly, and consider evaluating on a broader set of non-linear fine-tuning strategies beyond attention-only.
- Consider including a comparison with other dataless regularization approaches (e.g., weight decay, spectral norm) to further isolate the benefits of curvature-aware regularization.

## Score and Decision

The paper presents a novel, well-executed, and practically impactful contribution to task arithmetic. The connection to curvature approximation is original, the method is efficient and dataless, and the empirical results are strong across multiple benchmarks. The weaknesses are minor and do not undermine the core claims. I recommend acceptance.

MY FINAL SCORE: <score>8.5</score>
MY FINAL DECISION: <decision>Accept</decision>