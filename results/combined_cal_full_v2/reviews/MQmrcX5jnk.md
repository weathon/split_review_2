Now I have all the calibration data. Let me write the final consolidated review.

## Summary

This paper introduces Constrained Mass Transport (CMT), a variational framework for sampling from unnormalized Boltzmann distributions by constructing annealing paths under constraints on both the KL divergence (trust-region) and the entropy decay between successive intermediate densities. The approach yields analytical forms for the optimal intermediate densities (Propositions 2.1–2.3), characterizes the resulting annealing paths (Theorem 2.4), and is instantiated with normalizing flows. Empirical evaluation on four molecular systems (alanine dipeptide through the new ELIL tetrapeptide at d=219) shows CMT achieves substantially higher effective sample sizes on the largest systems while avoiding mode collapse. The paper also contributes the ELIL tetrapeptide benchmark with publicly released MD ground-truth data.

## Strengths

- **The dual-constraint formulation is principled and theoretically grounded.** The paper derives analytical solutions (Propositions 2.1–2.3) for the optimal intermediate densities under trust-region, entropy, and combined constraints, and characterizes the resulting annealing paths (Theorem 2.4). This provides a clean variational foundation for constructing annealing paths that goes beyond standard geometric schedules. The connection to trust-region methods from RL is well-motivated, and the entropy constraint addresses a genuine failure mode (premature convergence / mass teleportation) that the trust-region constraint alone cannot fix.

- **On the largest systems, the empirical results are compelling.** On alanine hexapeptide (d=180) and the new ELIL tetrapeptide benchmark (d=219), CMT achieves ESS of 29.63% and 26.06% respectively — roughly 1.6–2× higher than TA-BG (18.22%, 13.75%) and 2–3.6× higher than FAB (14.55%, 7.21%). Standard errors are small (0.08–0.26 percentage points), indicating reliable results. The number of target evaluations is matched across methods, providing a fair comparison.

- **The ablation study (Figures 2 and 3) directly validates the design choices.** The paper shows that omitting either constraint leads to measurable degradation: without the trust-region constraint, entropy drops too fast (mode collapse); without the entropy constraint, training is unstable and overlap is poor. The ★ notation in Figure 2d honestly flags that ESS values are not directly comparable when mode collapse occurs, and the Ramachandran plots provide a qualitative check.

- **The new ELIL tetrapeptide benchmark is a genuine community contribution.** It is described as the largest system studied to date under the setting of learning exclusively from energy evaluations, with more complex side-chain interactions than alanine-based benchmarks. The ground-truth MD data is publicly available via Zenodo (DOI 10.5281/zenodo.18822445).

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

1. **Over-claim in Section 5.2.** The paper states: "Across all systems and metrics, our method outperforms the baselines while requiring the same or fewer target evaluations" (line 237), and shortly after claims "superior mode coverage and resolution of metastable high-energy regions (RAM TV)." However, the paper's own Table 1 shows that on ELIL tetrapeptide, TA-BG achieves better RAM TV (0.0254) than CMT (0.0313), and this is correctly bolded as the best value. This over-claim is limited to one metric on one system and does not undermine the overall empirical case, but it should be corrected.

2. **A central scalability claim is deferred to the appendix without main-text support.** At line 144, the paper asserts that "the trust-region constraint controls the variance of the importance weights, keeping it approximately constant, independent of the problem dimension d (see Appendix C.3)," and cites this as evidence that the algorithm is "highly scalable." This is a strong claim, and the main text provides no theoretical summary or empirical demonstration to support it. Including a brief empirical check (e.g., importance weight variance vs. dimension on a synthetic problem) would substantially strengthen confidence in the scalability argument.

3. **Reporting of computational cost is incomplete.** The paper reports target evaluations (matched fairly across methods) but does not report the number of annealing steps T̃, total gradient updates, or wall-clock time in the main text — the value of T̃ is deferred to Algorithm 2 in the appendix. The Conclusion acknowledges that "a large number of gradient updates" is a key limitation. Reporting these numbers would allow readers to assess the training-cost versus sampling-quality trade-off.

### Trivial
None.

## Nice-to-Haves

