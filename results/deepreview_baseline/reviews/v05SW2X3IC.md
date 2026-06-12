## Summary

This paper proposes a learnable three-channel codec inspired by the Gray-Wyner network from information theory, designed to disentangle shared (common) information from task-specific information across two vision tasks. The authors characterize the limits of this approach via lossy common information, derive an optimization objective that trades off transmit and receive rates, and demonstrate on synthetic data, edge-case classification, and two real vision benchmarks (Cityscapes, COCO) that their method reduces redundancy compared to independent coding while remaining close to joint coding performance.

## Strengths

- **Principled information-theoretic foundation.** The paper connects classic Gray-Wyner network theory and lossy common information (Wyner, Gács-Körner) to a learnable codec framework, providing Theorem 1 (interaction information bounds relating the two common information measures) and Theorem 2 (an objective derived from the Gray-Wyner region). This bridges a gap between classical information theory and modern multitask representation learning.

- **Clear architectural design and objective.** The proposed architecture (shared analysis transform with a matching mechanism for the common channel, conditional entropy models) is well-motivated by the theory. The Lagrangian objective with parameter $\beta$ directly operationalizes the transmit-receive tradeoff, and the ablation comparing Shared, Separated, and Combined architectures on synthetic data supports the design choices.

- **Empirical validation across diverse settings.** The paper evaluates on a synthetic discrete source, colored MNIST with controlled mutual information (edge cases), and two realistic two-task vision scenarios (Cityscapes segmentation+depth, COCO detection+keypoint). The results show consistent redundancy reduction relative to independent coding.

## Weaknesses

### Fatal
None.

### Major

1. **Missing comparison to existing multitask compression methods.** The related work section cites several multitask codecs (Chamain et al., 2021; Feng et al., 2022; Guo et al., 2024), but the experimental evaluation only compares against Joint (single-channel) and Independent (no common channel) baselines. Without a comparison to these prior multitask schemes, it is unclear whether the proposed Gray-Wyner architecture provides a practical advantage over existing approaches.

2. **Relatively simple compression backbone.** The entropy model is based on Ballé et al. (2018) with a hyperprior replaced by the common representation. This is a reasonable proof-of-concept choice, but modern learned compression typically uses more sophisticated transforms and entropy models (e.g., ELIC, SWAG). The claim of practical value would be strengthened by showing compatibility with stronger backbones or by acknowledging this limitation more explicitly.

3. **Ad-hoc multi-task performance metric.** For the Cityscapes and COCO experiments, the paper sums the task performances after rescaling depth RMSE inversely. This is not a standard multi-task metric, and the individual rate-distortion curves (e.g., mIoU vs. rate, depth RMSE vs. rate) are not shown separately. This makes it difficult to assess whether the common channel benefits both tasks equally or primarily one.

### Minor

1. **Limited ablation on the auxiliary loss and β.** The auxiliary loss term (Eq. 15) is introduced to encourage matching of the two common-channel branches, with $\gamma=1$ fixed. The paper does not study the sensitivity to $\gamma$ or show how different values affect common channel usage. Similarly, only three $\beta$ values (1, 1.5, 2) are shown; a finer sweep would better illustrate the tradeoff.

2. **The connection between interaction information bounds (Theorem 1) and the learned representations is not empirically verified.** The paper states that the bounds are a motivation, but it does not attempt to estimate interaction information from the learned representations or check whether the gap between $C$ and $K$ influences the method's behavior.

3. **Claim about BD-rate advantage.** The abstract states "on average, a BD-rate advantage of -81.58% in transmit rate, against single-task codecs." It is unclear how this number is computed (which experiments, which baselines) and whether "single-task codecs" refers to the Independent baseline or something else. This claim should be more carefully stated.

### Trivial

- Some figures (especially Figure 3) have small legends and dense markers that are hard to read.
- The notation $I(X_1,X_2;\hat{Z}_1;\hat{Z}_2)$ for interaction information is used in the main text but defined only in the appendix. A brief inline clarification would help.

## Nice-to-Haves

- Extend the evaluation to include comparisons with the existing multitask codecs mentioned in related work.
- Show individual task performance curves (e.g., mIoU vs. rate and depth RMSE vs. rate) rather than a combined metric.
- Provide an empirical estimate of interaction information or a qualitative analysis of what common information is captured by the common channel (e.g., visualizations of $Y_0$ for image tasks).

## Novel Insights

Beyond the paper's own contributions, the key insight is that the Gray-Wyner network's transmit-receive tradeoff can be realized in a learnable codec through a simple matching mechanism on the common representation, and that the interaction information gap between the two lossy common information measures provides a theoretical justification for why perfect separation of common information is often unattainable in practice. The demonstration that $\beta=3/2$ (equal weight on transmit and receive rates) achieves competitive performance on both rates is a useful empirical observation.

## Suggestions

- Compare against at least one existing multitask compression method (e.g., Chamain et al. 2021 or Guo et al. 2024) to substantiate the claim of practical value.
- Include separate rate-distortion curves for each task in the vision experiments to assess per-task behavior.
- Add a sensitivity study on the auxiliary loss weight $\gamma$ and a finer grid of $\beta$ values.

## Score and Decision

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>