## Summary

This paper introduces Constrained Mass Transport (CMT), a variational framework for sampling unnormalized densities via a sequence of constrained optimization problems. CMT generates intermediate distributions under constraints on both the KL divergence (trust-region) and entropy decay between successive steps, producing a principled annealing path that generalizes standard geometric annealing. The authors instantiate the framework with normalizing flows, demonstrate strong empirical results on molecular benchmarks up to d=219, and introduce the ELIL tetrapeptide as a new large-scale benchmark.

## Strengths

- **Clean theoretical derivation (Section 2):** Propositions 2.1–2.3 derive closed-form solutions for optimal intermediate densities under trust-region, entropy, and combined constraints, yielding a geometric-tempered annealing path $q_i \propto q_0^{1-\beta_i} (\tilde{p}^{\alpha_i})^{\beta_i}$. Theorem 2.4 formally characterizes all three paths. This is a principled generalization of standard geometric annealing with automatic schedule tuning.

- **Strong empirical results on larger systems (Table 1):** On alanine hexapeptide (d=180) and ELIL tetrapeptide (d=219), CMT achieves substantially higher ESS than all baselines (29.63% vs 18.22% for TA-BG on hexapeptide; 26.06% vs 13.75% for TA-BG on ELIL) — roughly 1.6–2× improvement — with consistently better EUBO values.

- **Ablation study (Figures 2 and 3):** The paper systematically tests each constraint in isolation and both together. Figure 2 quantitatively shows that removing the trust-region constraint causes entropy to drop too rapidly, and removing the entropy constraint yields lower ESS between intermediates. Figure 3 visually confirms only the combined geometric-tempered method avoids mode collapse in Ramachandran plots. This directly supports the claim that both constraints are needed.

- **Sample efficiency:** CMT achieves better results using the same or fewer target density evaluations than FAB and TA-BG. Since target (energy) evaluations are often the bottleneck in molecular applications, this is practically relevant.

## Weaknesses

### Fatal
None.

### Major

- **Theory-practice gap (constraint satisfaction by learned flows):** The central theoretical results (Propositions 2.1–2.3) solve the constrained optimization exactly over all probability distributions, but the practical algorithm (Section 3) approximates each $q_{i+1}$ with a normalizing flow $\hat{q}_{i+1}$ via forward KL minimization. The paper provides no analysis — theoretical or empirical — of whether the learned flows approximately satisfy the KL and entropy constraints. Without verifying that $D_{\text{KL}}(\hat{q}_{i+1} \| \hat{q}_i) \leq \varepsilon_{\text{tr}}$ and $H(\hat{q}_i) - H(\hat{q}_{i+1}) \leq \varepsilon_{\text{ent}}$ hold for the learned approximations, the causal mechanism claimed for CMT's success is partially unsubstantiated. The ablation study (Figures 2, 3) provides indirect empirical support, but direct constraint verification is missing. This is the most significant weakness in the paper.

### Minor

- **Overclaiming on RAM TV for the largest system:** The abstract states CMT "consistently surpasses state-of-the-art variational methods" and the main text (line 237) says "Across all systems and metrics, our method outperforms the baselines." However, on ELIL tetrapeptide (d=219), CMT has *worse* RAM TV ($3.13 \times 10^{-2}$) than TA-BG ($2.54 \times 10^{-2}$). The paper notes TA-BG had only 2 successful runs out of 4, which reduces reliability, but the claim is still broader than the evidence warrants on this one system/metric combination.

- **Hyperparameter sensitivity not discussed in the main text:** CMT introduces two hyperparameters ($\varepsilon_{\text{tr}}$ and $\varepsilon_{\text{ent}}$) that control the entire annealing process. The paper states an analysis is in Appendix B, but the main text gives no indication of how these were chosen, how sensitive the method is to them, or whether the same values work across different systems.

- **Incomplete computational cost reporting:** The paper reports only target evaluations as the cost metric and notes (line 150) that Lagrangian optimization accounts for only 0.01% of training time on alanine dipeptide. However, it also acknowledges (line 265) that "a key limitation of the current approach is the large number of gradient updates needed to approximate each intermediate target during training." Without reporting the total number of gradient updates, wall-clock time, or GPU-hours, the comparison understates the true computational cost picture.

### Trivial

- **Notation inconsistency:** The trust-region bound is denoted $\varepsilon_u$ in equations (3) and (6) but $\varepsilon_{\text{tr}}$ in equations (2) and (9).
- **Algorithm 1 typo (line 168):** Uses $g_{\text{w-ent}}$ instead of $g_{\text{tr-ent}}$ from equation (11).
- **Number of annealing steps not in main text:** The parameter $\tilde{T}$ is referenced (line 223) but no specific value is given for any experiment.

## Nice-to-Haves

- Directly measuring constraint satisfaction by the learned flows (reporting actual $D_{\text{KL}}(\hat{q}_{i+1} \| \hat{q}_i)$ and $H(\hat{q}_i) - H(\hat{q}_{i+1})$ alongside the bounds at each step) would close the theory-practice gap and strengthen the paper's causal narrative.
- A brief sensitivity summary for $\varepsilon_{\text{tr}}$ and $\varepsilon_{\text{ent}}$ in the main text would improve practical usability.

## Removed Points

These points are flagged to be removed; treat them with caution:

- *"The claim that importance weight variance is independent of problem dimension d (line 144) is unsupported in the main text"* — The paper references Appendix C.3 for justification. Per policy, criticisms about content stripped by the parser from appendices are excluded.
- *"CMT trains multiple flow approximations while FAB/TA-BG train a single flow"* — This is an inherent consequence of the method's design, not a weakness. Each individual flow uses the same architecture as baselines.
- Various formatting nitpicks and parser artifacts.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Close the theory-practice gap:** Report the actual $D_{\text{KL}}(\hat{q}_{i+1} \| \hat{q}_i)$ and $H(\hat{q}_i) - H(\hat{q}_{i+1})$ values for the learned flows at each intermediate step, alongside the set bounds $\varepsilon_{\text{tr}}$ and $\varepsilon_{\text{ent}}$. This would directly confirm that the constraints designed in theory are active in practice.
2. **Temper the "consistently surpasses" language** to acknowledge the RAM TV result on ELIL tetrapeptide, or include a statistical test showing the difference is not significant given the small number of successful TA-BG runs.
3. **Report wall-clock time or gradient-step counts** for at least one system alongside target evaluations to give a complete computational cost comparison.
4. **State specific values** of $\tilde{T}$, $\varepsilon_{\text{tr}}$, and $\varepsilon_{\text{ent}}$ used for each system in the main text, with a brief summary of observed sensitivity.

## Score and Decision

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>