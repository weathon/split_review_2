## Summary

The paper introduces *Constrained Mass Transport* (CMT), a variational framework for sampling from unnormalized probability distributions by constructing a sequence of intermediate distributions under constraints on both the KL divergence (trust-region) and the entropy decay between successive steps. This combination mitigates mass teleportation and mode collapse that plague standard geometric annealing paths. The framework is instantiated with normalizing flows and importance-weighted forward KL minimization, and is evaluated on molecular Boltzmann generator benchmarks, including a newly introduced ELIL tetrapeptide system. CMT consistently outperforms state-of-the-art variational methods (FAB, TA-BG) across multiple metrics, achieving up to 2.5× higher effective sample size while avoiding mode collapse.

## Strengths

- **Novel and principled framework**: The combination of trust-region and entropy constraints for constructing annealing paths in sampling problems is novel. The theoretical characterization of optimal intermediate densities (Propositions 2.1–2.3) and the connection to annealing paths (Theorem 2.4) provide a solid foundation.
- **Strong empirical results**: CMT consistently outperforms strong baselines (FAB, TA-BG) on all four molecular systems, with particularly large gains on the larger systems (alanine hexapeptide and ELIL tetrapeptide). The improvements are demonstrated across multiple metrics (EUBO, ESS, Ramachandran TV), not just one.
- **Ablation study clearly justifies design choices**: The ablation on alanine hexapeptide (Figures 2 and 3) convincingly shows that both constraints are necessary—using only one constraint leads to mode collapse or unstable training, while the combination yields the best results.
- **Introduction of a new challenging benchmark**: The ELIL tetrapeptide (d=219) is a meaningful addition to the community, being the largest system studied to date under the purely energy-based variational sampling setting.
- **Computational efficiency of the dual optimization**: The paper demonstrates that solving for the Lagrangian multipliers adds negligible overhead (0.01% of training time on alanine dipeptide), making the method practical.

## Weaknesses

### Fatal
None.

### Major
- **Hyperparameter sensitivity not thoroughly explored**: The method introduces two hyperparameters (ε_tr and ε_ent) that control the constraint tightness. The paper does not provide a sensitivity analysis or guidance on how to set these values for new systems. While the ablation shows the effect of including/excluding constraints, the impact of different ε values is not studied.
- **Comparison of computational budgets is not fully controlled**: The baselines use different numbers of target evaluations (e.g., reverse KL uses 2.56×10^8 while CMT uses 1×10^8 on alanine dipeptide). While the paper notes this, the differences in compute could affect the comparison. A more controlled experiment where all methods are given the same budget would strengthen the claims.

### Minor
- **The 2.5× ESS improvement claim is not uniformly supported**: On alanine hexapeptide, CMT achieves 29.63% ESS vs TA-BG 18.22% (1.6×) and vs FAB 14.55% (2.0×). The 2.5× figure appears only when comparing to FAB on ELIL (26.06% vs 7.21% = 3.6×) or to reverse KL on some systems. The claim is slightly overstated.
- **The method still requires a large number of target evaluations**: While CMT is more sample-efficient than baselines, it still uses up to 8×10^8 target evaluations for the largest system. The paper acknowledges this as a limitation but does not discuss potential remedies beyond future work.

### Trivial
- The figure captions in the PDF extraction are somewhat garbled (e.g., repeated text), but this is a parser artifact and not a paper flaw.

## Nice-to-Haves

- A sensitivity analysis of ε_tr and ε_ent across different systems would greatly aid practitioners in applying the method.
- An investigation into adaptive schemes for setting ε_tr and ε_ent (e.g., based on the observed ESS between steps) could make the method more automatic.
- Comparison to diffusion-based Boltzmann generators (e.g., Liu et al. 2025, Choi et al. 2025) would further contextualize the results, though the paper notes these are less competitive on molecular systems.

## Novel Insights

Beyond the paper’s own contributions, the key insight is that constraining both the KL divergence (ensuring local overlap) and the entropy decay (preventing premature convergence) yields annealing paths that are qualitatively different from standard geometric paths. The theoretical result that the optimal intermediate densities under both constraints take the form of a geometric-tempered path (q_i ∝ q_0^{1-β_i} (p̃^{α_i})^{β_i}) provides a principled way to deviate from pure geometric annealing while maintaining tractability. This connection between trust-region optimization in probability space and annealing paths is a valuable conceptual contribution that may inspire further work on adaptive path construction.

## Suggestions

- Provide a sensitivity analysis for the constraint bounds ε_tr and ε_ent, perhaps on alanine dipeptide where computational cost is low, to guide hyperparameter selection.
- Consider reporting results with a fixed computational budget (e.g., same number of target evaluations) for all methods to enable a more direct comparison.
- Clarify the 2.5× ESS claim by specifying which baseline comparison yields this factor.

## Score and Decision

**Score**: 8  
**Decision**: Accept

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>