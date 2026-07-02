## Summary

This paper introduces Constrained Mass Transport (CMT), a variational framework for sampling from unnormalized densities by constructing a sequence of intermediate distributions under constraints on both KL divergence (trust-region) and entropy decay between successive steps. The authors derive closed-form optimal intermediate densities under each constraint, establish connections to geometric, tempered, and geometric-tempered annealing paths (Theorem 2.4), and instantiate the framework with normalizing flows for molecular Boltzmann generators. Empirical results on four molecular systems—including the newly introduced ELIL tetrapeptide (d=219)—show that CMT generally outperforms existing energy-based methods in ESS and EUBO while avoiding mode collapse.

## Strengths

1. **Clean theoretical characterization.** Propositions 2.1–2.3 derive closed-form optimal intermediate densities under trust-region, entropy, and combined constraints. Theorem 2.4 elegantly connects these constrained optimization problems to geometric, tempered, and geometric-tempered annealing paths, providing variational grounding for schedule design that was previously lacking.

2. **Well-designed ablation study (Figures 2 and 3).** The paper convincingly demonstrates that both constraints are necessary: the trust-region-only variant achieves superficially high ESS but exhibits mode collapse visible in Ramachandran plots; the entropy-only variant avoids mode collapse but has unstable training and low ESS; only the combined variant avoids both failure modes. The paper honestly marks mode-collapsed variants and notes their ESS is not directly comparable.

3. **Strong empirical results on larger systems.** On alanine hexapeptide (d=180) and ELIL tetrapeptide (d=219), CMT achieves roughly 1.6–1.9× the ESS of the best competing energy-based method (TA-BG) and ~2.0–3.6× that of FAB, with gaps large relative to standard errors and consistent across metrics (EUBO, ESS).

4. **ELIL tetrapeptide benchmark.** Introducing this larger system (d=219, complex side-chain interactions) as a purely energy-based benchmark is a useful community contribution for future work on molecular Boltzmann generators.

## Weaknesses

### Fatal

None.

### Major

1. **Section 5.2 overstates the empirical findings, contradicting the paper's own Table 1.** Line 237 states: "Across all systems and metrics, our method outperforms the baselines." However, Table 1 shows that on ELIL tetrapeptide, TA-BG achieves RAM TV of (2.54±0.13)×10⁻² while CMT achieves (3.13±0.03)×10⁻²—TA-BG is strictly better on this metric. The table honestly bolds TA-BG's value, but the accompanying text is inaccurate. The data supports a more nuanced claim ("CMT wins on most metrics and systems, with one exception on RAM TV for ELIL") that would be equally compelling and more credible. This is a factual error in the text relative to the reported data.

### Minor

1. **Imprecise "2.5× ESS" claim in the abstract and conclusion.** The abstract states CMT achieves "more than 2.5× higher effective sample size." Checking Table 1: this ratio holds for CMT vs FAB on ELIL tetrapeptide (~3.6×) but not for most other comparisons (e.g., vs TA-BG on hexapeptide ~1.6×, vs FAB on hexapeptide ~2.0×, vs TA-BG on ELIL ~1.9×, vs any baseline on smaller systems ~1.0–1.1×). The claim is true for at least one comparison but is presented as a general result without specification of which baseline or system. This framing reads as stronger than the aggregate data support.

2. **Internal contradiction about whether the Tempered variant shows mode collapse in Figure 3.** Line 241 states that visible mode collapse appears "in all cases except for the tempered (7) and geometric-tempered (9) variants." However, line 255 (Figure 3 caption) states: "The No constraint and Tempered plots show significant mode collapse." These descriptions directly contradict each other. The authors should resolve which description is correct—this is a basic consistency failure in the paper's own ablation analysis.

3. **Constraint-bound hyperparameters ε_tr and ε_ent are not stated in the main text.** These values control the entire algorithm (determining how much the KL can change per step and how fast entropy can decay) yet do not appear in the main paper. The appendix contains sensitivity analysis, which is good, but a reader cannot assess the method's sensitivity to these choices from the main text alone. Reporting the chosen values and a brief summary of the sensitivity findings (even one sentence) would significantly improve reproducibility and practitioner guidance.

### Trivial

None.

## Nice-to-Haves

- **Wall-clock time comparison.** CMT's sequential fitting of I intermediate distributions introduces overhead that target evaluation counts alone do not capture. Reporting total training time against baselines would strengthen the practical claims.
- **Statistical significance tests.** With four runs per setting, standard errors are informative, but simple significance testing (e.g., paired t-tests against the best baseline) would strengthen claims where gaps are narrower (e.g., alanine tetrapeptide: CMT ESS 68.60% vs TA-BG 65.81%).
- **Explicit entropy-constraint trade-off discussion.** The Geometric (trust-region only) variant achieves higher raw ESS (33.42%) than Geometric-tempered (29.63%) while suffering from mode collapse. The paper correctly marks this ESS as not comparable, but an explicit acknowledgment that the entropy constraint's primary benefit is mode coverage (at a modest ESS cost) would add transparency—this is already implied but not stated directly.

## Removed Points

- **Criticism that entropy-constraint-only solution does not depend on q_i**: Removed because the paper already acknowledges this limitation (lines 96-97), explaining that the KL gap between q_0 and q_1 can be arbitrarily large and that combining with the trust-region constraint addresses it.
- **Re: Reverse KL baseline using 2.56×10⁸ evaluations across all systems**: Removed as a minor observation about another method's setup rather than a weakness of this paper. The paper does not claim to explain this.
- **Criticism that the entropy constraint benefit "warrants more careful characterization"**: Demoted to Nice-to-have because the paper already handles this—it marks mode-collapsed ESS as not directly comparable and shows both constraints are necessary together.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Correct the overstatement in Section 5.2:** Replace "Across all systems and metrics, our method outperforms the baselines" with a precise statement that acknowledges the single RAM TV exception on ELIL tetrapeptide.
2. **Qualify the "2.5× ESS" claim** in the abstract and conclusion by specifying which comparison(s) this holds for, or restate as "up to 2.5× higher ESS on the largest system."
3. **Resolve the contradictory descriptions** of whether the Tempered (entropy-only) variant exhibits mode collapse in Figure 3.
4. **Report ε_tr and ε_ent values** in the main text with a brief sensitivity summary.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>