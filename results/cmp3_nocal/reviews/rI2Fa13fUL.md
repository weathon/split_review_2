## Summary

This paper introduces Generative Trajectory Policies (GTPs), a new policy class for offline RL that learns the entire solution map of a continuous-time generative ODE. The authors frame diffusion, consistency, and flow-matching models as instances of a unified ODE framework, then propose two key adaptations for offline RL: a closed-form score approximation that avoids expensive numerical ODE integration during training, and a variational, advantage-weighted objective for value-guided policy improvement. Empirically, GTP achieves strong results on D4RL benchmarks, most notably in the BC setting on AntMaze tasks where it substantially outperforms prior generative BC methods.

## Strengths

1. **The BC results on AntMaze are genuinely striking and well-documented (Table 1).** GTP-BC achieves an average of 66.3 on AntMaze tasks, compared to 44.1 for C-BC and 41.2 for D-BC — a ~50% improvement. The gap is particularly large on the hardest tasks (antmaze-medium-diverse: 85.0 vs 31.6; antmaze-large-diverse: 40.8 vs 12.8/26.6). These results provide strong evidence that learning the full trajectory map provides a meaningful inductive bias for long-horizon, multi-modal tasks, and this is the paper's most convincing empirical contribution.

2. **The score approximation (Section 4.1, Theorem 1) is a clean, theoretically-grounded simplification with clear practical benefit.** Replacing the multi-step ODE solver with the closed-form surrogate $\tilde{f}(x_t, t) = (x_t - x)/t$ is a clever trick that sidesteps a real computational bottleneck. The theorem showing the objectives differ by $O(h^p)$ provides principled justification, and Remarks 1 and 2 correctly identify the concrete benefits (one-step perturbation for efficiency, breaking the bootstrapping cycle for stability).

3. **The paper correctly identifies and systematically addresses three real practical challenges** (Section 4): computational burden, training instability from self-generated targets, and misaligned generative vs. RL objectives. These barriers to applying trajectory-based generative models in offline RL are genuine and well-articulated, and the proposed solutions are motivated by these challenges.

## Weaknesses

### Fatal
None.

### Major

1. **The paper's central efficiency claim is not tested with the required evidence.** The paper claims GTP "can achieve high performance even with a few sampling steps" (line 25) and that it "resolves the tension between expressiveness and efficiency" (line 257). However, GTP is evaluated at K=5 sampling steps while consistency models use K=2 (line 259). The paper never compares GTP against consistency models at the *same* step count, nor does it provide an ablation showing how GTP's performance varies with K. Without this evidence, the claim that GTP is "more efficient" than consistency models is unsubstantiated — GTP may simply achieve better performance at the cost of 2.5× more inference steps. A plot of performance vs. K for GTP, diffusion, and consistency models on 2–3 representative tasks would directly address this gap.

2. **The ablation study (Table 3) is too thin to support the paper's claims about the two key techniques.** The ablation evaluates only a single task (hopper-medium-expert). The "GTP-BC + linear Q-term" baseline with λ=0.01 achieves 111.4, close to GTP's 112.2, which undercuts the claim that the variational guidance is essential. The paper attributes the gap to brittleness and critic-scale sensitivity but does not demonstrate this across multiple tasks with varying critic scales. Similarly, the "w/o score approximation" baseline (99.7 vs 112.2) shows a meaningful degradation on one task, but a single data point is insufficient to support the general claim. A proper ablation should evaluate across at least 3–4 diverse tasks.

### Minor

1. **Abstract overstates the "perfect scores" claim.** The abstract and contribution list claim the method "achieves perfect scores on several notoriously hard AntMaze tasks." In fact, only one AntMaze task (antmaze-umaze, Table 2) reaches a perfect 100.0. The body text correctly states "a perfect score" (singular, line 302), but the abstract's "several" is misleading and should be corrected.

