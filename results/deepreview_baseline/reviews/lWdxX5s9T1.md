## Summary
This paper tackles the problem of asymmetric distance matrices in neural vehicle routing solvers—a critical limitation for real-world deployment. The authors propose RADAR, which combines a truncated SVD–based initialization to encode static directional structure from the cost matrix, and Sinkhorn normalization in attention to capture dynamic bidirectional context during encoding. Extensive experiments on synthetic benchmarks (17 variants covering ATSP, ACVRP, and multi-task setups) and three real-world datasets show consistent improvements over prior neural methods, including strong zero-shot generalization to larger instances and robust performance under varying asymmetry levels.

## Strengths
- **Addresses a clear and practical gap:** Most neural VRP solvers assume symmetric Euclidean distances, severely limiting real-world applicability. RADAR directly targets this bottleneck with a principled design.
- **Novel and well-motivated methodological contributions:**  
  - The SVD-based initialization is theoretically grounded—the constructed embeddings satisfy a formal asymmetry–aware condition (Def. 1) and provably reconstruct the distance matrix.  
  - Replacing row-wise softmax with Sinkhorn normalization is a clean way to inject bidirectional neighborhood information into attention, which is absent in prior work.
- **Extremely thorough empirical evaluation:**  
  - Experiments cover 16 + 1 synthetic VRP variants and 3 real-world tasks, with comparisons to a wide range of baselines (LKH, HGS, MatNet, ICAM, ELG, ReLD, UniCO, RRNCO, etc.).  
  - Ablation studies isolate the contribution of each component, analyze sensitivity to hyperparameters (SVD rank k, Sinkhorn iterations), and study the effect of coordinates and varying asymmetry levels.
- **Strong generalization and robustness:** RADAR achieves the smallest optimality gaps among neural methods, often matching or exceeding classical solvers on moderate sizes while being orders of magnitude faster. Zero-shot performance on 500- and 1000-node instances is particularly impressive.
- **Insightful analyses:** The study of coordinates vs. distance matrices (Sec 5.4) and the controlled asymmetry-level experiments (Sec 5.5) provide valuable understanding of when and why the proposed components are beneficial.

## Weaknesses

### Fatal
None.

### Major
1. **Scalability to very large instances is not demonstrated.** The largest instance tested has 1000 nodes. Many practical VRPs involve tens of thousands of nodes, where full-matrix SVD and iterative Sinkhorn normalization could become expensive. The paper provides runtime profiling up to 1000, but does not discuss or evaluate behavior at, e.g., 5000 or 10000 nodes.

2. **Sinkhorn normalization is a fixed procedure, not a learned component.** While the paper frames “dynamic asymmetry” as a layer-dependent effect, Sinkhorn normalization is a deterministic, non-parametric operation. The claim that it “models dynamic asymmetry” is somewhat overstated—it imposes a structural constraint (doubly stochastic attention) rather than learning how directionality changes across layers. The authors should clarify whether the dynamic aspect comes solely from the evolving embeddings under this fixed normalization.

### Minor
1. **The necessity of the SVD-based initialization for all asymmetric problems is not fully explored.** The ablation shows that removing SVD degrades performance, but on ACVRP the gains appear smaller than on ATSP. The paper could discuss scenarios (e.g., very noisy or non-low-rank matrices) where SVD may be less helpful.

2. **Comparisons with some baselines use retrained versions under z-score normalization, while others use original checkpoints.** This inconsistency (marked with †, ††, +) makes it slightly harder to assess fairness, though the authors do explain the setup. A unified training protocol for all neural baselines would have been cleaner.

3. **The definition of “static asymmetry” and “dynamic asymmetry” is motivated intuitively, but the transition from one to the other in the encoder layers is not formally characterized.** It remains unclear how the initial SVD-based static representation interacts with the dynamic normalization through multiple layers.

### Trivial
None.

## Nice-to-Haves
- Provide scaling experiments on instances with 5000+ nodes, or discuss the computational bounds of the randomized SVD and batched Sinkhorn steps.
- Compare Sinkhorn normalization with other doubly-stochastic normalizations (e.g., spectral attention, sinkformer) to further contextualize the choice.
- Include a theoretical or empirical analysis of the gradient flow through Sinkhorn (which is differentiable) and its effect on training stability.

## Novel Insights
Beyond the paper’s own contributions, a genuinely novel observation is that **coordinates contribute little structural information in asymmetric routing**—the main value of coordinates is enabling data augmentation (e.g., rotations) that promotes diversity during training. This insight, supported by the experiments in Sec 5.4, challenges the common practice of relying on coordinate-based inductive biases for neural VRP solvers and suggests a paradigm shift toward edge-feature-centric representations for asymmetric problems.

## Suggestions
- Add a discussion of the computational complexity of the SVD step (both memory and time) and how it scales with n, including potential approximations for large n.
- Clarify in the main text that Sinkhorn normalization is applied to the *raw attention scores* (after adding distance biases) and not to the final attention weights, and explain why this formulation is more beneficial than alternatives like double-normalizing QK^T without the distance term.
- To strengthen the dynamic asymmetry claim, consider showing an analysis of how attention scores differ from softmax to Sinkhorn across layers after training, e.g., by visualizing asymmetry in attention matrices.

## Score and Decision
The paper makes a clear, well-motivated, and empirically validated advance for a practically important limitation of neural VRP solvers. The methodology is novel, technically sound, and the experiments are comprehensive. The remaining concerns (scalability beyond 1000, the fixed nature of Sinkhorn) do not undermine the core contribution. I recommend acceptance.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>