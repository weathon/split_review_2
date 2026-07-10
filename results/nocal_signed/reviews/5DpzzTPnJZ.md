## Summary

This paper studies plasticity loss in deep RL from a theoretical perspective, characterizing two mechanisms (NTK rank collapse and gradient attenuation with a $\Theta(1/k)$ decay pattern) and proposing Sample Weight Decay (SWD), a recency-biased replay sampling method intended to counteract gradient decay. Experiments across TD3, Double DQN, and SAC on MuJoCo, ALE, and DMC benchmarks show consistent performance improvements.

## Strengths

- **Theoretical framing of two plasticity-loss mechanisms.** The paper formally characterizes plasticity loss through NTK rank collapse and gradient attenuation ($\Theta(1/k)$ decay), going beyond purely empirical prior work on plasticity loss in RL. The decomposition in Theorem 3 into a distribution-shift term with a $1/k$ scaling and a target-drift term is the paper's most distinctive theoretical claim.

- **SWA reverse validation is a clean experimental idea.** Showing that oversampling old data (SWA) hurts both gradient magnitude and performance provides a conceptually neat empirical counterpart to the hypothesis that recent samples are critical for maintaining plasticity.

- **Consistent empirical improvements across breadth.** SWD shows improvements across 3 algorithms (TD3, Double DQN, SAC) × 3 benchmarks (MuJoCo, ALE, DMC), evaluated with proper aggregate metrics (IQM, stratified bootstrap CIs). The UTD experiment showing larger benefit at higher update frequencies (30.1% at UTD=5) is insightful and consistent with the gradient decay motivation.

## Weaknesses

### Major

- **Internal contradiction in the GraMa evidence.** The paper states "a larger *GraMa* value indicates a weaker learning capability of the neural network" (line 232), then presents results showing SWD maintains a *higher* GraMa value than SAC (Figure 6) and concludes SWD mitigates plasticity loss. If higher GraMa = weaker learning, then SWD having higher GraMa implies *worse* plasticity, not better. The contradiction also appears in the SWA ablation (Figure 5): the paper says SWA exhibits lower GraMa but also greater plasticity loss, which is inconsistent with the stated GraMa interpretation. **This undermines Section 6.3 as evidence for plasticity-specific claims.** Resolving whether the definition or the interpretation is incorrect is essential before the GraMa results can support the paper's conclusions.

- **Theory-method gap is asserted but not established.** Theorem 3 analyzes the full-batch gradient at initialization in FQI, where the $1/k$ factor emerges from the replay buffer distribution recursion. SWD modifies the stochastic sampling distribution via recency-weighted sampling. The paper claims SWD "neutralizes the $1/k$ attenuation" (line 164) but provides no formal argument linking recency-weighted stochastic sampling to the $1/k$ decay derived for the full-batch gradient. The method is presented as flowing "principledly" from theory, but the link remains intuitive rather than demonstrated.

- **Theorem 3's clean $1/k$ result has narrower scope than presented.** The elimination of the target-drift term relies on setting $\hat{f}_{H+1} \equiv 0$ (the terminal condition), which makes the target-drift term vanish only at step $H$. For all earlier steps $h < H$, the target-drift term survives and its behavior (whether it also exhibits $1/k$ decay, dominates, or leads to a different overall gradient pattern) is not characterized. The abstract and introduction present the $1/k$ gradient decay as a general result about deep RL, but the rigorous derivation is confined to a special case.

### Minor

- **Theorem 3 equation reference error.** Theorem 3 states "For the optimization objective defined in **Equation 1**" (line 140), but Equation 1 is Proposition 1's empirical distribution recursion ($\mu_h^{k+1} = \frac{k}{k+1}\mu_h^k + \frac{1}{k+1}\hat{d}_h^{k+1}$), not the loss function.

- **Overclaimed SOTA and synergy.** The paper claims "SOTA performance" on DMC Humanoid tasks, but comparisons with other plasticity methods (ReGraMa, S&P, Plasticity Injection) are limited to one environment (Humanoid Run). In that comparison, SWD+S&P achieves identical scores to SWD alone (~240 across all metrics), providing no evidence of the claimed "synergistic performance improvements" (line 50).

### Trivial

None.

## Nice-to-Haves

- Expand the comparison with plasticity methods to at least one additional environment to support claims of general superiority and orthogonality.
- Discuss computational overhead (O(|𝒟|) per-step weight computation) more explicitly in the main text, even if the bucket approximation mitigates it.

## Removed Points

These points are flagged to be removed, treat them with caution:
- The criticism that Section 4.1 (NTK degeneration) is "largely background" — this is a description, not a weakness; the paper identifies this mechanism and connects it to prior work.
- The notation concern about ∇f^2 being ambiguous — the meaning is clear in context.
- The criticism that PER is "not the most relevant comparison" — the paper also compares with plasticity-specific methods in Section 6.5.
- The concern about confidence intervals not being reported numerically — standard for this type of aggregate visualization.
- Computational cost concerns — addressed by the bucket-based approximation mentioned in Section 6.6.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Resolve the GraMa contradiction immediately.** Either the description of GraMa on line 232 is incorrect, or the interpretation of Figures 5-6 is incorrect. Correct whichever is wrong, so the plasticity evidence is internally consistent.
2. **Either tighten or honestly scope the theory-method connection.** Either provide a formal argument linking the $1/k$ full-batch gradient decay to recency-weighted stochastic sampling, or explicitly state that SWD is inspired by the intuition from Theorem 3 rather than derived from it.
3. **Acknowledge the scope of Theorem 3.** State explicitly that the clean $1/k$ analysis applies rigorously at the terminal step and discuss what can be said about earlier steps.
4. **Tone down the SOTA and synergy claims** to match what the evidence supports.

## Score and Decision

This paper has genuine contributions: a theoretical framework for understanding plasticity loss and a simple, effective method (SWD) that consistently improves RL performance across multiple settings. The empirical improvements are credible and the SWA reverse validation is well-designed.

However, the paper has three significant issues that prevent it from delivering on its claimed narrative. The GraMa evidence is internally contradictory — the paper's own definition contradicts the conclusions drawn from it. The connection between the theoretical result and the SWD method is asserted but not demonstrated, overstating the "principled" grounding. And the key theorem's clean result applies to a narrower scope than the paper presents. These problems cut to the core of what the paper claims to contribute (theoretically grounded, plasticity-evidenced solution), and require major revision to resolve.

MY FINAL SCORE: <score>5</score>
MY FINAL DECISION: <decision>Reject</decision>