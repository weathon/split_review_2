## Summary

This paper studies plasticity loss in deep reinforcement learning. It provides a theoretical analysis attributing plasticity loss to two mechanisms: rank collapse of the Neural Tangent Kernel (NTK) and gradient magnitude decay of order Θ(1/k). Focusing on the gradient decay mechanism, the authors propose Sample Weight Decay (SWD), a replay buffer sampling strategy that assigns linearly decaying weights based on sample age to counteract gradient attenuation. Experiments on MuJoCo, ALE, and DMC tasks with TD3, Double DQN, and SAC show consistent but modest performance improvements.

## Strengths

- The paper tackles an important and timely problem—plasticity loss in deep RL—which has received significant attention but lacks theoretical grounding.
- The proposed SWD method is simple, lightweight, and can be easily integrated into existing off-policy RL algorithms with minimal overhead.
- The experimental evaluation covers multiple algorithms (TD3, Double DQN, SAC), multiple environments (MuJoCo, ALE, DMC), and includes ablation studies, comparisons with other plasticity methods, and analysis using the GraMa plasticity metric.
- The paper demonstrates that SWD can be combined with other plasticity-preserving techniques (e.g., S&P) to yield further improvements, suggesting orthogonality.

## Weaknesses

### Fatal

None.

### Major

1. **The theoretical analysis is not rigorous and does not convincingly support the paper’s core claims.**  
   The derivation of the Θ(1/k) gradient decay (Theorem 3) relies on strong assumptions: setting \(\hat{f}_{H+1} \equiv 0\) to eliminate the target-drift term, which is unrealistic in practical deep RL with bootstrapping. The analysis is performed for Fitted Q-Iteration with population loss, not for neural network training with gradient descent. The connection between this simplified setting and actual deep RL training is not established. The paper claims to “bridge the gap between empiricism and theory,” but the theory is too disconnected from practice to serve that purpose. Without the appendix (which is stripped), the proofs cannot be verified, but even the presented sketch raises serious concerns.

2. **The method SWD is essentially a recency bias heuristic, and the paper does not compare it to simple baselines that achieve similar effects.**  
   A natural baseline is to sample uniformly from a fixed-size replay buffer that only retains the most recent N transitions (a sliding window). This also gives higher weight to recent data and is a standard practice in many RL implementations. The paper compares SWD only to uniform sampling from the full buffer and to PER, but not to a sliding-window baseline. Without this comparison, it is unclear whether the linear decay weighting of SWD provides any benefit over a hard cutoff. The claimed “principled” derivation from theory is undermined by the lack of such a baseline.

3. **The empirical improvements are modest and may not be statistically significant.**  
   In Figure 1, the aggregate IQM improvements are small (e.g., SAC: ~640 to ~680; TD3: ~3800 to ~4000; Double DQN: ~4600 to ~4800). The 95% stratified bootstrap confidence intervals are shown but are extremely narrow, which is suspicious given the variability typical in RL. The paper does not report confidence intervals for individual task curves (Figures 2, 3), only mean ± std. The improvements in some environments (e.g., HalfCheetah, Walker2d) appear marginal. The claim of “SOTA performance on challenging DMC Humanoid tasks” is not supported by comparisons to recent state-of-the-art methods beyond the few plasticity-focused baselines included.

4. **The paper overclaims the novelty and significance of the theoretical contribution.**  
   The NTK rank collapse mechanism has been discussed in prior work (e.g., Kumar et al., 2023; Lyle et al., 2022). The paper acknowledges this but does not provide new theoretical insights beyond what is already known. The gradient attenuation analysis is the claimed novel contribution, but as noted, it is derived under unrealistic assumptions. The paper’s framing as a “unified theory” is not justified.

### Minor

- The paper uses GraMa as a plasticity metric but defines it only by reference. The interpretation is confusing: the paper states “a larger GraMa value indicates a weaker learning capability,” but in Figure 6, SWD maintains a higher GraMa than SAC, which would imply SWD has weaker plasticity. This needs clarification.
- The ablation study with SWA (weighting older samples more) is a useful sanity check, but the results are not surprising and do not strongly validate the theory.
- The hyperparameter sensitivity analysis (Table 12, 13) is mentioned but the actual tables are in the stripped appendix, so the reader cannot evaluate them.

### Trivial

- The paper contains some unclear phrasing (e.g., “the rank and gradient lost in non-stationarity” in the title is awkward).
- The figures are referenced but the captions are duplicated in the text.

## Nice-to-Haves

- A comparison to a sliding-window replay buffer baseline would greatly strengthen the empirical evaluation.
- A more rigorous theoretical treatment that accounts for neural network training dynamics (e.g., using NTK theory for gradient descent) would make the theory more convincing.
- Reporting confidence intervals for individual task learning curves would help assess the reliability of the improvements.

## Novel Insights

None beyond the paper’s own contributions. The observation that gradient magnitude decays during training is not new; the paper’s attempt to formalize it as Θ(1/k) is not convincingly established. The SWD method is a simple heuristic that is not derived from the theory in a unique way.

## Suggestions

- Add a baseline that samples uniformly from a replay buffer of fixed size (e.g., the most recent 1e5 steps) to isolate the effect of recency bias from the specific linear decay scheme.
- Clarify the GraMa metric definition and interpretation. If higher GraMa indicates weaker plasticity, explain why SWD shows higher GraMa in Figure 6 while also improving performance.
- Provide a more thorough discussion of the assumptions behind Theorem 3 and why the Θ(1/k) decay is expected to hold in practical deep RL settings.
- Include the hyperparameter sensitivity tables and decay strategy comparisons in the main paper or ensure they are available in the appendix for reviewers.

## Score and Decision

The paper addresses an important problem and proposes a simple, practical method. However, the theoretical analysis that is presented as the main contribution is not rigorous and does not convincingly support the method. The empirical gains are modest, and the method is not adequately compared to simple baselines that achieve similar recency bias. The paper overclaims its theoretical novelty. On balance, the contribution is not strong enough for acceptance at ICLR.

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>