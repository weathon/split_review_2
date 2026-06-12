## Summary

This paper introduces Direct Optimal Action Learning (DOAL), a framework for policy extraction from Q-value functions in offline RL. Instead of end-to-end backpropagation through iterative sampling chains (as in BRAC with diffusion/flow policies), DOAL computes a target action by gradient ascent on data actions using Q-value gradients, then trains the policy to match this target using efficient distribution-native losses. A Batch-Normalizing Optimizer is derived that replaces the opaque regularization coefficient α with an interpretable trust-region parameter δ. The paper also provides strong baselines by properly tuning the number of MaxQ samples, and demonstrates improvements on OGBench and partial improvements on D4RL.

## Strengths

- **Clean conceptual framework with formal backing.** Proposition 1 rigorously establishes the relationship between the BRAC gradient and a target-matching objective, showing they are "similar but different." This provides a principled foundation for the DOAL approach rather than just a heuristic.

- **Practical hyperparameter reinterpretation.** The Batch-Normalizing Optimizer (Proposition 2) replaces the notoriously sensitive α with δ, which controls the expected magnitude of the action update. Table 3 convincingly shows that while α varies over two orders of magnitude across environments, δ remains stable (0.03–0.1 for OGBench), easing hyperparameter transfer.

- **Comprehensive experimental design.** The paper tests 3 Q-value functions (IQL, Q-learning, ReBRAC) × 3 policy classes (Gaussian, flow, diffusion) across 15 tasks. The computational cost analysis (Section 5.2) is thorough, showing DOAL adds only ~2 extra network calls, and the regression analysis linking calls to runtime is informative.

- **Honest and nuanced reporting.** The paper transparently acknowledges where DOAL does not improve (IQL-based results on D4RL), explains likely causes (unreliable Q-value gradients from IQL), and identifies the tanh inductive bias as a factor. This builds credibility.

- **Actionable baseline contribution.** The analysis of n_sample in MaxQ sampling (Section 4, Proposition 3) is practically useful—the authors' properly-tuned IFQL baselines substantially outperform prior reported numbers on OGBench (329 vs. 218 total for IQL-based methods).

## Weaknesses

### Fatal
None.

### Major

- **Inconsistent empirical gains on D4RL.** On the widely-used D4RL Adroit benchmark, DOAL with IQL-based value functions shows no improvement (Table 1: totals of 518 vs. 520), and DOAL with Q-learning shows no improvement either (Table 2: DMFQL total 614 vs. MFQL 623). Only with regularized Q-learning (DMFReBRAC: 630 vs. MFReBRAC: 614) is there a modest gain. This limits the practical impact, especially since D4RL remains a primary benchmark. The paper should more carefully characterize when and why DOAL helps versus hurts.

- **Unclear interaction between DOAL and Q-value reliability.** The paper identifies that DOAL requires reliable Q-value gradients but does not provide a principled mechanism to determine when gradients are reliable enough. The observation that regularized Q-learning enables DOAL improvements is empirical rather than predictive. This makes it hard for practitioners to know when to deploy DOAL without exhaustive experimentation.

- **The trust-region claim is somewhat overstated.** The paper argues that δ is shareable across policies for the same task/value function, but this claim is only supported in Appendix G (not shown here) and only within the same Q-value setup. The practical claim of "simplified hyperparameter search" would be stronger if δ were shown to transfer across different Q-value functions or even across different datasets of similar characteristics.

### Minor

- **Proposition 1 requires MSE as BC loss.** The formal result connecting BRAC gradients to target matching is proven only for squared L2 loss (Proposition 1). The paper extends this heuristically to other losses (flow matching, diffusion losses) by "replacing" the MSE loss with the native loss. While practical, this extension lacks formal justification—especially since the gradient equivalence in Proposition 1 may not hold for non-quadratic losses.

- **Limited exploration of δ sensitivity.** Only 3 values of δ are tested per benchmark suite (0.03, 0.1, 0.3 for OGBench; 0.0003, 0.001, 0.003 for D4RL). A more systematic sensitivity analysis (e.g., showing the full performance landscape as a function of δ) would strengthen the claim that δ is easier to tune than α.

- **Table formatting issues make comparisons difficult.** Several tables have garbled entries (e.g., "6 ±23" for DIFQL on antmaze-large-navigate appears to be a parsing artifact, and the ± values are inconsistent). While these are likely parser issues, they make it hard to verify the exact numbers.

### Trivial
None.

## Nice-to-Haves

- A discussion or experiment showing how DOAL interacts with different numbers of flow/diffusion steps during training would clarify whether the efficiency gains are robust to the generative model's complexity.
- A visualization or analysis of the learned action targets (a^target) compared to the data actions and the final policy outputs would provide intuitive understanding of what DOAL is actually learning.

## Novel Insights

The paper offers a genuinely useful reframing: treating the BRAC objective as implicitly learning a target action rather than directly optimizing a policy, and then arguing this decoupling enables native distribution losses. The insight that α can be reinterpreted as controlling a trust region on the target action's shift distance, and that normalizing by batch gradient statistics yields a more stable hyperparameter, is novel and practically actionable. Additionally, the analysis of n_sample in MaxQ sampling—the formal argument that increasing samples exacerbates maximization bias rather than monotonically improving quality—is an underappreciated point that the community should take seriously.

## Suggestions

- Conduct a deeper analysis of when DOAL's gradient-based targets are beneficial vs. harmful—for instance, by examining the correlation between Q-value gradient reliability (e.g., ensemble disagreement) and DOAL's improvement over baselines.
- Extend the δ analysis to show cross-task transfer (e.g., does a δ tuned on one OGBench task work on another?) to substantiate the "shareable hyperparameter" claim.
- Add an ablation comparing DOAL with and without batch normalization of the gradient to isolate the contribution of the normalizer itself versus simply using a scaled gradient.

## Score and Decision

The paper presents a clean and well-motivated framework with practical value (efficient computation, interpretable hyperparameters). The formal results (Propositions 1–3) are correct and useful. The experimental evaluation is thorough in breadth but the empirical gains are inconsistent—strong on OGBench with Q-learning but negligible on D4RL without regularization. The contribution is incremental but genuine, and the reframing of BRAC as target matching is a useful conceptual advance. However, the limited and conditional improvement on standard benchmarks tempers enthusiasm.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: Accept