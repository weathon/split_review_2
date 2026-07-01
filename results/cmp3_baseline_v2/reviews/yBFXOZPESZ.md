## Summary

The paper proposes **Ano**, a new stochastic optimizer that decouples update direction and magnitude: the sign of the momentum provides the direction, while the instantaneous gradient norm scaled by the inverse of a Yogi-like second-moment estimate provides the step size. An extension called **Anolog** replaces the fixed momentum coefficient \(\beta_1\) with a logarithmically increasing schedule. The authors provide a non-convex convergence rate of \(\tilde{\mathcal{O}}(K^{-1/4})\) and present experiments in computer vision, NLP, and reinforcement learning, claiming improved robustness to noise and non-stationarity.

## Strengths

- **Intuitive design principle:** Decoupling direction (via momentum sign) from magnitude (via instantaneous gradient norm) is a conceptually clean way to avoid the conservative dynamics of momentum-coupled updates in high-noise regimes.
- **Broad empirical scope:** The evaluation spans supervised (CIFAR-100, GLUE) and reinforcement learning (SAC on MuJoCo, PPO on Atari-5) tasks, with multiple seeds and confidence intervals. On RL benchmarks Ano consistently achieves higher mean rank and normalized score than Adam, Lion, and Grams.
- **Ablation study:** Table 6 systematically isolates the contribution of each component (gradient norm vs. momentum norm, sign-based direction, second-moment rule, momentum schedule), helping to validate the design choices.

## Weaknesses

### Fatal

1. **Reproducibility statement refers to non-existent hardware/software.** The paper states experiments were run on an RTX 5090 GPU with CUDA 12.9 and PyTorch 2.9.0. As of the review date, none of these exist (RTX 5090 not released, CUDA 12.9 and PyTorch 2.9.0 are unreleased future versions). This renders the entire experimental section suspect and undermines the credibility of all empirical claims. Without trustworthy experiments, the paper’s core evidence collapses.

### Major

2. **Overclaimed extension of Yogi.** The paper claims to “extend Yogi by introducing a decay factor that explicitly controls variance memory,” yet the update rule in Algorithm 1 is exactly the original Yogi update (with no additional decay factor). This misrepresentation weakens confidence in the novelty of the second-moment design.
3. **Theory–practice mismatch.** The convergence analysis assumes \(\beta_{1,k}=1-1/\sqrt{k}\), but the practical Ano uses a fixed \(\beta_1\) and Anolog uses a logarithmic schedule. The theoretical result therefore applies to a variant that is not implemented or evaluated, creating a gap between analysis and actual algorithm.
4. **Suspicious formatting in GLUE results (Table 3).** The “Default” and “Tuned” sections both contain a duplicate “Adam” row with different numbers (presumably one is meant to be “Adan”). This suggests a data reporting error and reduces trust in the numerical accuracy of the benchmark.
5. **Unsubstantiated speed-up claim.** The text asserts that Ano “reaches the final performance of Adam using approximately 50–70% fewer training steps” based solely on visual inspection of learning curves. No quantitative measurement, statistical test, or direct comparison across multiple environments is provided to support this strong claim.

### Minor

6. **Incomplete comparison with decoupled baselines.** The ablation includes “AdamGrad” (Adam second moment + gradient magnitude + momentum sign) and achieves competitive RL performance (9855 vs. Ano’s 10520). A direct comparison with standard Adam (momentum magnitude) is shown, but a clearer discussion of whether the benefit is primarily from the sign-direction vs. the gradient-magnitude scaling would be helpful.
7. **Missing description of the “decay factor” in the second-moment term.** The paper mentions “introducing a decay factor” without specifying how it differs from the standard \(\beta_2\) in Yogi. Only from the ablation table (where “Yogi+\(\beta_2\)-decay” is listed) can one infer that an extra decay is perhaps added, but the main text and algorithm do not clarify this.

## Nice-to-Haves

- Compare against other noise-robust optimizers such as RAdam, Lookahead, or SWA to better situate the method.
- Provide a direct head-to-head comparison on large-scale supervised training (e.g., ImageNet, language pre-training) to clarify where the method saturates.
- Release the full source code with a working hardware configuration to enable independent verification.

## Novel Insights

None beyond the paper’s own contributions. The core idea of using the sign of the momentum for direction and the raw gradient for magnitude is a natural combination of sign-based and adaptive methods. The main novel insight—that this decoupling is particularly beneficial in non-stationary RL settings—is empirically plausible but fatally compromised by the reproducibility issue.

## Suggestions

- **Address the fatal flaw:** Provide a revised reproducibility statement using current hardware/software versions and, if necessary, rerun or re-report the experiments with verifiable configurations.
- **Clarify the Yogi extension:** State explicitly whether the second-moment update is exactly Yogi or includes an additional decay; if it is just Yogi, remove the claim of extension.
- **Align theory with practice:** Either analyze the fixed-\(\beta_1\) case or implement and evaluate Ano with the square-root schedule used in the analysis.
- **Correct the GLUE table:** Fix the duplicate “Adam” entries and ensure all baseline names are accurate.
- **Quantify the speed-up claim:** Report e.g. area-under-curve or the actual step count at which each method reaches a given reward threshold, with confidence intervals.

## Score and Decision

Given the fatal flaw in the reproducibility statement, the experimental evidence cannot be trusted, and the paper’s empirical contribution is unsupported. The theoretical analysis is partial and mismatched, and the novelty of the method does not outweigh these issues. I strongly recommend rejection.

MY FINAL SCORE: 1.0</score>
MY FINAL DECISION: Reject</decision>