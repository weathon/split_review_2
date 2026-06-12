## Summary

This paper introduces TD-JEPA, a zero-shot unsupervised reinforcement learning method that learns state and task encoders, a policy-conditioned multi-step predictor, and latent-parameterized policies by minimizing a novel temporal-difference (TD) latent-predictive loss. The predictor approximates successor features, enabling test-time optimization of any reward function entirely in latent space. The method is supported by theoretical analysis (gradient matching, non-collapse, and error bounds) and strong empirical results across 13 datasets from ExoRL and OGBench, particularly excelling in pixel-based domains.

## Strengths

- **Novel combination of TD learning and latent-predictive representations for multi-policy, multi-step prediction.** While prior latent-predictive RL methods focus on one-step dynamics, single-policy, or on-policy data, TD-JEPA’s off-policy TD loss enables scalable training from offline reward-free transitions while capturing long-term, policy-conditional dynamics.

- **Strong theoretical grounding.** The paper provides a rigorous analysis (Theorems 1-4) showing that TD-JEPA’s objectives recover low-rank factorizations of successor measures, match gradients of standard TD losses for successor approximation, and avoid collapse under appropriate initialization. The gradient matching argument generalizes and unifies several prior theoretical results.

- **Comprehensive and well-designed empirical evaluation.** The method is benchmarked on 65 tasks across 13 datasets covering locomotion, navigation, and manipulation with both proprioceptive and pixel observations. The probability of improvement analysis (Fig. 2) convincingly demonstrates that TD-JEPA is consistently among the top methods, with clear advantages in pixel-based settings.

- **Clear ablations isolating key design choices.** The paper systematically ablates the prediction target (multi-step policy-conditional vs. one-step behavioral), the use of separate state/task encoders, and the benefit of pre-trained representations for fast downstream adaptation (Fig. 3, Fig. 4). These experiments support the authors’ design decisions.

## Weaknesses

### Fatal
None.

### Major

- **Theoretical analysis is limited to a heavily simplified setting.** The formal guarantees (Theorems 1-4) assume a tabular environment, linear predictors, orthonormal representations, uniform state distribution, and symmetric transition matrices (A1-A3). While the authors note these assumptions can be relaxed, the connection between the idealized theory and practical neural-network-based training is not bridged. This weakens the paper’s central claim that TD-JEPA is a *principled* approach for deep RL.

- **Several baselines (“BYOL*”, “BYOL-γ*”, “ICVF*”) are repurposed for zero-shot RL for the first time in this paper.** Although the authors state they tuned these baselines over comparable hyperparameter grids, the novelty of this instantiation raises concerns about fairness and reproducibility: the community lacks prior reference results for these baselines in the zero-shot setting, and the implementation choices may inadvertently favor TD-JEPA. A more conservative comparison using only established zero-shot methods (e.g., Laplacian, HILP, FB, RLDP) would strengthen the empirical claims.

- **The method has many interacting components (state encoder, task encoder, two predictors, policy network, target networks, orthonormality regularization, BC regularization in OGBench).** The ablation study is partial; e.g., the individual importance of the orthonormality regularization and the BC regularization for OGBench is not separately evaluated. This makes it difficult to attribute improvements specifically to the novel TD-JEPA loss versus auxiliary design choices.

### Minor

- **Performance on several OGBench subsets (e.g., cube-single, cube-double, puzzle-3x3) is not clearly superior to baselines.** In Table 1, for OGBench proprioception, Laplacian, FB, and HILP achieve comparable or higher average scores than TD-JEPA. The paper’s overall conclusion that TD-JEPA “matches or outperforms” baselines is correct but the advantage is less pronounced in proprioceptive settings than in pixel-based ones.

- **The paper lacks a discussion of computational cost.** TD-JEPA requires training two encoders, two predictors, and a policy network with TD updates, which appears more expensive than contrastive methods like FB. A comparison of wall-clock time or parameter count would aid practitioners.

### Trivial
None.

## Nice-to-Haves

- An ablation isolating the effect of orthonormality regularization versus the core TD-JEPA loss.
- A breakdown of computational resources (training time, GPU memory) for TD-JEPA relative to top baselines.
- Additional experiments on large-scale or real-robot datasets, as suggested by the authors.

## Novel Insights

Beyond the paper’s own contributions, the key insight is that *multi-policy, multi-step latent prediction can be made off-policy via temporal-difference bootstrapping*, which yields a direct connection to successor feature learning. The paper’s theoretical gradient matching result (Theorems 1 and 3) provides a unified view of latent-predictive objectives (Monte Carlo and TD) and standard successor measure approximation losses, showing that training representations to predict long-term latents is equivalent to optimizing a low-rank factorization of policy-conditional dynamics. This bridges two previously separate lines of work: self-predictive representation learning and successor-feature-based zero-shot RL.

## Suggestions

- Strengthen the empirical comparison by additionally reporting performance using *only* established zero-shot methods (Laplacian, HILP, FB, RLDP) as baselines, with the newly introduced BYOL-variants relegated to supplementary analysis.
- Provide an ablation on the orthonormality regularization coefficient to demonstrate its necessity and sensitivity.
- Include a brief discussion (or reference) on how the idealized assumptions in the theoretical analysis could be relaxed, and what conditions would make the practical algorithm fail.

## Score and Decision

I rate this paper as a clear accept due to its novel algorithmic contribution, strong theoretical support, and thorough empirical validation. The weaknesses (simplified theory and some baseline construction concerns) are not fatal and are partially addressed by the paper’s own discussion.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>