## Summary

This paper proposes reframing curriculum learning in goal-conditioned reinforcement learning (GCRL) as a mechanism for selective data acquisition. Using a simple GridWorld environment with UVFAs and potential-based reward shaping, the authors compare uniform goal sampling to a hand-crafted edge-biased curriculum. Results show modest improvements on harder edge goals (e.g., +0.034 success rate at H=16) but large variance across seeds. The paper argues this supports viewing curricula as structural biases that reshape state-goal distributions rather than merely exploration heuristics.

## Strengths

- The paper provides a clear and well-motivated framing of curriculum learning through the lens of data distribution, which offers a conceptually useful perspective for thinking about curricula in GCRL.
- The experimental setup is clean: it isolates the effect of distributional shift by comparing uniform vs. biased sampling with identical architectures and training protocols.
- The use of UVFAs is appropriate for studying how data distribution affects value function approximation across the state-goal space.

## Weaknesses

### Major

1. **Trivial domain and insufficient experimental evidence.** The paper evaluates only on a small deterministic GridWorld with hand-crafted goal bias. The improvements on edge goals are modest (e.g., from 0.183±0.131 to 0.217±0.125 at H=16) and consistently within one standard deviation of the uniform baseline, indicating no statistical significance. The paper does not report any significance tests or effect sizes. Such preliminary results on a toy environment cannot support the claimed general insights about curriculum learning or open-ended learning.

2. **No comparison to existing curriculum methods.** The paper only compares uniform sampling to a manual edge-biased curriculum. There is no comparison to any prior curriculum learning approach (e.g., reverse curriculum generation, automatic goal generation, teacher-student frameworks, self-play). Without such comparisons, the core claim—that curriculum should be viewed as selective data acquisition—is neither new nor empirically justified, as the effect of distributional bias is already well understood in the curriculum learning literature.

3. **No direct analysis of approximation error.** Despite claiming that curricula "reduce approximation error on a shared evaluation set," the paper never measures or reports value approximation error. The only evaluation metric is success rate, which conflates value function quality with exploration and policy execution. This weakens the central argument that curricula improve function approximation in targeted regions.

4. **Overclaimed connection to open-ended learning.** The paper repeatedly frames its work as a "pathway toward more persistent and open-ended agents," yet the experiments involve a single static GridWorld with a fixed set of 1000 episodes. There is no demonstration of continual learning, skill acquisition, or adaptation to new tasks. This connection is purely motivational and unsupported by any evidence.

### Minor

5. **Incomplete and sloppy references.** The conclusion contains a placeholder citation ("?") and the references include "First Wang and Others. Title placeholder for wang et al. 2024." This indicates insufficient care in preparing the manuscript and undermines confidence in the paper's rigor.

6. **Underspecified curriculum weighting scheme.** The "weighted curriculum" experiment (Section 3.2) is described qualitatively but the exact sampling proportions are never provided. The large difference in overall success rates between the "Baseline" and "Weighted" conditions (e.g., NoCurr overall ~0.37 vs ~0.28) suggests these may have been run under different settings, but this is not explained, making the comparison difficult to interpret.

7. **Limited analysis of distributional shift.** Figure 2 shows a bar chart of training distributions, but the paper does not provide quantitative measures of distribution similarity (e.g., KL divergence, coverage metrics) or relate these to value function learning directly.

### Trivial

- The paper could clarify whether UVFA training is performed offline from collected trajectories or online with continuing interaction. The protocol suggests offline training from fixed datasets, but this is not explicitly stated.

## Nice-to-Haves

- Include statistical significance tests (e.g., bootstrap confidence intervals or paired tests across seeds) to substantiate the claimed improvements.
- Compare against at least one established automated curriculum method (e.g., ALP-GMM, self-play goal generation, or Hindsight Experience Replay).
- Directly measure and report value function approximation error (e.g., mean squared error against Monte Carlo estimates) on the evaluation set.
- Provide a clearer formal connection between curriculum-induced distribution shift and the "zone of proximal development" concept mentioned in the introduction.

## Novel Insights

None beyond the paper's own contributions. The idea that curriculum biases the training data distribution is intuitive and has been widely recognized in prior work (e.g., Florensa et al. 2017, Portelas et al. 2020). The paper's main insight—that this bias can be intentionally exploited—is already implicit in most curriculum learning methods.

## Suggestions

1. Strengthen the empirical foundation by (a) testing in more complex environments (e.g., continuous control with sparse rewards), (b) including statistical significance tests, and (c) measuring value approximation error directly.
2. Compare against existing curriculum methods to demonstrate that the selective-data-acquisition perspective yields practical advantages over standard approaches.
3. Replace the overclaimed connection to open-ended learning with a more grounded discussion of how curricula could be integrated into continual learning setups, or remove the open-ended framing entirely given the limited scope of the experiments.
4. Clean up the references and fill in all placeholders before any resubmission.

## Score and Decision

**Score:** 3  
**Decision:** Reject  

The paper presents a conceptually interesting reframing of curriculum learning, but the experimental evidence is far too weak for a top venue like ICLR: the domain is trivial, the results are not statistically significant, there is no comparison to existing methods, and the connection to open-ended learning is unsupported. The work reads as a preliminary exploration that would be more appropriate for a workshop than a main conference.

MY FINAL SCORE: <score>3</score>  
MY FINAL DECISION: <decision>Reject</decision>