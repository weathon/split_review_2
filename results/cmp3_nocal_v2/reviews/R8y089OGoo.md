## Summary

This paper proposes DIPOLE, a novel RL algorithm for fine-tuning diffusion policies. The core idea is to introduce a greedified KL-regularized objective (Eq. 5) whose closed-form optimal solution decomposes into a pair of dichotomous policies — a positive policy weighted by sigmoid(βG) and a negative policy weighted by (1−sigmoid(βG)) — which are then recombined via a CFG-style score combination during inference. This yields bounded regression weights (avoiding the explosion of exponential weighting) while enabling controllable greediness through the ω hyperparameter. The method is evaluated on 39 tasks across ExORL and OGBench (offline and offline-to-online) and scaled to a 1B-parameter VLA driving model on NAVSIM.

## Strengths

1. **Clean, mathematically elegant derivation (Sections 3.1–3.2).** The paper starts from the standard KL-regularized RL objective, identifies its limitations (unstable exponential weights, inefficient learning), constructs a greedified alternative (Eq. 5), derives its closed-form solution (Theorem 1, Eq. 6), and algebraically decomposes it into dichotomous sigmoid-weighted policies (Eqs. 7–8). The resulting connection to classifier-free guidance (Eq. 10) is a genuinely neat synthesis that provides theoretical grounding for CFG-style inference in RL fine-tuning.

2. **Addresses a real practical problem.** The instability of exp-weighted regression for diffusion policy optimization (loss explosion from large β, sample dominance by high-return trajectories) is a well-documented limitation. The paper articulates this trade-off clearly and proposes a bounded sigmoid alternative that directly addresses both issues.

3. **Solid empirical evaluation.** Results across 39 tasks on two benchmarks (ExORL, OGBench) with 8 random seeds and standard deviations are reported. Both offline and offline-to-online settings are covered. DIPOLE achieves best or near-best performance on most task categories, and the improvement over the imitation-learned baseline is clear.

4. **Demonstrated scalability to large models.** Fine-tuning a 1B-parameter VLA model for autonomous driving on NAVSIM (Table 4) shows the method works beyond small-scale benchmarks. The navtrain result (89.7 PDMS, +1.4 over imitation baseline) is a clean generalization comparison.

## Weaknesses

### Fatal
None.

### Major
- **Missing DPPO comparison on standard RL benchmarks.** The paper criticizes DPPO-style methods (Ren et al., 2025) for "crude Gaussian-based approximation" and "prolonged training" (lines 22–23) and argues DIPOLE avoids these issues. Yet DPPO is only included in the NAVSIM comparison (Table 4), not in the ExORL or OGBench evaluations (Tables 1–3) where the standard diffusion RL baselines reside. Since DPPO is the primary policy-gradient competitor for diffusion RL, its absence from the main RL benchmarks is a structural gap that limits what can be concluded about DIPOLE's relative advantages in the standard setting.

### Minor
- **Missing ablation: sigmoid-weighted regression without the dichotomy.** A central claim is that the dichotomous decomposition enables stable training and "simultaneously utiliz[es] both good and bad data" (line 105). However, a natural baseline is missing: train a *single* diffusion model with sigmoid-weighted regression (replacing exp(βG) with σ(βG) in Eq. 4) and compare against DIPOLE. If the single model performs comparably, the contribution of the dichotomous structure beyond what the sigmoid already provides is unclear. The paper includes "DIPOLE w/o rs" (which still uses the dichotomy) and CFGRL (which uses a hard indicator), neither of which isolates this effect. This ablation would directly test whether the dichotomy earns its keep.

- **OGBench results show variability.** On humanoidmaze-large-navigate, IFQL (11±2) outperforms DIPOLE (6±2). On antsoccer-arena-navigate, FQL (60±2) outperforms DIPOLE (57±7) (Table 2). The paper's claim that DIPOLE "achieves better performance compared to other baselines" (line 173) is true on aggregate but masks that DIPOLE is behind on 2 of 6 categories. A more precise framing would strengthen the paper.

