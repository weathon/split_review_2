## Summary

TD-JEPA introduces a temporal-difference latent-predictive loss to train state and task encoders, a multi-step policy-conditioned predictor, and a set of policies entirely from offline reward-free transitions. The predictor approximates successor features in latent space, enabling zero-shot optimization of any downstream reward function. The method is theoretically grounded (showing connections to successor measure factorization and non-collapse) and empirically matches or outperforms state-of-the-art zero-shot RL baselines across locomotion, navigation, and manipulation tasks with both proprioceptive and pixel observations.

## Strengths

- **Novel combination of TD learning and latent prediction for zero-shot RL.** While latent-predictive objectives have been used as auxiliary losses, TD-JEPA makes them the core learning signal for end-to-end training of encoders, predictors, and policies. The off-policy TD formulation allows learning from offline datasets and captures long-term, multi-policy dynamics—a clear advance over one-step or on-policy latent-predictive methods.
- **Strong theoretical support.** The paper provides rigorous analysis linking the TD-JEPA loss to successor measure approximation (Thm. 1–4), demonstrates a non-collapse guarantee under appropriate initialization (Thm. 2), and shows gradient matching between the latent-predictive loss and direct successor-measure TD losses (Thm. 3). This theoretic framework extends and unifies prior results (Tang et al., 2023; Blier et al., 2021).
- **Comprehensive and carefully designed empirical evaluation.** Experiments span 13 datasets from ExoRL and OGBench, covering proprioceptive and pixel observations across locomotion, navigation, and manipulation. The paper evaluates against 7 baselines, including both established zero-shot methods (FB, HILP, Laplacian) and representation-learning methods adapted to zero-shot (BYOL, BYOL-γ, ICVF). The probability-of-improvement analysis (Fig. 2) provides a rigorous multi-domain comparison.
- **Ablations and adaptation experiments add depth.** The paper isolates the impact of multi-step policy-conditioned prediction (Fig. 3 left) and separate state/task encoders (Fig. 3 right). The fine-tuning experiments (Fig. 4) show that learned representations enable rapid downstream adaptation, demonstrating practical utility beyond zero-shot.
- **Clear exposition of the algorithm and design choices.** Algorithm 1 is detailed and reproducible, with all loss terms, target networks, and regularization clearly specified. The connection to successor features is well-motivated and illustrated in Figure 1.

## Weaknesses

### Fatal
None.

### Major
- **Behavior cloning (BC) regularization in OGBench may bias comparisons.** The paper states that BC regularization is applied (App. E.6), but does not clarify whether the same regularization was applied to all baselines. If BC regularization was used only for TD-JEPA, its advantage in OGBench (especially in low-coverage tasks) could be inflated. This should be explicitly addressed.
- **All baselines use an explicit state encoder, which the authors report improves their performance.** While this makes the comparison more equitable, it also means the baselines differ from their original implementations. The hyperparameter tuning for these adapted baselines might not be equally exhaustive across methods, potentially favoring TD-JEPA. A robustness analysis (e.g., varying encoder capacity) would strengthen the claims.

### Minor
- **Theoretical results rely on strong assumptions** (symmetry of transition matrices, uniform state distribution, linear predictors). While these are standard in the related theoretical works cited, the paper does not relax them or provide empirical evidence that the idealized behavior holds in practice (e.g., measuring asymmetry in learned successor measures).
- **Some empirical gains are modest or within confidence intervals.** On proprioception tasks (DMC and OGBench), TD-JEPA is often competitive but not clearly superior to the best baseline (e.g., FB on walker, BYOL-γ on OGBench_RGB). The probability-of-improvement analysis shows statistical significance mainly in pixel domains. The title claim of "matches or outperforms" is accurate but should not be overstated.
- **Computational cost is not discussed.** TD-JEPA trains two encoders, two predictors, target networks for all four, and a policy network. A comparison of training time or parameter count relative to simpler methods like FB would help practitioners assess trade-offs.

### Trivial
None.

## Nice-to-Haves

- An ablation that removes BC regularization from TD-JEPA on OGBench to measure its impact.
- Empirical validation of the symmetry assumption (e.g., Frobenius norm of $P^{\pi_z} - (P^{\pi_z})^\top$ in the learned latent space).
- Scaling experiments on a real-robot dataset (as suggested in the conclusion) to test robustness to sensor noise and distribution shift.

## Novel Insights

The paper offers a fresh perspective on representation learning for zero-shot RL: temporal-difference latent-prediction, rather than Monte-Carlo or one-step prediction, is the key to learning representations that are predictive of long-term, policy-conditioned dynamics. The result that the TD-JEPA loss implicitly optimizes a bilinear factorization of the successor measure (Thm. 3) connects the method to the forward-backward algorithm, while the non-collapse guarantee (Thm. 2) explains why joint embedding architectures can succeed without negative examples. This synthesis of latent-predictive and successor-feature approaches is likely to inspire further theoretical and algorithmic work.

## Suggestions

1. Clarify whether BC regularization was applied uniformly to all baselines in OGBench. If not, provide an additional comparison without BC regularization for TD-JEPA.
2. Include a brief discussion of computational cost (e.g., wall-clock time per training step, number of parameters) relative to FB and other efficient baselines.
3. Add a small experiment measuring the empirical asymmetry of learned successor measures to assess how far the theoretical assumptions are from practice.

## Score and Decision

MY FINAL SCORE: <score>8.5</score>
MY FINAL DECISION: <decision>Accept</decision>