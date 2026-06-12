## Summary
The paper introduces Constrained Mass Transport (CMT), a variational framework for learning Boltzmann generators that constructs intermediate distributions via constrained optimization—specifically, a trust-region constraint on KL divergence and an entropy decay constraint—yielding automatic annealing schedules that mitigate mass teleportation and mode collapse. The framework is instantiated with normalizing flows and evaluated on molecular systems up to d=219 (the newly introduced ELIL tetrapeptide), demonstrating consistent improvements over state-of-the-art methods including FAB and TA-BG.

## Strengths
- **Clean theoretical framework with analytical solutions**: The constrained optimization problems in Eqs. (2), (7), (9) all admit closed-form solutions (Propositions 2.1–2.3), and Theorem 2.4 establishes a precise connection between the constraints and annealing paths (geometric, tempered, geometric-tempered). This is elegant and provides real insight into why the constraints work.

- **Strong and consistent empirical results**: CMT outperforms FAB and TA-BG across all four systems on EUBO and ESS, with the advantage growing substantially on larger systems. On ELIL tetrapeptide (d=219), CMT achieves 26.06% ESS versus 13.75% (TA-BG) and 7.21% (FAB). The ablation study (Figures 2–3) convincingly demonstrates that both constraints are necessary, with the combination avoiding the failure modes of each alone.

- **Practical algorithmic design**: The importance-weighted forward KL formulation enables sample reuse via replay buffers, the dual optimization cost is negligible (~0.01% of training time), and the trust-region constraint controls importance weight variance. The method is described with sufficient detail for reproducibility.

- **New benchmark contribution**: The ELIL tetrapeptide (d=219) is the largest system studied purely from energy evaluations without MD samples, advancing the frontier for variational molecular sampling.

## Weaknesses
### Fatal
None.

### Major
- **RAM TV metric inconsistency on largest system**: On ELIL tetrapeptide, TA-BG achieves better RAM TV (2.54×10⁻²) than CMT (3.13×10⁻²), contradicting the "consistently surpasses" claim. While CMT wins on EUBO and ESS, the worse performance on the qualitative Ramachandran plot metric for the most challenging benchmark deserves discussion. This suggests the ESS improvement may partly reflect better density estimation in high-probability regions without fully resolving all metastable states.

### Minor
- **Hyperparameter sensitivity**: The trust-region bound ε_tr and entropy bound ε_ent are key hyperparameters. The paper does not discuss sensitivity analysis in the main text, and it is unclear how robust the method is to these choices across systems of different dimensionality. While Appendix D likely covers some of this, the lack of guidance in the main paper limits practical adoption.

- **Gap between theory and practice**: The theoretical framework assumes exact intermediate distributions q_i, but these are approximated by normalizing flows. The convergence guarantees from the constrained optimization framework do not directly carry over. The paper does not quantify this approximation gap, making it unclear how much of the theoretical benefit is retained in practice.

### Trivial
None.

## Nice-to-Haves
- A comparison of wall-clock time across methods would complement the target evaluation counts and give practitioners a clearer picture of computational cost.
- Sensitivity analysis on ε_tr and ε_ent presented in the main text (even briefly) would strengthen the practical contribution.

## Novel Insights
The key novel insight is that combining a trust-region constraint (which produces geometric annealing paths with automatic scheduling) with an entropy decay constraint (which produces tempered paths) yields a hybrid geometric-tempered path that inherits the overlap-maintaining properties of both while avoiding their individual failure modes. The trust-region alone still permits mass teleportation (as the right mode can emerge without overlap), and the entropy constraint alone can cause a large initial KL jump when H(q₀) ≫ H(p). Their combination, enforced jointly via Eq. (9), provides a principled solution that previous annealing methods addressed only via heuristic schedule tuning.

## Suggestions
- Address the RAM TV discrepancy on ELIL tetrapeptide more explicitly—e.g., is TA-BG's better Ram TV a statistical artifact, or does it reflect genuinely better mode coverage in low-density regions despite worse overall ESS?
- Include a brief sensitivity analysis of ε_tr and ε_ent in the main text to guide practitioners.

## Score and Decision
The paper presents a well-motivated theoretical framework with elegant analytical results, strong empirical evidence on challenging benchmarks, and a convincing ablation study. The combination of trust-region and entropy constraints is a novel and principled contribution to annealing-based sampling. The main weakness is the inconsistent RAM TV performance on the largest system, but overall the paper makes a clear and valuable contribution to the field.

MY FINAL SCORE: <score>7</score>
MY FINAL DECISION: Accept