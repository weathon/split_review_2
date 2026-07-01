## Summary

This paper introduces Constrained Mass Transport (CMT), a variational framework for sampling from unnormalized densities by constructing intermediate distributions under constraints on both the KL divergence (trust-region) and entropy decay between successive steps. The framework yields closed-form solutions for the optimal intermediate densities (Propositions 2.1–2.3), which are then approximated by normalizing flows. On molecular Boltzmann generator benchmarks, CMT consistently outperforms existing methods, with the largest gains on the harder high-dimensional systems (alanine hexapeptide d=180, ELIL tetrapeptide d=219). The paper also introduces the ELIL tetrapeptide as a new benchmark.

## Strengths

1. **Clean theoretical framework with closed-form solutions.** Propositions 2.1–2.3 derive analytical forms for the optimal intermediate densities under trust-region, entropy, and combined constraints. The explicit expressions for \(q_{i+1}\) in terms of \(q_i\), \(\tilde{p}\), and the Lagrangian multipliers are a genuine contribution that goes beyond prior work (Blessing et al., 2025) by extending trust-region optimization to sampling and adding an entropy constraint.

2. **The combination of KL and entropy constraints is well-motivated and validated by ablation.** The paper identifies a concrete failure mode of geometric annealing (mass teleportation), shows why neither constraint alone suffices (Proposition 2.2 yields a path independent of \(q_i\); the trust-region-only path can still teleport mass), and validates the combined approach via ablation (Figures 2–3). The ablation convincingly shows that both constraints are necessary to simultaneously achieve high ESS and avoid mode collapse.

3. **Strong empirical results on the hardest systems.** On alanine hexapeptide (d=180), CMT achieves 29.63% ESS vs TA-BG's 18.22% — a clear advantage with non-overlapping standard errors. On ELIL tetrapeptide (d=219), CMT achieves 26.06% ESS vs TA-BG's 13.75%. These are substantial improvements where sampling is most challenging.

4. **New benchmark contribution.** The ELIL tetrapeptide (d=219) is a useful addition to the evaluation suite, and the ground-truth MD data is made publicly available (DOI in the reproducibility statement).

5. **Computational efficiency of the Lagrangian dual.** The dual optimization accounts for ~0.01% of training time on alanine dipeptide (line 150), meaning the constraints come at essentially no additional cost.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

1. **Overclaim on RAM TV for the ELIL tetrapeptide.** The paper states that "Across all systems and metrics, our method outperforms the baselines" and "provides superior mode coverage and resolution of metastable high-energy regions (RAM TV)" (Section 5.2). On the ELIL tetrapeptide, however, CMT's RAM TV is \(3.13 \times 10^{-2}\), while TA-BG achieves \(2.54 \times 10^{-2}\) — meaning TA-BG is strictly better on this metric for this system. The paper does not acknowledge this exception. This does not invalidate the overall results, but the blanket claim should be qualified.

2. **No empirical analysis of how well the learned flow tracks the theoretical optimal path.** The paper derives optimal intermediate densities \(q_i\) analytically, then (a) estimates their normalization constants \(\mathcal{Z}_{i+1}\) via Monte Carlo from \(q_i\) samples and (b) approximates \(q_{i+1}\) via a normalizing flow using those same samples. These are stacked approximations whose fidelity is not empirically characterized. The paper argues that the trust-region constraint controls importance-weight variance, but provides no diagnostic showing how closely the learned \(\hat{q}_i\) resembles the theoretical \(q_i\) (e.g., by comparing estimated vs. ground-truth \(\mathcal{Z}_{i+1}\) on a tractable projection). While the strong empirical results suggest the algorithm works, this gap between theory and practice goes unexamined.

3. **The "2.5× higher ESS" claim in the abstract is imprecise.** The claim is technically supported — CMT achieves 26.06% ESS vs FAB's 7.21% on ELIL (ratio \(\approx 3.61\times\)), and FAB is a state-of-the-art variational method. However, against the strongest baseline (TA-BG) the maximum ratio is 1.90× (on ELIL). The abstract does not specify which comparison yields 2.5×, which may give an inflated first impression. The paper would be stronger by being precise about this comparison.

4. **No wall-clock time or GPU-hour comparison.** The paper mentions "the large number of gradient updates" as a key limitation (Section 6) but reports only target evaluations as a cost metric. Since gradient updates and target evaluations are different resources, wall-clock time would help readers gauge the practical trade-off.

### Trivial
None.

## Nice-to-Haves

- **Statistical significance for close comparisons.** For close ESS values (e.g., alanine tetrapeptide: CMT 68.60±0.21 vs TA-BG 65.81±0.24), a simple test or confidence interval would clarify reliability.
- **Analyze the faithfulness of the approximation.** A diagnostic comparing the learned \(\hat{q}_i\) to the theoretical \(q_i\) (e.g., on a low-dimensional projection) would directly validate that the practical algorithm tracks the theory.
- **Hyperparameter sensitivity discussion** in the main text (beyond the appendix reference) would help practitioners gauge the method's robustness to \(\varepsilon_{\text{tr}}\) and \(\varepsilon_{\text{ent}}\).

## Removed Points

These points were identified in the input review but are removed per the filtering guidelines:

- **Typo in Algorithm 1** (`g_{\text{w-ent}}` vs. `g_{\text{tr-ent}}`): This could be a parser artifact or a minor inconsistency; removed per formatting/typo rules.
- **Stray `(x)` in Eq. 10 integrand:** Parser artifact, not a paper flaw.
- **Figure caption repetition:** Parser artifact.
- **Claim about Appendix C.3 being stripped:** The parser strips appendices from all papers; the argument exists in the original submission. The underlying concern (unanalyzed theory-practice gap) is retained as Minor Weakness #2.
- **Hyperparameter sensitivity dismissed due to stripped Appendix B:** Same appendix-stripping rationale.
- **Strong form of the 2.5× ESS criticism:** The reviewer claimed the "largest ratio is 1.90×," which is factually incorrect — CMT vs FAB on ELIL yields 3.61× (>2.5×), and FAB is a state-of-the-art variational method. A softened version about precision is retained as Minor Weakness #3.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Qualify the RAM TV claim in Section 5.2 to acknowledge the ELIL tetrapeptide exception (Table 1: TA-BG achieves better RAM TV on this system).
2. Add a brief diagnostic showing how well the learned flow approximates the theoretical optimal path, e.g., by comparing estimated vs. ground-truth normalization constants on a tractable low-dimensional projection.
3. Clarify in the abstract which comparison yields the 2.5× ESS improvement (e.g., "achieving up to 2.5× higher effective sample size than the strongest baseline on the largest systems").
4. Report wall-clock time or GPU hours alongside target evaluations to contextualize the stated "key limitation" of gradient update cost.

## Score and Decision

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>