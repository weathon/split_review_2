## Summary

This paper proposes to interpret curriculum learning in goal-conditioned reinforcement learning (GCRL) as a mechanism for selective data acquisition rather than merely an exploration heuristic. Using Universal Value Function Approximators (UVFAs) in a GridWorld environment, the authors compare uniform goal sampling with a hand-designed curriculum that upweights edge (harder) goals. The results show modest improvements in success rates on edge goals, supporting the reframing of curriculum as a structural bias on the training distribution.

## Strengths

- **Clear conceptual framing** – The paper articulates a coherent perspective that connects curriculum design in GCRL to open-ended learning and data selection. This reframing is well-motivated by referencing recent work on persistent learning (Hughes et al., 2024).
- **Controlled experimental setup** – By keeping architecture, training protocol, and environment identical except for the goal-sampling distribution, the paper isolates the effect of the curriculum and makes the distributional shift directly observable.
- **Relevant research question** – Understanding how curricula alter the state-goal visitation distribution is a valid and under-explored angle within the curriculum learning literature.

## Weaknesses

### Fatal
- **None** – The core claim is not invalidated, but it is not convincingly supported either.

### Major
- **Insufficient empirical evidence** – The experiments are limited to a single deterministic GridWorld with a hand-designed curriculum. Only 1000 episodes per seed and three seeds are used. The reported gains on edge goals (e.g., +0.08 at H=16) are small, and overlapping error bars suggest the results are not statistically reliable. No measure of function approximation error (e.g., MSE of the learned value function) is provided, despite the paper claiming curricula “reduce approximation error.”
- **Limited novelty of the reframing** – The idea that curricula shape training distributions is already implicit in much prior work on automatic curriculum learning (e.g., Florensa et al., 2017; Portelas et al., 2020; Held et al., 2018). The paper does not formally distinguish its perspective from these existing approaches, nor does it derive new theoretical or algorithmic insights.
- **Manual, non-adaptive curriculum** – The edge-biased sampling is hand-crafted and static. The paper does not propose or evaluate automated methods for selective data acquisition, which limits the practical relevance and the generality of the conclusions. The authors acknowledge this as a limitation, but it remains a central weakness in assessing the paper’s contribution.
- **No comparison to state-of-the-art curriculum methods** – The baseline is only uniform sampling. The paper would be stronger if it compared against existing curriculum GCRL methods (e.g., GoalGAN [Held et al.], ALP-GMM [Colas et al.], or Self-Play [Racanière et al.]) to demonstrate that the selective-data-acquisition view leads to competitive or complementary performance.

### Minor
- **Missing direct analysis of approximation error** – The paper repeatedly claims that curricula reduce value-function approximation error, but the evaluation relies entirely on success rates. Reporting the actual prediction error (e.g., MSE on held-out goals) would directly support the central thesis.
- **Figures have inconsistencies** – Figure 1 and Figure 2 are nearly identical but have different captions and slightly varying numerical values. The weighted curriculum results (Figure 3) are introduced in the text before the figure reference is clear. This makes the experimental narrative harder to follow.

### Trivial
- **None**

## Nice-to-Haves

- Report confidence intervals or statistical significance tests (e.g., paired bootstrap) to substantiate the observed improvements.
- Include a direct comparison of learned value functions with ground-truth values (under the shaped reward) to quantify where curricula reduce error.
- Test the same selective-data-acquisition perspective with an automated curriculum (e.g., teacher-student or adversarial goal generation) to show it generalizes beyond hand-coded biases.

## Novel Insights

The paper’s central insight – that curricula serve as a data-selection mechanism that biases the state-goal distribution toward underachieved regions – is a valid but not new observation. The same intuition underlies many existing curriculum methods (e.g., self-paced learning, reverse curriculum generation). The paper does not introduce a new algorithm, theoretical result, or unexpected empirical finding that would constitute a novel contribution beyond its own framing.

## Suggestions

- **Directly measure value function approximation error** on a held-out set of state-goal pairs for both conditions. This would provide a cleaner test of the claim that curricula “reduce approximation error.”
- **Increase the scale** – use more seeds, more episodes, and a larger grid to reduce variance and increase confidence in the results.
- **Extend to an automated curriculum** – even a simple adaptive scheme (e.g., sample goals where the current agent fails most often) would strengthen the argument that selective data acquisition is a general principle.
- **Report effect sizes** (e.g., Cohen’s d) or a Bayesian analysis to quantify the strength of the curriculum effect.

## Score and Decision

**Score:** 3

**Decision:** Reject

*Rationale*: The paper’s core reframing is conceptually plausible but lacks substantial empirical support. The experiments are narrow (single environment, hand-crafted curriculum, small sample size) and the reported gains are modest and not statistically convincing. The paper does not introduce new algorithms, theoretical analysis, or results that advance the field beyond what is already known about curriculum learning. Given the competitive standards of ICLR, the contribution is too preliminary to warrant acceptance.

MY FINAL SCORE: <score>3</score>  
MY FINAL DECISION: <decision>Reject</decision>