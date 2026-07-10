## Summary

This paper introduces Constrained Mass Transport (CMT), a variational framework for sampling from unnormalized densities by constructing annealing paths subject to trust-region (KL divergence) and entropy constraints between successive intermediate distributions. The authors derive closed-form solutions showing that these constraints yield geometric, tempered, and geometric-tempered annealing paths respectively (Propositions 2.1–2.3, Theorem 2.4). They instantiate the framework with normalizing flows and evaluate it on molecular Boltzmann generator benchmarks up to d=219 (ELIL tetrapeptide), achieving up to ~1.9× higher effective sample size than state-of-the-art baselines (TA-BG, FAB) while using comparable or fewer target evaluations.

## Strengths

- **Clean theoretical derivation (Section 2, Propositions 2.1–2.3, Theorem 2.4):** The analytical solutions to the constrained optimization problems (trust-region, entropy, and combined) are derived in closed form, establishing a principled connection to geometric, tempered, and geometric-tempered annealing paths. This replaces heuristic schedule design with a well-motivated optimization framework and is the paper's strongest contribution.

- **Novel dual-constraint idea in the sampling context:** Combining trust-region and entropy constraints for constructing annealing paths in variational sampling is genuinely new. The theoretical motivation—trust-region constraints prevent mass teleportation by controlling distributional overlap, while entropy constraints prevent premature convergence—is clearly articulated and grounded in known failure modes of geometric annealing.

- **Strong empirical results on the two largest systems:** On alanine hexapeptide (d=180), CMT achieves 29.63% ESS vs 18.22% for TA-BG (1.6× improvement). On ELIL tetrapeptide (d=219), CMT achieves 26.06% ESS vs 13.75% for TA-BG (1.9× improvement). TA-BG failed on 2/4 ELIL runs while CMT succeeded in all 4, further supporting the robustness claim. EUBO improvements are also consistent across all systems.

- **Transparent and informative ablation study:** The ablation (Figures 2–3) shows the trust-region-only variant achieving higher ESS-to-target (33.42%) than the full CMT (29.63%), with the paper providing the mode-collapse explanation and leaving the data visible for readers to evaluate independently. This level of transparency is commendable.

## Weaknesses

### Major

1. **Overstated "consistently surpasses" claim in abstract and conclusion.** On ELIL tetrapeptide, CMT underperforms TA-BG on RAM TV (3.13×10⁻² vs 2.54×10⁻²), a key metric measuring distributional fidelity in the Ramachandran projection. TA-BG's value is bolded as best in Table 1. While CMT leads on ESS and EUBO on this system (and on all three metrics on the other three systems), the blanket claim that CMT "consistently surpasses state-of-the-art variational methods" (abstract, line 35, conclusion) is too strong and should be qualified to acknowledge this exception.

2. **Ablation does not cleanly establish that both constraints are simultaneously necessary.** The Geometric (trust-region-only) variant achieves higher ESS to target (33.42%) than full CMT (29.63%). The paper attributes this to mode collapse (marked with ★ in Figure 2d), and the main text states "Using a single or no constraint leads to mode collapse" (Figure 3 caption). However, the Figure 3 description also states that "The Geometric and Geometric-tempered plots show more diverse distributions," and the main text claims "Visible signs of mode collapse appear in all cases except for the tempered (7) and geometric-tempered (9) variants"—which itself contradicts the Figure 3 caption that says "The...Tempered plots show significant mode collapse." These internal inconsistencies create genuine ambiguity about whether the Geometric (trust-region-only) variant's mode collapse is clearly visible in the presented evidence. The trust-region constraint appears to do most of the heavy lifting, with the entropy constraint acting as a regularizer that trades some ESS for robustness. The paper should resolve these inconsistencies and discuss this trade-off more explicitly rather than claiming both are strictly "necessary."

### Minor

3. **Several EUBO values show exactly ±0.00 standard error across 4 independent runs** (e.g., CMT on alanine dipeptide: -175.00 ± 0.00, alanine tetrapeptide: -334.00 ± 0.00, ELIL: -277.83 ± 0.00). A standard error of exactly zero across stochastic training runs is suspicious and likely reflects rounding to two decimal places. If the metric is saturating or numerically insensitive on these systems, the fine-grained comparisons between methods (e.g., -333.99 vs -334.00) become less meaningful. More significant digits or a more discriminative metric would be beneficial.

4. **The paper acknowledges the large number of gradient updates as a key limitation** (conclusion) but does not report wall-clock time or gradient counts alongside the target-evaluation metric. While target evaluations are the field standard, providing concrete gradient counts or timing would allow a more complete assessment of the cost-performance trade-off that the authors themselves highlight.

### Trivial

None.

## Nice-to-Haves

- Clarify the ablation inconsistency between the main text (which claims Tempered avoids mode collapse) and the Figure 3 caption (which says Tempered has significant mode collapse).
- Report EUBO with more significant digits on systems where values cluster tightly.
- Report wall-clock time or gradient update counts as a supplement to target evaluations.
- Add brief statistical significance tests (e.g., bootstrap) for the main comparisons between CMT and the best baseline.

## Removed Points

These points are flagged to be removed; treat them with caution:

- **Lagrangian dual optimization bias (speculative):** The harsh critic raised a concern about Monte Carlo estimates of Z_{i+1} creating a feedback loop of biased multiplier estimates. The paper explicitly notes that the trust-region constraint ensures sufficient overlap, keeping variance low. This is a speculative concern not supported by evidence in the paper or observed in experiments. **[REMOVED: speculative, not a verified weakness]**
- **Deferred proof to appendix:** The critic criticized that the equality-constraint claim is "asserted without proof in the main text." Deferring proofs to appendices is standard practice in ML conference papers. **[REMOVED: standard formatting practice]**
- **Forward KL cost asymmetry:** The critic noted that forward KL uses fewer target evaluations because it is trained from MD samples. The paper explicitly acknowledges this and excludes forward KL from direct comparison. **[REMOVED: already addressed by the paper]**
- **Circularity of importance weights:** The critic raised a concern that if q̂_i is a poor approximation of q_i, the bootstrap degrades. This is a known property of all sequential importance sampling methods; the trust-region constraint is specifically designed to mitigate this. **[REMOVED: generic concern, not specific to this paper]**
- **Hyperparameter selection / code release:** These are appendix-stripped issues. The parser removes appendix content; the original submission contains these details. **[REMOVED: per hard rules about missing appendix content]**
- **Missing related works / reproducibility nitpicks:** Generic concerns not specific enough to constitute substantive weaknesses. **[REMOVED]**
- **Weakness about the "Due to convexity" claim being deferred:** Standard practice for conference papers. **[REMOVED]**
- **Claim that Geometric variant does NOT show mode collapse:** The harsh critic claimed the Figure 3 caption shows Geometric does not have mode collapse, but the caption says "more diverse distributions" relative to the clearly collapsed variants, which does not necessarily mean "no mode collapse." The paper marks Geometric with ★ indicating mode collapse. The inconsistency is real but subtler than stated. **[MOVED to main weakness #2, properly framed]**

## Novel Insights

None beyond the paper's own contributions. The key insight—that combining trust-region and entropy constraints in a variational framework yields principled annealing paths with automatic schedule tuning—is already clearly articulated by the authors.

## Suggestions

1. **Qualify "consistently surpasses"** in the abstract and conclusion to acknowledge the RAM TV exception on ELIL tetrapeptide (e.g., "surpasses on ESS and EUBO while being competitive on Ramachandran fidelity").
2. **Resolve the ablation inconsistencies** between the main text and Figure 3 caption regarding which single-constraint variants exhibit visible mode collapse. Provide a clearer visual demonstration or quantitative metric (e.g., density coverage) for mode collapse in the Geometric variant.
3. **Report EUBO with more significant digits** on systems where the metric is saturating, or explicitly acknowledge that the metric is approaching its lower bound.
4. **Add wall-clock time or gradient update counts** as a supplement to target evaluations, since the paper itself identifies gradient updates as a key limitation.

## Score and Decision

**Calibration anchors (retrieved across Round 1 and Round 2):**

| Anchor | Path | Avg Score | Round | Itemized? | Comparison |
|--------|------|-----------|-------|-----------|------------|
| Annealing Flow | XcAJ0qsMgh.md | 3.60 | R1 | Yes | Much weaker experiments (synthetic ≤d=50), incremental novelty. CMT is clearly stronger. |
| Neural Sampling Boltzmann | TUvg5uwdeG.md | 6.40 | R1/R2 | Yes | Similar theoretical ambition but only 2D/8D experiments, missed prior work. CMT has stronger molecular-scale validation. |
| BNEM | ybWOYIuFl6.md | 6.00 | R1/R2 | Yes | Only toy systems (2D GMM, 4-particle DW). CMT's molecular benchmarks up to d=219 are much more convincing. |
| NETS | 8NiTKmEzJV.md | 6.25 | R1/R2 | Yes | Novelty concerns, limited high-dim experiments. CMT's theory is cleaner and molecule-scale results stronger. |
| BoPITO | pRCOZllZdT.md | 7.00 | R2 | Yes | Only tested on alanine dipeptide (d=60). CMT tests up to d=219 with more baselines and stronger experiments. |
| Provable Benefit ALMC | P6IVIoGRRg.md | 7.00 | R2 | No | Theory paper on annealed MCMC; different contribution type. |
| Generator Matching | RuP17cJtZo.md | 8.00 | R1 | No | Broad generative modeling framework; different scope and stronger novelty. |
| Flow Matching Atoms | CkozFajtKq.md | 6.33 | R2 | No | Different task (MD acceleration, not sampling from energy). |
| SVGD Convergence | sbG8qhMjkZ.md | 8.00 | R1 | No | Pure theory paper; different contribution. |

**Round 1 bracket:** [6.5, 7.5]. The paper's strengths (favorability 11–13) match the best anchors, while its weaknesses (lowest favorability -0.46) are less damaging than the weakest items in Neural Sampling (-1.92), NETS (-1.33), and BNEM (-1.55). This places CMT above the 6.0–6.4 cluster.

**Round 2 narrowing:** Comparing against BoPITO (7.00), CMT has stronger empirical validation (d=60–219 vs d=60 only) and cleaner theoretical development, but shares the characteristic of overstated claims relative to evidence. The paper's weakness favorabilities (-0.46, -0.28, 0.82, 1.61) are comparable to BoPITO's weakest items (-0.62, -0.15). Given stronger experiments but similar presentation issues, CMT is slightly above BoPITO.

**Final score:** 7.0. The theoretical contribution is genuine and well-developed, the empirical results on large systems are strong, and the identified weaknesses are addressable with revisions to the claims and presentation. This is a clear accept.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>