- The paper could more explicitly discuss the tension between ESS and mode coverage shown in the ablation: the trust-region-only variant achieves the *highest* ESS (33.42%) but is marked as mode-collapsed. Explaining this would preempt a natural reader question.
- A wall-clock time or GPU-hour comparison would help practitioners assess the practical trade-off, especially since CMT trains sequential flow approximations.

## Removed Points

The following points from the input review were flagged for removal:

- **Criticism that the ELIL "largest system" claim is "not fully verifiable without checking all cited work"**: The paper appropriately hedges with "to the best of our knowledge." Per policy, references cited in the paper are assumed to exist, and this criticism was removed.
- **Section-by-section notes about proofs being deferred to appendix (e.g., existence of finite I, constraint always being active)**: This is standard practice for conference papers; deferring proofs to the appendix does not constitute a weakness.
- **Request for hyperparameter sensitivity summary in main text**: Acceptable to defer to appendix.
- **Note about ESS vs. mode coverage tension**: The paper already addresses this with the ★ notation in Figure 2d and accompanying text.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- Correct the over-claim in Section 5.2: qualify that CMT outperforms baselines on most metrics across all systems, with the exception of RAM TV on ELIL tetrapeptide where TA-BG is stronger.
- Consider adding a brief empirical illustration of the variance claim for the Z estimator (e.g., importance weight variance vs. dimension) in the main text.
- Report the number of annealing steps T̃ and a summary of gradient updates or relative training cost in the main text, even briefly.

---

**Calibration Report**

All rounds of calibration_search and itemized_calibration were performed. Round 1 (bracketing) retrieved anchors across score ranges. Round 2 (narrowing within [5.5, 7.5]) retrieved closer anchors.

**Anchors retrieved:**

| Path | Avg Score | Round | Itemized | Comparison |
|---|---|---|---|---|
| XcAJ0qsMgh (Annealing Flow) | 3.60 | R1 | Yes | Same problem domain but weaker: limited experiments, missing baselines, incremental novelty. Current paper is clearly stronger. |
| TUvg5uwdeG (Neural Sampling from Boltzmann Densities) | 6.40 | R1 | Yes | Strong theory, limited experiments (mostly 2D). Current paper has stronger experiments but similar-level theoretical contribution. Comparable quality. |
| 8NiTKmEzJV (NETS) | 6.25 | R1 | Yes | Novelty overlap concerns (negative-weight weaknesses). Rejected despite score. Current paper has clearer novelty. |
| kRjLBXWn1T (Correcting Flows) | 5.25 | R1 | Yes | Different topic (image generation). Weaker connection to theory. |
| 1hT2fsHbK9 (Discrete→Continuous) | 5.25 | R1 | Yes | Theoretical links considered unsurprising. Weaker experiments. |
| ybWOYIuFl6 (BNEM) | 6.00 | R2 | Yes | Incremental over iDEM, toy experiments only. Current paper is stronger on novelty and experimental scope. |
| pRCOZllZdT (Boltzmann priors for ITO) | 7.00 | R2 | No | Different topic (transfer operators). |
| GK5ni7tIHp (Training-free Guidance) | 6.25 | R2 | No | Different subfield (molecular design). |
| 3tM1l5tSbv (Generative Learning) | 6.75 | R2 | No | Different topic (optimization). |

**Round 1 bracket:** Between 5.5 and 7.5.

**Weighted-item comparison:** My draft's strengths all carry weights 9.97–11.17 (strongly positive). My weaknesses carry weights 4.58–6.93 (all positive, meaning the scoring model does not view them as severe). No weakness has a negative weight. By comparison, the 6.40 anchor (TUvg5uwdeG) had several negative-weight weaknesses (novelty concerns at -1.40, -3.89), and the 6.25 anchor (8NiTKmEzJV) had multiple negative-weight weaknesses about prior-art overlap. The current paper has no such negative-weight items. This places it above those anchors. The paper is closest in quality to TUvg5uwdeG (6.40, Accept) but with stronger experimental validation and fewer severity concerns, suggesting a score around 6.5.

**Final bracket determination for Round 2:** Within [5.5, 7.5], the paper's weighted-item profile is stronger than the 6.00–6.40 anchors and comparable to the upper end of the bracket (closer to 6.5–7.0 than to 5.5–6.0).

## Score and Decision

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>