- **NAVSIM navtest result is not a fair generalization comparison.** The paper reports DP-VLA w/ DIPOLE navtest at 94.8 PDMS (+6.5 over imitation baseline), but this variant is trained and evaluated on the same test split (Table 4 caption + lines 211–212 acknowledge this). The fair generalization comparison is the navtrain variant (89.7 PDMS, +1.4). The paper is transparent about the split used, but the 94.8 number is prominently featured and the methodological caveat could be stated more prominently in the abstract and claims.

- **Hyperparameter ω not discussed.** The greediness factor ω is introduced in Eq. (5) as a new hyperparameter, but the paper does not report what values of ω were used across experiments, how they were selected, or sensitivity to this choice. Since ω directly controls the greediness–conservatism trade-off, this information is important for practical use. (The paper refers to Appendix D.4 for ablation studies, which may partially address this.)

- **Computational cost of training two models.** DIPOLE trains separate positive and negative diffusion models (line 107), roughly doubling the training cost compared to single-model approaches. The paper acknowledges this implicitly (two separate LoRA modules for the VLA experiments, line 125) but does not discuss the cost-benefit trade-off or whether parameter-sharing could be applied more broadly.

- **Clarification needed on what the negative policy learns.** The paper states π⁻ "focuses on reward minimization" (line 105, abstract). In practice, π⁻ is trained on the same dataset with complementary sigmoid weights 1−σ(βG), so it learns to emulate low-advantage actions from the behavior policy. This is not "reward minimization" in an agentive sense (it does not seek out novel low-reward states). A clarifying discussion would prevent misinterpretation.

### Trivial
None.

## Nice-to-Haves

- A comparison of DIPOLE with a single-diffusion-model variant using sigmoid-weighted regression (no dichotomy) would cleanly isolate the benefit of the dichotomous structure.
- Including DPPO on ExORL or OGBench (even on a subset of tasks) would substantially strengthen the claim that DIPOLE improves over policy-gradient approaches.
- Reporting ω values used across experiments and a sensitivity curve would improve practical usability.

## Removed Points

These points were flagged by the harsh critic but are removed after verification against the paper:

- **"Eq. (5) is reverse-engineered, not derived from first principles."** Removed. The paper transparently states "We begin by formulating a greedier learning objective" (line 81) and cites related work sharing a similar design spirit (line 85). It does not claim to derive Eq. (5) from first principles. The presentation is intellectually honest about constructing the objective.

- **"NAVSIM navtest presentation is misleading."** Removed (demoted to Minor instead). The paper explicitly states in Table 4's caption that "navtrain/navtest represent different data splits used for trajectory rollout" and explains in the text that the navtest variant is "trained on the test split without using any ground-truth" (lines 211–212). The distinction is transparently reported, though the generalization caveat could be more prominent.

- **"Score approximation errors from combining two diffusion models."** Removed. The reviewer acknowledges this is standard practice (CFG has the same issue) and not a flaw. It is a technical observation about a standard limitation that applies to all methods using score combination.

## Novel Insights

The harsh critic correctly identifies that the central novelty — decomposing the greedified KL-regularized optimal policy into dichotomous sigmoid-weighted policies and recombining via CFG-style score interpolation — is mathematically elegant and practically motivated. The connection between KL-regularized RL and classifier-free guidance (Eq. 10) is the paper's most interesting insight and is well-supported by the derivation. However, no genuinely novel insight emerges from the reviews beyond what the paper itself contributes: the critic's key concern (is the dichotomy additive over just using sigmoid weights?) is an empirical question that only the authors can answer with additional experiments.

## Suggestions

1. Add a sigmoid-weighted single-model baseline. This is the single most informative experiment for establishing the value of the dichotomous structure.
2. Include DPPO on at least a subset of the standard RL benchmark tasks to substantiate the critique of policy-gradient methods.
3. Report ω values used in all experiments and include a sensitivity analysis.
4. In the abstract and conclusion, distinguish more carefully between the navtrain (generalization) and navtest (within-distribution) results, or lead with the navtrain number and present the navtest result as a supplementary demonstration.

## Score and Decision

MY FINAL SCORE: <score>7</score>
MY FINAL DECISION: <decision>Accept</decision>