2. **Theorem 2 restates a well-known result without adequate acknowledgment.** The advantage-weighted objective $\pi^*(a|s) \propto \pi_{\text{BC}}(a|s) \exp(\eta A(s,a))$ is the standard solution to KL-regularized policy optimization, appearing in prior work such as AWR (Peng et al., 2019), AWAC (Nair et al., 2020), and Diffusion-QL (Wang et al., 2023). Presenting this as a theorem without noting its established nature overstates the theoretical contribution. The novelty is in *applying* this weighting to the GTP generative loss, not in the weighting itself.

3. **No training-time comparison against baselines.** The paper acknowledges that "reducing the substantial training time of this model class remains an important avenue for future research" (line 351), but never quantifies GTP's training cost relative to D-QL, C-AC, QGPO, or other baselines it claims to outperform. Without this comparison, readers cannot assess whether GTP's modest average improvements (e.g., +1.1 on Gym, +1.5 on AntMaze vs. the next-best method) justify potentially much higher training cost.

4. **Incomplete baseline results in Table 2.** C-AC is missing on 3 of 6 AntMaze tasks and BDM on 2 of 6. The AntMaze average row lists dashes for these methods, which makes the comparison less informative. The paper should either explain why these results are unavailable or report them if they exist in the cited sources.

5. **Statistical significance is not discussed.** Given the variance in several results (e.g., antmaze-mp: GTP 83.3 ± 8.1 vs QGPO 83.6, where the intervals overlap substantially), it is unclear which improvements are meaningful. The paper would benefit from a brief discussion of significance or effect size for key comparisons.

### Trivial
None.

## Nice-to-Haves

- Compare GTP-BC against CTM-BC (the closest generative analogue that also learns the full trajectory) to isolate whether the benefit comes from trajectory modeling itself or from the RL-specific adaptations.
- Add a multi-task ablation for the variational guidance (the paper's claim that the linear Q-term baseline is "brittle" would be much stronger if demonstrated on 3–4 tasks with varying critic scales).
- Add an inference-time step-count ablation (performance vs. K) to substantiate the "flexible, multi-step, deterministic generation" claim.

## Removed Points

These points are flagged to be removed; treat them with caution.

- *The generative framework (Section 3) is expository rather than novel.* — The paper is transparent about the connection to CTM (Eq. 3–4 are "inspired by (Kim et al., 2024)"), and the contributions are explicitly framed around the RL adaptations, not the framework itself. Removed as a strawman.
- *Eq. (4) derivation concern.* — The reviewer questioned whether the linear interpolation follows from Eq. (3). The derivation is mathematically correct: substituting the integrated form into Eq. (2) yields Eq. (4). Removed as a misunderstanding.
- *"Several" framing is "standard rhetorical inflation."* — Judgment about writing style, not a concrete weakness. Removed.
- *Missing GAN/VAE/EBM baselines.* — The paper does not claim to compare against these methods in its experiments, and they are not the relevant SOTA baselines for generative policies. Removed as scope creep.
- *The paper "does not resolve the expressiveness-efficiency trade-off it claims to address."* — The framing is too strong. The paper's claim is about bridging the gap between diffusion (many steps) and consistency (few steps). GTP at K=5 outperforming both is consistent with this claim. The real weakness is the missing K ablation (retained as Major weakness #1), not a fundamental inconsistency.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Correct the abstract to say "a perfect score" (or specify which tasks) rather than "several."
2. Add a plot or table showing performance vs. number of sampling steps K for GTP, a diffusion policy, and a consistency model on 2–3 representative tasks. This directly addresses the paper's central claim about efficiency.
3. Expand the ablation study (Table 3) to at least 3–4 tasks, and include a comparison of the linear Q-term baseline across those tasks with multiple λ values to substantiate the claim about brittleness.
4. Acknowledge that Theorem 2 is a known result from prior KL-regularized RL works, with the novelty being its application to the GTP consistency loss.
5. Add training wall-clock times for the main baselines (D-QL, C-AC, QGPO) for at least one task, so readers can assess the training efficiency trade-off.

## Score and Decision

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>