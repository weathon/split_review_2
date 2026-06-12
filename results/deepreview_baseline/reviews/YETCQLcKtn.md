## Summary

This paper proposes PolicyFlow, an on-policy reinforcement learning algorithm that integrates continuous normalizing flow (CNF) policies with PPO-style optimization. The key technical contributions are: (1) an approximation of importance ratios using velocity field variations along interpolation paths, avoiding costly full ODE simulation during training, and (2) a Brownian Regularizer that implicitly encourages entropy growth in the flow-based policy without explicit likelihood computation. Experiments on MultiGoal, MuJoCo Playground, and IsaacLab benchmarks show PolicyFlow achieves competitive or superior performance compared to PPO with Gaussian policies and flow-based baselines (FPO, DPPO), particularly demonstrating better multimodal behavior capture.

## Strengths

- **Novel and practical approach to a well-motivated problem**: The paper addresses a genuine limitation—extending PPO to expressive generative policies without the computational burden of full ODE simulation. The importance ratio approximation via velocity field variations is clever and practically motivated, offering a clear computational advantage over methods that require backpropagating through full generative chains.

- **Principled entropy regularization for flow policies**: The Brownian Regularizer provides a lightweight, theoretically-inspired alternative to expensive entropy computation for CNF policies. The connection to the heat equation and score-velocity relationship is elegant, and the ablation studies (MultiGoal, Fig. 2) convincingly demonstrate its practical benefit in preventing mode collapse.

- **Comprehensive empirical evaluation**: The paper evaluates on diverse benchmarks (MultiGoal, MuJoCo Playground, IsaacLab) with multiple baselines (PPO, FPO, DPPO). The ablation studies (clipping range, initialization, time sampling, interpolation paths) are thorough and provide useful practical insights. The training time comparison (Table 2) honestly acknowledges the computational overhead.

- **Clear exposition of the core technical idea**: The derivation from Eq. (8) to Eq. (13) is well-structured, and the approximation error bound (Eq. 11) provides theoretical grounding. The algorithm pseudocode (Algorithm 1) is detailed and reproducible.

## Weaknesses

### Major

- **Theoretical justification of the importance ratio approximation is incomplete**: The paper claims an approximation error bound of O(ε) (Eq. 11), but this is stated as a remark with reference to Appendix A (which is not provided in the main text). The bound's dependence on the clipping range ε is intuitive but the derivation is not presented. More critically, the approximation in Eq. (10) replaces the integral over the true ODE trajectory with an expectation over a linear interpolation path. The conditions under which this approximation is valid (e.g., smoothness of the velocity field, small time horizon) are not rigorously discussed. The bound O(ε) appears to assume the policy update is small, which is circular since ε controls the update size.

- **The Brownian Regularizer's theoretical grounding is overstated**: The paper acknowledges in a remark that "the velocity field in our policy is not obtained via flow matching gradients, and thus does not strictly correspond to the rectified flow dynamics." This is a significant caveat. The regularizer (Eq. 15-16) is derived from the score-velocity relationship for rectified flows (Eq. 14), but the policy's velocity field is learned via RL, not flow matching. The connection to Brownian motion/heat equation is therefore heuristic rather than principled. The paper would benefit from a clearer separation between the inspiration and the actual mathematical justification.

- **Limited comparison with FPO and DPPO on IsaacLab**: The paper states that FPO and DPPO are not compared on IsaacLab due to framework differences (JAX vs PyTorch). While this is a practical constraint, it weakens the claim that PolicyFlow is "competitive or superior" to these methods. The MuJoCo Playground results (Fig. 3) show PolicyFlow outperforming FPO and DPPO, but the paper does not provide statistical significance tests for these comparisons. Given that FPO and DPPO are the primary baselines, this is a notable gap.

- **The MultiGoal experiment, while visually compelling, lacks quantitative metrics**: Figure 2 shows trajectory distributions, but there is no quantitative measure of "diversity" or "balance" (e.g., entropy of goal distribution, coverage score). The claim that PolicyFlow "achieves the most diverse and more balanced goal-reaching behaviors" is based on visual inspection alone. A quantitative metric would strengthen this key result.

### Minor

- **The paper does not discuss the sensitivity to the Brownian regularizer weight w_b**: The MultiGoal experiment uses w_b = 0.25, but there is no ablation showing how performance varies with this hyperparameter. Given that the regularizer is a core contribution, understanding its sensitivity is important.

- **The training time comparison (Table 2) shows PolicyFlow is 30-80% slower than PPO**: While the paper frames this as "less than 50% increase" or "below twice that of PPO," the overhead is non-trivial. The paper should discuss whether this overhead is justified by the performance gains, especially in environments where PolicyFlow does not significantly outperform PPO (e.g., Open-Drawer, Quadcopter, H1, Go2 in Table 1).

- **The approximation in Eq. (10) uses an expectation over p(t) = U[0,1]**: The paper does not discuss the variance of this Monte Carlo estimate. With a single t sample per data point (as in Algorithm 1, line 15-16), the gradient estimates may have higher variance than the full ODE simulation. The ablation on time sampling (Fig. 4c) shows minor differences, but this does not directly address variance.

### Trivial

- The paper uses "purposed" instead of "proposed" in the conclusion (Section 6).
- The diagram description in the text is redundant with the figure caption.

## Nice-to-Haves

- A quantitative diversity metric for the MultiGoal experiment (e.g., entropy of goal visitation distribution, Jensen-Shannon divergence from uniform).
- Ablation on the Brownian regularizer weight w_b to show sensitivity.
- A discussion of when the importance ratio approximation might break down (e.g., large policy updates, highly nonlinear velocity fields).
- Comparison with a simpler baseline: PPO with a mixture of Gaussians policy, which can also capture multimodality.

## Novel Insights

The paper's core insight—that importance ratios for CNF policies can be approximated by velocity field variations along a simple interpolation path, avoiding costly ODE simulation—is genuinely novel and practically valuable. The Brownian Regularizer, while heuristic, offers a computationally lightweight approach to entropy regularization for flow-based policies that is more principled than ad hoc noise injection. The paper demonstrates that expressive generative policies can be trained with on-policy RL at a computational cost only modestly higher than Gaussian policies, which is an important step toward practical deployment of more expressive policy classes.

## Suggestions

1. Provide a quantitative diversity metric for the MultiGoal experiment (e.g., entropy of goal distribution, or the fraction of goals reached across episodes).
2. Add an ablation study on the Brownian regularizer weight w_b to show sensitivity and provide guidance for hyperparameter selection.
3. Clarify the theoretical conditions under which the importance ratio approximation (Eq. 10) is valid, beyond the O(ε) bound. Discuss potential failure cases.
4. Include statistical significance tests (e.g., paired t-tests or confidence intervals) for the MuJoCo Playground comparisons with FPO and DPPO.
5. Discuss the variance of the Monte Carlo estimate in Eq. (10) and whether multiple t samples per data point would improve stability.

## Score and Decision

The paper presents a novel and practical approach to a well-motivated problem, with solid empirical validation across diverse benchmarks. The core technical contributions (importance ratio approximation and Brownian Regularizer) are clever and address genuine limitations of prior work. The main weaknesses are: (1) incomplete theoretical justification of the approximation, (2) the Brownian Regularizer's connection to Brownian motion is more heuristic than the paper suggests, and (3) limited quantitative evaluation of the key multimodal diversity claim. These weaknesses are significant but not fatal—the paper's practical contributions are clear and the empirical results are convincing. The paper is a solid contribution to the intersection of generative models and RL.

Score: 6 (borderline accept)

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>