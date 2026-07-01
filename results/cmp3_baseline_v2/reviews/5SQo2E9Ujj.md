## Summary

This paper studies curriculum learning in goal-conditioned reinforcement learning (GCRL) through the lens of data selection. The authors compare uniform goal sampling to curriculum-biased sampling in a GridWorld environment using Universal Value Function Approximators (UVFAs), finding that curricula shift the state-goal distribution toward underachieved goals, reduce approximation error, and improve success on harder edge goals. The paper argues that curriculum learning should be understood as a structural mechanism for selective data acquisition rather than merely an exploration heuristic.

## Strengths

- **Clear conceptual framing**: The paper offers a useful reframing of curriculum learning as selective data acquisition rather than just an exploration heuristic, which provides a principled lens for understanding why curricula work in GCRL.
- **Well-motivated research question**: The connection to open-ended learning (OEL) and the work of Hughes et al. (2024) provides a compelling motivation for studying how curricula shape data distributions.
- **Clean experimental setup**: The GridWorld environment with UVFAs allows for clear isolation of the effect of curriculum-induced distributional shifts, making the analysis interpretable.

## Weaknesses

### Fatal
None.

### Major
- **Insufficient empirical support for core claims**: The paper's central claim is that curriculum learning should be viewed as a structural mechanism for data acquisition, yet the experiments show only modest improvements (e.g., +0.02 overall, +0.08 on edge goals at H=16) with high variance (standard deviations often comparable to or exceeding the reported gains). The results do not convincingly demonstrate that the curriculum mechanism is doing something fundamentally different from exploration heuristics.
- **No comparison to existing curriculum methods**: The paper only compares uniform sampling to a hand-crafted edge-biased curriculum. There is no comparison to established curriculum learning methods (e.g., self-paced learning, teacher-student frameworks, adversarial goal generation like AMIGo, or automated curriculum learning approaches). Without such baselines, it is unclear whether the proposed perspective offers any practical advantage over existing approaches.
- **Limited scope and generalizability**: The experiments are conducted only in a small GridWorld with hand-designed goal distributions. The paper acknowledges this as a limitation but does not provide any evidence that the findings would transfer to more complex domains (e.g., continuous control, robotic manipulation, or visual environments). The claim that this perspective "provides a concrete entry point into the larger challenge of scaling toward lifelong and open-ended learning" is not supported by the evidence presented.

### Minor
- **The curriculum is hand-crafted and static**: The "curriculum" is simply a fixed oversampling of edge goals, which is not adaptive to the agent's learning progress. This is a very weak instantiation of curriculum learning and does not capture the dynamic, adaptive nature of most modern curriculum learning methods.
- **High variance in results**: The standard deviations are large relative to the reported gains (e.g., edge success: 0.183 ± 0.131 vs 0.217 ± 0.125), making it difficult to assess statistical significance. The paper does not report any statistical tests.
- **Missing analysis of approximation error**: The abstract and introduction claim that curricula "reduce approximation error," but the results section does not present any direct measurement of value function approximation error. The claims about approximation error are inferred from success rates rather than directly measured.

### Trivial
- The paper uses "PBRs" as an abbreviation for Potential-Based Reward Shaping, which is non-standard (typically "PBRS").
- Table 1 appears to have a truncated caption ("Table 1: Pc").

## Nice-to-Haves

- Include comparisons to adaptive curriculum methods (e.g., self-paced learning, ALP-GMM, AMIGo) to demonstrate whether the selective data acquisition perspective offers practical advantages.
- Measure value function approximation error directly (e.g., MSE against ground-truth values computed via dynamic programming) to support the claim that curricula reduce approximation error.
- Test in at least one additional environment (e.g., a continuous control task or a more complex discrete environment like MiniGrid) to demonstrate generalizability.
- Report statistical significance tests (e.g., confidence intervals, t-tests) to support the claim that curriculum improvements are reliable.

## Novel Insights

None beyond the paper's own contributions. The idea that curriculum learning shapes the training distribution is not new—it is implicit in most curriculum learning papers (e.g., Bengio et al., 2009; Florensa et al., 2017). The paper's main contribution is making this perspective explicit and testing it in a simple GCRL setting, but the empirical results are too preliminary to constitute a genuinely novel insight.

## Suggestions

- Strengthen the empirical evaluation by including adaptive curriculum baselines and measuring approximation error directly.
- Consider testing in a more complex environment (e.g., MiniGrid or a continuous control task) to demonstrate that the findings generalize beyond simple GridWorld.
- Report confidence intervals or statistical tests to quantify the reliability of the observed improvements.

## Score and Decision

The paper presents a conceptually interesting reframing of curriculum learning but provides insufficient empirical evidence to support its core claims. The experiments are limited to a single simple environment, use only a hand-crafted static curriculum, show only modest and high-variance improvements, and lack comparisons to existing curriculum methods. While the perspective is worth noting, the paper does not meet the bar for acceptance at ICLR in its current form.

MY FINAL SCORE: <score>3</score>
MY FINAL DECISION: <decision>Reject</decision>