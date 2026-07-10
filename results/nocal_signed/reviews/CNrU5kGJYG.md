The scoring model provides useful calibration. Let me finalize the review.

## Summary

This paper proposes TrojanTO, a post-training action-level backdoor attack against Trajectory Optimization (TO) models in offline RL. It first empirically demonstrates that traditional RL backdoor vectors (reward manipulation) are ineffective against TO models, and then designs a three-component method (trajectory filtering, batch poisoning, alternating training) that achieves high attack success with only 0.3% poisoned trajectories across DT, GDT, and DC models on six D4RL tasks.

## Strengths

1. **Empirical analysis of an underexplored threat (Section 4).** The systematic investigation of how target action selection (Table 1), trigger design (Tables 2-3), and reward manipulation (Figure 1) affect backdoor efficacy against TO models is a genuine contribution. The finding that reward manipulation — the primary attack vector for traditional RL backdoors — is ineffective against TO models is well-demonstrated. The observation that boundary target actions yield much higher ASR than interior ones is a non-obvious finding.

2. **Technically coherent method design.** TrojanTO's three components — trajectory filtering (to avoid distribution shift), batch poisoning (for trigger consistency), and alternating training via MI-FGSM with bi-level optimization — are each clearly motivated by specific challenges identified in Section 4. The design choices are internally consistent.

3. **Low poisoning rate with measurable efficacy.** Achieving backdoor efficacy with an average of 0.3% poisoned trajectories (vs. Baffle's 10%) is practically significant under the post-training threat model. The method is demonstrated across three TO architectures and six D4RL environments.

## Weaknesses

### Fatal
None.

### Major

1. **ASR threshold ε is never specified — the primary metric is uninterpretable.** Equation (2) defines ASR based on a threshold ε that determines whether an output action is "close enough" to the target action, but its numerical value is never stated. All quantitative ASR and CP results depend entirely on this unstated parameter. Without ε, the reader cannot assess whether the attack achieves fine-grained control (tight tolerance) or merely coarse approximation (loose tolerance). This is especially problematic for continuous action spaces where the notion of "success" depends wholly on the tolerance.

2. **Numerically impossible CP value reveals likely data inconsistency.** In Table 4, Baffle on Walk with DT reports ASR=0.328, BTP=0.581, CP=0.000. The paper states CP is the harmonic mean computed per run and then averaged. For average CP to round to 0.000, every individual run's CP must be effectively 0, which requires ASR≈0 or BTP≈0 per run. But average ASR=0.328 means some runs have ASR>0. If those runs also have BTP>0 (as the 0.581 average suggests), CP would be >0. This three-number combination is mathematically impossible under the described formula and suggests a data error or discrepancy between the formula and actual computation. This undermines confidence in the aggregate numbers, though it pertains to a baseline rather than the proposed method.

### Minor

3. **No variance reported in main results; suspicious zero-variance pattern in supplementary tables.** Tables 4 and 5 report only point estimates (averaged over 3 seeds) without standard deviations. In Tables 6 and 7, at least 18 of 24 entries show ±0.000 standard deviation across seeds — implausible for stochastic D4RL environments and suggesting either rounding that hides real variance or an evaluation procedure that inadvertently eliminated stochasticity. The reader cannot assess the stability of the quantitative claims.

4. **IMC baseline adaptation is undocumented.** IMC (Pang et al., 2020) was originally proposed for image classifiers. The paper never explains how it is adapted to the TO model setting — what loss function, trigger constraints, or optimization procedure are used. As presented, the comparison is opaque.

### Trivial

5. **Figure 1 legend lists "w/ RM-4" twice** (in both orange and green), suggesting a labeling error.

## Nice-to-Haves

- An ε-sweep showing how ASR varies with different tolerances would directly address the sensitivity of the "success" claim.
- Controlled comparisons at matched poisoning rates (e.g., TrojanTO at 10% or Baffle adapted to action-level) would strengthen the efficiency argument.
- Per-run ASR, BTP, and CP values for the anomalous Baffle/Walk/DT cell would resolve the inconsistency concern.

## Removed Points

These points from the input review were removed with justification:
- **Unfair baseline comparison (different poisoning rates):** Removed — the asymmetry favors the baseline (Baffle uses 33× more data), making TrojanTO's advantage a stronger result.
- **Defense section lacks numerical results:** Removed — defense results are in Appendix B.1, stripped by the parser.
- **Bi-level optimization asymmetry:** Removed — optimizing the trigger solely for attack success is intentional design, not an oversight.
- **BTP normalization denominator issue:** Removed — speculative, no evidence from the paper.
- **Various appendix/formatting/reproducibility nitpicks:** Removed per guidelines (parser artifacts, not author errors).

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Specify ε in the main paper and provide an ε-sweep showing how ASR varies with tolerance.
2. Resolve the CP inconsistency for Baffle/Walk/DT — provide per-run ASR, BTP, and CP values to clarify the computation.
3. Add standard deviations to all main tables; explain the zero-variance results in Tables 6-7.
4. Describe the IMC adaptation explicitly in the main paper.
5. Report the trajectory filtering length threshold ε value.

## Score and Decision

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>