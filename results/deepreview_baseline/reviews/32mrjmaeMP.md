## Summary

This paper proposes TAK (Task Arithmetic with KFAC regularization), a dataless method to improve weight disentanglement in Task Arithmetic by linking representation drift regularization to curvature matrix approximation. The authors show that the regularization term can be reformulated as a quadratic form involving the Generalized Gauss-Newton (GGN) matrix, enabling the use of Kronecker-Factored Approximate Curvature (KFAC) to make the computation tractable. They further introduce an accumulation scheme that merges per-task curvature factors into a single surrogate, achieving constant complexity in the number of tasks, and demonstrate state-of-the-art performance on task addition and negation benchmarks across vision and language domains.

## Strengths

- **Novel and principled connection**: The paper establishes a clean theoretical link between representation drift regularization in Task Arithmetic and curvature matrix approximation (GGN), which is well-studied in optimization literature. This allows leveraging decades of research on efficient curvature estimation.

- **Practical contribution with strong empirical results**: TAK achieves state-of-the-art results on task addition (86.0% abs. on ViT-B/32) and negation while being fully dataless, matching or surpassing τ-Jp which requires access to other tasks' data. The method demonstrates exceptional robustness to the scaling coefficient α, eliminating the need for held-out tuning.

- **Computational efficiency**: The KFAC pre-computation requires only ~4 minutes for all 8 Vision tasks (with MC=1), and the accumulated regularizer maintains O(1) complexity in the number of tasks. The empirical validation that 128-256 examples suffice for KFAC estimation is valuable.

- **Thorough experimental evaluation**: The paper includes vision (8 Vision benchmark, three ViT architectures) and language tasks (T5-base, six datasets), ablation studies on KFAC estimation quality, compression techniques, training frequency, and a comparison of merging strategies.

## Weaknesses

### Major

- **The "dataless" claim is somewhat misleading**: While the regularizer itself does not require data from other tasks during training, the KFAC matrices are computed on the *same task's* training data. The paper's Figure 7a shows that using more data (up to 128-256 examples) improves performance. For many applications, using 128 examples from each task is feasible, but calling this "dataless" (when it still requires task-specific data for pre-computation) overstates the contribution. The key advance is that it avoids *cross-task* data sharing, not that it truly requires zero data.

- **Limited analysis of failure cases and limitations**: The paper does not discuss when TAK might underperform or where the Kronecker approximation breaks down. For example, the ViT-B/32 results show a small gap between the naïve multi-task and accumulated regularizer (Tab 3), but the paper does not analyze when this gap might become significant or what architectural properties influence this.

- **The non-linear regime justification is weak**: The paper applies TAK in the non-linear regime by pairing it with Attention-Only Fine-Tuning, citing that this induces "kernel-like" behavior. However, the theoretical justification for why a curvature regularizer derived under linearization should work in non-linear settings is not rigorously established. The empirical results are promising, but the reasoning feels post-hoc.

### Minor

- **Comparison with related methods is incomplete**: The paper compares against τ-Jp (which uses data from other tasks) but does not extensively discuss scenarios where data *is* available—would a hybrid approach (using some data + KFAC) be even better? Also, TaLoS results are taken from the original paper rather than re-implemented, which may introduce evaluation differences.

- **The Kronecker accumulation heuristic (Eq. 8) lacks theoretical justification**: The heuristic of merging Kronecker factors via separate sums of A and B matrices is presented as an approximation, but no bound on the approximation error or analysis of when it might fail is provided.

### Trivial

- The paper mentions "8 Vision" benchmark but some dataset names in tables (e.g., RESISC36 vs. RESISC45) appear inconsistent.

## Novel Insights

None beyond the paper's own contributions: the key insight is recognizing that representation drift regularization under linearization leads to a quadratic form that is exactly the GGN matrix, which can then be approximated via KFAC. This connection to curvature optimization literature is the core intellectual contribution.

## Suggestions

- Clarify the "dataless" terminology throughout the paper—perhaps "data-free cross-task regularization" or "without requiring other tasks' data" is more precise than "dataless," which could be misinterpreted.

- Provide a theoretical analysis or bound on the Kronecker accumulation approximation error. Even a simple empirical study showing when the gap between naïve multi-task and accumulated regularizer becomes significant would strengthen the paper.

- Include a discussion of computational costs for larger models (e.g., ViT-L/14) and whether the memory overhead of KFAC becomes prohibitive without compression.

## Score and Decision

The paper makes a novel, well-executed contribution to task arithmetic by establishing a principled connection between representation drift regularization and curvature approximation. The empirical results are strong, the method is practical and efficient, and the experiments are thorough across multiple architectures and modalities. The limitations (the "dataless" claim nuance and the non-linear regime justification) are not fatal—the core contribution of linking weight disentanglement to KFAC is solid and clearly demonstrated.

MY FINAL SCORE: <score>8</score>  
MY FINAL DECISION: <decision>Accept</decision>